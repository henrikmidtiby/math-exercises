allexercises:
	find . -name "Makefile" | awk ' {gsub(/\/Makefile/, ""); print}' | sort | xargs -n1 sh -c 'cd $$0 && make exercises'

cleanallexercises:
	find . -name "Makefile" | awk ' {gsub(/\/Makefile/, ""); print}' | sort | xargs -n1 sh -c 'cd $$0 && make clean'

extractallexercises:
	find . -name "*.tex"  | sort | xargs -n1 sh -c 'python3 src/exerciseconverter.py $$0'
