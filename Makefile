MAJOR  ?= 0
MINOR  ?= 2
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

cover:
	rm -rf $(BASE)/coverage
	make -i test
	$(PYTHON) -m coverage html

test:
	$(PYTHON) setup.py test


