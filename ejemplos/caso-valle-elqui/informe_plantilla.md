---
title: "Informe técnico de verificación de SLA — Caso Agrícola Valle de Elqui"
lang: es-CL
---

<div class="portada">
<p class="etiqueta">Evaluación 3 · Informe técnico</p>
<h1 class="titulo">Verificación del cumplimiento del SLA del enlace dedicado de Agrícola Valle de Elqui</h1>
<p class="subtitulo">Período evaluado: septiembre de 2026</p>
<table class="datos-portada">
<tr><th>Asignatura</th><td>{asignatura}</td></tr>
<tr><th>Sección</th><td>{seccion}</td></tr>
<tr><th>Integrante</th><td>{integrantes}</td></tr>
<tr><th>Docente</th><td>{docente}</td></tr>
<tr><th>Fecha</th><td>{fecha}</td></tr>
<tr><th>Repositorio (tag v1.1)</th><td>{repositorio}</td></tr>
</table>
</div>

<div class="salto"></div>

## Índice

01. Identificación · 02. Resumen ejecutivo · 03. Alcance y referencias · 04. Metodología · 05. Resultados · 06. Análisis de incumplimientos · 07. Conclusiones técnicas · 08. Recomendaciones · 09. Automatización del proceso · Anexos A a E

## 01. Identificación

*Tabla 1. Datos del servicio evaluado.*

| Campo | Detalle |
|---|---|
| Servicio | Internet dedicado simétrico de 200 Mbps (cláusula 2.1) |
| Cliente | Agrícola Valle de Elqui SpA, planta Vicuña |
| Proveedor | NorteNet Telecomunicaciones |
| Período evaluado | 01-sep-2026 00:00 a 30-sep-2026 23:59 · {dias} días · {T} min |
| Punto de demarcación | Puerto LAN del CPE instalado en la planta Vicuña (cláusula 2.2) |
| Servicios del cliente sobre el enlace | ERP, trazabilidad de exportación y telefonía IP |
| Cargo mensual | ${cargo} neto (cláusula 8.4) |
| Integrante | {integrantes} |
| Repositorio | {repositorio} |

## 02. Resumen ejecutivo

<div class="resumen">

**Veredicto global: {global}.** En septiembre de 2026 NorteNet no cumplió dos compromisos: la disponibilidad fue de {A} % (objetivo ≥ 99,9 %) y el ticket {resp_peor} tuvo primera respuesta a los {resp_max} min (objetivo ≤ 60 min en todos los incidentes). Latencia ({lat} ms), jitter ({jit} ms), throughput ({thr} Mbps) y MTTR ({mttr_max} min como máximo) cumplen; la pérdida no puede evaluarse por cobertura insuficiente ({per_cob} %). Corresponde un crédito de **{cred_apl} %, equivalente a ${monto} neto**; el crédito de 50 % solicitado no tiene respaldo contractual.

</div>

## 03. Alcance y referencias

**Cláusulas evaluadas.** 3.1 Disponibilidad, 3.2 Latencia, 3.3 Jitter, 3.4 Pérdida, 3.5 Throughput, 4.1 Tiempo de respuesta y 4.2 MTTR. Las cláusulas 2.1 y 2.2 fijan el servicio y el punto donde se mide.

**Cláusulas que regulan la evaluación.** 5.1 Validez de la medición (cobertura ≥ 90 % del mes); 6.1 Exclusiones (a: mantención programada con ≥ 72 h de aviso y máximo 4 h/mes; b: fuerza mayor declarada; c: falla atribuible al cliente); 6.2 Tratamiento del tiempo excluido (se considera disponible); 7.2 Respaldo eléctrico del CPE a cargo del cliente; 8.1 y 8.2 Créditos; 8.3 Tope de 50 %; 8.4 Cargo mensual.

**Normas de medición.** ITU-T Y.1540 (disponibilidad y parámetros de desempeño de paquetes IP), RFC 3393 (variación del retardo, IPDV/jitter), RFC 5357 (TWAMP) y RFC 6349 (metodología de prueba de throughput TCP).

