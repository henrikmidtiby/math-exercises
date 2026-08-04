files := $(shell ls *.tex)

clean:
	rm -f *.aux *.log *.toc *.out

cleanall: clean
	rm -f *.pdf *.json

pdfs:
	for filename in $(files); do \
	  pdflatex $$filename ; \
	done

exercises:
	for filename in $(files); do \
	  uv run python ../../src/exercise_converter/exerciseconverter.py $$filename ; \
	done

