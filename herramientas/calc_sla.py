#!/usr/bin/env python3
"""calc_sla.py - Calculadora de cumplimiento de SLA.

Lee los objetivos (YAML) y las mediciones validas (CSV) de un caso y entrega,
por metrica, el valor medido, la cobertura, el veredicto y el credito.

Uso:
    python3 herramientas/calc_sla.py -o CASO/objetivos.yaml -m CASO/mediciones.csv [--json salida.json]

Formato del CSV: fecha,metrica,valor,unidad,muestras,referencia
  - caida_atribuible: minutos de caida atribuible al proveedor (los excluidos no se cargan).
  - latencia / perdida: valor mensual; 'muestras' se usa para la cobertura (5.1).
  - jitter: un valor por semana con sus muestras; se pondera por muestras.
  - throughput: una fila por prueba iperf3 valida.
  - respuesta / mttr: una fila por ticket (minutos).
"""
import argparse
import csv
import json
import sys

import yaml

CUMPLE, NO_CUMPLE, INSUF = "CUMPLE", "NO CUMPLE", "EVIDENCIA INSUFICIENTE"


def compara(valor, operador, objetivo):
    return valor >= objetivo if operador == ">=" else valor <= objetivo


def leer_mediciones(ruta):
    filas = {}
    with open(ruta, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["valor"] = float(r["valor"])
            r["muestras"] = int(r["muestras"]) if r.get("muestras") else None
            filas.setdefault(r["metrica"], []).append(r)
    return filas


def credito_disponibilidad(a, tramos):
    for t in tramos:
        if t["desde"] <= a < t["hasta"]:
            return t["credito"]
    return 0.0


def calcular(obj, med):
    T = obj["minutos_periodo"]
    cmin = obj["cobertura_minima"]
    m = obj["metricas"]
    res = {}

    # Disponibilidad (3.1)
    caidas = [r["valor"] for r in med.get("caida_atribuible", [])]
    caida = sum(caidas)
    a = (T - caida) / T * 100
    permitido = T * (1 - m["disponibilidad"]["objetivo"] / 100)
    ok = compara(round(a, 2), ">=", m["disponibilidad"]["objetivo"])
    res["disponibilidad"] = {
        "medido": a, "cobertura": 1.0, "veredicto": CUMPLE if ok else NO_CUMPLE,
        "credito": 0.0 if ok else credito_disponibilidad(a, obj["creditos_disponibilidad"]),
        "detalle": {"T": T, "caidas": caidas, "caida_atribuible": caida,
                    "permitido": permitido, "exceso": max(0.0, caida - permitido)},
    }

    # Metricas con cobertura (latencia, perdida) y jitter ponderado
    for nombre in ("latencia", "perdida"):
        filas = med.get(nombre, [])
        muestras = sum(r["muestras"] or 0 for r in filas)
        cob = muestras / T
        valor = filas[0]["valor"] if filas else None
        if valor is None or cob < cmin:
            ver = INSUF
        else:
            ver = CUMPLE if compara(valor, m[nombre]["operador"], m[nombre]["objetivo"]) else NO_CUMPLE
        res[nombre] = {"medido": valor, "cobertura": cob, "veredicto": ver,
                       "detalle": {"muestras": muestras, "esperadas": T}}

    filas = med.get("jitter", [])
    n = sum(r["muestras"] for r in filas)
    prod = [r["valor"] * r["muestras"] for r in filas]
    jit = sum(prod) / n if n else None
    cob = n / T
    simple = round(sum(r["valor"] for r in filas) / len(filas) + 1e-9, 2) if filas else None
    if jit is None or cob < cmin:
        ver = INSUF
    else:
        ver = CUMPLE if compara(round(jit, 2), m["jitter"]["operador"], m["jitter"]["objetivo"]) else NO_CUMPLE
    res["jitter"] = {"medido": jit, "cobertura": cob, "veredicto": ver,
                     "detalle": {"semanas": [(r["valor"], r["muestras"]) for r in filas],
                                 "productos": prod, "suma_productos": sum(prod),
                                 "muestras": n, "promedio_simple": simple}}

    # Throughput (3.5)
    pruebas = [r["valor"] for r in med.get("throughput", [])]
    minimo = m["throughput"].get("pruebas_minimas", 4)
    prom = sum(pruebas) / len(pruebas) if pruebas else None
    if len(pruebas) < minimo:
        ver = INSUF
    else:
        ver = CUMPLE if compara(prom, ">=", m["throughput"]["objetivo"]) else NO_CUMPLE
    res["throughput"] = {"medido": prom, "cobertura": len(pruebas) / minimo, "veredicto": ver,
                         "detalle": {"pruebas": pruebas, "suma": sum(pruebas), "minimo": minimo}}

    # Respuesta (4.1) y MTTR (4.2): se exige en todos los tickets
    for nombre in ("respuesta", "mttr"):
        filas = med.get(nombre, [])
        vals = [r["valor"] for r in filas]
        lim = m[nombre]["objetivo"]
        fuera = [(r["referencia"].split()[0], r["valor"]) for r in filas if r["valor"] > lim]
        ver = INSUF if not vals else (CUMPLE if not fuera else NO_CUMPLE)
        res[nombre] = {"medido": max(vals) if vals else None, "cobertura": 1.0, "veredicto": ver,
                       "detalle": {"tickets": [(r["referencia"].split()[0], r["valor"]) for r in filas],
                                   "cumplen": len(vals) - len(fuera), "total": len(vals),
                                   "fuera": fuera}}

    # Creditos (8.2): solo incumplimientos comprobados
    for nombre in obj["metricas_credito_otras"]:
        res[nombre]["credito"] = obj["credito_otras"] if res[nombre]["veredicto"] == NO_CUMPLE else 0.0
    res["mttr"]["credito"] = 0.0

    suma = sum(r["credito"] for r in res.values())
    aplicado = min(suma, obj["tope_credito"])
    monto = aplicado * obj["cargo_mensual"]
    global_ok = all(r["veredicto"] == CUMPLE for r in res.values())
    algun_no = any(r["veredicto"] == NO_CUMPLE for r in res.values())
    veredicto_global = CUMPLE if global_ok else (NO_CUMPLE if algun_no else INSUF)

    # Viabilidad serie / paralelo (Anexo 7)
    infra = obj.get("infraestructura")
    viab = None
    if infra:
        serie = 1.0
        for c in infra["serie"]:
            serie *= c["disponibilidad"] / 100
        con_respaldo = 1.0
        acceso_par = None
        for c in infra["serie"]:
            a_c = c["disponibilidad"] / 100
            if c.get("respaldo"):
                r = next(x for x in infra["respaldo"] if x["paralelo_con"] == c["respaldo"])
                a_c = 1 - (1 - a_c) * (1 - r["disponibilidad"] / 100)
                acceso_par = a_c
            con_respaldo *= a_c
        viab = {"serie": serie * 100, "con_respaldo": con_respaldo * 100,
                "acceso_paralelo": acceso_par * 100 if acceso_par else None,
                "caida_esperada_serie": (1 - serie) * T,
                "caida_esperada_respaldo": (1 - con_respaldo) * T,
                "permitido": permitido}

    orden = ["disponibilidad", "latencia", "jitter", "perdida", "throughput", "respuesta", "mttr"]
    res = {k: res[k] for k in orden}
    return {"metricas": res, "credito_suma": suma, "credito_aplicado": aplicado,
            "monto": monto, "veredicto_global": veredicto_global, "viabilidad": viab}


def imprimir(obj, out):
    m = obj["metricas"]
    print(f"Servicio : {obj['servicio']}")
    print(f"Periodo  : {obj['periodo']} ({obj['dias_periodo']} dias, {obj['minutos_periodo']} min)")
    print(f"Cobertura minima exigida: {obj['cobertura_minima']*100:.0f} %\n")
    print(f"{'Metrica':<15}{'Objetivo':<14}{'Medido':<14}{'Cobertura':<11}{'Veredicto':<24}Credito")
    for nombre, r in out["metricas"].items():
        o = m[nombre]
        objetivo = f"{o['operador']} {o['objetivo']:g} {o['unidad']}"
        medido = "-" if r["medido"] is None or r["veredicto"] == INSUF and nombre == "perdida" \
            else f"{r['medido']:.2f} {o['unidad']}"
        print(f"{nombre:<15}{objetivo:<14}{medido:<14}{r['cobertura']*100:>7.2f} %  "
              f"{r['veredicto']:<24}{r['credito']*100:.0f} %")
    d = out["metricas"]["disponibilidad"]["detalle"]
    print(f"\nCaida atribuible : {' + '.join(f'{c:g}' for c in d['caidas'])} = {d['caida_atribuible']:g} min")
    print(f"Caida permitida  : {d['permitido']:.2f} min   Exceso: {d['exceso']:.2f} min")
    j = out["metricas"]["jitter"]["detalle"]
    print(f"Jitter ponderado : {j['suma_productos']:.1f} / {j['muestras']} = "
          f"{out['metricas']['jitter']['medido']:.2f} ms (promedio simple {j['promedio_simple']:.2f} ms, no aplica)")
    for nombre in ("respuesta", "mttr"):
        dd = out["metricas"][nombre]["detalle"]
        print(f"{nombre.capitalize():<17}: {dd['cumplen']} de {dd['total']} tickets dentro del umbral"
              + (f"; fuera: {', '.join(f'{t} ({v:g} min)' for t, v in dd['fuera'])}" if dd["fuera"] else ""))
    partes = " + ".join(f"{r['credito']*100:.0f} %" for r in out["metricas"].values() if r["credito"])
    print(f"\nCredito: {partes} = {out['credito_suma']*100:.0f} % (tope {obj['tope_credito']*100:.0f} %)"
          f" -> aplicado {out['credito_aplicado']*100:.0f} % x ${obj['cargo_mensual']:,} = ${out['monto']:,.0f}")
    print(f"VEREDICTO GLOBAL: {out['veredicto_global']}")
    v = out["viabilidad"]
    if v:
        print(f"\nViabilidad: serie actual {v['serie']:.3f} % (caida esperada {v['caida_esperada_serie']:.1f} min/mes)"
              f" | con respaldo en paralelo {v['con_respaldo']:.3f} % ({v['caida_esperada_respaldo']:.1f} min/mes)"
              f" | permitido {v['permitido']:.2f} min/mes")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-o", "--objetivos", required=True)
    p.add_argument("-m", "--mediciones", required=True)
    p.add_argument("--json", help="guarda el resultado en JSON para generar el informe")
    a = p.parse_args()
    with open(a.objetivos, encoding="utf-8") as f:
        obj = yaml.safe_load(f)
    out = calcular(obj, leer_mediciones(a.mediciones))
    imprimir(obj, out)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
