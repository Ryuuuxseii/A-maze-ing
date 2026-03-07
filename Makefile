MAIN = a_maze_ing.py\

CACHE = __pycache__\
		.mypy_cache\


install:
	pip install -e .
	pip install flake8 mypy

run:
	python3 $(MAIN) config.txt

debug:
	python3 -m pdb $(MAIN) config.txt

clean:
	rm -fr $(CACHE)

lint:
	flake8 .
	mypy . \
	--warn-return-any\
	--warn-unused-ignores\
	--ignore-missing-imports\
	--disallow-untyped-defs\
	--check-untyped-defs\

 lint-strict:
	flake8 . 
	mypy . --strict