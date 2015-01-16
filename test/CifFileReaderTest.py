import unittest

import os
from mmCif import *
import mmCif.mmcifIO as mmcif_IO

class  CifFileReaderTestCase(unittest.TestCase):

    def setUp(self):

        self.path = os.path.dirname(os.path.realpath(__file__))

    def test_inData_outDict(self):
        cfr = mmcif_IO.CifFileReader(input='data')
        cif_dictionary = cfr.read(self.path + "/../../../resources/usage-example.cif", output='cif_dictionary')
        self.assertIsInstance(cif_dictionary, dict, "Failed to create python dictionary from cif file")
        self.assertListEqual(cif_dictionary.keys(), ["TEST_CIF", "BLOCK_2"], "DataBlocks not read correctly")
        self.assertEqual(cif_dictionary["BLOCK_2"]["_extra"]["strange_value"], "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly")

    def test_inData_outWrap(self):
        cfr = mmcif_IO.CifFileReader(input='data')
        cif_wrapper = cfr.read(self.path + "/../../../resources/usage-example.cif", output='cif_wrapper')
        self.assertIsInstance(cif_wrapper["TEST_CIF"], CIFWrapper, "Failed to create CIFWrapper using lexical parser")
        self.assertListEqual(cif_wrapper.keys(), ["TEST_CIF", "BLOCK_2"], "DataBlocks not read correctly")
        self.assertEqual(cif_wrapper["BLOCK_2"]._extra.strange_value[0], "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly")

    def test_inData_outFile(self):
        cfr = mmcif_IO.CifFileReader(input='data')
        cif_file = cfr.read(self.path + "/../../../resources/usage-example.cif", output='cif_file')
        self.assertIsInstance(cif_file, CifFile, "Failed to create CifFile using algorithmic parser")
        self.assertListEqual(cif_file.getDataBlockIds(), ["TEST_CIF", "BLOCK_2"], "DataBlocks not read correctly")
        self.assertEqual(cif_file.getDataBlock("BLOCK_2").getCategory("_extra").getItem("strange_value").value,
            "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly")

    def test_inDict_outFile(self):
        cfr = mmcif_IO.CifFileReader(input='dictionary')
        cif_file = cfr.read(self.path + "/../../../resources/usage-example.cif", output='cif_file')
        self.assertIsInstance(cif_file, CifFile, "Failed to create CifFile using lexical parser")
        self.assertListEqual(cif_file.getDataBlockIds(), ["TEST_CIF", "BLOCK_2"], "DataBlocks not read correctly")
        self.assertEqual(cif_file.getDataBlock("BLOCK_2").getCategory("_extra").getItem("strange_value").value,
            "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly")

if __name__ == '__main__':
    unittest.main()
