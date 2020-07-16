# -*- coding=utf-8 -*-

import copy
import re

try:
    from collections import OrderedDict
except ImportError:
    # fallback: try to use the ordereddict backport when using python 2.6
    try:
        from ordereddict import OrderedDict
    except ImportError:
        # backport not installed: use local OrderedDict
        from pdbecif.mmcif.ordereddict import OrderedDict

__author__ = "Glen van Ginkel (Protein Data Bank in Europe; http://pdbe.org)"
__date__ = "$28-Jun-2018 18:23:30$"

# imports

# constants
__all__ = [
    "CIFWrapperTable",
    "CIFWrapper",
    "Item",
    "Category",
    "SaveFrame",
    "DataBlock",
    "CifFile",
]

_reserved = ["loop_", "save_", "data_", "_"]
ascii_char = re.compile(r"[^\x00-\x7F]")  # Match non-ASCII characters
# exception classes
# interface functions
# classes


class CIFWrapperTable(object):

    """
    CIFWrapperTable represents (and wraps up) mmCif category like dictionaries.
    Categories that are stored as dictionary like objects are represented as
    tables and their items and data are accessed using familiar python 'dot'
    notation.
    """

    _DATA = {}
    _preserve_order = False

    def __init__(self, d, preserve_token_order=False):
        self._DATA = d
        if preserve_token_order:
            self._preserve_order = preserve_token_order

    def __getattr__(self, attr_in):
        return self._DATA.get(attr_in)

    def __setattr__(self, itemName, itemValue):
        if itemName == "_DATA":
            self.__dict__["_DATA"] = copy.deepcopy(itemValue)
        elif itemName == "_preserve_order":
            self.__dict__["_preserve_order"] = copy.deepcopy(itemValue)
        else:
            self.__setitem__(itemName, itemValue)

    def __iter__(self):
        """CIFWrapperTable row iterator which makes row access available"""
        numRows = len(list(self._DATA.values())[0])
        idx = 0
        if self._preserve_order:
            while idx < numRows:
                yield OrderedDict((k, v[idx]) for k, v in list(self._DATA.items()))
                idx += 1
        else:
            while idx < numRows:
                yield dict((k, v[idx]) for k, v in list(self._DATA.items()))
                idx += 1

    def __contains__(self, itemNameIn):
        """Support for 'in' operator"""
        return itemNameIn in self._DATA

    def __getitem__(self, itemNameIn):
        return self._DATA.get(itemNameIn)

    def __setitem__(self, itemName, itemValue):
        if not isinstance(itemValue, list):
            itemValue = [
                itemValue,
            ]
        if itemName not in self._DATA:
            self._DATA.setdefault(itemName, itemValue)
        else:
            self._DATA[itemName] = copy.deepcopy(itemValue)

    def __delitem__(self, itemName):
        if itemName in self._DATA:
            del self._DATA[itemName]

    def search(self, item, value):
        """return list Rows in table where item contain has value"""
        results = {}
        try:
            results.update(
                [
                    (idx, dict((k, v[idx]) for k, v in list(self._DATA.items())))
                    for idx, el in enumerate(self._DATA[item])
                    if value.match(el)
                ]
            )
        except AttributeError:
            results.update(
                [
                    (idx, dict((k, v[idx]) for k, v in list(self._DATA.items())))
                    for idx, el in enumerate(self._DATA[item])
                    if el == value
                ]
            )
        return results

    def searchiter(self, item, value):
        """
        Highly optimised search for values of items in tables

        return list Rows in table where item contain has value

        """
        for idx, el in enumerate(self._DATA[item]):
            try:
                if value.match(el):
                    yield dict((k, v[idx]) for k, v in list(self._DATA.items()))
            except AttributeError:
                if el == value:
                    yield dict((k, v[idx]) for k, v in list(self._DATA.items()))

    def contents(self):
        return list(self._DATA.keys())


#    def __repr__(self):
#        return str(self._DATA)


