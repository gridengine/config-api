
include ./util/include.mk

# The command line arguments of pandoc were renamed between version 1.x and 2.x,
# so find out which pandoc version we are using and set options accordingly.
PANDOC_VERSION_MAJOR = $(shell pandoc -v | grep "^pandoc" | cut -d" " -f 2 | cut -d"." -f 1)
PANDOC_VERSION_GE_2 = $(shell [ $(PANDOC_VERSION_MAJOR) -ge 2 ] && echo true)

ifeq ($(PANDOC_VERSION_GE_2),true)
	PANDOC_OPTS = --pdf-engine=xelatex
else
	PANDOC_OPTS = -R --latex-engine=xelatex
endif

all: build doc

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

pdf:
	(cd doc/UserDocumentation; pandoc $(PANDOC_OPTS) --template=template.tex --listings -H listings.tex \
		--variable mainfont=Georgia --variable sansfont=Arial \
		--variable fontsize=10pt --variable version="$(REVISION)" \
		--variable title="Grid Engine Configuration API User Guide" \
		--variable author="Univa Engineering" --variable company="Univa Corporation" \
		--variable UGELongVersion="$(REVISION)" --variable UGEShortVersion="$(REVISION)" \
		--variable UGEFullName="Univa Grid Engine" --variable UGEShortName="Grid Engine" \
		--variable doc-family="Univa Grid Engine Documentation" \
		--toc -s UGEConfigLibraryDoc.md -o UGEConfigLibraryDoc.pdf)

dist: egg doc
	cp doc/UserDocumentation/UGEConfigLibraryDoc.pdf doc/build
	rsync -arvlP doc/build/* dist/doc/
	cp doc/UGEConfigLibraryHLD.pdf dist/doc
	(cd dist; zip -r config-api.zip `ls -d *`)

egg: uge/__init__.py
	python setup.py bdist_egg

test: uge/__init__.py
	mkdir -p build
	python setup.py nosetests

clean:
	make -C doc clean
	rm -f doc/UserDocumentation/UGEConfigLibraryDoc.pdf
	rm -rf build *.egg-info `find . -name '*.pyc'`
	rm -rf dist

tidy: clean
