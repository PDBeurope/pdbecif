"""
This mmcif package contains all the classes necessary to read and write
either a data or a dictionary mmCIF file.

Reading files can be acheived using either CifFileReader or MMCIF2Dict:
--------------------------------------------------------------------------------
1. CifFileReader
--------------------------------------------------------------------------------

INPUT:
There are two types of behaviour that can be configured when instantiating the
CifFileReader. You can specify the file type as either 'data' (default) or
'dictionary'.

 - If 'dictionary' is specified the reader will always return a CifFile object
   regardless of the 'output' flag in the read() method.
 - If 'data' is specified (this is the default behaviour), the 'output' flag
   in the read metho

import mmCif.mmcifIO as mmcif
cfr = mmcif.CifFileReader(input='dictionary')

READING:
By changing the 'output' parameter, users can customize the way in which mmCIF
is returned. output takes one of three values i.e.:
    1. 'cif_dictionary' returns a tuple of datablock_id and mmCIF data
        (cif_id, cif_dictionary) = cfr.read("../../resources/dodgy.cif", output='cif_dictionary')

    2. 'cif_wrapper' returns a CIFWrapper object that encapsulates mmCIF-like
        dictionaries for python 'dot' notation data access
        cif_wrapper = cfr.read("../../resources/dodgy.cif", output='cif_wrapper')

    3. 'cif_file' returns a CifFile object that fully encapsulates all
        components of mmCIF files
        cif_file = cfr.read("../../resources/dodgy.cif", output='cif_file')

NB: if 'input' is set as 'dictionary' when instantiating CifFileReader, 'output'
will have no effect
--------------------------------------------------------------------------------
2. MMCIF2Dict
--------------------------------------------------------------------------------

A very low level access to mmCIF data files. MMCIF2Dict has one method 'parse()'
that returns (datablock_id, mmCIF_data) tuples as (str, dict)

MMCIF2DICT is very fast at reading mmCIF data.

################################################################################
Writing files:

CifFileWriter accepts mmCIF-like dictionaries, CIFWrapper objects, and CifFile
objects to write. Files can be compressed while writing using the
compress=True flag.

Examples continued from above:

cfd = mmcif.CifFileWriter("../../resources/cif_dictionary_test.cif")
cfd.write(cif_dictionary)
cfw = mmcif.CifFileWriter("../../resources/cif_wrapper_test.cif")
cfw.write(cif_wrapper)
cff = mmcif.CifFileWriter("../../resources/cif_file_test.cif")
cff.write(cif_file)

"""

__author__ = "Glen van Ginkel (Protein Data Bank in Europe; http://pdbe.org)"
__date__ = "$30-Jun-2012 18:23:30$"

# imports
import os.path
import re
import gzip
from mmCif import *
from mmCif.utils import openGzip
from mmCif.utils import pretty_print
from com.globalphasing.startools import StarTokeniser
from com.pdbe.mmciftools import MMCIF2Dict

# constants

# exception classes

print("DEPRECATION NOTICE:")
print("===================")
print()
print("Imports from mmCIF/com are going to be deprecated with the new version.")
print("Please import from pdbecif package.")
print("See documentation: https://pdbeurope.github.io/pdbecif/ for details.")


class LoopValueMultiplesError(Exception):

    """"""

    def __init__(self, lineno):
        self.lineno = int(lineno)
        self.msg = "Number of values is not a multiple of items \
                (loop_ start: line %s)"

    def __str__(self):
        return repr(self.msg % str(self.lineno))


class BadStarTokenError(Exception):

    """"""

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return "Tokenizer detected bad token: [" + repr(self.token.value) + "]"


# classes


