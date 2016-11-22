
include ./util/include.mk

all: build doc dist

# Stubs for default targets
.PHONY:deps install clean dist egg distclean test doc
deps install test:

uge/__init__.py : ./util/params.mk
	echo "__version__ = '$(VERSION)'" > $@

distclean: tidy

build: uge/__init__.py
	python setup.py build

doc: 
	PYTHONPATH=$(PWD) make -C doc html

dist: egg doc
	rsync -arvlP doc/build/* dist/doc/

egg: uge/__init__.py
	python setup.py bdist_egg

test: uge/__init__.py
	mkdir -p build
	python setup.py nosetests

clean:
	make -C doc clean
	rm -rf build *.egg-info `find . -name '*.pyc'`

tidy: clean
	rm -rf dist

