files := $(shell ls *.tex)

clean:
	rm *.pdf *.aux *.log *.toc *.out

exercises: 
	echo $(files)
	for filename in $(files); do \
	  pdflatex $$filename ; \
	  pdflatex $$filename ; \
	  pdflatex $$filename ; \
	done
