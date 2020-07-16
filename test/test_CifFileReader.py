import os
import unittest

import pdbecif
import pdbecif.mmcif_io as mmcif_IO
from pdbecif.mmcif import CifFile, CIFWrapper


class CifFileReaderTestCase(unittest.TestCase):
    def setUp(self):

        self.FILE_ROOT = os.path.dirname(os.path.dirname(pdbecif.__file__))
        self.TEST_CIF_FILE = os.path.join(self.FILE_ROOT, "data/usage-example.cif")
        self.TEST_DIC_FILE = os.path.join(self.FILE_ROOT, "data/usage-example.dic")

    def __assertEqual(self, l1, l2, msg):
        if isinstance(l1, list):
            l1.sort()
        if isinstance(l2, list):
            l2.sort()

        return self.assertEqual(l1, l2, msg)

    def test_inData_outDict(self):
        cfr = mmcif_IO.CifFileReader(input="data", preserve_order=True)
        cif_dictionary = cfr.read(self.TEST_CIF_FILE, output="cif_dictionary")
        self.assertIsInstance(
            cif_dictionary, dict, "Failed to create python dictionary from cif file"
        )
        self.__assertEqual(
            list(cif_dictionary.keys()),
            ["TEST_CIF", "BLOCK_2"],
            "DataBlocks not read correctly",
        )
        self.__assertEqual(
            cif_dictionary["BLOCK_2"]["_extra"]["strange_value"],
            "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly",
        )

    def test_inData_outWrap(self):
        cfr = mmcif_IO.CifFileReader(input="data", preserve_order=True)
        cif_wrapper = cfr.read(self.TEST_CIF_FILE, output="cif_wrapper")
        self.assertIsInstance(
            cif_wrapper["TEST_CIF"],
            CIFWrapper,
            "Failed to create CIFWrapper using lexical parser",
        )
        self.__assertEqual(
            list(cif_wrapper.keys()),
            ["TEST_CIF", "BLOCK_2"],
            "DataBlocks not read correctly",
        )
        self.__assertEqual(
            cif_wrapper["BLOCK_2"]._extra.strange_value[0],
            "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly",
        )

    def test_inData_outFile(self):
        cfr = mmcif_IO.CifFileReader(input="data", preserve_order=True)
        cif_file = cfr.read(self.TEST_CIF_FILE, output="cif_file")
        self.assertIsInstance(
            cif_file, CifFile, "Failed to create CifFile using algorithmic parser"
        )
        self.__assertEqual(
            cif_file.getDataBlockIds(),
            ["TEST_CIF", "BLOCK_2"],
            "DataBlocks not read correctly",
        )
        self.__assertEqual(
            cif_file.getDataBlock("BLOCK_2")
            .getCategory("_extra")
            .getItem("strange_value")
            .value,
            "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly",
        )

    def test_inDict_outFile(self):
        cfr = mmcif_IO.CifFileReader(input="dictionary", preserve_order=True)
        cif_file = cfr.read(self.TEST_CIF_FILE, output="cif_file")
        self.assertIsInstance(
            cif_file, CifFile, "Failed to create CifFile using lexical parser"
        )
        self.__assertEqual(
            cif_file.getDataBlockIds(),
            ["TEST_CIF", "BLOCK_2"],
            "DataBlocks not read correctly",
        )
        self.__assertEqual(
            cif_file.getDataBlock("BLOCK_2")
            .getCategory("_extra")
            .getItem("strange_value")
            .value,
            "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly",
        )


if __name__ == "__main__":
    unittest.main()
