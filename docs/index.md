# PDBeCIF: mmCif/CIF/STAR parser and API

**Author**: Glen van Ginkel; and others

PDBeCIF is a lightweight pure python package for manipulating mmCIF formatted files distributed by the wwPDB. The package contains objects and modules for accessing mmCIF data in different ways depending on the type and speed of task required.

As is mentioned above, the PDBeCIF package is a pure python implementation and as such, has no external dependencies. PDBeCIF is compatible with python 2 (>=2.5) (and Python 3 as of version 1.2.0).

Documentation and examples on how to use the PDBeCif package are provided below. A more detailed description of the methods and attributes of objects within the package can also be found on api implementation page.

## Installation

The pdbecif parser is a part of python package index [PYPI](https://pypi.org/project/PDBeCif) as such it can be conveniently installed by:

```
pip install pdbecif
```

Alternativelly, clone the repository and install the package from source:

```
git clone https://gitlab.ebi.ac.uk/pdbe/PDBeCIF.git
pip install -e PDBeCIF
```

## Package documentation

```eval_rst
.. toctree::
   :maxdepth: 1

   documentation/quick
   documentation/objects
   documentation/use_cases
```

## API documentation

Comprehensive API documentation with information on every function, class and method. This is automatically generated from the `PDBeCIF` source code and comments.

```eval_rst
.. toctree::
   :maxdepth: 1

   documentation/api
```