class CIFWrapper(object):

    """
    CIFWrapper is a wrapper object for the output of the MMCIF2Dict object
    i.e., an mmCIF-like python dictionary object. This implies that mmCIF-like
    dictionaries written outside this package may be used to initialize the
    CIFWrapper class as well. The CIFWrapper object emulates python objects by
    providing access to mmCIF categories and items using the familiar python
    'dot' notation.
    """

    _DATA = {}
    _preserve_order = False

    def __init__(self, d, data_id=None, preserve_token_order=False):
        if preserve_token_order:
            self._DATA = OrderedDict()
            self._preserve_order = True

        if d is not None:
            __dictionary = copy.deepcopy(d)
            self.data_id = data_id if data_id is not None else ""
            try:
                # Check if it is a mmCIF-like dictionary with datablock id
                # Expecting
                #   {
                #       DATABLOCK_ID: { CATEGORY: { ITEM: VALUE } }
                #   }
                (datablock_id, datablock) = list(__dictionary.items())[
                    0
                ]  # arbitrarily take the first datablock
                category = list(datablock.values())[0]
                item = list(category.values())[0]
                # Extract data block id from dictionary
                self.data_id = datablock_id
                self._DATA = datablock
            except AttributeError:
                # mmCif-like dictionary doesn't appear to contain datablock id
                #   {
                #       CATEGORY: { ITEM: VALUE }
                #   }
                # DATABLOCK_ID is set to self.data_id
                # TODO: Should a unique datablock ID br generated if
                #       self.data_id == ''
                self._DATA = __dictionary
            self.__convertDictToCIFWrapperTable()

    def __getattr__(self, attr_in):
        return self._DATA.get(attr_in)

    def __convertDictToCIFWrapperTable(self):
        """Converter for mmCIF-like dictionaries or MMCIF2Dict parser output"""
        for k in list(self._DATA.keys()):
            j = OrderedDict() if self._preserve_order else {}
            for k2, v2 in list(self._DATA[k].items()):
                if isinstance(v2, list):
                    j[k2] = v2
                else:
                    j[k2] = [
                        v2,
                    ]
            self._DATA.update(
                {k: CIFWrapperTable(j, preserve_token_order=self._preserve_order)}
            )

    def unwrap(self):
        """Extract encapsulated data to return an mmCIF-like python dictionary
        """
        # TODO: Might have to copy.deepcopy to ensure clean references
        cleaned_map = OrderedDict() if self._preserve_order else {}
        for k, v in list(self._DATA.items()):
            cleaned_map.setdefault(k, OrderedDict() if self._preserve_order else {})
            for k2, v2 in list(v._DATA.items()):
                cleaned_map[k][k2] = v2
        if self.data_id is not None and self.data_id != "":
            return {self.data_id: cleaned_map}
        else:
            return {str(id(self)): cleaned_map}

    def __contains__(self, tableNameIn):
        """Support for the 'in' operator to check the existence of categoties
        """
        return tableNameIn in self._DATA

    def __getitem__(self, tableNameIn):
        return self._DATA.get(tableNameIn)

    #    def __setitem__(self, tableName, tableValue):
    #        if not isinstance(tableValue, list):
    #            tableValue = [tableValue, ]
    #        if tableName not in self._DATA:
    #            self._DATA.setdefault(tableName, tableValue)
    #        else:
    #            self._DATA[tableName] = tableValue

    def __delitem__(self, tableName):
        if tableName in self._DATA:
            del self._DATA[tableName]

    def contents(self):
        return list(self._DATA.keys())


