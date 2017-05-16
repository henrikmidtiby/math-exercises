allexercises:
	find . -name "Makefile" | awk ' {gsub(/\/Makefile/, ""); print}' | sort | xargs -n1 sh -c 'cd $$0 && make exercises'

cleanallexercises:
	find . -name "Makefile" | awk ' {gsub(/\/Makefile/, ""); print}' | sort | xargs -n1 sh -c 'cd $$0 && make clean'

extractallexercises:
	find . -name "*.tex"  | sort | xargs -n1 sh -c 'python3 src/exerciseconverter.py $$0'

collectalljsonfiles:
	rm -f combinedjsonfiles.txt
	find . -name "*.json"  | sort | xargs -n1 sh -c 'cat $$0 >> combinedjsonfiles.txt'

finderrorsinjsonfiles:
	find . -name "*.json"  | sort | xargs -n1 sh -c 'grep -H emph "$$0"'