**Evidencia.** Anexos 1 a 7 del caso (NMS, tickets, Zabbix, TWAMP, pruebas de throughput e infraestructura). Los anexos propios de este informe se identifican con letras (A a E).

**Fuera de alcance.** Calidad de las aplicaciones del cliente, desempeño de la red Wi-Fi interna y mediciones tomadas fuera de la demarcación.

## 04. Metodología

### 4.1 Variables comprometidas por métrica

*Tabla 2. Variables pactadas en el contrato.*

| Métrica (cláusula) | Unidad | Operador y umbral | Período | Punto de medición | Método / herramienta | Estadístico pactado |
|---|---|---|---|---|---|---|
| Disponibilidad (3.1) | % | ≥ 99,9 | Mes calendario | Demarcación (2.2) | No especificado; se usa NMS del cliente contrastado con tickets | Acumulado mensual |
| Latencia (3.2) | ms | ≤ 30 | Mensual | CPE ↔ servidor de medición del proveedor en La Serena | ICMP cada 60 s | RTT promedio |
| Jitter (3.3) | ms | ≤ 10 | Mensual | Demarcación | TWAMP (RFC 5357), jitter según RFC 3393 | Promedio mensual |
| Pérdida (3.4) | % | ≤ 0,5 | Mensual | Demarcación | TWAMP | Porcentaje mensual |
| Throughput (3.5) | Mbps | ≥ 180 (90 % de 200) | Mensual, ≥ 4 pruebas | Demarcación | iperf3 TCP (RFC 6349) | Promedio de las pruebas |
| Tiempo de respuesta (4.1) | min | ≤ 60 | Por incidente | Apertura del ticket → primera respuesta | Sistema de tickets del proveedor | 100 % de los incidentes |
| MTTR (4.2) | min | ≤ 240 (4 h) | Por incidente atribuible | Inicio → fin de la caída | NMS del cliente y tickets | Valor por incidente |

Criterio adoptado para el MTTR: el contrato no indica desde qué instante se mide. Se usa la duración registrada por el NMS (inicio de la caída a restauración), por ser la base más exigente para el proveedor. Con la base alternativa (apertura del ticket a restauración) los valores son 49, 71 y 27 min, y el veredicto no cambia.

### 4.2 Validez de las fuentes de evidencia

*Tabla 3. Decisión sobre cada fuente.*

| Fuente (anexo) | Métrica | Decisión | Fundamento |
|---|---|---|---|
| NMS del cliente (Anexo 1) | Disponibilidad, MTTR | Se acepta | Registra inicio y fin de los 5 eventos; los horarios son coherentes con los tickets del Anexo 2. |
| Tickets y avisos del proveedor (Anexo 2) | Clasificación, respuesta | Se acepta | Contiene hora de apertura, primera respuesta y diagnóstico de cierre de cada evento. |
| Zabbix del cliente, ICMP 60 s (Anexo 3) | Latencia | Se acepta | Método, frecuencia y extremos coinciden con la cláusula 3.2; cobertura {lat_cob} %. |
| Reporte del proveedor, 22,1 ms (Anexo 3) | Latencia | Se descarta | Medido entre PE y core en Santiago, no entre el CPE y el servidor de La Serena (3.2). |
| TWAMP del cliente, jitter semanal (Anexo 4) | Jitter | Se acepta con observación | Medido desde la demarcación (3.3); cobertura {jit_cob} %. Ver inconsistencia en 4.4. |
| TWAMP del cliente, 0,31 % (Anexo 5) | Pérdida | Se descarta para veredicto | Solo cubre del 01 al 18-sep; cobertura {per_cob} % < 90 % (5.1). |
| Reporte del proveedor, 0,18 % (Anexo 5) | Pérdida | Se descarta | Medido entre PE y core, fuera de la demarcación (3.4). |
| iperf3 TCP en puerto LAN del CPE, 4 pruebas (Anexo 6) | Throughput | Se acepta | Herramienta, punto y cantidad mínima de pruebas según 3.5. |
| Speedtest web del gerente por Wi-Fi, 95 Mbps (Anexo 6) | Throughput | Se descarta | Herramienta, punto y medio físico distintos de lo pactado; incluye la red Wi-Fi interna del cliente. |
| Disponibilidad anual por componente (Anexo 7) | Viabilidad | Se usa como dato de diseño | Son valores anuales del proveedor; no miden el mes evaluado. |