class Item(object):

    """
    Item objects are stored and managed by Category objects while Item
    objects store and manage values in CIF files. Items that are lists would
    represent looped categories.
    """

    def __init__(self, item_name, parent):
        """"""
        self.value = None
        self.type = str
        self.mandatory = False
        self.isColumn = False
        self.id = item_name
        self.name = self.id

        self.parent = parent
        self.parent.items[self.id] = self

    def getItemName(self):
        """"""
        return self.id

    def setValue(self, item_value, item_type="DEFAULTSTRING"):
        """"""
        if self.value is None and self.isColumn is False:
            if isinstance(item_value, list) and len(item_value) == 1:
                self.value = item_value[0]
                self.type = [
                    item_type,
                ]
            elif isinstance(item_value, list) and len(item_value) > 1:
                self.value = item_value
                self.isColumn = True
                self.parent.isTable = True
                self.type = [item_type for item_type in item_value]
            else:
                self.value = item_value
                self.type = item_type

        elif self.value is not None and self.isColumn is False:
            self.value = [self.value, item_value]
            self.type = [self.type, item_type]
            self.isColumn = True
            self.parent.isTable = True
        else:
            self.value.append(item_value)
            self.type.append(item_type)

    def getRawValue(self):
        """Raw value is the unformatted value stored by the item"""
        return self.value

    def getFormattedValue(self):
        """Return the value as it should appear (formatted) in the CIF file"""
        if isinstance(self.value, list):
            formatted_value = [_formatVal(v) if v else "." for v in self.value]
        else:
            formatted_value = _formatVal(self.value) if self.value else "."
        return formatted_value

    def remove(self):
        """Remove Item from Category and add Item to the Category recycle bin
        """
        self.parent.removeChild(self)

    def reset(self):
        """Clear the value of Item for one or all values to '.'"""
        if self.value is not None:
            if isinstance(self.value, list):
                self.value = [None for v in self.value]
            else:
                self.value = None
        self.type = None

    def __repr__(self):
        """"""
        return '<%s "%s": %s>' % (
            self.__class__.__name__,
            self.id,
            "COLUMN" if self.isColumn else "",
        )


class Category(object):

    """
    Category objects store and manage Item objects. Categories that contain
    Items that are lists of values would represent looped categories.
    Category objects are stored and managed by either DataBlock of SaveFrame
    objects.
    """

    def __init__(self, category_id, parent):
        """"""
        self.recycleBin = {}
        self.isTable = False
        self.id = category_id.lstrip("_")
        self._maxTagLength = 0

        self.parent = parent
        self.parent.categories[self.id] = self

        self.preserve_order = self.parent.preserve_order
        self.items = OrderedDict() if self.preserve_order else {}

    def getId(self):
        """"""
        return self.id

    def setItem(self, item):
        """"""
        try:
            item.isalnum()  # duck typing
            item = Item(item, self) if item not in self.items else self.items.get(item)
        except AttributeError:
            pass
        try:
            self._maxTagLength = (
                len("_" + self.id + item.id)
                if len("_" + self.id + item.id) > self._maxTagLength
                else self._maxTagLength
            )
        except AttributeError:
            # TODO: Raise appropriate exception as it is neither string nor
            # Item
            return None
        if (
            item.value is not None
            and isinstance(item.value, list)
            and self.isTable is False
        ):
            self.isTable = True
        return self.items.setdefault(item.id, item)

    def getItem(self, item_name):
        """"""
        return self.items.get(item_name, None)

    def getItemNames(self):
        """List the Items (by name) stored by Category"""
        return list(self.items.keys())

    def getItems(self):
        """Retrieve all Item objects"""
        return list(self.items.values())

    def remove(self):
        """Remove Category from SaveFrame or DataBlock and add Category to
        SaveFrame or DataBlock recycle bin"""
        self.parent.removeChild(self)

    def removeChild(self, child):
        """Remove Item from the Category using Item(object) or item name
        ID(string)"""
        try:
            if child.id in self.items:
                self.recycleBin[child.id] = self.items.pop(child.id)
                return True
        except AttributeError:
            if child in self.items:
                self.recycleBin[child] = self.items.pop(child)
                return True
        return False
        # TODO: Should Category be removed if num Items is zero?
        # if len(self.items) == 0:
        #    self.remove()

    def __repr__(self):
        return '<%s "_%s" with items %s>' % (
            self.__class__.__name__,
            self.id,
            str(self.getItemNames()),
        )