class CifFileWriter(object):

    """
    CifFileWriter writes mmCIF formatted files and accepts mmCIF-like dictionary
    files, CIFWrapper objects, and CifFile objects.
    """

    DATABLOCK = "data_%s\n#\n"
    CATEGORY = "_%s"
    ITEM = ".%s"
    CAT_ITM = "_%s.%s"
    VALUE = "%s"
    NEWLINE = "#\n"
    LOOP = "loop_\n"
    SAVEFRAMESTART = "save_%s\n#\n"
    SAVEFRAMEEND = "save_\n\n"

    _handle = None

    def __init__(self, file_path=None, compress=False, mode="wt", preserve_order=False):
        #        """"""
        #        #orig
        #        self._handle = openGzip(
        #            file_path,
        #            'w') if file_path is not None else file_path
        # new
        self.compress = compress
        self.preserve_token_order = preserve_order

        if (file_path and isinstance(file_path, str)) or file_path is None:
            file_path = (
                file_path
                if (file_path and isinstance(file_path, str) and not compress)
                else (
                    file_path + ".gz"
                    if (
                        file_path
                        and isinstance(file_path, str)
                        and not file_path.endswith(".gz")
                        and compress
                    )
                    else file_path
                )
            )
            self._handle = (
                openGzip(file_path, mode) if file_path is not None else file_path
            )
        else:
            raise TypeError("file_path argument is not a string")

        self.verbose = False  # TODO: Not implemented

    def __del__(self):
        """Make sure any open file objects are closed when CifFileWriter is
        destroyed by the garbage collector"""
        if self._handle:
            self._handle.flush()
            self._handle.close()
            self._handle = None

    def write(self, cifObjIn, compress=False, mode="wt", preserve_order=False):

        token_ordering = (
            self.preserve_token_order or preserve_order
        )  # preserve ordering of either flag is True

        if isinstance(cifObjIn, CifFile):
            cifObjIn.preserve_order = (
                token_ordering
                if not cifObjIn.preserve_order
                else cifObjIn.preserve_order
            )
            self._writeCifObj(cifObjIn, compress, mode)
        elif isinstance(cifObjIn, CIFWrapper):
            if self._handle is not None:
                cif_file = CifFile(
                    self._handle.name, preserve_token_order=cifObjIn._preserve_order
                )
                if cifObjIn.data_id is None:
                    cifObjIn.data_id = os.path.basename(self._handle.name).replace(
                        " ", "_"
                    )
                cif_data = cifObjIn.unwrap()
                cif_file.import_mmcif_data_map(cif_data)
                self._writeCifObj(cif_file, compress, mode)
            else:
                print("Cannot write CifFile as no path/filename was provided")
        elif isinstance(cifObjIn, dict):
            if self._handle is not None and cifObjIn != {}:
                cif_file = CifFile(
                    self._handle.name, preserve_token_order=token_ordering
                )
                # Check if it is a mmCIF-like dictionary
                # Expecting
                #   {
                #       DATABLOCK_ID: { CATEGORY: { ITEM: VALUE } }
                #   }
                datablock_id = ""
                try:
                    (datablock_id, datablock) = list(cifObjIn.items())[0]
                    category = list(datablock.values())[0]
                    item = list(category.values())[0]
                    cif_file.import_mmcif_data_map(cifObjIn)
                except AttributeError:
                    # ... but can also handle
                    #   {
                    #       CATEGORY: { ITEM: VALUE }
                    #   }
                    # DATABLOCK_ID is set to file_path
                    datablock_id = os.path.basename(self._handle.name).replace(" ", "_")
                    cif_file.import_mmcif_data_map({datablock_id: cifObjIn})

                self._writeCifObj(cif_file, compress, mode)
            else:
                print("Cannot write CifFile as no path/filename was provided")
        else:
            print("Could not write CIF file (object provided not supported)")

    def _writeCifObj(self, cifObjIn, compress=False, mode="wt"):
        """"""
        if self._handle is None:
            try:
                if compress:
                    self._handle = gzip.open(cifObjIn.file_path + ".gz", mode)
                else:
                    self._handle = openGzip(cifObjIn.file_path, mode)
            except Exception as err:
                print("CifFileWriter error: %s" % str(err))
                print("Could not write mmCIF file (No output path/filename specified)")
                return

        for datablock in cifObjIn.getDataBlocks():
            self._handle.write(self.DATABLOCK % datablock.getId())
            for category in datablock.getCategories():
                if not category.isTable:
                    for item in category.getItems():
                        tag = self.CAT_ITM % (category.getId(), item.name)
                        tag = tag.ljust(category._maxTagLength + 8)
                        self._handle.write(tag + item.getFormattedValue() + "\n")
                else:
                    self._handle.write(self.LOOP)
                    table = []
                    colLen = None
                    for item in category.getItems():
                        tag = self.CAT_ITM % (category.getId(), item.name)
                        tag = tag.ljust(category._maxTagLength + 8)
                        self._handle.write(tag + "\n")
                        table.append(item.getFormattedValue())
                        if not colLen:
                            colLen = len(item.value)

                    self._handle.write(pretty_print(table, transpose=True))
                self._handle.write("\n" + self.NEWLINE)
                # HANDLE SAVEFRAMES #

            for saveframe in datablock.getSaveFrames():
                self._handle.write(self.SAVEFRAMESTART % saveframe.getId())
                for category in saveframe.getCategories():
                    if not category.isTable:
                        for item in category.getItems():
                            tag = self.CAT_ITM % (category.getId(), item.name)
                            tag = tag.ljust(category._maxTagLength + 8)
                            self._handle.write(tag + item.getFormattedValue() + "\n")
                    else:
                        self._handle.write(self.LOOP)
                        table = []
                        colLen = None
                        for item in category.getItems():
                            tag = self.CAT_ITM % (category.getId(), item.name)
                            tag = tag.ljust(category._maxTagLength + 8)
                            self._handle.write(tag + "\n")
                            table.append(item.getFormattedValue())
                            if not colLen:
                                colLen = len(item.value)
                        self._handle.write(pretty_print(table, transpose=True))
                    self._handle.write("\n" + self.NEWLINE)
                self._handle.write(self.SAVEFRAMEEND)
        self._handle.flush()
        # self._handle.close()
        # self._handle = None


