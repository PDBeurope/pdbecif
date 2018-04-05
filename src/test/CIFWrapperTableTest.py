import unittest

from mmCif import CIFWrapper, CIFWrapperTable

class  CIFWrapperTableTestCase(unittest.TestCase):

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

#    def tearDown(self):
#        self.foo.dispose()
#        self.foo = None


    def test_wrapperTableContains(self):
        cif_wrapper = CIFWrapper(self.raw_dictionary['TEST_BLOCK_2'], "NEW_ID")
        self.assertIsInstance(cif_wrapper, CIFWrapper, "Failed to instantiate CIFWrapper from 2-level mmCIF-like dictionary")
        self.assertEqual(cif_wrapper.data_id, "NEW_ID", "'NEW_ID' not set correctly as datablock ID")
        self.assertFalse('bogus' in cif_wrapper, "CIFWrapper.__contains__ not returning boolean")
        self.assertTrue('_test_category_1' in cif_wrapper, "CIFWrapper.__contains__ not returning boolean")
        test_category_1 = cif_wrapper._test_category_1

        self.assertFalse('bogus' in test_category_1, "CIFWrapperTable.__contains__ not returning boolean")
        self.assertTrue('test_value_1' in test_category_1, "CIFWrapperTable.__contains__ not returning boolean")

    def test_delitem(self):
        cif_wrapper = CIFWrapper(self.raw_dictionary['TEST_BLOCK_1'])
        del cif_wrapper._test_category_2['test_value_2']
        self.assertFalse('test_value_2' in cif_wrapper._test_category_2, "Failed to delete item from category")
        columns = list([k for k in cif_wrapper._test_category_2][0].keys())
        columns.sort()
        self.assertEqual(columns, ['test_value_1', 'test_value_3'], "item deletion failed or gave inconsistent results")


#    def test_wrapperTable_getattr(self):
#        cif_wrapper = CIFWrapper(self.raw_dictionary['TEST_BLOCK_2'], "NEW_ID")
#        # dot notation access
#        test_category_1 = cif_wrapper._test_category_1
#        self.assertIsInstance(test_category_1, CIFWrapperTable, "(Dot access) Failed to instantiate CIFWrapperTable")
#        self.assertIsNone(test_category_1.bogus, "(Dot access) Missing item request failed to return None")
#        # dictionary-like access
#        test_category_1 = cif_wrapper.__getitem__("_test_category_1") # []
#        self.assertIsInstance(test_category_1, CIFWrapperTable, "(Dict access) Failed to instantiate CIFWrapperTable")
#        self.assertIsNone(test_category_1.bogus, "(Dict access) Missing item request failed to return None")

    def test_wrapperTable_getattr(self):
        cif_wrapper = CIFWrapper(self.raw_dictionary['TEST_BLOCK_2'], "NEW_ID")
#        # dot notation access
        cif_wrapper._test_category_1.test_value_3 = "Bundy"
        self.assertEqual(cif_wrapper._test_category_1['test_value_3'], ["Bundy",], "Dot-notation attribute setting failed to overwrite or gave inconsistent results")
        self.assertEqual(cif_wrapper._test_category_1.test_value_3, ["Bundy",], "Dot-notation attribute setting failed to overwrite or gave inconsistent results")



    def test_wrapperTable_setattr_setitem(self):
        cif_wrapper = CIFWrapper(self.raw_dictionary['TEST_BLOCK_2'], "NEW_ID")
#        # dot notation access
        cif_wrapper._test_category_1['test_value_2'] = ['a', 'b', 'c', 'd']
        self.assertEqual(cif_wrapper._test_category_1['test_value_2'], ['a', 'b', 'c', 'd'], "Conventional attribute setter failed or gave inconsistent results")
        cif_wrapper._test_category_1['test_value_2'] = "FOO"
        self.assertEqual(cif_wrapper._test_category_1['test_value_2'], ["FOO",], "Attribute setter failed to overwrite or gave inconsistent results")
        cif_wrapper._test_category_1.test_value_3 = "Bundy"
        self.assertEqual(cif_wrapper._test_category_1['test_value_3'], ["Bundy",], "Dot-notation attribute setting failed to overwrite or gave inconsistent results")

    def test_iter(self):
        cif_wrapper = CIFWrapper(self.raw_dictionary['TEST_BLOCK_1'])
        rows_in = [ {'test_value_3': 'A ->\nLINE = A', 'test_value_2': 'Sleepy', 'test_value_1': 1},
            {'test_value_3': 'B ->\nLINE = B', 'test_value_2': 'Dopey', 'test_value_1': 2},
            {'test_value_3': 'C ->\nLINE = C', 'test_value_2': 'Bashful', 'test_value_1': 3},
            {'test_value_3': 'D ->\nLINE = D', 'test_value_2': 'Grumpy', 'test_value_1': 4}
        ]
        rows_out = [row for row in cif_wrapper._test_category_2]
        self.assertEqual(rows_out, rows_in, "Row iteration failed or gave inconsistent results")

    def test_search(self):
        cif_wrapper = CIFWrapper(self.raw_dictionary['TEST_BLOCK_1'])
        check_row = {'test_value_3': 'C ->\nLINE = C', 'test_value_2': 'Bashful', 'test_value_1': 3}
        result = cif_wrapper._test_category_2.search('test_value_1', 3)
        self.assertEqual(result[2], check_row, "Category search failed or gave inconsistent results")

    def test_searchIter(self):
        cif_wrapper = CIFWrapper(self.raw_dictionary['TEST_BLOCK_1'])
        check_row = {'test_value_3': 'C ->\nLINE = C', 'test_value_2': 'Bashful', 'test_value_1': 3}
        result = [row for row in cif_wrapper._test_category_2.searchiter('test_value_1', 3)]
        self.assertEqual(result[0], check_row, "Row iteration failed or gave inconsistent results")

    def test_listContents(self):
        cif_wrapper = CIFWrapper(self.raw_dictionary['TEST_BLOCK_1'])
        items = cif_wrapper._test_category_1.contents()
        items.sort()
        self.assertEqual(items, ['test_value_1', 'test_value_2', 'test_value_3'], "Item list for the category is incorrect")


if __name__ == '__main__':
    unittest.main()
