MAIN = a_maze_ing.py 

FILES = a_maze_ing.py \
		mazegen/generator.py \
		mazeparse/parser.py

CACHE = */__pycache__\
		.mypy_cache \
		mazegen.egg-info

CONFIG = config.txt

run:
	python3 $(MAIN) $(CONFIG)

install:
	pip install flake8 mypy build

build:
	python3 -m build

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


.PHONY: install run debug clean lint