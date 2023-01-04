SHELL := /bin/bash

clean: ## remove python/pytest cache files and other temp junk
	find . -name '*.pyc' | xargs rm -rf
	find . -name '*__pycache__' | xargs rm -rf
	find . -name '*.cache' | xargs rm -rf
	rm -r .pytest_cache 2>/dev/null || true

lint: ## check code with linters
	pylama .

isort: ## sort imports
	isort .

black: ## format code
	black .

format: clean isort black ## do isort and black
