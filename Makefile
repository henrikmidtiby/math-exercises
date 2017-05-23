allexercises:
	find . -name "Makefile" | awk ' {gsub(/\/Makefile/, ""); print}' | sort | xargs -n1 sh -c 'cd $$0 && make exercises'

listallexercises:
	find . -name "*.tex" | sort 

cleanallexercises:
	find . -name "Makefile" | awk ' {gsub(/\/Makefile/, ""); print}' | sort | xargs -n1 sh -c 'cd $$0 && make clean'

extractallexercises:
	find . -name "*.tex"  | sort | xargs -n1 sh -c 'python3 src/exerciseconverter.py $$0'

collectalljsonfiles:
	rm -f combinedjsonfiles.txt
	find . -name "*.json"  | sort | xargs -n1 sh -c 'cat $$0 >> combinedjsonfiles.txt'

finderrorsinjsonfiles:
	@echo ""
	@echo "               =================================="
	@echo "               =================================="
	@echo ""
	@echo "               Issues with the latex command emph"
	@echo "" 
	@echo "               =================================="
	@echo "               =================================="
	@echo ""
	find . -name "*.json"  | sort | xargs -n1 sh -c 'grep -H emph "$$0" || true'
	# The lines below are commented out as they result in a very large amount of output.
	# echo "Maybe issues with forced newline"
	# find . -name "*.json"  | sort | xargs -n1 sh -c 'grep -H \\\\\\\\\\\\\\\\ "$$0" || true'
