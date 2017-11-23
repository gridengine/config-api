
include ./util/include.mk

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
	(cd doc/UserDocumentation; pandoc -R -N --template=template.tex --listings -H listings.tex\
		--variable mainfont=Georgia --variable sansfont=Arial \
        --variable fontsize=10pt --variable version="$(REVISION)" \
		--variable title="Grid Engine Configuration API User Guide" \
		--variable author="Univa Engineering" --variable company="Univa Corporation" \
		--variable UGELongVersion="$(REVISION)" --variable UGEShortVersion="$(REVISION)" \
		--variable UGEFullName="Univa Grid Engine" --variable UGEShortName="Grid Engine" \
		--variable doc-family="Univa Grid Engine Documentation" \
		--latex-engine=xelatex --toc -s UGEConfigLibraryDoc.md -o UGEConfigLibraryDoc.pdf)

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
	rm -rf build *.egg-info `find . -name '*.pyc'`
	rm -rf dist

tidy: clean
