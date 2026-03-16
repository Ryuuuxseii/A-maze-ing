MAIN = a_maze_ing.py 

FILES = a_maze_ing.py \
		mazegen/generator.py \
		mazeparse/parser.py

CACHE = */__pycache__\
		.mypy_cache

CONFIG = config.txt


install:
	pip install flake8 mypy build

run:
	python3 $(MAIN) $(CONFIG)

debug:
	python3 -m pdb $(MAIN) $(CONFIG)

clean:
	rm -fr $(CACHE)

lint:
	flake8 $(FILES)
	mypy $(FILES) \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	flake8 $(FILES) 
	mypy . --strict


.PHONY: install run debug clean lint lint-strict