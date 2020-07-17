"""
A very low level access to mmCIF data files. MMCIF2Dict has one method 'parse()'
that returns (datablock_id, mmCIF_data) tuples as (str, dict)

MMCIF2DICT is very fast at reading mmCIF data.
"""
__author__ = "Glen van Ginkel (Protein Data Bank in Europe; http://pdbe.org)"
__date__ = "$30-Jun-2012 18:23:30$"

# imports
import os.path
import re
from pdbecif.utils import openGzip

# constants

# exception classes


class MMCIFWrapperSyntaxError(Exception):

    """"""

    def __init__(self, category):
        self.category = category

    def __str__(self):
        return "More items than values for category " + repr(self.category) + "!"


class MultipleLoopCategoriesError(Exception):

    """"""

    def __init__(self, lineno):
        self.lineno = int(lineno)
        self.msg = "Multiple categories detected in single loop \
                (loop_ start: line %s)"

    def __str__(self):
        return repr(self.msg % str(self.lineno))


class MMCIF2Dict:

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

    loopRE = re.compile(r"^\s*[L|l][O|o][O|o][P|p]_.*")
    # commentsRE = re.compile(r'(.*?)\s#.*$')
    dataRE = re.compile(r"^\s*[D|d][A|a][T|t][A|a]_(?P<data_heading>.*)\s*")
    saveRE = re.compile(r"^\s*[S|s][A|a][V|v][E|e]_(?P<save_heading>.*)\s*")
    dataNameRE = re.compile(
        r"^\s*(?P<data_category>_[\S]+)(?:\.)(?P<category_item>\S+)(?P<remainder>.*)"
    )
    dataValueRE = re.compile(r'\s*(\'[\S\s]+?\'(?=\s)|"[\S\s]+?"(?=\s)|[\S]+)', re.M)
    header = ""
    data_map = None
    file_path = None
    reserve_token_order = False

    def parse(
        self,
        file_path,
        ignoreCategories=[],
        preserve_token_order=False,
        onlyCategories=[],
    ):
        """Public method which only functions to check the existence of
        the mmCIF file in preparation for reading in the private parseFile
        method.
        """
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return self._parseFile(
                file_path, ignoreCategories, preserve_token_order, onlyCategories
            )
        else:
            print("The file provided does not exist or is not a file.")
            return None

    def _tokenizeData(self, line):
        """Private method that will do the work of parsing the mmCIF data file
        return Dictionary"""
        if "'" in line or '"' in line:
            return [
                x[1:-1] if x[0] == x[-1] and x[0] in ["'", '"'] else x
                for x in self.dataValueRE.findall(line)
            ]
        else:
            return line.strip().split()

    def _parseFile(
        self, file_path, ignoreCategories, preserve_token_order, onlyCategories
    ):
        """Private method that will do the work of parsing the mmCIF data file
        return Dictionary"""

        if preserve_token_order:
            try:
                from collections import OrderedDict as _dict
            except ImportError:
                # fallback: try to use the ordereddict backport when using python 2.6
                try:
                    from ordereddict import OrderedDict as _dict
                except ImportError:
                    # backport not installed: use local OrderedDict
                    from mmCif.ordereddict import OrderedDict as _dict
        else:
            _dict = dict

        mmcif_like_file = _dict()
        data_block = _dict()
        save_block = _dict()

        data_heading = ""
        line_num = 0
        try:
            with openGzip(file_path, "rt") as f1:
                table_names = []
                table_values = []
                table_values_array = []
                isLoop = False
                multiLineValue = False
                skipCategory = False
                for line in f1:
                    line_num += 1
                    if skipCategory:
                        flag = False
                        while line:
                            check = (
                                line.strip().startswith("_")
                                or self.loopRE.match(line.strip()[:5])
                                or self.saveRE.match(line.strip()[:5])
                                or self.dataRE.match(line.strip()[:5])
                            )
                            if flag:
                                if check:
                                    isLoop = False
                                    break
                            else:
                                if not check:
                                    flag = True
                            if not (
                                self.saveRE.match(line.strip()[:5])
                                or self.dataRE.match(line.strip()[:5])
                            ):
                                try:
                                    line = next(f1)
                                    line_num += 1
                                except StopIteration:
                                    break
                            else:
                                break
                        skipCategory = False

                    if (
                        isLoop is True
                        and table_values_array != []
                        and (
                            self.loopRE.match(line) is not None
                            or (line.strip().startswith("_"))
                        )
                    ):
                        isLoop = False
                        num_item = len(table_names)
                        if len(table_values_array) % num_item != 0:
                            raise MMCIFWrapperSyntaxError(category)
                        for val_index, item in enumerate(table_names):
                            data_block[category][item] = table_values_array[
                                val_index::num_item
                            ]
                        table_values_array = []

                    if line.strip() == "":
                        continue
                    if line.startswith("#"):
                        continue
                    if "\t#" in line or " #" in line and not line.startswith(";"):
                        new_line = ""
                        for tok in self.dataValueRE.findall(line):
                            if not tok.startswith("#"):
                                new_line += tok + " "
                            else:
                                break
                        # make sure to preserve the fact that ';' was not the first character
                        line = (
                            new_line if not new_line.startswith(";") else " " + new_line
                        )
                        # Fails for entries "3snv", "1kmm", "1ser", "2prg", "3oqd"
                        # line = re.sub(r'\s#.*$', '', line)
                    if line.startswith(";"):
                        while "\n;" not in line:
                            try:
                                line += next(f1)
                                line_num += 1
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
                                    data_block[category][item] = table_values_array[
                                        val_index::num_item
                                    ]
                                table_names = []
                                table_values_array = []
                            mmcif_like_file[data_heading] = data_block
                            data_block = _dict()
                        data_heading = self.dataRE.match(line).group("data_heading")
                    elif self.saveRE.match(line):
                        while line.strip() != "save_":
                            try:
                                line = next(f1)
                                line_num += 1
                            except StopIteration:
                                break
                        continue
                    elif self.loopRE.match(line):
                        # Save and clear the table_values_array buffer from the
                        # previous loop that was read
                        if table_values_array != []:
                            for itemIndex, name in enumerate(table_names):
                                data_block[category].update(
                                    {
                                        name: [
                                            row[itemIndex] for row in table_values_array
                                        ]
                                    }
                                )
                            table_values_array = []
                        isLoop = True
                        category, item, value = None, None, None
                        # Stores items of a category listed in loop blocks
                        table_names = []
                        # Stores values of items in a loop as a single row
                        table_values = []
                    elif self.dataNameRE.match(line):
                        # Match category and item simultaneously
                        m = self.dataNameRE.match(line)
                        category = m.group("data_category")
                        item = m.group("category_item")
                        remainder = m.group("remainder")
                        value = None
                        if isLoop and remainder != "":
                            """Append any data values following the last loop
                            category.item tag should any exist"""
                            table_values += self._tokenizeData(remainder)
                            line = ""
                        else:
                            line = remainder + "\n"
                        if not isLoop:
                            if line.strip() != "":
                                value = self._tokenizeData(line)
                            else:
                                # For cases where values are on the following
                                # line
                                try:
                                    line = next(f1)
                                    line_num += 1
                                except StopIteration:
                                    break
                            while value is None:
                                char_start = 1 if line.startswith(";") else 0
                                while line.startswith(
                                    ";"
                                ) and not line.rstrip().endswith("\n;"):
                                    try:
                                        line += next(f1)
                                        line_num += 1
                                    except StopIteration:
                                        break
                                value = (line[char_start : line.rfind("\n;")]).strip()
                                if char_start > 0:
                                    value = (
                                        line[char_start : line.rfind("\n;")]
                                    ).strip()
                                else:
                                    value = self._tokenizeData(" " + line)
                            if (ignoreCategories and category in ignoreCategories) or (
                                onlyCategories and category not in onlyCategories
                            ):
                                pass
                            else:
                                if category in data_block:
                                    data_block[category].update(
                                        {item: value if len(value) > 1 else value[0]}
                                    )
                                else:
                                    data_block.setdefault(
                                        category,
                                        _dict(
                                            {
                                                item: value
                                                if len(value) > 1
                                                else value[0]
                                            }
                                        ),
                                    )  # OrderedDict here preserves item order
                        else:
                            if (ignoreCategories and category in ignoreCategories) or (
                                onlyCategories and category not in onlyCategories
                            ):
                                skipCategory = True
                            else:
                                data_block.setdefault(
                                    category, _dict()
                                )  # OrderedDict here preserves item order
                                table_names.append(item)
                    else:
                        if multiLineValue is True:
                            table_values.append((line[1 : line.rfind("\n;")]).strip())
                            multiLineValue = False
                            line = line[line.rfind("\n;") + 2 :]
                            if line.strip() != "":
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
                        data_block[category][item] = table_values_array[
                            val_index::num_item
                        ]
                    table_values_array = []
                if data_block != {}:
                    mmcif_like_file[data_heading] = data_block
            return mmcif_like_file
        except KeyError as key_err:
            print("KeyError [line %i]: %s" % (line_num, str(key_err)))
        except IOError as io_err:
            print("IOException [line %i]: %s" % (line_num, str(io_err)))


#        except StopIteration as gen_err:
#            print mmcif_like_file
#            print "StopIteration [line %i]: %s" % (line_num, str(gen_err))
