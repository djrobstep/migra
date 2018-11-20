.PHONY: docs

# test commands and arguments
tcommand = py.test -x
tmessy = -svv
targs = --cov-report term-missing --cov migra

test:
	$(tcommand) $(targs) tests

stest:
	$(tcommand) $(tmessy) $(targs) tests

gitclean:
	git clean -fXd

clean:
	find . -name \*.pyc -delete
	rm -rf .cache
	rm -rf build

fmt:
	isort -rc .
	black .

lint:
	flake8 .
