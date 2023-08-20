VERSION := $(shell grep __version__ htk/__version__.py | awk '{ print $$3 }' | tr -d "'")

## help - Display help about make targets for this Makefile
help:
	@cat Makefile | grep '^## ' --color=never | cut -c4- | sed -e "`printf 's/ - /\t- /;'`" | column -s "`printf '\t'`" -t

## isort - isort Python files
isort:
	isort -rc *

## clean - Cleans build artifacts
clean:
	rm -rf dist/*
	rm -rf build/*

## version - Shows current version of package
version:
	echo $(VERSION)

## package - Builds a package for dist
package:
	python setup.py sdist bdist_wheel

## repackage - Alias of 'make clean package'
repackage: clean package

## install - Install a built dist
install:
	sh -c "pip install -U dist/htk-$(VERSION).tar.gz"

## upload - Uploads a package to PyPI
upload:
	sh -c "twine upload dist/htk-$(VERSION)-py2.py3-none-any.whl"

## publish - Clean, package, and publish to PyPI
publish: repackage upload
