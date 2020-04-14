import unittest
from mmCif import *

class  ItemTestCase(unittest.TestCase):

    def setUp(self):
        self.cf = CifFile("test.cif", preserve_token_order=True)
        self.db = DataBlock("TEST", parent=self.cf)
        self.ct = Category("_foo", parent=self.db)
        self.im = Item("bar", parent=self.ct)
        str(self.im)
#    def tearDown(self):
#        self.foo.dispose()
#        self.foo = None

    def test_getItemName(self):
        self.assertEqual(self.im.getItemName(), "bar", "Could not get Item name")

    def test_setValue(self):
        self.im.setValue("val_1")
        self.assertEqual(self.im.value, "val_1", "Item value not set correctly")
        self.assertEqual(self.im.type, 'DEFAULTSTRING', "Item type not set correctly")
        self.assertEqual(self.im.isColumn, False, "Item isColumn not set correctly")

        self.im.setValue("val_2")
        self.assertEqual(self.im.value, ["val_1", "val_2"], "Item value not set correctly")
        self.assertEqual(self.im.type, ['DEFAULTSTRING', 'DEFAULTSTRING'], "Item type not set correctly")
        self.assertEqual(self.im.isColumn, True, "Item isColumn not set correctly")

    def test_getRawValue(self):
        self.im.value = None
        self.im.setValue("_val_3")
        self.assertEqual(self.im.getRawValue(), "_val_3", "T1: Item raw value not set correctly")

        self.im.setValue(""""val_4" test 4'""")
        self.assertEqual(self.im.getRawValue(), ['_val_3', '"val_4" test 4\''], "T2: Item raw value not set correctly")

        self.im.setValue(7357.73570)
        self.assertEqual(self.im.getRawValue(), ['_val_3', '"val_4" test 4\'', 7357.7357], "T3: Item raw value not set correctly")

        self.im.setValue("7357\n73570")
        self.assertEqual(self.im.getRawValue(), ['_val_3', '"val_4" test 4\'', 7357.7357, '7357\n73570'], "T4: Item raw value not set correctly")

    def test_non_ascii_quoted_properly(self):
        self.im.value = None
        self.im.setValue("α-alanine")
        self.assertEqual(self.im.getFormattedValue(),'"α-alanine"', " getFormattedValue not handling non-ascii properly")

    def test_getFormattedValue(self):
        self.im.value = None
        self.im.setValue("_val_3")
        self.assertEqual(self.im.getFormattedValue(), '"_val_3"', "T1: Item raw value not set correctly")

        self.im.setValue(""""val_4" test 4'""")
        self.assertEqual(self.im.getFormattedValue(), ['"_val_3"', '\n;"val_4" test 4\'\n;\n'], "T2: Item raw value not set correctly")

        self.im.setValue(7357.73570)
        self.assertEqual(self.im.getFormattedValue(), ['"_val_3"', '\n;"val_4" test 4\'\n;\n', '7357.7357'], "T3: Item raw value not set correctly")

        self.im.setValue("7357\n73570")
        self.assertEqual(self.im.getFormattedValue(), ['"_val_3"', '\n;"val_4" test 4\'\n;\n', '7357.7357', '\n;7357\n73570\n;\n'], "T4: Item raw value not set correctly")
        

        im_2 = Item('bogus', parent = self.ct)
        im_2.reset()
        im_2.value = None
        im_2.parent.isColumn = False
        im_2.isTable = False
        im_2.setValue(['X', ])
        im_2.getFormattedValue()
        im_2.value = '_val_"'
        im_2.getFormattedValue()
        im_2.value = "_val_'"
        im_2.getFormattedValue()
        im_2.value = '_val_ \n"'
        im_2.getFormattedValue()
        im_2.value = "_val_3 \n'"
        im_2.getFormattedValue()
        im_2.value = 'val \n"'
        im_2.getFormattedValue()
        im_2.value = "val \n'"
        im_2.getFormattedValue()
        im_2.remove()

    def test_remove(self):
        self.im.remove()
        self.assertIsNone(self.ct.items.get("bar"), "did not remove Item as expected")
        self.assertIsNotNone(self.ct.recycleBin.get("bar", None), "Item not moved to recycleBin as expected")
        self.assertEqual(self.ct.recycleBin.get("bar"), self.im, "Item expected in recycleBin but not found")

    def test_reset(self):
        self.im.setValue("val_1")
        self.im.reset()
        self.assertEqual(self.im.value, None, "Item values have not reset to None as expected")
        self.im.setValue("val_1")
        self.im.setValue("val_2")
        self.im.reset()
        self.assertEqual(self.im.value, [None, None], "Item values have not reset to None as expected")

if __name__ == '__main__':
    unittest.main()
