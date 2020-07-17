![GitHub](https://img.shields.io/github/license/pdbeurope/pdbecif) ![tests](https://github.com/PDBeurope/pdbecif/workflows/pdbecif%20tests/badge.svg) ![documentation](https://github.com/PDBeurope/pdbecif/workflows/pdbecif%20documentation/badge.svg)
# PDBeCIF

PDBeCIF is a package that is used to work with mmCIF formatted files. The package
contains modules for accessing mmCIF data in different ways depending
on the type of task required.

The first mechanism (while slower) allows users to access ANY mmCIF formatted
file and includes Reader and Writer objects for mmCIF file IO.

This not only includes mmCIF data files but mmCIF dictionaries as well.

The second mechanism is a highly optimised (algorithmic) mmCIF parser that
currently has NO Reader and Writer objects. This module (fastCif) can only be
used for accessing public mmCIF data files.

The fastCif module also contains wrappers that emulate python objects from
python dictionaries and so mmCIF categories and items are accessed using 'dot'
notation. There are also convenience methods for searching rows in categories
where items have a particular value.

The documentation on how to use the toolkit can be found [here](https://pdbeurope.github.io/pdbecif/).
