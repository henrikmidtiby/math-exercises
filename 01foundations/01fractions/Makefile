files := $(shell ls *.tex)

clean:
	rm -f *.aux *.log *.toc *.out

cleanall: clean
	rm -f *.pdf *.json

exercises: 
	for filename in $(files); do \
	  pdflatex $$filename ; \
	  pdflatex $$filename ; \
	  pdflatex $$filename ; \
	  python ../../src/exercise_converter/exerciseconverter.py $$filename ; \
	done