### 4.3 Cobertura de cada medición (cláusula 5.1)

Mínimo exigido: 0,90 × {T} min = {per_req} min ({per_req_dias} días). Se asume 1 muestra por minuto en ICMP (pactado) y en TWAMP (supuesto, ver 4.4).

*Tabla 4. Cobertura frente al mínimo de 90 %.*

| Medición | Cálculo | Cobertura | Resultado |
|---|---|---|---|
| Disponibilidad (NMS) | El Anexo 1 no reporta interrupciones del registro | 100,00 % | Válida |
| Latencia (Zabbix ICMP) | {lat_mu} / {T} × 100 | {lat_cob} % | Válida |
| Jitter (TWAMP) | {jit_mu} / {T} × 100 | {jit_cob} % | Válida |
| Pérdida (TWAMP) | {per_mu} / {T} × 100 (18 días × 1.440 min) | {per_cob} % | No válida |
| Throughput (iperf3) | {thr_n} pruebas válidas / 4 exigidas | {thr_n} de 4 | Válida |

Control de consistencia: las {lat_falt} muestras de latencia faltantes ({T} − {lat_mu}) equivalen exactamente a la suma de los cinco eventos de caída (210 + 55 + 105 + 75 + 30 = 475 min). Esto confirma que el registro ICMP no tuvo lagunas propias y que las muestras perdidas corresponden a periodos sin servicio.

### 4.4 Información faltante

*Tabla 5. Datos que faltan y cómo resolverlos.*

| Dato faltante | Métrica afectada | Efecto actual | Qué se requiere |
|---|---|---|---|
| Registro TWAMP de pérdida del 19 al 30-sep | Pérdida (3.4) | Métrica no evaluable; no genera crédito | Al menos {per_falta} min adicionales ({per_falta_dias} de los 12 días faltantes) medidos en la demarcación, p. ej. logs del reflector TWAMP de NorteNet. |
| Origen de las muestras de jitter posteriores al 19-sep | Jitter (3.3) | El Anexo 4 informa muestras en las semanas 15–21 y 22–30, pero el Anexo 5 indica que el colector TWAMP se detuvo el 19-sep | Logs del colector o confirmación de una segunda fuente TWAMP. Si esas muestras no fueran válidas, la cobertura de jitter bajaría de 90 % y la métrica pasaría a evidencia insuficiente. Se evalúa con el Anexo 4 tal como fue entregado. |
| Frecuencia de muestreo TWAMP | Jitter y pérdida (cobertura) | Se asume 1 muestra/min | Configuración del colector TWAMP del cliente. |
| Declaración formal de fuerza mayor para E2 (obras viales) | Disponibilidad (6.1b) | E2 se trata como atribuible | Documento formal de NorteNet. Aun con él: A = ({T} − {caida_sin_e2}) / {T} × 100 = {A_sin_e2} %, que sigue en el tramo de 10 %. |
| Causa del retraso en la respuesta de INC-2672 | Tiempo de respuesta (4.1) | No altera el veredicto | Registro de escalamiento del proveedor para sustentar el reclamo y la recomendación. |

## 05. Resultados

### 5.1 Clasificación de los eventos de caída

*Tabla 6. Clasificación según cláusulas 6.1, 6.2 y 7.2.*

