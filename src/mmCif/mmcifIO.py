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
from com.globalphasing.startools import StarTokeniser

# constants

# exception classes


class MMCIFWrapperSyntaxError(Exception):

    """"""

    def __init__(self, category):
        self.category = category

    def __str__(self):
        return "More items than values for category " + \
            repr(self.category) + "!"


class LoopValueMultiplesError(Exception):

    """"""

    def __init__(self, lineno):
        self.lineno = int(lineno)
        self.msg = "Number of values is not a multiple of items \
                (loop_ start: line %s)"

    def __str__(self):
        return repr(self.msg % str(self.lineno))


class MultipleLoopCategoriesError(Exception):

    """"""

    def __init__(self, lineno):
        self.lineno = int(lineno)
        self.msg = "Multiple categories detected in single loop \
                (loop_ start: line %s)"

    def __str__(self):
        return repr(self.msg % str(self.lineno))


class BadStarTokenError(Exception):

    """"""

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return "Tokenizer detected bad token: [" + \
            repr(self.token.value) + "]"


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

    def __init__(self, file_path=None):
        """"""
        
        if file_path and isinstance(file_path, str):
            self._handle = openGzip(
                file_path,
                'w') if file_path is not None else file_path
        elif file_path is None:
            pass
        else:
            from exceptions import TypeError
            raise TypeError("file_path argument is not a string")
        
        self.verbose = False  # TODO: Not implemented

    def __del__(self):
        """Make sure any open file objects are closed when CifFileWriter is
        destroyed by the garbage collector"""
        if self._handle:
            self._handle.flush()
            self._handle.close()
            self._handle = None

    def write(self, cifObjIn, compress=False, mode='w'):
        if isinstance(cifObjIn, CifFile):
            self._writeCifObj(cifObjIn, compress, mode)
        elif isinstance(cifObjIn, CIFWrapper):
            if self._handle is not None:
                cif_file = CifFile(self._handle.name)
                if cifObjIn.data_id is None:
                    cifObjIn.data_id = os.path.basename(
                        self._handle.name).replace(' ', '_')
                cif_data = cifObjIn.unwrap()
                cif_file.import_mmcif_data_map(cif_data)
                self._writeCifObj(cif_file, compress, mode)
            else:
                print("Cannot write CifFile as no path/filename was provided")
        elif isinstance(cifObjIn, dict):
            if self._handle is not None and cifObjIn != {}:
                cif_file = CifFile(self._handle.name)
                # Check if it is a mmCIF-like dictionary
                # Expecting
                #   {
                #       DATABLOCK_ID: { CATEGORY: { ITEM: VALUE } }
                #   }
                datablock_id = ''
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
                    datablock_id = os.path.basename(
                        self._handle.name).replace(' ',
                                                   '_')
                    cif_file.import_mmcif_data_map({datablock_id: cifObjIn})

                self._writeCifObj(cif_file, compress, mode)
            else:
                print("Cannot write CifFile as no path/filename was provided")
        else:
            print("Could not write CIF file (object provided not supported)")

    def _writeCifObj(self, cifObjIn, compress=False, mode='w'):
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
                        tag = (self.CAT_ITM % (category.getId(), item.name))
                        tag = tag.ljust(category._maxTagLength + 8)
                        self._handle.write(
                            tag + item.getFormattedValue() + "\n")
                else:
                    self._handle.write(self.LOOP)
                    table = []
                    colLen = None
                    for item in category.getItems():
                        tag = (self.CAT_ITM % (category.getId(), item.name))
                        tag = tag.ljust(category._maxTagLength + 8)
                        self._handle.write(tag + "\n")
                        table.append(item.getFormattedValue())
                        if not colLen:
                            colLen = len(item.value)
                    for rI in range(len(table[0])):
                        self._handle.write(
                            " ".join([col[rI] for col in table]) + "\n")
                self._handle.write(self.NEWLINE)
                # HANDLE SAVEFRAMES #

            for saveframe in datablock.getSaveFrames():
                self._handle.write(self.SAVEFRAMESTART % saveframe.getId())
                for category in saveframe.getCategories():
                    if not category.isTable:
                        for item in category.getItems():
                            tag = (
                                self.CAT_ITM %
                                (category.getId(), item.name))
                            tag = tag.ljust(category._maxTagLength + 8)
                            self._handle.write(
                                tag + item.getFormattedValue() + "\n")
                    else:
                        self._handle.write(self.LOOP)
                        table = []
                        colLen = None
                        for item in category.getItems():
                            tag = (
                                self.CAT_ITM %
                                (category.getId(), item.name))
                            tag = tag.ljust(category._maxTagLength + 8)
                            self._handle.write(tag + "\n")
                            table.append(item.getFormattedValue())
                            if not colLen:
                                colLen = len(item.value)
                        for rI in range(len(table[0])):
                            self._handle.write(
                                " ".join([col[rI] for col in table]) + "\n")
                    self._handle.write(self.NEWLINE)
                self._handle.write(self.SAVEFRAMEEND)
        self._handle.flush()
        # self._handle.close()
        # self._handle = None