class SaveFrame(object):
    """
    SaveFrame objects store and manage Category objects (Dictionary CIF only).
    SaveFrame objects are stored and managed by DataBlock objects.
    """

    def __init__(self, saveFrame_id, parent):
        """"""
        self.id = saveFrame_id
        self.recycleBin = {}

        self.parent = parent
        self.parent.saveFrames[self.id] = self

        self.preserve_order = self.parent.preserve_order
        self.categories = OrderedDict() if self.preserve_order else {}

    def updateId(self, saveFrame_id):
        """Change the SaveFrame definition ID"""
        self.id = saveFrame_id

    def getId(self):
        """"""
        return self.id

    def setCategory(self, category):
        """"""
        try:
            category.isalnum()  # duck typing
            category = (
                Category(category.lstrip("_"), self)
                if category.lstrip("_") not in self.categories
                else self.categories.get(category.lstrip("_"))
            )
        except AttributeError:
            pass
        return self.categories.setdefault(category.id, category)

    def getCategory(self, category):
        """"""
        category = category.lstrip("_")
        return self.categories.get(category, None)

    def getCategoryIds(self):
        """List the Categories (by ID) stored by SaveFrame"""
        return list(self.categories.keys())

    def getCategories(self):
        """Retrieve all Category objects"""
        return list(self.categories.values())

    def remove(self):
        """Remove SaveFrame from DataBlock and add SaveFrame to DataBlock
        recycle bin"""
        self.parent.removeChild(self)

    def removeChild(self, child):
        """Remove Category from the SaveFrame using Category(object) or
        Category ID(string)"""
        try:
            if child.id in self.categories:
                self.recycleBin[child.id] = self.categories.pop(child.id)
                return True
        except AttributeError:
            if child in self.categories:
                self.recycleBin[child] = self.categories.pop(child)
                return True
        return False

    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.id)


class DataBlock(object):
    """
    DataBlock stores and manages SaveFrame and Category objects in CIF files.
    """

    def __init__(self, block_id, parent):
        """"""
        self.id = block_id
        self.recycleBin = {}

        self.parent = parent
        self.parent.data_blocks[self.id] = self

        self.preserve_order = self.parent.preserve_order
        if self.preserve_order:
            self.categories = OrderedDict()
            self.saveFrames = OrderedDict()
        else:
            self.categories = {}
            self.saveFrames = {}

    def updateId(self, block_id):
        """Change the DataBlock ID"""
        self.id = block_id

    def getId(self):
        """"""
        return self.id

    # CATEGORIES

    def setCategory(self, category):
        """"""
        try:
            category.isalnum()  # duck typing
            category = (
                Category(category.lstrip("_"), self)
                if category.lstrip("_") not in self.categories
                else self.categories.get(category.lstrip("_"))
            )
        except AttributeError:
            pass
        return self.categories.setdefault(category.id, category)

    def getCategory(self, category):
        """"""
        category = category.lstrip("_")
        return self.categories.get(category, None)

    def getCategoryIds(self):
        """List the Categories (by ID) stored by SaveFrame"""
        return list(self.categories.keys())

    def getCategories(self):
        """Retrieve all Category objects"""
        return list(self.categories.values())

    # SAVEFRAMES
    def setSaveFrame(self, saveFrame):
        """"""
        try:
            saveFrame.isalnum()  # duck typing
            saveFrame = (
                SaveFrame(saveFrame, self)
                if saveFrame not in self.saveFrames
                else self.saveFrames.get(saveFrame)
            )
        except AttributeError:
            pass
        return self.saveFrames.setdefault(saveFrame.id, saveFrame)

    def getSaveFrame(self, saveFrameId):
        """"""
        return self.saveFrames.get(saveFrameId, None)

    def getSaveFrameIds(self):
        """List the SaveFrames (by ID) stored by DataBlock"""
        return list(self.saveFrames.keys())

    def getSaveFrames(self):
        """Retrieve all SaveFrame objects stored by DataBlock"""
        return list(self.saveFrames.values())

    def remove(self):
        """Remove DataBlock from CifFile and add DataBlock to CifFile
        recycle bin"""
        self.parent.removeChild(self)

    def removeChild(self, child):
        """Remove Category/SaveFrame from the DataBlock using
        Category/SaveFrame(object) or Category/SaveFrame ID(string)"""
        if isinstance(child, Category) and child.id in self.categories:
            self.recycleBin[child.id] = self.categories.pop(child.id)
            return True
        elif isinstance(child, SaveFrame) and child.id in self.saveFrames:
            self.recycleBin[child.id] = self.saveFrames.pop(child.id)
            return True
        elif isinstance(child, str) and (
            child.lstrip("_") in self.categories or child in self.saveFrames
        ):
            removed = []
            child_as_cat = child.lstrip("_")
            if child_as_cat in self.categories:
                self.recycleBin[child_as_cat] = self.categories.pop(child_as_cat)
                removed.append("categories")
            elif child in self.saveFrames:
                self.recycleBin[child] = self.saveFrames.pop(child)
                removed.append("saveFrames")

            if len(removed) > 0:
                print("Warning: '%s' removed from %s" % (child, " and ".join(removed)))
                return True
            else:
                return False
        else:
            return False

    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.id)


