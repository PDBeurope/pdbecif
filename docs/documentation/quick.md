# Quick start

## Reading using CifFileReader

Typical use case very often looks like this:

```python
>>> from pdbecif.mmcif_io import CifFileReader

>>> cfr = CifFileReader()
>>> cif_obj = cfr.read("1tqn_updated.cif", output='cif_wrapper')

>>> print(cif_obj)
{'1TQN': <pdbecif.mmcif.CIFWrapper object at 0x7fac9693c110>}
>>> cif_data = list(cif_obj.values())[0]
>>> print(cif_data)
<pdbecif.mmcif.CIFWrapper at 0x7fac9601ef10>

>>> print(cif_data._entity_poly_seq)
<pdbecif.mmcif.CIFWrapperTable at 0x7fac966eea50>

# using dot-notation
>>> print(cif_data._entity_poly.pdbx_strand_id)
['A']

# using slice notation
>>> print(cif_data['_entity_poly']['pdbx_strand_id'])
['A']

>>> print(cif_data._entity_poly.search('entity_id', '1'))
{0: {'entity_id': '1',
     'type': 'polypeptide(L)',
     'nstd_linkage': 'no',
     'nstd_monomer': 'no',
     'pdbx_seq_one_letter_code': 'MALYGTHSHGLFKKLGI...HHHH',
     'pdbx_seq_one_letter_code_can': 'MALYGTHSHGLFKKLGIPGPTPLPFLGNHHHH',
     'pdbx_strand_id': 'A',
     'pdbx_target_identifier': '?'}}
```

## Reading using MMCIF2Dict

MMCIF2Dict is a purely algorithmic parser that convers mmCIF files into python dictionaries

```python
>>> from pdbecif.mmcif_tools import MMCIF2Dict

>>> mmcif_dict = MMCIF2Dict()
>>> cif_dict = mmcif_dict.parse("1tqn_updated.cif")

>>> pdb_id = list(cif_dict.keys())[0]
>>> print(pdb_id)
'1TQN'

mmcif_categories = list(cif_dict['1TQN'].keys())
>>> print(mmcif_categories)
['_entry', '_citation', '_citation_author']

>>> polymer_name = cif_dict['1TQN']['_entity']['pdbx_description'][0]
>>> print(polymer_name)
'cytochrome P450 3A4'

>>> hem_name = cif_dict['1TQN']['_entity']['pdbx_description'][1]
>>> print(hem_name)
'PROTOPORPHYRIN IX CONTAINING FE'

```

## Writing data

PDBeCif package contains `CifFileWriter` object that allows you to write out
both `python dictionaries` and `CIFWrapper` object.

```python
>>> from pdbecif.mmcif_io import CifFileWriter

obj = {
    "root": {
        "category1": {
            "subcatA": "val1",
            "subcatB": "val2"
        },
        "category2": {
            "subcat1": [0,1,2],
            "subcat2": ["a", "b", "c"]
        }
    }
}

# write out python dictionary
>>> writer = CifFileWriter('cif_file.cif')
>>> print(writer)
<pdbecif.mmcif_io.CifFileWriter object at 0x7f83cb575410>

>>> writer.write(obj)


# write out CIFWrapper object
>>> from pdbecif.mmcif_io import CifFileReader, CifFileWriter

>>> cfr = CifFileReader()
>>> cif_obj = cfr.read("example.cif", output='cif_file')
>>> CifFileWriter('/path/to/file.cif').write(cif_obj)

```
