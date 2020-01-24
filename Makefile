default:
	echo 'Make what?'

clean:
	rm -rf dist/*
	rm -rf build/*

package:
	python setup.py sdist bdist_wheel

repackage: clean package

install:
	sh -c "pip install -U dist/htk-`cat VERSION`.tar.gz"

upload:
	sh -c "twine upload dist/htk-`cat VERSION`-py2.py3-none-any.whl"

isort:
	isort -rc *