| Ev. | Fecha y horario (NMS) | Duración | Ticket | Clasificación | Fundamento |
|---|---|---|---|---|---|
| E1 | 03-sep 02:00–05:30 | 210 min | MNT-0903 | **Excluido** | Mantención programada. Aviso 29-ago 10:00 → inicio 03-sep 02:00 = 112 h ≥ 72 h; 210 min = 3,5 h ≤ 4 h/mes (6.1a). Se cuenta como tiempo disponible (6.2). |
| E2 | 09-sep 14:12–15:07 | 55 min | INC-2611 | **Atribuible** | Corte de fibra de acceso por obras viales. No existe declaración formal de fuerza mayor (6.1b); la planta externa es responsabilidad del proveedor. |
| E3 | 15-sep 10:40–12:25 | 105 min | INC-2648 | **Excluido** | CPE sin energía por corte eléctrico en la planta, sin UPS. El respaldo eléctrico es del cliente (7.2), por lo que es falla atribuible al cliente (6.1c). |
| E4 | 21-sep 22:05–23:20 | 75 min | INC-2672 | **Atribuible** | Falla de tarjeta de línea en el PE La Serena, equipo del proveedor. |
| E5 | 27-sep 08:30–09:00 | 30 min | INC-2690 | **Atribuible** | Mantención de emergencia. Aviso 26-sep 18:00 → inicio 27-sep 08:30 = 14,5 h < 72 h; no cumple 6.1a. |

Total registrado: 475 min. Excluido: 315 min (E1 + E3). Atribuible al proveedor: {caida_atr} min (E2 + E4 + E5).

### 5.2 Disponibilidad, caída permitida y exceso

```
T total            = {dias} días × 1.440 min/día = {T} min
T caída atribuible = {caidas_suma} = {caida_atr} min
A                  = (T total − T caída atribuible) / T total × 100
                   = ({T} − {caida_atr}) / {T} × 100
                   = {caida_disp} / {T} × 100 = {A4} % ≈ {A} %
Caída permitida    = T total × (1 − 0,999) = {T} × 0,001 = {permitido} min
Exceso             = {caida_atr} − {permitido} = {exceso} min
```

{A} % < 99,9 % → **no cumple** (3.1). El valor cae en el tramo 99,5 % a < 99,9 %, al que corresponde un crédito de {cred_disp} % (8.1).

### 5.3 Latencia, jitter, pérdida y throughput

**Latencia (3.2).** Estadístico pactado: RTT promedio mensual.

```
Latencia = {lat} ms (promedio Zabbix, Anexo 3)  →  {lat} ms ≤ 30 ms  →  CUMPLE
```

El p95 (41,2 ms) y el máximo (118 ms) no son el estadístico pactado y no se usan para el veredicto.

**Jitter (3.3).** El promedio mensual se obtiene ponderando cada semana por su número de muestras, ya que las semanas no tienen la misma cantidad de muestras (la última tiene 9 días).

```
Jitter = Σ (jitter semana × muestras semana) / Σ muestras
{jit_lineas}
Σ productos = {jit_suma}      Σ muestras = {jit_mu}
Jitter = {jit_suma} / {jit_mu} = {jit3} ms ≈ {jit} ms  →  {jit} ms ≤ 10 ms  →  CUMPLE
```

El promedio simple de las cuatro semanas ({jit_simple} ms) superaría el umbral, pero no es el promedio mensual porque da el mismo peso a semanas con distinta cantidad de muestras. La semana 15–21 sep (13,8 ms) supera el umbral de forma aislada; el contrato evalúa el mes completo.

**Pérdida (3.4).**

```
Cobertura = {per_mu} / {T} × 100 = {per_cob} %  <  90 %  →  EVIDENCIA INSUFICIENTE
```

El valor parcial de {per_val} % (01 al 18-sep) no se extrapola al mes. El reporte del proveedor (0,18 %) se midió fuera de la demarcación.

**Throughput (3.5).** Estadístico pactado: promedio de las pruebas iperf3 del mes.

```
Umbral     = 0,90 × 200 Mbps = 180 Mbps
Throughput = ({thr_pruebas}) / {thr_n} = {thr_suma} / {thr_n} = {thr} Mbps
{thr} Mbps ≥ 180 Mbps  →  CUMPLE   (desviación +{desv_thr} Mbps)
```

La prueba del 19-sep (171 Mbps) queda bajo el umbral, pero la cláusula evalúa el promedio. El Speedtest de 95 Mbps no se considera (Tabla 3).

### 5.4 Tiempo de respuesta y MTTR por ticket

*Tabla 7. Verificación por ticket (cláusulas 4.1 y 4.2).*

