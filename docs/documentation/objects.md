# Objects description

## CifFileReader

There are two types of behaviour that can be configured when instantiating the
`CifFileReader`. You can specify the file type as either 'data' (default) or
'dictionary'.

* If 'dictionary' is specified the reader will always return a `CifFile` object
   regardless of the 'output' flag in the `read()` method.
* If 'data' is specified (this is the default behaviour), the 'output' flag
   in the read method.

```python
import pdbecif.mmcif_io as mmcif
cfr = mmcif.CifFileReader(input='dictionary')
```

By changing the 'output' parameter, users can customize the way in which mmCIF
is returned. output takes one of three values i.e.:

  1. 'cif_dictionary' returns a tuple of datablock_id and mmCIF data

      ```python
      (cif_id, cif_dictionary) = cfr.read("../../resources/dodgy.cif", output='cif_dictionary')
      ```

  2. 'cif_wrapper' returns a `CIFWrapper` object that encapsulates mmCIF-like
      dictionaries for python 'dot' notation data access

      ```python
      cif_wrapper = cfr.read("../../resources/dodgy.cif", output='cif_wrapper')
      ```

  3. 'cif_file' returns a `CifFile` object that fully encapsulates all
      components of mmCIF files

      ```python
       cif_file = cfr.read("../../resources/dodgy.cif", output='cif_file')
      ```

NB: if 'input' is set as 'dictionary' when instantiating `CifFileReader`, 'output'
will have no effect

## CifFileWriter

`CifFileWriter` accepts mmCIF-like dictionaries, `CIFWrapper` objects, and `CifFile`
objects to write. Files can be compressed while writing using the
`compress=True` flag.

Examples continued from above:

```python
cfd = mmcif.CifFileWriter("../../resources/cif_dictionary_test.cif")
cfd.write(cif_dictionary)
cfw = mmcif.CifFileWriter("../../resources/cif_wrapper_test.cif")
cfw.write(cif_wrapper)
cff = mmcif.CifFileWriter("../../resources/cif_file_test.cif")
cff.write(cif_file)
```

## MMCIF2Dict

A very low level access to mmCIF data files. `MMCIF2Dict` has one method `parse()`
that returns `(datablock_id, mmCIF_data)` tuples as `(str, dict)`

`MMCIF2Dict` is very fast at reading mmCIF data.

```python
from pdbecif.mmcif_tools import MMCIF2Dict

>>> obj = MMCIF2Dict().parse('1tqn_updated.cif')
>>> print(obj)
```

Resulting structure is a plain python dictionary with mmCIF category names
organized as keys. Value to that key is another python dictionary
with mmCIF fields being keys and value is either a string (provided there
is just a single value) or an array if `_loop` element was present and there
are multiple values to a given field.

### Category examples

### Category with a single value per field

```json
{
    "1TQN": {
        "_entry": {
            "id": "1TQN"
        },
        "_symmetry": {
            "entry_id": "1TQN",
            "space_group_name_H-M": "I 2 2 2",
            "pdbx_full_space_group_name_H-M": "?",
            "cell_setting": "?",
            "Int_Tables_number": "23",
            "space_group_name_Hall": "?"
        }
}
```

### Multivalue category per field

```json
{
        "_entity": {
            "id": ["1", "2", "3"],
            "type": ["polymer", "non-polymer", "water"],
            "src_method": ["man", "syn", "nat"],
            "pdbx_description": ["cytochrome P450 3A4", "PROTOPORPHYRIN IX CONTAINING FE", "water"],
            "formula_weight": ["55594.637", "616.487", "18.015"],
            "pdbx_number_of_molecules": ["1", "1", "190"],
            "pdbx_ec": ["1.14.14.1", "?", "?"],
            "pdbx_mutation": ["?", "?", "?"],
            "pdbx_fragment": ["?", "?", "?"],
            "details": ["?", "?", "?"]
        }
}
```