class CifFileReader(object):

    """
    CifFileReader takes a path to an mmCIF file location (data or dictionary
    CIF and once read will return an mmcif.CifFile object
    """

    def __init__(self, input="data", verbose=False, preserve_order=False):
        """"""
        self.input = input
        self.file_path = None
        self.verbose = verbose  # TODO: Not implemented
        self.preserve_token_order = preserve_order

    def read(
        self,
        file_path,
        output="cif_dictionary",
        ignore=[],
        preserve_order=False,
        only=None,
    ):

        token_ordering = (
            self.preserve_token_order or preserve_order
        )  # preserve ordering of either flag is True
        if self.input == "data":
            # (datablock_id, mmcif_dict) = MMCIF2Dict().parse(file_path, ignoreCategories=ignore)
            mmcif_dict = MMCIF2Dict().parse(
                file_path,
                ignoreCategories=ignore,
                preserve_token_order=token_ordering,
                onlyCategories=only,
            )
            if output == "cif_dictionary":
                return mmcif_dict
            elif output == "cif_wrapper":
                return dict(
                    (
                        (
                            block_id,
                            CIFWrapper(
                                block_data,
                                data_id=block_id,
                                preserve_token_order=token_ordering,
                            ),
                        )
                        for block_id, block_data in list(mmcif_dict.items())
                    )
                )
                # return CIFWrapper(mmcif_dict, data_id=datablock_id)
            elif output == "cif_file":
                return CifFile(
                    file_path,
                    mmcif_data_map=mmcif_dict,
                    preserve_token_order=token_ordering,
                )
            else:
                return
        else:
            return self._exportCifFile(file_path, token_ordering)

    def _processLoop(self, category, loopItems, loopValues):
        """Create the Items in a category given an array of items and item values
        """

        valNum = len(loopValues)
        itmNum = len(loopItems)
        if valNum % itmNum != 0:
            raise LoopValueMultiplesError()
        loopItems = [category.getItem(i) for i in loopItems]
        for i in range(valNum):
            loopItems[i % itmNum].setValue(loopValues[i][0], loopValues[i][1])

    def _exportCifFile(self, file_path, token_ordering):
        """"""
        cf = None
        if file_path is not None:
            cif_file = openGzip(file_path, "r")

            tokeniser = StarTokeniser()
            tokeniser.start_matching(cif_file)

            if cif_file:
                cf = CifFile(file_path, preserve_token_order=token_ordering)
            db = None
            sf = None
            cc = None
            ci = None
            loopItems = []
            loopValues = []
            loop_state = False
            save_state = False
            loop_value_state = False

            # Keller tokenizer provides the following tokens:
            # "", "MULTILINE", "COMMENT", "GLOBAL", "SAVE_FRAME", "SAVE_FRAME_REF",
            # "LOOP_STOP", "DATA_BLOCK", "LOOP", "BAD_CONSTRUCT", "DATA_NAME", "SQUOTE_STRING",
            # "DQUOTE_STRING", "NULL", "UNKNOWN", "SQUARE_BRACKET", "STRING", "BAD_TOKEN"

            DATA_TOKENS = [
                "MULTILINE",
                "SQUOTE_STRING",
                "DQUOTE_STRING",
                "NULL",
                "UNKNOWN",
                "STRING",
            ]
            # NB: Square bracket  types are not currently handled

            for tok in tokeniser:
                if tok.type_string == "BAD_TOKEN":
                    raise BadStarTokenError(tok)

                if tok.type_string == "DATA_BLOCK":
                    db = cf.setDataBlock(tok.value[tok.value.find("_") + 1 :])
                    loop_state = False
                    save_state = False

                elif tok.type_string == "LOOP":
                    loop_value_state = False
                    if not loop_state:
                        loop_state = True
                    if loopValues != []:
                        self._processLoop(cc, loopItems, loopValues)
                        loopItems = []
                        loopValues = []

                elif tok.type_string == "SAVE_FRAME":
                    if save_state:
                        save_state = False
                    else:
                        sf = db.setSaveFrame(tok.value[tok.value.find("_") + 1 :])
                        save_state = True
                    if loop_state:
                        loop_state = False
                        if loopValues != []:
                            self._processLoop(cc, loopItems, loopValues)
                            loopItems = []
                            loopValues = []

                elif tok.type_string == "DATA_NAME":
                    [category_name, item_name] = tok.value.split(".")
                    if loop_value_state:
                        loop_state = False
                        loop_value_state = False
                        if loopValues != []:
                            self._processLoop(cc, loopItems, loopValues)
                            loopItems = []
                            loopValues = []

                    if not save_state:
                        cc = db.setCategory(category_name)
                    else:
                        cc = sf.setCategory(category_name)

                    if loop_state:
                        loopItems.append(item_name)

                    ci = cc.setItem(item_name)

                elif tok.type_string in DATA_TOKENS:  # It's a data contatining token
                    token_value = tok.value
                    if loop_state:
                        loopValues.append((token_value, tok.type_string))
                        if not loop_value_state:
                            loop_value_state = True
                    else:
                        ci.setValue(token_value, tok.type_string)
            if loopValues != []:
                self._processLoop(cc, loopItems, loopValues)
                loopItems = []
                loopValues = []

        return cf