| Ticket | Evento | Apertura | 1ª respuesta | Respuesta | ≤ 60 min | Caída (NMS) | MTTR | ≤ 240 min |
|---|---|---|---|---|---|---|---|---|
| INC-2611 | E2 | 09-sep 14:18 | 14:41 | 23 min | Sí | 14:12–15:07 | 55 min | Sí |
| INC-2648 | E3 | 15-sep 10:47 | 11:20 | 33 min | Sí | 10:40–12:25 | No aplica (cliente) | — |
| INC-2672 | E4 | 21-sep 22:09 | 23:15 | 66 min | **No** | 22:05–23:20 | 75 min | Sí |
| INC-2690 | E5 | 27-sep 08:33 | 08:40 | 7 min | Sí | 08:30–09:00 | 30 min | Sí |

MNT-0903 es un aviso de mantención programada y no un incidente, por lo que no se le exige tiempo de respuesta. INC-2648 se incluye en 4.1 porque la cláusula aplica a todos los incidentes; su resultado (33 min) no cambia el veredicto.

```
Tiempo de respuesta: {resp_ok} de {resp_tot} incidentes ≤ 60 min = {resp_pct} %  <  100 % exigido  →  NO CUMPLE
                     {resp_peor}: 66 − 60 = {resp_exc} min sobre el umbral
MTTR máximo:         {mttr_max} min ≤ 240 min  →  CUMPLE
```

### 5.5 Tabla de resultados

*Tabla 8. Resultado por métrica.*

| Métrica | Objetivo | Medido | Desviación | Fuente | Veredicto | Crédito |
|---|---|---|---|---|---|---|
| Disponibilidad | ≥ 99,9 % | {A} % | {desv_A} pp | NMS + tickets (Anexos 1 y 2) | **{ver_disponibilidad}** | {cred_disp} % |
| Latencia | ≤ 30 ms | {lat} ms | {desv_lat} ms | Zabbix ICMP (Anexo 3) | {ver_latencia} | 0 % |
| Jitter | ≤ 10 ms | {jit} ms | {desv_jit} ms | TWAMP ponderado (Anexo 4) | {ver_jitter} | 0 % |
| Pérdida | ≤ 0,5 % | No evaluable | — | TWAMP, cobertura {per_cob} % (Anexo 5) | {ver_perdida} | 0 % |
| Throughput | ≥ 180 Mbps | {thr} Mbps | +{desv_thr} Mbps | iperf3 (Anexo 6) | {ver_throughput} | 0 % |
| Tiempo de respuesta | ≤ 60 min (100 %) | {resp_max} min máx. ({resp_ok} de {resp_tot}) | +{resp_exc} min | Tickets (Anexo 2) | **{ver_respuesta}** | {cred_resp} % |
| MTTR | ≤ 240 min | {mttr_max} min máx. | {desv_mttr} min | NMS + tickets | {ver_mttr} | — |
| **Global** | | | | | **{global}** | **{cred_apl} %** |

Las cifras de esta tabla coinciden con la salida de calc_sla.py (Anexo C).

## 06. Análisis de incumplimientos

*Tabla 9. Incumplimientos comprobados y evidencia insuficiente.*

| Hallazgo | Qué ocurrió | Cuándo | Causa | Impacto en el negocio | Origen | Efecto |
|---|---|---|---|---|---|---|
| Disponibilidad | {caida_atr} min de caída atribuible frente a {permitido} min permitidos | 09-sep (55 min), 21-sep (75 min), 27-sep (30 min) | Corte de fibra de acceso sin ruta alternativa; falla de tarjeta en PE La Serena; mantención de emergencia avisada con 14,5 h | Interrupción del ERP, la trazabilidad de exportación y la telefonía IP durante {caida_atr} min | Proveedor | Crédito de {cred_disp} % (8.1) |
| Tiempo de respuesta | Primera respuesta de INC-2672 a los 66 min | 21-sep, 22:09 → 23:15 | La evidencia no indica la causa; el incidente ocurrió en horario nocturno | El cliente estuvo sin información del proveedor durante casi toda la caída: la respuesta llegó 5 min antes de la restauración (23:20) | Proveedor | Crédito de {cred_resp} % (8.2) |
| Pérdida (evidencia insuficiente) | No hay registro TWAMP desde el 19-sep | 19 al 30-sep | Colector TWAMP del cliente detenido por disco lleno y no recuperado | No es posible verificar la pérdida ni reclamar un eventual 5 % adicional | Cliente | Sin crédito |

