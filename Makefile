.PHONY: docs

# test commands and arguments
tcommand = py.test -x
tmessy = -svv
targs = --cov-report term-missing --cov migra

test:
	docker build -t migra-postgres --build-arg LOCAL_USER=$$USER - < tests/Dockerfile 
	$(eval ID := $(shell docker run -d -p 5432:5432 migra-postgres))
	$(tcommand) $(tmessy) $(targs) tests || true
	docker stop $(ID)
	docker rm $(ID)

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
