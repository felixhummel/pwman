.PHONY: default
default: tests

.PHONY: develop
develop:
	python setup.py develop

.PHONY: tests
tests:
	tox

.PHONY: coverage
coverage: tests
	python -mwebbrowser -t docs/coverage/index.html

.PHONY: shell
shell:
	tox --notest
	.tox/py27/bin/python

.PHONY: example_gen
example_gen:
	pwman example_gen

# thx, http://peterdowns.com/posts/first-time-with-pypi.html
.PHONY: publish_test
publish_test:
	python setup.py sdist bdist_wheel
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: publish_prod
publish_prod:
	python setup.py sdist bdist_wheel

