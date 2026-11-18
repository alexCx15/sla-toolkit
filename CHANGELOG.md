# Changelog

## [1.1] - 2026-11-18
### Agregado
- ejemplos/caso-valle-elqui/: sla.md, objetivos.yaml, mediciones.csv, portada.yaml, informe_plantilla.md, salida_calc.txt, informe.md, informe.pdf.
- calc_sla.py: cobertura por métrica a partir de las muestras (cláusula 5.1) y veredicto "EVIDENCIA INSUFICIENTE".
- calc_sla.py: promedio de jitter ponderado por muestras.
- calc_sla.py: verificación de tiempo de respuesta y MTTR ticket por ticket.
- calc_sla.py: tramos de crédito, tope, monto y disponibilidad serie/paralelo; salida JSON (--json).
- generar_informe.py y Makefile: regeneración del informe y del PDF con `make informe`.
### Pendiente
- calc_sla.py: clasificación automática de eventos atribuibles/excluidos (hoy se hace a mano según 6.1 y 7.2).
- calc_sla.py: cálculo de horas de anticipación de avisos de mantención a partir de fechas.
- calc_sla.py: leer las caídas con hora de inicio y fin en lugar de minutos ya calculados.

## [1.0] - 2026-11-18
### Agregado
- herramientas/calc_sla.py: disponibilidad, latencia, pérdida y throughput contra objetivos en YAML.
