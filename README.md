![GitHub](https://img.shields.io/github/license/pdbeurope/pdbecif) ![tests](https://github.com/PDBeurope/pdbecif/workflows/pdbecif%20tests/badge.svg) ![documentation](https://github.com/PDBeurope/pdbecif/workflows/pdbecif%20documentation/badge.svg)
# PDBeCIF

## [Documentation](https://pdbeurope.github.io/pdbecif/)

PDBeCIF is a package that is used to work with mmCIF formatted files. The package ontains modules for accessing mmCIF data in different ways depending on the type of task required.

The first mechanism (while slower) allows users to access ANY mmCIF formatted file and includes Reader and Writer objects for mmCIF file IO.

This not only includes mmCIF data files but mmCIF dictionaries as well.

The second mechanism is a highly optimised (algorithmic) mmCIF parser that currently has NO Reader and Writer objects. This module (fastCif) can only be used for accessing public mmCIF data files.

The fastCif module also contains wrappers that emulate python objects from python dictionaries and so mmCIF categories and items are accessed using 'dot' notation. There are also convenience methods for searching rows in categories where items have a particular value.

Make sure you check out our extensive documentation. If in doubt on how to use the parser or would like to ask for a feature, just open a GH issue.

## Cite PDBeCIF

**PDBeCIF: an open‑source mmCIF/CIF parsing and processing package**

Glen van Ginkel, Lukáš Pravda, José M. Dana, Mihaly Varadi, Peter Keller, Stephen Anyango and Sameer Velankar

BMC Bioinformatics (2021) 22:383

DOI: [10.1186/s12859-021-04271-9](https://doi.org/10.1186/s12859-021-04271-9)

## Useful links

* wwPDB mmCIF reference dictionary: http://mmcif.wwpdb.org/
* CIF specification: https://www.iucr.org/resources/cif/spec/version1.1/cifsyntax#charset]
