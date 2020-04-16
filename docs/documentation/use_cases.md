# Use cases

```python
from mmcif.mmcif import CifFile, CifWrapper, CifFileWriter
import mmcif.mmcif_io as mmcif
```

## Creating objects

### Example 1 - Creating an mmCIF like dictionary by hand (manually)

```python
mmcif_like = {
    'TEST_CIF': {
            '_test_category_1': {
                'test_value_1': 1,
                'test_value_2': 2,
                'test_value_3': 3
            },
            '_test_category_2': {# Loop/table
                'test_value_1': [1, 2, 3, 4],
                'test_value_2': ["Sleepy", "Dopey", "Bashful", "Grumpy"],
                'test_value_3': [\
                    'A ->\nLINE = A',
                    'B ->\nLINE = B',
                    'C ->\nLINE = C',
                    'D ->\nLINE = D'
                ]
            }
        }
    }
```

### Example 2 - Creating a CifWrapper object from mmCif-like dictionaries

```python
    cif_wrapper = CIFWrapper(mmcif_like)
    print(cif_wrapper.data_id, cif_wrapper)
```

### Example 3 - Creating an mmCif-like dictionary from a CifWrapper object

```python
    data_dict = cif_wrapper.unwrap()
    print(data_dict)
```

### Example 4 - Creating a CifFile object from an mmCif-like dictionary

#### Method 1: (instantiation)

```python
    cif_file_1 = CifFile(filename="usage-test-1.cif", mmcif_data_map=mmcif_like)
```

#### Method 2: (dictionary import)

```python
    cif_file_2 = CifFile(filename="usage-test-2.cif")
    cif_file_2.import_mmcif_data_map(mmcif_like)
    print(cif_file_1, cif_file_2)
```

## Reading from files

### Example 5 - INPUT: mmCif data files, OUTPUT: mmCif-like dictionary

```python
    cfr = CifFileReader(input='data')
    (cif_id, cif_dictionary) = cfr.read(path + "/usage-example.cif", output='cif_dictionary', ignore=["_atom_site", "_atom_site_anisotrop"])
    print("mmCIF-like dictionary:", cif_dictionary)
```

### Example 6 - INPUT: mmCif data files, OUTPUT: CIFWrapper object

```python
    cfr = CifFileReader(input='data')
    cif_wrapper = cfr.read(path + "/usage-example.cif", output='cif_wrapper')
    print("CIFWrapper:", cif_wrapper)
```

### Example 7 - INPUT: mmCif data files, OUTPUT: CifFile object

```python
    cfr = CifFileReader(input='data')
    cif_file = cfr.read(path + "/usage-example.cif", output='cif_file')
    print("CifFile:", cif_file)
```

## Writing to files

Using the objects from examples 5, 6, and 7 above

### Example 8 - INPUT: mmCif-like dictionary

```python
    cfd1 = CifFileWriter("./cif_dictionary_test-1.cif")
```

#### Method 1

NO datablocks defined in mmCIF-like dictionary (Define your own) Datablock ID defaults to filename defined in CifFileWriter if none provided.

```python
    cfd1.write(cif_dictionary)
```

#### Method 2: DataBlocks defined in mmCIF-like dictionary

```python
    cfd2 = CifFileWriter("./cif_dictionary_test-2.cif")
    cfd2.write({cif_id:cif_dictionary})
```

### Example 9 - INPUT: CIFWrapper object

```python
    cfw = CifFileWriter("./cif_wrapper_test.cif")
    cfw.write(cif_wrapper)
```

### Example 10 - INPUT: CifFile object

```python
    cff = CifFileWriter("./cif_file_test.cif")
    cff.write(cif_file)
```

## Using an mmCIF-like python dictionary

Using the CIF dictionary directly to access data. The following examples
use the objects from examples 5, 6, and 7 above.

Data are accessed using standard data access mechanisms for
python dictionaries:

```python
user_dict['_cif_category']['cif_item']
```

### Example 11 - Accessing the value of an item

```python
    print("_test_keyword.field_1", cif_dictionary["_test_keyword"]["field_1"])
```

### Example 12 - Accessing all items of a category

```python
    print("_valid_CIF", cif_dictionary["_valid_CIF"])
```

## Using a CIFWrapper object

The CIFWrapper object is a wrapper for the mmCIF-like dictionary used to
emulate python objects. Data are accessed using familiar 'dot' notation:

user_dict._cif_category.cif_item

Categories (tables) also have useful methods for filtering i.e.: `search()` and `searchiter()`

```python
    cif_wrapper_2 = cfr.read(path + "/1smv.cif", output='cif_wrapper')

    # Example 13 - Check table exists and get all the contents of the table
    if '_struct_ref_seq_dif' in cif_wrapper_2:
        print(cif_wrapper_2._struct_ref_seq_dif)

        # Example 14 - Check column exists in a table and get all contents of the column
        if 'details' in cif_wrapper_2._struct_ref_seq_dif and cif_wrapper_2._struct_ref_seq_dif.details:
            print(cif_wrapper_2._struct_ref_seq_dif.details)

            # Example 15 - Search a table for rows where values in column match and get
            #              all results as dict in the form {match_row_index : {row}}
            print(cif_wrapper_2._struct_ref_seq_dif.search('details', 'DELETION'))

            # Example 16 - Iterate over search results (table rows) where values in
            #              column match the given searchterm and get rows as
            #              {column_name: value_for_row}
            for searchResult in cif_wrapper_2._struct_ref_seq_dif.searchiter('details', 'DELETION'):
                print(searchResult)
                break # only show one to demonstrate the principle

            # Example 17 - Iterate over all rows in a table and get rows as
            #              {column_name: value_for_row}
            for row in cif_wrapper_2._struct_ref_seq_dif:
                print(row)
                break # only show one to demonstrate the principle
```