class CifFileReader(object):

    """
    CifFileReader takes a path to an mmCIF file location (data or dictionary
    CIF and once read will return an mmcif.CifFile object
    """

    def __init__(self, input='data', verbose=False):
        """"""
        self.input = input
        self.file_path = None
        self.verbose = verbose  # TODO: Not implemented

    def read(self, file_path, output='cif_dictionary', ignore=[]):
        if self.input == 'data':
            #(datablock_id, mmcif_dict) = MMCIF2Dict().parse(file_path, ignoreCategories=ignore)
            mmcif_dict = MMCIF2Dict().parse(file_path, ignoreCategories=ignore)
            if output == 'cif_dictionary':
                return mmcif_dict
            elif output == 'cif_wrapper':
                return dict(((block_id, CIFWrapper(block_data, data_id=block_id)) for block_id, block_data in list(mmcif_dict.items())))
                # return CIFWrapper(mmcif_dict, data_id=datablock_id)
            elif output == 'cif_file':
                return CifFile(file_path, mmcif_data_map=mmcif_dict)
            else:
                return
        else:
            return self._exportCifFile(file_path)

    def _processLoop(self, category, loopItems, loopValues):
        """Create the Items in a category given an array of items and item values
        """

        valNum = len(loopValues)
        itmNum = len(loopItems)
        if valNum % itmNum != 0:
            raise LoopValueMultiplesError()
        loopItems = [category.getItem(i) for i in loopItems]
        for i in range(valNum):
            loopItems[i % itmNum].setValue(
                                           loopValues[i][0],
                                           loopValues[i][1]
                                           )

    def _exportCifFile(self, file_path = None):
        """"""
        cf = None
        if file_path:
            cif_file = openGzip(file_path, 'r')

            tokeniser = StarTokeniser()
            tokeniser.start_matching(cif_file)
            
            if cif_file:
                cf = CifFile(file_path)
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

            DATA_TOKENS = ["MULTILINE", "SQUOTE_STRING", "DQUOTE_STRING", "NULL", "UNKNOWN", "STRING"]
            # NB: Square bracket  types are not currently handled

            for tok in tokeniser:
                if tok.type_string == 'BAD_TOKEN':
                    raise BadStarTokenError(tok)

                if tok.type_string == 'DATA_BLOCK':
                    db = cf.setDataBlock(tok.value[tok.value.find('_')+1:])
                    loop_state = False
                    save_state = False

                elif tok.type_string == 'LOOP':
                    loop_value_state = False
                    if not loop_state:
                        loop_state = True                        
                    if loopValues != []:
                        self._processLoop(cc, loopItems, loopValues)
                        loopItems = []
                        loopValues = []
                    
                elif tok.type_string == 'SAVE_FRAME':
                    if save_state:
                        save_state = False
                    else:
                        sf = db.setSaveFrame(tok.value[tok.value.find('_')+1:])
                        save_state = True
                    if loop_state:
                        loop_state = False
                        if loopValues != []:
                            self._processLoop(cc, loopItems, loopValues)
                            loopItems = []
                            loopValues = []

                elif tok.type_string == 'DATA_NAME':
                    [category_name, item_name] = tok.value.split('.')
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

                elif tok.type_string in DATA_TOKENS: # It's a data contatining token
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


