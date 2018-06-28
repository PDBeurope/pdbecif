[![pipeline status](https://gitlab.com/glenveegee/PDBeCIF/badges/master/pipeline.svg)](https://gitlab.com/glenveegee/PDBeCIF/commits/master)
[![coverage report](https://gitlab.com/glenveegee/PDBeCIF/badges/master/coverage.svg)](https://gitlab.com/glenveegee/PDBeCIF/commits/master)

# PDBeCIF 
Protein Data Bank in Europe (PDBe; http://pdbe.org) mmCif/CIF/STAR parser and API

used to work with STAR, CIF, and mmCIF formatted files. The package
contains modules for accessing mmCIF data in different ways depending
on the type of task required.

Typical usage often looks like this:

```python
from mmCif import *
from mmcifIO import mmcifIO
```

## Reading from a file

### INPUT: Any STAR/CIF/mmCIF file, OUTPUT: CifFile object
```python
    cfr = mmcifIO.CifFileReader(input='dictionary')
    cif_file = cfr.read(os.path.join(<your_path>, "usage-example.cif"), output='cif_file')
    print "CifFile:", cif_file
```

## Writing to a file

### INPUT: CifFile object
```python
    # create a file writer
    cff = mmcifIO.CifFileWriter(os.path.join(<your_path>, "cif_output_test.cif"))
    # write the file
    cff.write(cif_file)
```


## Using a CifFile object
    
    Using the CifFile object to access, edit and update mmCIF data.
    The following examples use a CifFile object with roughly the following structure.

    Data are manipulated using the accessors and mutators provided:

    NB: See the Test suite in mmCif.test for more examples

### Example 1 - Working with CifFile

```python
    print "DataBlock ids:", cif_file.getDataBlockIds() #List all datablock ids
    print "DataBlock objects:", cif_file.getDataBlocks() #List all datablock objects
    data_block_1 = cif_file.getDataBlock("TEST_CIF") #Get a specific datablock
    data_block_1 = cif_file.getDataBlocks()[0] #Get the first datablock
    data_block_2 = cif_file.setDataBlock("BLOCK_2") # Create another empty datablock
    data_block_3 = cif_file.setDataBlock("BLOCK_3") # Create another empty datablock
    cif_file.removeChild(data_block_2) # Remove datablock (Method 1 - given object)
    cif_file.removeChild("BLOCK_3") # Remove datablock (Method 2 - given ID)
    print "RECYCLED DATABLOCKS:", cif_file.recycleBin # Removed objects are stored in a recycle bin
```

### Example 2 - Working with DataBlock

NB: Category and SaveFrame are handled in the same manner

```python
    data_block_1 = cif_file.getDataBlock("TEST_CIF") #Get a specific datablock
    data_block_4 = cif_file.setDataBlock("BLOCK_4") # Create another empty datablock
    data_block_5 = cif_file.setDataBlock("BLOCK_5") # Create another empty datablock
    data_block_5.getId() # Get the datablock ID
    data_block_5.updateId("BLOCK_5.1") # Change the datablock ID
    print "Category ids:", data_block_1.getCategoryIds() #List all category ids
    print "Category objects:", data_block_1.getCategories() #List all category objects
    category_1 = data_block_1.getCategory("_test_keyword") #Get a specific category
    category_2 = data_block_4.setCategory("CATEGORY_2") #Create an empty category
    category_3 = data_block_4.setCategory("CATEGORY_3") #Create an empty category
    data_block_4.removeChild(category_2) # Remove category (Method 1 - given object)
    data_block_4.removeChild("CATEGORY_3") # Remove category (Method 2 - given ID)
    data_block_5.remove() # Remove datablock from CifFile
    print "RECYCLED CATEGORIES:", data_block_4.recycleBin # Removed objects are stored in a recycle bin
```

### Example 3 - Working with Category

```python
    category_1 = data_block_1.getCategory("_test_keyword") #Get a specific category
    category_4 = data_block_4.setCategory("CATEGORY_4") # Create another empty category
    category_5 = data_block_4.setCategory("CATEGORY_5") # Create another empty category
    print "Item names:", category_1.getItemNames() #List all item names
    print "Item objects:", category_1.getItems() #List all item objects
    item_1 = category_1.getItem("field_1") #Get a specific item
    item_2 = category_4.setItem("ITEM_2") #Create an empty item
    item_3 = category_4.setItem("ITEM_3") #Create an empty item
    category_4.removeChild(item_2) # Remove item (Method 1 - given object)
    category_4.removeChild("ITEM_3") # Remove item (Method 2 - given ID)
    category_5.remove() # Remove category from DataBlock
    print "RECYCLED ITEMS:", category_4.recycleBin # Removed objects end up in the recycle bin
```

### Example 4 - Working with Item

```python
    item_1 = category_1.getItem("field_1") #Get a specific item
    item_4 = category_4.setItem("ITEM_4") # Create another empty item
    item_5 = category_4.setItem("ITEM_5") # Create another empty item
    print "Value (raw):", item_1.getRawValue() #Get raw item value (Method 1 - using accessor)
    print "Value (raw):", item_1.value #Get raw item value (Method 2 - using attribute)
    print "Value (formated):", item_1.getFormattedValue() #Get the formated value (for file export)
    item_4.setValue("VALUE_2") #Set the item value
    item_5.setValue([9, 8, 7, 6, 5]) #Set the item value
    item_5.remove() # Remove item from Category
    print "RECYCLED ITEMS:", category_4.recycleBin # Removed objects end up in the recycle bin
```
### Example 5 - Method chaining
    For every object the setXXXX() method always returns the this you are
    trying to set. If no object is present it creates a new one and returns it.
    setXXXX() can therefor be used as both accessor and mutator
```python

    cif_file.setDataBlock("BLOCK_6").setCategory("CATEGORY_6").setItem("ITEM_6").setValue("VALUE_6")
```

## Installation

### pip

    pip install git+http://gitlab.com/glenveegee/PDBeCIF.git

Optionally, you can specify a tag/branch. For example:

    pip install git+http://gitlab.com/glenveegee/PDBeCIF.git@v1.3.4

### Manual

You can also simply download a release from https://gitlab.com/glenveegee/PDBeCIF/releases and copy it to your Python library path.

