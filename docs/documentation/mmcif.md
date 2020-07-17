# pdbecif

This mmcif module contains all the classes necessary to read and write
either a data or a dictionary mmCIF file.

Reading files can be acheived using either `CifFileReader` or `MMCIF2Dict`:

## pdbecif.mmcif

The module contains all the objects necessary to represent
either a data CIF file or a dictionary CIF file.

### mmCIF data files

DATA mmCIF files are represented one of 3 ways (interchangeable):

1. As a series of objects that encapsulate each major component of mmCIF
    `CifFile -> DataBlock -> [ SaveFrame -> ] Category -> Item`
2. As a python wrapper to a dictionary. Categories and items are accessed
   through the familiar python dot (.) notation.
3. As a dictionary of the form

    ```python
    {
        DATABLOCK_ID: { CATEGORY: { ITEM:  VALUE } }
    }
    ```

### mmCIF dictionaries

DICTIONARY mmCIF files can ONLY be represented as (1) above i.e.:

1. As a series of objects that encapsulate each major component of mmCIF

`CifFile -> DataBlock -> [ SaveFrame -> ] Category -> Item`

Due to the presence of SaveFrame objects they are not interchangeable as the
conversion to dictionary type objects has not yet been implemented.

```eval_rst
.. automodule:: pdbecif.mmcif
    :members:
```

## pdbecif.mmcif_io

```eval_rst
.. automodule:: pdbecif.mmcif_io
    :members:
```

## pdbecif.mmcif_tools

```eval_rst
.. automodule:: pdbecif.mmcif_tools
    :members:
```

## pdbecif.ordereddict

```eval_rst
.. automodule:: pdbecif.ordereddict
    :members:
```

## pdbecif.utils

```eval_rst
.. automodule:: pdbecif.utils
    :members:
```
