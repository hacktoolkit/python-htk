## help - Display help about make targets for this Makefile
help:
	@cat Makefile | grep '^## ' --color=never | cut -c4- | sed -e "`printf 's/ - /\t- /;'`" | column -s "`printf '\t'`" -t

## clean - cleans build artifacts
clean:
	rm -rf dist/*
	rm -rf build/*

## package - builds a package for dist
package:
	python setup.py sdist bdist_wheel

## repackage - alias of 'make clean package'
repackage: clean package

## install - install a built dist
install:
	sh -c "pip install -U dist/htk-`cat VERSION`.tar.gz"

## upload - uploads a package to PyPI
upload:
	sh -c "twine upload dist/htk-`cat VERSION`-py2.py3-none-any.whl"

## isort - isort Python files
isort:
	isort -rc *
