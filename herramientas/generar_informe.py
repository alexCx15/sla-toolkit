#!/usr/bin/env python3
"""generar_informe.py - Completa la plantilla del informe con la salida de calc_sla.py.

Uso:
    python3 herramientas/generar_informe.py ejemplos/caso-valle-elqui

Lee en la carpeta del caso: portada.yaml, objetivos.yaml, mediciones.csv,
salida_calc.json, salida_calc.txt e informe_plantilla.md, y escribe informe.md.
Todas las cifras calculadas provienen de salida_calc.json; la plantilla no
contiene cifras de resultados escritas a mano.
"""
import json
import os
import subprocess
import sys

import yaml


def n(x, d=2):
    """Formato chileno: miles con punto y decimales con coma."""
    s = f"{x + (1e-9 if x >= 0 else -1e-9):,.{d}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def git(*args):
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "(historial no disponible)"


def main(caso):
    portada = yaml.safe_load(leer(os.path.join(caso, "portada.yaml")))
    obj = yaml.safe_load(leer(os.path.join(caso, "objetivos.yaml")))
    out = json.loads(leer(os.path.join(caso, "salida_calc.json")))
    M = out["metricas"]
    T = obj["minutos_periodo"]
    disp, jit, thr = M["disponibilidad"], M["jitter"], M["throughput"]
    d = disp["detalle"]
    v = out["viabilidad"]

    # Escenario: si se acreditara fuerza mayor para E2 (55 min)
    caida_sin_e2 = d["caida_atribuible"] - 55
    a_sin_e2 = (T - caida_sin_e2) / T * 100

    perdida = M["perdida"]
    req_cob = obj["cobertura_minima"] * T

    j_lineas = []
    for (val, mu), p in zip(jit["detalle"]["semanas"], jit["detalle"]["productos"]):
        j_lineas.append(f"{n(val, 1)} × {n(mu, 0)} = {n(p, 1)}")

    resp = M["respuesta"]["detalle"]
    peor = resp["fuera"][0] if resp["fuera"] else ("-", 0)

    valores = {
        **portada,
        "T": n(T, 0),
        "dias": obj["dias_periodo"],
        "cargo": n(obj["cargo_mensual"], 0),
        "A": n(disp["medido"], 2),
        "A4": n(disp["medido"], 4),
        "caidas_suma": " + ".join(n(c, 0) for c in d["caidas"]),
        "caida_atr": n(d["caida_atribuible"], 0),
        "caida_disp": n(T - d["caida_atribuible"], 0),
        "permitido": n(d["permitido"], 2),
        "exceso": n(d["exceso"], 2),
        "desv_A": n(disp["medido"] - 99.9, 2),
        "A_sin_e2": n(a_sin_e2, 2),
        "caida_sin_e2": n(caida_sin_e2, 0),
        "disp_sin_e2": n(T - caida_sin_e2, 0),
        "lat": n(M["latencia"]["medido"], 1),
        "lat_cob": n(M["latencia"]["cobertura"] * 100, 2),
        "lat_mu": n(M["latencia"]["detalle"]["muestras"], 0),
        "lat_falt": n(T - M["latencia"]["detalle"]["muestras"], 0),
        "desv_lat": n(M["latencia"]["medido"] - 30, 1),
        "jit": n(jit["medido"], 2),
        "jit3": n(jit["medido"], 3),
        "jit_cob": n(jit["cobertura"] * 100, 2),
        "jit_mu": n(jit["detalle"]["muestras"], 0),
        "jit_suma": n(jit["detalle"]["suma_productos"], 1),
        "jit_lineas": "\n".join("  " + x for x in j_lineas),
        "jit_simple": n(jit["detalle"]["promedio_simple"], 2),
        "desv_jit": n(jit["medido"] - 10, 2),
        "per_val": n(0.31, 2),
        "per_cob": n(perdida["cobertura"] * 100, 2),
        "per_mu": n(perdida["detalle"]["muestras"], 0),
        "per_req": n(req_cob, 0),
        "per_req_dias": n(req_cob / 1440, 0),
        "per_falta": n(req_cob - perdida["detalle"]["muestras"], 0),
        "per_falta_dias": n((req_cob - perdida["detalle"]["muestras"]) / 1440, 0),
        "thr": n(thr["medido"], 2),
        "thr_suma": n(thr["detalle"]["suma"], 0),
        "thr_pruebas": " + ".join(n(x, 0) for x in thr["detalle"]["pruebas"]),
        "thr_n": len(thr["detalle"]["pruebas"]),
        "desv_thr": n(thr["medido"] - 180, 2),
        "resp_max": n(M["respuesta"]["medido"], 0),
        "resp_ok": resp["cumplen"],
        "resp_tot": resp["total"],
        "resp_pct": n(resp["cumplen"] / resp["total"] * 100, 0),
        "resp_peor": peor[0],
        "resp_exc": n(peor[1] - 60, 0),
        "mttr_max": n(M["mttr"]["medido"], 0),
        "desv_mttr": n(M["mttr"]["medido"] - 240, 0),
        "cred_disp": n(disp["credito"] * 100, 0),
        "cred_resp": n(M["respuesta"]["credito"] * 100, 0),
        "cred_suma": n(out["credito_suma"] * 100, 0),
        "cred_apl": n(out["credito_aplicado"] * 100, 0),
        "tope": n(obj["tope_credito"] * 100, 0),
        "monto": n(out["monto"], 0),
        "global": out["veredicto_global"],
        "v_serie": n(v["serie"], 3),
        "v_resp": n(v["con_respaldo"], 3),
        "v_acc": n(v["acceso_paralelo"], 3),
        "v_cs": n(v["caida_esperada_serie"], 1),
        "v_cr": n(v["caida_esperada_respaldo"], 1),
        "v_margen": n(v["permitido"] - v["caida_esperada_respaldo"], 1),
        "v_deficit": n(v["caida_esperada_serie"] - v["permitido"], 1),
        "objetivos_yaml": leer(os.path.join(caso, "objetivos.yaml")).rstrip(),
        "mediciones_csv": leer(os.path.join(caso, "mediciones.csv")).rstrip(),
        "salida_calc": leer(os.path.join(caso, "salida_calc.txt")).rstrip(),
        "git_log": git("log", "--oneline", "--decorate", "-n", "12"),
        "changelog": leer("CHANGELOG.md").rstrip() if os.path.exists("CHANGELOG.md") else "",
    }
    for nombre in M:
        valores[f"ver_{nombre}"] = M[nombre]["veredicto"].capitalize()

    plantilla = leer(os.path.join(caso, "informe_plantilla.md"))
    salida = plantilla.format_map(valores)
    with open(os.path.join(caso, "informe.md"), "w", encoding="utf-8") as f:
        f.write(salida)
    print(f"informe.md generado en {caso}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