Los eventos E1 (mantención programada) y E3 (falta de UPS en el CPE) no constituyen incumplimientos del proveedor. Sin embargo, E3 significó 105 min sin servicio para la planta, un tiempo mayor que cualquiera de los eventos atribuibles.

## 07. Conclusiones técnicas

### 7.1 Veredicto

**Global: {global}.** No cumplen la disponibilidad ({A} % < 99,9 %) y el tiempo de respuesta ({resp_ok} de {resp_tot} incidentes dentro de 60 min). Cumplen la latencia ({lat} ms), el jitter ({jit} ms), el throughput ({thr} Mbps) y el MTTR ({mttr_max} min como máximo). La pérdida queda con evidencia insuficiente.

### 7.2 Crédito de servicio

*Tabla 10. Cálculo del crédito.*

| Concepto | Cláusula | Crédito |
|---|---|---|
| Disponibilidad {A} %: tramo 99,5 % a < 99,9 % | 8.1 | {cred_disp} % |
| Tiempo de respuesta: incumplimiento | 8.2 | {cred_resp} % |
| Latencia, jitter y throughput: cumplen | 8.2 | 0 % |
| Pérdida: evidencia insuficiente, no es incumplimiento comprobado | 8.2 | 0 % |
| **Suma** | — | **{cred_suma} %** |
| Tope | 8.3 | {tope} % (no se alcanza) |

```
Crédito aplicado = mín({cred_suma} %, {tope} %) = {cred_apl} %
Monto            = {cred_apl} % × ${cargo} = ${monto} neto
```

### 7.3 Viabilidad del objetivo de 99,9 %

Los componentes del servicio están en serie (basta que uno falle para que el servicio caiga), con disponibilidades anuales informadas por el proveedor (Anexo 7).

```
Infraestructura actual (serie):
A serie = A CPE × A fibra × A PE × A backbone
        = 0,9995 × 0,9980 × 0,9999 × 0,9999 = {v_serie} %
Caída esperada = (1 − A serie) × {T} min = {v_cs} min/mes  >  {permitido} min permitidos

Con radioenlace de respaldo en paralelo con la fibra:
A acceso = 1 − (1 − 0,9980) × (1 − 0,9950) = 1 − 0,0020 × 0,0050 = {v_acc} %
A total  = 0,9995 × {v_acc} % × 0,9999 × 0,9999 = {v_resp} %
Caída esperada = (1 − A total) × {T} min = {v_cr} min/mes  ≤  {permitido} min (margen {v_margen} min)
```

Con la infraestructura actual el objetivo de 99,9 % **no es viable**: la disponibilidad esperada ({v_serie} %) queda bajo el compromiso y la caída esperada supera la permitida en {v_deficit} min/mes. La fibra de acceso de ruta única es el componente más débil. Con el radioenlace en paralelo la disponibilidad esperada sube a {v_resp} % y el objetivo pasa a ser viable, aunque con un margen reducido de {v_margen} min/mes; el CPE (99,95 %) pasa a ser el componente limitante. El cálculo supone que fibra y radioenlace fallan de forma independiente, lo que exige rutas y equipos de acceso distintos.

### 7.4 Respuesta al gerente de operaciones

*Tabla 11. Revisión de las afirmaciones del correo.*

