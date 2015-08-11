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

# thx, http://peterdowns.com/posts/first-time-with-pypi.html
.PHONY: publish_test
publish_test:
	python setup.py register -r pypitest
	python setup.py sdist upload -r pypitest

.PHONY: publish_prod
publish_prod:
	python setup.py register -r pypi
	python setup.py sdist upload -r pypi