## Using a CifFile object

Using the CifFile object to access, edit and update mmCIF data.
The following examples use the CifFile object objects from example 7 above.

Data are manipulated using the accessors and mutators provided:

NB: See the Test suite in mmCif.test for more examples

### Example 18 - Working with CifFile
```python    
    print("DataBlock ids:", cif_file.getDataBlockIds()) #List all datablock ids
    print("DataBlock objects:", cif_file.getDataBlocks()) #List all datablock objects
    data_block_1 = cif_file.getDataBlock("TEST_CIF") #Get a specific datablock
    data_block_1 = cif_file.getDataBlocks()[0] #Get the first datablock
    data_block_2 = cif_file.setDataBlock("BLOCK_2") # Create another empty datablock
    data_block_3 = cif_file.setDataBlock("BLOCK_3") # Create another empty datablock
    cif_file.removeChild(data_block_2) # Remove datablock (Method 1 - given object)
    cif_file.removeChild("BLOCK_3") # Remove datablock (Method 2 - given ID)
    print("RECYCLED DATABLOCKS:", cif_file.recycleBin) # Removed objects are stored in a recycle bin
```

### Example 19 - Working with DataBlock

```python
    """NB: Category and SaveFrame are handled in the same manner"""
    data_block_1 = cif_file.getDataBlock("TEST_CIF") #Get a specific datablock
    data_block_4 = cif_file.setDataBlock("BLOCK_4") # Create another empty datablock
    data_block_5 = cif_file.setDataBlock("BLOCK_5") # Create another empty datablock
    data_block_5.getId()) # Get the datablock ID
    data_block_5.updateId("BLOCK_5.1") # Change the datablock ID
    print("Category ids:", data_block_1.getCategoryIds()) #List all category ids
    print("Category objects:", data_block_1.getCategories()) #List all category objects
    category_1 = data_block_1.getCategory("_test_keyword") #Get a specific category
    category_2 = data_block_4.setCategory("CATEGORY_2") #Create an empty category
    category_3 = data_block_4.setCategory("CATEGORY_3") #Create an empty category
    data_block_4.removeChild(category_2) # Remove category (Method 1 - given object)
    data_block_4.removeChild("CATEGORY_3") # Remove category (Method 2 - given ID)
    data_block_5.remove()) # Remove datablock from CifFile
    print("RECYCLED CATEGORIES:", data_block_4.recycleBin) # Removed objects are stored in a recycle bin
```


### Example 20 - Working with Category

```python
    category_1 = data_block_1.getCategory("_test_keyword") #Get a specific category
    category_4 = data_block_4.setCategory("CATEGORY_4") # Create another empty category
    category_5 = data_block_4.setCategory("CATEGORY_5") # Create another empty category
    print("Item names:", category_1.getItemNames()) #List all item names
    print("Item objects:", category_1.getItems()) #List all item objects
    item_1 = category_1.getItem("field_1") #Get a specific item
    item_2 = category_4.setItem("ITEM_2") #Create an empty item
    item_3 = category_4.setItem("ITEM_3") #Create an empty item
    category_4.removeChild(item_2) # Remove item (Method 1 - given object)
    category_4.removeChild("ITEM_3") # Remove item (Method 2 - given ID)
    category_5.remove()) # Remove category from DataBlock
    print("RECYCLED ITEMS:", category_4.recycleBin) # Removed objects end up in the recycle bin
```

### Example 21 - Working with Item

```python
    item_1 = category_1.getItem("field_1") #Get a specific item
    item_4 = category_4.setItem("ITEM_4") # Create another empty item
    item_5 = category_4.setItem("ITEM_5") # Create another empty item
    print("Value (raw):", item_1.getRawValue()) #Get raw item value (Method 1 - using accessor)
    print("Value (raw):", item_1.value #Get raw item value (Method 2 - using attribute)
    print("Value (formated):", item_1.getFormattedValue()) #Get the formated value (for file export)
    item_4.setValue("VALUE_2") #Set the item value
    item_5.setValue([9, 8, 7, 6, 5]) #Set the item value
    item_5.remove()) # Remove item from Category
    print("RECYCLED ITEMS:", category_4.recycleBin) # Removed objects end up in the recycle bin
```

### Example 22 - Method chaining

For every object the `setXXXX()` method always returns the this you are
trying to set. If no object is present it creates a new one and returns it.
`setXXXX()` can therefor be used as both accessor and mutator

```python
    cif_file.setDataBlock("BLOCK_6").setCategory("CATEGORY_6").setItem("ITEM_6").setValue("VALUE_6")
```
