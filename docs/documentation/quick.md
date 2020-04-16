# Quick start

Typical use case very often looks like this:

```
>>> from mmCif import mmcifIO

>>> cfr = mmcifIO.CifFileReader()
>>> cif_obj = cfr.read("usage-example.cif", output='cif_wrapper')

>>> print cif_obj
{'3K1Q': <mmCif.CIFWrapper object at 0xa65ee10>}
>>> cif_data = cif_obj.values()[0]
>>> print cif_data
<mmCif.CIFWrapper object at 0xa65ee10>

>>> print cif_data._entity_poly_seq
<mmCif.CIFWrapperTable object at 0xa8faa90>

# using dot-notation
>>> print cif_data._entity_poly.pdbx_strand_id
['A', 'B', 'C', 'D,E', 'F,G,H,L,M,N,R,S,T,Y', 'I,J,K,O,P,Q,U,V,W,X']

# using slice notation
>>> print cif_data['_entity_poly']['pdbx_strand_id']
['A', 'B', 'C', 'D,E', 'F,G,H,L,M,N,R,S,T,Y', 'I,J,K,O,P,Q,U,V,W,X']

>>> print cif_data._entity_poly.search('entity_id', '5')
{4: {'entity_id': '5',
     'nstd_linkage': 'no',
     'nstd_monomer': 'no',
     'pdbx_seq_one_letter_code': 'MPLHMIPQVAHAMVRAAAAGRLTL.....DCGQIVGLDLHVEPSD',
     'pdbx_seq_one_letter_code_can': 'MPLHMIPQVAHAMVRAAAAGRLTL.....DCGQIVGLDLHVEPSD',
     'pdbx_strand_id': 'F,G,H,L,M,N,R,S,T,Y',
     'type': 'polypeptide(L)'
    }
}
```