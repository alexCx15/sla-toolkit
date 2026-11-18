export LC_ALL := C.UTF-8
export LANG := C.UTF-8
CASO = ejemplos/caso-valle-elqui

.PHONY: informe calc clean

informe: calc
	python3 herramientas/generar_informe.py $(CASO)
	pandoc $(CASO)/informe.md -s \
		--css herramientas/estilo.css --embed-resources --pdf-engine=wkhtmltopdf \
		--pdf-engine-opt=--enable-local-file-access \
		-V margin-top=18mm -V margin-bottom=18mm -V margin-left=16mm -V margin-right=16mm \
		--pdf-engine-opt=--footer-center --pdf-engine-opt="Página [page] de [topage]" \
		--pdf-engine-opt=--footer-font-size --pdf-engine-opt=8 \
		-o $(CASO)/informe.pdf

calc:
	python3 herramientas/calc_sla.py -o $(CASO)/objetivos.yaml -m $(CASO)/mediciones.csv \
		--json $(CASO)/salida_calc.json > $(CASO)/salida_calc.txt

clean:
	rm -f $(CASO)/salida_calc.txt $(CASO)/salida_calc.json $(CASO)/informe.md $(CASO)/informe.pdf