class CifFile(object):
    """
    CifFile represents all the objects contained/part of an mmCIF file or
    dictionary. It stores and manages DataBlock objects.
    """

    def __init__(self, file_path=None, mmcif_data_map=None, preserve_token_order=False):
        """"""
        self.recycleBin = {}
        self.file_path = file_path
        self.preserve_order = preserve_token_order
        self.data_blocks = OrderedDict() if preserve_token_order else {}

        if mmcif_data_map is not None:
            self.import_mmcif_data_map(mmcif_data_map)

    def setDataBlock(self, datablock):
        """"""
        try:
            datablock.isalnum()  # duck typing
            datablock = (
                DataBlock(datablock, self)
                if datablock not in self.data_blocks
                else self.data_blocks.get(datablock)
            )
        except AttributeError as attr_err:
            pass
        return self.data_blocks.setdefault(datablock.id, datablock)

    def getDataBlock(self, dataBlockId):
        """"""
        return self.data_blocks.get(dataBlockId, None)

    def getDataBlockIds(self):
        """List the DataBlocks (by ID) stored by CifFile"""
        return list(self.data_blocks.keys())

    def getDataBlocks(self):
        """Retrieve all DataBlock objects stored by CifFile"""
        return list(self.data_blocks.values())

    def import_mmcif_data_map(self, mmcif_data_map):
        """Populates all objects necessary to represent mmCIF data files.
        mmcif_data_map is an mmCIF-like dictionary of the form
            {
                DATABLOCK_ID: { CATEGORY: { ITEM:  VALUE } }
            }
        """
        if isinstance(mmcif_data_map, dict) and mmcif_data_map != {}:
            for datablock_id, categories_items_and_values in list(
                mmcif_data_map.items()
            ):
                data_block_obj = self.setDataBlock(datablock_id)
                for category, items_and_values in list(
                    categories_items_and_values.items()
                ):
                    category_obj = data_block_obj.setCategory(category)
                    for item, value in list(items_and_values.items()):
                        item = category_obj.setItem(item).setValue(value)
        else:
            if not isinstance(mmcif_data_map, dict):
                print(
                    "Data import was unsuccessful. Data was not supplied as mmCIF-like dictionary"
                )
            elif mmcif_data_map == {}:
                pass

    def removeChild(self, child):
        """Remove DataBlock from the CifFile using
        DataBlock(object) or DataBlock ID(string)
        @return True if child removed else False
        """
        try:
            if child.id in self.data_blocks:
                self.recycleBin[child.id] = self.data_blocks.pop(child.id)
                return True
        except AttributeError:
            if child in self.data_blocks:
                self.recycleBin[child] = self.data_blocks.pop(child)
                return True
        return False

    def __repr__(self):
        return "<%s%s>" % (
            self.__class__.__name__,
            ' "' + self.file_path + '"' if self.file_path is not None else "",
        )


# internal functions & classes
def _formatVal(val):
    """Format any value as it would appear in a CIF file"""
    reserved = ("_", "#", "$", "'", '"', "[", "]", ";")

    val = str(val)
    has_space = " " in val and "\n" not in val

    if "'" in val:
        val = '"%s"' % val
    elif '"' in val:
        val = "'%s'" % val
    elif re.search(ascii_char, val):
        # Checks if non-ascii character present
        val = '"%s"' % val
    else:
        val = ('"%s"' % val) if val.startswith(reserved) or has_space else val

    if "\n" in val:
        if val[0] in ("'", '"'):
            val = val[1:-1]
        val = "\n;" + val + "\n;\n"
    elif (
        "\n" not in val
        and val[0] in ("'", '"')
        and ("'" in val[1:-1] and '"' in val[1:-1])
    ):
        val = "\n;" + val[1:-1] + "\n;\n"

    return val
