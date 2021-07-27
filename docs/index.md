# PDBeCIF: mmCif parser and API

**Author**: Glen van Ginkel; and others

PDBeCIF is a lightweight pure python package for manipulating mmCIF formatted files distributed by the wwPDB. Reading CIF files is supported as well, writtin is not. The package contains objects and modules for accessing mmCIF data in different ways depending on the type and speed of task required.

As is mentioned above, the PDBeCIF package is a pure python implementation and as such, has no external dependencies. PDBeCIF is compatible with python 2 (>=2.5) (and Python 3 as of version 1.2.0).

Documentation and examples on how to use the PDBeCif package are provided below. A more detailed description of the methods and attributes of objects within the package can also be found on api implementation page.

## Installation

The pdbecif parser is a part of python package index [PYPI](https://pypi.org/project/PDBeCif) as such it can be conveniently installed by:

```
pip install pdbecif
```

Alternativelly, clone the repository and install the package from source:

```
pip install git+https://github.com/PDBeurope/pdbecif.git@master#egg=pdbecif
```

## Package documentation

```eval_rst
.. toctree::
   :maxdepth: 1

   documentation/quick
   documentation/bio
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

## Reference

If you find this resource useful, please cite it as:

* Glen van Ginkel, Lukáš Pravda, José M. Dana, Mihaly Varadi, Peter Keller, Stephen Anyango and Sameer Velankar. [PDBeCIF: an open‑source mmCIF/CIF parsing and processing package](https://doi.org/10.1186/s12859-021-04271-9) BMC Bioinformatics (2021) 22:383
