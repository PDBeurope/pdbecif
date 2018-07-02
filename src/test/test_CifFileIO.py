import unittest

import os
from mmCif import *
from mmCif.mmcifIO import CifFileReader, CifFileWriter

class  CifFileIOTestCase(unittest.TestCase):

    def setUp(self):
        self.FILE_ROOT = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.dirname(os.path.join(self.FILE_ROOT, '..', '..', '..'))
        self.TEST_CIF_FILE = os.path.join(self.path, "data/usage-example.cif")
        self.TEST_DIC_FILE = os.path.join(self.path, "data/usage-example.dic")
        self.raw_dictionary = {
            'TEST_BLOCK_1': {
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
            },
            'TEST_BLOCK_2': {
                '_test_category_1': {
                    'test_value_1': [1, 2, 3, 4]
                }
            }
        }

    # Compares two unsorted lists
    def __assertListEqual(self, l1, l2, msg):
        l1.sort()
        l2.sort()

        return self.assertListEqual(l1, l2, msg)

    def tearDown(self):
        from glob import glob
        for file in glob(os.path.join(self.FILE_ROOT, 'io_testcase*')):
            os.unlink(file)

    def test_inData_outDict(self):
        cfr = CifFileReader(input='data', preserve_order=True)
        cif_dictionary = cfr.read(self.TEST_CIF_FILE, output='cif_dictionary')
        self.assertIsInstance(cif_dictionary, dict, "Failed to create python dictionary from cif file")
        self.__assertListEqual(list(cif_dictionary.keys()), ["TEST_CIF", "BLOCK_2"], "DataBlocks not read correctly")
        self.assertEqual(cif_dictionary["BLOCK_2"]["_extra"]["strange_value"], "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly")

    def test_inData_outWrap(self):
        cfr = CifFileReader(input='data', preserve_order=True)
        cif_wrapper = cfr.read(self.TEST_CIF_FILE, output='cif_wrapper')
        self.assertIsInstance(cif_wrapper["TEST_CIF"], CIFWrapper, "Failed to create CIFWrapper using lexical parser")
        self.__assertListEqual(list(cif_wrapper.keys()), ["TEST_CIF", "BLOCK_2"], "DataBlocks not read correctly")
        self.assertEqual(cif_wrapper["BLOCK_2"]._extra.strange_value[0], "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly")

    def test_inData_outFile(self):
        cfr = CifFileReader(input='data', preserve_order=True)
        cif_file = cfr.read(self.TEST_CIF_FILE, output='cif_file')
        self.assertIsInstance(cif_file, CifFile, "Failed to create CifFile using algorithmic parser")
        self.__assertListEqual(cif_file.getDataBlockIds(), ["TEST_CIF", "BLOCK_2"], "DataBlocks not read correctly")
        self.assertEqual(cif_file.getDataBlock("BLOCK_2").getCategory("_extra").getItem("strange_value").value,
            "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly")

    def test_inDict_outFile(self):
        cfr = CifFileReader(input='dictionary', preserve_order=True)
        cif_file = cfr.read(self.TEST_CIF_FILE, output='cif_file')
        self.assertIsInstance(cif_file, CifFile, "Failed to create CifFile using lexical parser")
        self.__assertListEqual(cif_file.getDataBlockIds(), ["TEST_CIF", "BLOCK_2"], "DataBlocks not read correctly")
        self.assertEqual(cif_file.getDataBlock("BLOCK_2").getCategory("_extra").getItem("strange_value").value,
            "Three#Blind#Mice",
            "All levels of CIF file not translated to dictionary correctly")

    def test_ignoreCategories(self):
        cfr = CifFileReader(input='data', preserve_order=True)
        cif_file = cfr.read(self.TEST_CIF_FILE, output='cif_file', ignore=['_test_loop_2', '_valid_CIF'])
        self.assertIsInstance(cif_file, CifFile, "Failed to create CifFile using algorithmic parser")
        self.__assertListEqual(cif_file.getDataBlockIds(), ["TEST_CIF", "BLOCK_2"], "DataBlocks not read correctly")
        categories_A = cif_file.getDataBlock("TEST_CIF").getCategoryIds()
        categories_A.sort()
        self.assertEqual(categories_A,
            ['test_keyword', 'test_loop_1', 'valid_cif'],
            "Categories were not ignored correctly")
        categories_B = cif_file.getDataBlock("BLOCK_2").getCategoryIds()
        categories_B.sort()
        self.assertEqual(categories_B,
            ['equivalence_test', 'extra'],
            "Categories were not ignored correctly")

    def test_openGzipError(self):
        with self.assertRaises(TypeError):
            cfw = CifFileWriter(file_path=9999)
        
    def test_write_ciffile_after_ciffile_dictionary_import(self):
        # Test write CifFile initialized by dictionary
        unit_test_file = "io_testcase_1.cif"
        cfw = CifFileWriter()
        cif_file = CifFile(os.path.join(self.FILE_ROOT, unit_test_file))
        cif_file.import_mmcif_data_map(self.raw_dictionary)
        cfw.write(cif_file)
        cfr = CifFileReader(input='data', preserve_order=True)
        test_file = cfr.read(os.path.join(self.FILE_ROOT, unit_test_file), output='cif_wrapper')
        data_block_ids = list(test_file.keys())
        data_block_ids.sort()
        self.assertEqual(data_block_ids,
            ['TEST_BLOCK_1', 'TEST_BLOCK_2'],
            "Datablock(s) were not written correctly")
        self.assertEqual(test_file['TEST_BLOCK_1']._test_category_2.test_value_1,
            ['1', '2', '3', '4'],
            "mmCIF data  was not written correctly")


    def test_write_ciffile_after_cifwrapper_dictionary_import(self):
        # Test write CifFile initialized by CIFWrapper and dictionary import
        unit_test_file = "io_testcase_2.cif"
        cfw = CifFileWriter(file_path=os.path.join(self.FILE_ROOT, unit_test_file))
        cif_obj = dict((k, CIFWrapper(v, preserve_token_order=True))
                       for k, v in list(self.raw_dictionary.items()))
        cif_wrapper = CIFWrapper(
            {'TEST_BLOCK_1': self.raw_dictionary['TEST_BLOCK_1']}, preserve_token_order=True)
        cfw.write(cif_wrapper)
        cif_wrapper = CIFWrapper(
            {'TEST_BLOCK_2': self.raw_dictionary['TEST_BLOCK_2']}, preserve_token_order=True)
        cfw.write(cif_wrapper)
        del cfw
        cfr = CifFileReader(input='data', preserve_order=True)
        test_file = cfr.read(os.path.join(self.FILE_ROOT, unit_test_file), output='cif_wrapper')
        data_block_ids = list(test_file.keys())
        data_block_ids.sort()
        self.assertEqual(data_block_ids,
            ['TEST_BLOCK_1', 'TEST_BLOCK_2'],
            "Datablock(s) were not written correctly")
        self.assertEqual(test_file['TEST_BLOCK_1']._test_category_2.test_value_1,
            ['1', '2', '3', '4'],
            "mmCIF data  was not written correctly")

    def test_write_raw_dictionary_with_block_id(self):
        unit_test_file = "io_testcase_3.cif"
        # Test raw dictionary (WITH datablock id)
        cfw = CifFileWriter(file_path=os.path.join(self.FILE_ROOT, unit_test_file))
        cfw.write(self.raw_dictionary)
        del cfw
        cfr = CifFileReader(input='data', preserve_order=True)
        test_file = cfr.read(os.path.join(self.FILE_ROOT, unit_test_file), output='cif_wrapper')
        data_block_ids = list(test_file.keys())
        data_block_ids.sort()
        self.assertEqual(data_block_ids,
            ['TEST_BLOCK_1', 'TEST_BLOCK_2'],
            "Datablock(s) were not written correctly")
        self.assertEqual(test_file['TEST_BLOCK_1']._test_category_2.test_value_1,
            ['1', '2', '3', '4'],
            "mmCIF data  was not written correctly")

    def test_write_raw_dictionary_without_block_id(self):
        unit_test_file = "io_testcase_4.cif"
        # Test raw dictionary (WITHOUT datablock id)
        cfw = CifFileWriter(file_path=os.path.join(self.FILE_ROOT, unit_test_file))
        cfw.write(self.raw_dictionary['TEST_BLOCK_1'])
        del cfw
        cfr = CifFileReader(input='data', preserve_order=True)
        test_file = cfr.read(os.path.join(self.FILE_ROOT, unit_test_file), output='cif_wrapper')
        data_block_ids = list(test_file.keys())
        data_block_ids.sort()
        self.assertEqual(data_block_ids,
            [unit_test_file,],
            "Datablock(s) were not written correctly")
        self.assertEqual(test_file[unit_test_file]._test_category_2.test_value_1,
            ['1', '2', '3', '4'],
            "mmCIF data  was not written correctly")

    def test_write_mmCIF_dictionary(self):
        unit_test_file = "io_testcase_5.cif"
        cfr = CifFileReader(input='dictionary', preserve_order=True)
        cif_file = cfr.read(self.TEST_DIC_FILE, output='cif_file')
        cfw = CifFileWriter(file_path=os.path.join(self.FILE_ROOT, unit_test_file))
        cfw.write(cif_file)
        test_file = cfr.read(os.path.join(self.FILE_ROOT, unit_test_file), output='cif_file')
        test_value = test_file.getDataBlock('TEST')\
            .getSaveFrame('some_interesting_category')\
            .getCategory('category')\
            .getItem('mandatory_code')\
            .value
        self.assertEqual(test_value, 'no', 'mmCIF dictionary file was not written correctly')





if __name__ == '__main__':
    unittest.main()
