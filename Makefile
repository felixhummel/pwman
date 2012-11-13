.PHONY: default develop tests coverage shell example_gen

default: tests

develop:
	python setup.py develop

tests:
	tox -- -pdb

coverage: tests
	python -mwebbrowser -t docs/coverage/index.html

shell:
	tox --notest
	.tox/py27/bin/python

example_gen:
	pwman example_gen