| Afirmación | ¿Se sostiene? | Fundamento |
|---|---|---|
| "Septiembre fue un desastre. Se cayó varias veces." | Parcialmente | Hubo 5 caídas (475 min), pero 2 están excluidas por contrato (E1 mantención programada, E3 falta de UPS del cliente). Las 3 atribuibles suman {caida_atr} min y hacen que la disponibilidad ({A} %) no cumpla. |
| "Speedtest de 95 Mbps cuando pagamos 200." | No | El Speedtest usó otra herramienta, otro punto y Wi-Fi interno (3.5). Las pruebas iperf3 en la demarcación promedian {thr} Mbps, sobre el umbral de 180 Mbps. La diferencia apunta a la red interna o al equipo del gerente. |
| "En Zabbix vi peaks de 118 ms." | No como base de reclamo | El valor existe (máximo del Anexo 3), pero la cláusula 3.2 evalúa el RTT promedio mensual: {lat} ms ≤ 30 ms, cumple. |
| "Exigir el crédito máximo (50 %)." | No | El 50 % exigiría disponibilidad < 99,0 % o acumular créditos hasta el tope. Corresponde {cred_apl} % = ${monto} neto. Incluso si la pérdida se hubiera podido medir y no cumpliera, el crédito sería 20 %. |

## 08. Recomendaciones

*Tabla 12. Recomendaciones priorizadas.*

| # | Hallazgo | Recomendación | Qué mejora | Prioridad |
|---|---|---|---|---|
| 1 | Disponibilidad {A} % y {caida_atr} min atribuibles | Presentar a NorteNet el reclamo por {cred_apl} % (${monto} neto) adjuntando las Tablas 6, 7 y 8. | Recupera el monto que corresponde, con respaldo verificable | Alta |
| 2 | A serie {v_serie} %: objetivo no viable con fibra de ruta única | Contratar el radioenlace de respaldo en paralelo, con ruta y equipo de acceso independientes de la fibra. | Disponibilidad esperada de {v_resp} %; elimina el punto único de falla del acceso | Alta |
| 3 | Pérdida no evaluable por colector TWAMP detenido | Restaurar el colector, ampliar el disco, configurar alertas de espacio y de ausencia de muestras en Zabbix, y solicitar los logs del reflector TWAMP de NorteNet. | Evidencia completa (≥ 90 %) para futuros reclamos | Alta |
| 4 | E3: 105 min sin servicio por CPE sin UPS | Instalar UPS para el CPE con autonomía mínima de 2 h, con monitoreo de batería. | Evita la caída más larga del mes, que no es compensable por contrato | Media |
| 5 | INC-2672 respondido en 66 min, en horario nocturno | Exigir al proveedor un procedimiento de escalamiento 24×7 con contactos y plazos. | Cumplimiento de 4.1 fuera de horario hábil | Media |
| 6 | Inconsistencia entre Anexos 4 y 5 en el jitter posterior al 19-sep | Obtener los logs del colector y documentar qué sistema generó cada muestra. | Asegura que el veredicto de jitter sea defendible ante el proveedor | Media |
| 7 | Contrato sin inicio definido de MTTR; E2 y E5 en zona gris | En la renovación, definir el inicio del MTTR, el plazo para declarar fuerza mayor y el tratamiento de las mantenciones de emergencia. | Menos discusión en futuros reclamos | Media |
| 8 | Reclamo basado en Speedtest por Wi-Fi y en el máximo de latencia | Definir un protocolo interno: medir solo en la demarcación con iperf3 y reportar el estadístico pactado. | Evita reclamos sin sustento contractual | Baja |

## 09. Automatización del proceso

### 9.1 Flujo

*Tabla 13. Flujo desde los anexos hasta el PDF.*

| Paso | Entrada | Proceso | Salida | Tipo |
|---|---|---|---|---|
| 1 | Anexos del caso | Clasificación de eventos, validación de fuentes y carga de datos | objetivos.yaml, mediciones.csv | Manual |
| 2 | YAML + CSV | herramientas/calc_sla.py | salida_calc.txt y salida_calc.json | Automático |
| 3 | JSON + informe_plantilla.md | herramientas/generar_informe.py (str.format) | informe.md | Automático |
| 4 | informe.md | pandoc con motor wkhtmltopdf y estilo.css | informe.pdf | Automático |
| 5 | Carpeta del caso | Commit en rama caso/valle-elqui, merge a main y tag | Versión v1.1 | Manual (comandos git) |

Nivel de automatización: **intermedio-avanzado**. Un solo comando (`make informe`) ejecuta los pasos 2 a 4.

