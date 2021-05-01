# Biological use cases

You can find a couple of use cases with a biological value that demonstrates the use of the pdbecif parser along with some of its features.

## Reading PDB macromolecular files in the mmCIF format

wwPDB distributes macromolecular data in the mmCIF format. For our use case, we will use PDB entry: 7cgo. This large molecular machine contains some 330K atoms and drives the rotation of the flagellum for bacterial mobility.

Let us first download the [updated mmCIF file](https://www.ebi.ac.uk/pdbe/entry-files/download/7cgo_updated.cif) from [Protein Data Bank in Europe](http://pdbe.org/). This file contains more annotations to place this biomacromolecular structure in its biological context to the standard [wwPDB file](https://www.ebi.ac.uk/pdbe/entry-files/download/7cgo.cif)  load the whole file in memory:

```python
from pdbecif.mmcif_io import CifFileReader

data = CifFileReader().read('7cgo_updated.cif')
```

now we can traverse the tree-like structure in any way we like. See the tree hierarchy below highlighting some of the important categories

```
7CGO
├── _entry
│   ├── id
├── _entity
│   ├── id
│   ├── type
│   ├── src_method
│   ├── pdbx_description
│   ├── formula_weight
│   ├── pdbx_ec
├── _atom_site
│   ├── id
│   └── type_symbol
```

So accessing content of the `_entity` category is as simple as:

```python
data['7CGO']['_entity']
```

We can have a look on how many atoms are there in the entry:

```
len(pdb['_atom_site']['id'])
```

as well as e.g. loop through all the categories that contain information related to the EM experiment:

```python
for k, v in data['7CGO'].items():
    if k[0:3] == '_em':
        print(k)
        print(v)
```

Whenever you are unsure on what certain data category contains you can always refer back to the [reference](http://mmcif.wwpdb.org/) and browse through the dictionary.

### Speed optimization for large entires

In the previous example, we parsed and processed the entire file including the large `_atom_site` category. This is often not needed. Particularly, if we are interested in data annotations only and not in coordinates.

this can be achieved by discarding the `_atom_site` category such as:

```python
data = CifFileReader().read('7cgo_updated.cif', ignore=['_atom_site'])
```

Noticed the speed improvement? Further optimization can be achieved by specifying only the categories one is interested in. Let's assume we are interested in primary sequences of all the polymeric entities found in the PDB entry. Such information is included in `_entity_poly` category so let's extract that one and print those out along with the polymeric type:

```python
data = CifFileReader().read('7cgo_updated.cif', only=['_entity_poly'])

entity_poly = data['7CGO']['_entity_poly']
poly_types = entity_poly['type']
sequences = entity_poly['pdbx_seq_one_letter_code']

for p_type, sequence in zip(poly_types, sequences):
    print(f'{p_type}: {sequences}')
```

## Reading wwPDB Biologically Interesting molecule Reference Dictionary

The Biologically Interesting molecule Reference Dictionary ([BIRD](https://www.wwpdb.org/data/bird)) contains information about biologically interesting peptide-like antibiotic and inhibitor molecules in the PDB archive.

Let us first download the [reference dictionary](https://ftp.wwpdb.org/pub/pdb/data/bird/prd/prdcc-all.cif.gz) from the FTP area, load the whole file in memory:

```python
from pdbecif.mmcif_io import CifFileReader

data = CifFileReader().read('prdcc-all.cif.gz')
```

and check how many such molecules are there:

```python
len(data)
```

Next we can extract e.g. InChIKeys of all the molecules specified in the dictionary including molecular type:

```python
for k, v in data.items():
    if '_pdbx_chem_comp_descriptor' not in v:
        continue

    descriptor = v['_pdbx_chem_comp_descriptor']

    if 'InChIKey' not in descriptor['type']:
        continue

    inchikey_index = descriptor['type'].index('InChIKey')
    inchikey = descriptor['descriptor'][inchikey_index]

    mol_type = v['_chem_comp']['type']

    print(f'{k} | {mol_type}: {inchikey}')
```
