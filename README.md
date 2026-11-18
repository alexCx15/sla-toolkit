# sla-toolkit

Herramientas para verificar el cumplimiento de un SLA de enlace dedicado y generar el informe técnico.
Asignatura Infraestructura de Telecomunicaciones — Alexander Cortes.

## Estructura

```
herramientas/
  calc_sla.py          calculadora (YAML + CSV -> veredictos, crédito, serie/paralelo)
  generar_informe.py   completa la plantilla del informe con la salida de la calculadora
  estilo.css           estilo del PDF
ejemplos/caso-valle-elqui/
  sla.md, objetivos.yaml, mediciones.csv, portada.yaml
  informe_plantilla.md, salida_calc.txt, salida_calc.json, informe.md, informe.pdf
Makefile
CHANGELOG.md
```

## Uso

Requisitos: Python 3 con `pyyaml`, `pandoc` y `wkhtmltopdf`.

```
make informe     # calcula, genera informe.md y convierte a informe.pdf
make calc        # solo la calculadora
```