### 9.2 Qué se automatizó y qué se hizo a mano

- **Automatizado en calc_sla.py:** disponibilidad, caída permitida y exceso; cobertura de cada medición a partir de las muestras; **promedio ponderado del jitter**; promedio de throughput con control de pruebas mínimas; verificación ticket por ticket de respuesta y MTTR; tramos de crédito, suma, tope y monto; disponibilidad serie/paralelo.
- **Automatizado en generar_informe.py:** inserción de todas las cifras, veredictos y anexos en la plantilla. La plantilla no contiene cifras de resultado escritas a mano.
- **Manual:** clasificación de eventos (requiere interpretar diagnósticos frente a las cláusulas 6.1 y 7.2), aceptación o descarte de fuentes, identificación de información faltante, análisis, respuesta al gerente y recomendaciones. La clasificación automática de eventos queda registrada como mejora pendiente en el CHANGELOG.

### 9.3 Comandos para regenerar el informe

```
git clone {repositorio}
cd sla-toolkit && git checkout v1.1
pip install pyyaml          # requiere también pandoc y wkhtmltopdf
make informe                # calc_sla.py → generar_informe.py → pandoc
```

### 9.4 Declaración de uso de IA

- **Herramienta:** Claude (Anthropic), en los pasos 2 y 3 del flujo: apoyo en la programación de calc_sla.py y generar_informe.py, y en la redacción de la plantilla del informe.
- **Contexto entregado:** enunciado de la evaluación (EVA 3), especificaciones del informe, caso resuelto de Clínica Limarí como referencia de formato y material de clases sobre SLA.
- **Revisión:** la clasificación de eventos, las decisiones sobre las fuentes y las conclusiones se contrastaron con las cláusulas del contrato.
- **Verificación de cifras:** todas las cifras del informe se insertan desde salida_calc.json, por lo que coinciden con salida_calc.txt (Anexo C); los cálculos manuales del Anexo D se recalcularon de forma independiente.

<div class="salto"></div>

## Anexos

### Anexo A — objetivos.yaml

```yaml
{objetivos_yaml}
```

### Anexo B — mediciones.csv

Solo se cargan mediciones válidas. E1 y E3 no se cargan por estar excluidos. La pérdida se carga con sus muestras para que la calculadora determine su cobertura.

```
{mediciones_csv}
```

### Anexo C — Salida completa de calc_sla.py

```
$ python3 herramientas/calc_sla.py -o ejemplos/caso-valle-elqui/objetivos.yaml \
          -m ejemplos/caso-valle-elqui/mediciones.csv --json ejemplos/caso-valle-elqui/salida_calc.json
{salida_calc}
```

### Anexo D — Cálculos manuales

```
Anticipación E1:  29-ago 10:00 → 03-sep 02:00 = 5 días × 24 h − 8 h = 112 h  (≥ 72 h)
Anticipación E5:  26-sep 18:00 → 27-sep 08:30 = 6 h + 8,5 h = 14,5 h        (< 72 h)
Respuesta:        INC-2611 14:41 − 14:18 = 23 min · INC-2648 11:20 − 10:47 = 33 min
                  INC-2672 23:15 − 22:09 = 66 min · INC-2690 08:40 − 08:33 = 7 min
MTTR (NMS):       E2 15:07 − 14:12 = 55 min · E4 23:20 − 22:05 = 75 min · E5 09:00 − 08:30 = 30 min
MTTR (ticket):    INC-2611 15:07 − 14:18 = 49 min · INC-2672 23:20 − 22:09 = 71 min · INC-2690 09:00 − 08:33 = 27 min
Escenario E2 FM:  A = ({T} − {caida_sin_e2}) / {T} × 100 = {disp_sin_e2} / {T} × 100 = {A_sin_e2} %  → tramo 10 %
Cobertura pérdida: mínimo {per_req} min − registrados {per_mu} min = faltan {per_falta} min ({per_falta_dias} días)
```

### Anexo E — Historial de commits y CHANGELOG

```
{git_log}
```

```
{changelog}
```
