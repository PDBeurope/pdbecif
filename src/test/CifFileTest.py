import unittest
from mmCif import *

class  CifFileTestCase(unittest.TestCase):

    def setUp(self):
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
        self.cf = CifFile()

#    def tearDown(self):
#        self.foo.dispose()
#        self.foo = None

    def test_setDataBlock(self):
        db = self.cf.setDataBlock("TEST")
        self.assertIsInstance(db, DataBlock, "CifFile.setDataBlock created an invalid object")
        db2 = self.cf.setDataBlock(DataBlock("TEST", parent=self.cf))
        self.assertIsInstance(db2, DataBlock, "CifFile.setDataBlock created an invalid object")

    def test_registerChild(self):
        db = DataBlock("TEST", self.cf)
        self.assertIsInstance(self.cf.getDataBlock("TEST"), DataBlock, "CifFile.getDataBlock returned an invalid object")

    def test_getDataBlock(self):
        self.cf.setDataBlock("TEST")
        self.assertIsInstance(self.cf.getDataBlock("TEST"), DataBlock, "CifFile.getDataBlock returned an invalid object")

    def test_getDataBlockIds(self):
        self.cf.setDataBlock("TEST")
        msg = "CifFile.getDataBlockIds returned incorrect list of DataBlock IDs"
        self.assertListEqual(self.cf.getDataBlockIds(), ["TEST",], msg)

    def test_getDataBlocks(self):
        db = self.cf.setDataBlock("TEST")
        msg = "CifFile.getDataBlocks returned incorrect list of DataBlocks"
        self.assertListEqual(self.cf.getDataBlocks(), [db,], msg)

    def test_removeChildByString(self):
        db = self.cf.setDataBlock("TEST")
        msg = "CifFile.removeChild"
        self.assertTrue(self.cf.removeChild("TEST"), msg+" did not return expected True")
        self.assertListEqual(self.cf.getDataBlocks(), [], msg+" datablocks should be an empty list")
        self.assertIsInstance(self.cf.recycleBin.get("TEST"), DataBlock, msg+" recyclebin should contain a DataBlock instance")
        self.assertEquals(self.cf.recycleBin.get("TEST"), db, msg+" recyclebin should contain the datablock instance")

    def test_removeChildByObj(self):
        db = self.cf.setDataBlock("TEST")
        msg = "CifFile.removeChild"
        self.assertTrue(self.cf.removeChild(db), msg+" did not return expected True")
        self.assertListEqual(self.cf.getDataBlocks(), [], msg+" datablocks should be an empty list")
        self.assertIsInstance(self.cf.recycleBin.get("TEST"), DataBlock, msg+" recyclebin should contain a DataBlock instance")
        self.assertEquals(self.cf.recycleBin.get("TEST"), db, msg+" recyclebin should contain the datablock instance")

    def test_removeChildBadRef(self):
        self.cf.setDataBlock("TEST")
        msg = "CifFile.removeChild"
        self.assertFalse(self.cf.removeChild("FAIL"), msg+" did not return expected False" )

    def test_dictionaryImport(self):
        cf = CifFile()
        cf.import_mmcif_data_map(self.raw_dictionary)
        self.assertIsNotNone(cf.getDataBlock('TEST_BLOCK_2'), "CifFile failed to import dictionary")
        self.assertIsInstance(cf.getDataBlock('TEST_BLOCK_2'), DataBlock, "CifFile.__init__ failed to import dictionary")
        self.assertEqual(cf.getDataBlock('TEST_BLOCK_2'
            ).getCategory('_test_category_1'
            ).getItem('test_value_1'
            ).value, [1, 2, 3, 4], "CifFile failed to import dictionary")
            
    def test_initializeWithDictionary(self):
        cf = CifFile(mmcif_data_map=self.raw_dictionary)
        
        self.assertIsInstance(cf, CifFile, "CifFile.__init__ failed to import dictionary")
        self.assertIsNotNone(cf.getDataBlock('TEST_BLOCK_2'), "CifFile.__init__ failed to import dictionary")
        self.assertEqual(cf.getDataBlock('TEST_BLOCK_2'
            ).getCategory('_test_category_1'
            ).getItem('test_value_1'
            ).value, [1, 2, 3, 4], "CifFile.__init__ failed to import dictionary")
        cf = CifFile(mmcif_data_map={})

if __name__ == '__main__':
    unittest.main()
