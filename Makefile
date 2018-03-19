.PHONY: docs

# test commands and arguments
tcommand = PYTHONPATH=. py.test -x
tmessy = -svv
targs = --cov-report term-missing --cov migra

pip:
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

tox:
	tox tests

test:
	$(tcommand) $(targs) tests

stest:
	$(tcommand) $(tmessy) $(targs) tests

clean:
	git clean -fXd
	find . -name \*.pyc -delete
	rm -rf .cache

docs:
	cd docs && mkdocs build

docsserve:
	cd docs && mkdocs serve

fmt:
	black .

lint:
	flake8 .

tidy: clean lint

all: tidy docs tox

publish:
	python setup.py sdist bdist_wheel --universal
	twine upload dist/*
