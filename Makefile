MAJOR  ?= 1
MINOR  ?= 3
PATCH  ?= ${PATCH}

PACKAGE := mmCif

SHELL := /bin/sh
PY_VERSION := 2.7

export PYTHONUNBUFFERED := 1

BASE := $(shell /bin/pwd)
SOURCE := $(BASE)/src
PYTHON := $(shell /usr/bin/which python$(PY_VERSION))

SEDI   = sed -i.bak

.PHONY: build clean release describe deploy package bundle bundle.local

version:
	$(SEDI) "s/[[:digit:]]*\.[[:digit:]]*\.[[:digit:]]*/$(MAJOR).$(MINOR).$(PATCH)/g" $(SOURCE)/$(PACKAGE)/__init__.py
	rm -f $(SOURCE)/$(PACKAGE)/__init__.py.bak
	$(SEDI) "s/[[:digit:]]*\.[[:digit:]]*\.[[:digit:]]*/$(MAJOR).$(MINOR).$(PATCH)/g" $(BASE)/setup.py
	rm -f $(BASE)/setup.py.bak

cover:
	tox -r --skip-missing-interpreters -c toxcov.ini

test:
	tox --skip-missing-interpreters -r

clean:
  $(shell cat .gitignore | xargs rm -rf)

package:
	$(PYTHON) setup.py sdist bdist_wheel