class MMCIF2Dict():

    """
    MMCIF2Dict is a purely algorithmic parser that takes as input public
    mmCIF files and creates a python dictionary from them.

    Because this parser is highly optimised for public mmCIF format, it is
    highly unlikely that it will work successfully on any other formatted mmCIF
    file.

    MMCIF2Dict will not work on mmCIF dictionaries!


    Users are able to speed up parsing of public mmCIF data files substantially
    by including a list of categoriies that the parser can ignore if
    encountered.

    For example:

    parser.parse(path, ignoreCategories=["_atom_site", "_atom_site_anisotrop"])

    will ignore all coordinate lines in the file.

    """
    loopRE = re.compile(r'^\s*[L|l][O|o][O|o][P|p]_.*')
    # commentsRE = re.compile(r'(.*?)\s#.*$')
    dataRE = re.compile(r'^\s*[D|d][A|a][T|t][A|a]_(?P<data_heading>.*)\s*')
    saveRE = re.compile(r'^\s*[S|s][A|a][V|v][E|e]_(?P<save_heading>.*)\s*')
    dataNameRE = re.compile(r'^\s*(?P<data_category>_[\S]+)(?:\.)(?P<category_item>\S+)(?P<remainder>.*)')
    dataValueRE = re.compile(r'\s*(\'[\S\s]+?\'(?=\s)|"[\S\s]+?"(?=\s)|[\S]+)', re.M)
    header = ''
    data_map = None
    file_path = None

    def parse(self, file_path, ignoreCategories=[]):
        """Public method which only functions to check the existence of
        the mmCIF file in preparation for reading in the private parseFile
        method.
        """
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return self._parseFile(file_path, ignoreCategories)
        else:
            print("The file provided does not exist or is not a file.")
            return None

    def _tokenizeData(self, line):
        """Private method that will do the work of parsing the mmCIF data file
        return Dictionary"""
        if "'" in line or '"' in line:
            return (
                [x[1:-1] if x[0] == x[-1] and x[0] in ["'", '"']
                    else x for x in self.dataValueRE.findall(line)]
            )
        else:
            return line.strip().split()

    def _parseFile(self, file_path, ignoreCategories):
        """Private method that will do the work of parsing the mmCIF data file
        return Dictionary"""

        mmcif_like_file = {}
        data_heading = ""
        data_block = {}
        save_block = {}
        line_num = 0
        try:
            with openGzip(file_path, 'r') as f1:
                table_names = []
                table_values = []
                table_values_array = []
                isLoop = False
                multiLineValue = False
                skipCategory = False
                for line in f1:
                    line_num+=1
                    if skipCategory:
                        flag = False
                        while line:
                            check = (line.strip().startswith('_') or
                                self.loopRE.match(line.strip()[:5]) or
                                self.saveRE.match(line.strip()[:5]) or
                                self.dataRE.match(line.strip()[:5]))
                            if flag:
                                if check:
                                    isLoop = False
                                    break
                            else:
                                if not check:
                                    flag = True
                            if not (self.saveRE.match(line.strip()[:5]) or
                                self.dataRE.match(line.strip()[:5])):
                                try:
                                    line = next(f1)
                                    line_num+=1
                                except StopIteration:
                                    break
                            else:
                                break
                        skipCategory = False

                    if isLoop is True and table_values_array != [] and (self.loopRE.match(line) is not None or (line.strip().startswith('_'))):
                        isLoop = False
                        num_item = len(table_names)
                        if len(table_values_array) % num_item != 0:
                            raise MMCIFWrapperSyntaxError(category)
                        for val_index, item in enumerate(table_names):
                            data_block[category][item] = table_values_array[val_index::num_item]
                        table_values_array = []

                    if line.strip() == "":
                        continue
                    if line.startswith('#'):
                        continue
                    if '\t#' in line or ' #' in line and not line.startswith(';'):
                        new_line = ''
                        for tok in self.dataValueRE.findall(line):
                            if not tok.startswith('#'):
                                new_line += tok+" "
                            else:
                                break
                        # make sure to preserve the fact that ';' was not the first character
                        line = new_line if not new_line.startswith(';') else " "+new_line
                        # Fails for entries "3snv", "1kmm", "1ser", "2prg", "3oqd"
                        # line = re.sub(r'\s#.*$', '', line) 
                    if line.startswith(';'):
                        while '\n;' not in line:
                            try:
                                line += next(f1)
                                line_num+=1
                            except StopIteration:
                                break
                        multiLineValue = True
                    if self.dataRE.match(line):
                        if data_block != {}:
                            if table_values_array != []:
                                isLoop = False
                                num_item = len(table_names)
                                if len(table_values_array) % num_item != 0:
                                    raise mmCifSyntaxError(category)
                                for val_index, item in enumerate(table_names):
                                    data_block[category][item] = table_values_array[val_index::num_item]
                                table_names = []
                                table_values_array = []
                            mmcif_like_file[data_heading] = data_block
                            data_block = {}
                        data_heading = self.dataRE.match(line).group('data_heading')
                    elif self.saveRE.match(line):
                        while line.strip() != 'save_':
                            try:
                                line = next(f1)
                                line_num+=1
                            except StopIteration:
                                break
                        continue
                    elif self.loopRE.match(line):
                        # Save and clear the table_values_array buffer from the
                        # previous loop that was read
                        if table_values_array != []:
                            for itemIndex, name in enumerate(table_names):
                                data_block[category].update({name:[row[itemIndex] for row in table_values_array]})
                            table_values_array = []
                        isLoop = True
                        category, item, value = None, None, None
                        #Stores items of a category listed in loop blocks
                        table_names = []
                        #Stores values of items in a loop as a single row
                        table_values = []
                    elif self.dataNameRE.match(line):
                        # Match category and item simultaneously
                        m = self.dataNameRE.match(line)
                        category = m.group('data_category')
                        item = m.group('category_item')
                        remainder = m.group('remainder')
                        value = None
                        if isLoop and remainder != '':
                            """Append any data values following the last loop
                            category.item tag should any exist"""
                            table_values += self._tokenizeData(remainder)
                            line = ''
                        else:
                            line = remainder + "\n"
                        if not isLoop:
                            if line.strip() != '':
                                value = self._tokenizeData(line)
                            else:
                                # For cases where values are on the following
                                # line
                                try:
                                    line = next(f1)
                                    line_num +=1
                                except StopIteration:
                                    break
                            while value is None:
                                char_start = 1 if line.startswith(';') else 0
                                while line.startswith(';') and not line.rstrip().endswith('\n;'):
                                    try:
                                        line += next(f1)
                                        line_num+=1
                                    except StopIteration:
                                        break
                                value = (line[char_start:line.rfind('\n;')]).strip()
                                if char_start > 0:
                                    value = (line[char_start:line.rfind('\n;')]).strip()
                                else:
                                    value = self._tokenizeData(" "+line)
                            if ignoreCategories and category in ignoreCategories:
                                pass
                            else:
                                if category in data_block:
                                    data_block[category].update({item: value if len(value) > 1 else value[0]})
                                else:
                                    data_block.setdefault(category, {item: value if len(value) > 1 else value[0]})
                        else:
                            if ignoreCategories and category in ignoreCategories:
                                skipCategory = True
                            else:
                                data_block.setdefault(category, {})
                                table_names.append(item)
                    else:
                        if multiLineValue is True:
                            table_values.append((line[1:line.rfind('\n;')]).strip())
                            multiLineValue = False
                            line = line[line.rfind('\n;') + 2:]
                            if line.strip() != '':
                                table_values += self._tokenizeData(line)
                        else:
                            table_values += self._tokenizeData(line)

                        if table_values != []:
                            table_values_array += table_values
                            table_values = []
                if isLoop is True and table_values_array != []:
                    isLoop = False
                    num_item = len(table_names)
                    for val_index, item in enumerate(table_names):
                        data_block[category][item] = table_values_array[val_index::num_item]
                    table_values_array = []
                if data_block != {}:
                    mmcif_like_file[data_heading] = data_block
            return mmcif_like_file
        except KeyError as key_err:
            print("KeyError [line %i]: %s" %(line_num, str(key_err)))
        except IOError as io_err:
            print("IOException [line %i]: %s" % (line_num, str(io_err)))
#        except StopIteration as gen_err:
#            print mmcif_like_file
#            print "StopIteration [line %i]: %s" % (line_num, str(gen_err))
