import unittest
from mmCif import *

class  CategoryTestCase(unittest.TestCase):

    def setUp(self):
        self.cf = CifFile("test.cif")
        self.db = DataBlock("TEST", parent=self.cf)
        self.ct = Category("_foo", parent=self.db)
        str(self.ct)

#    def tearDown(self):
#        self.foo.dispose()
#        self.foo = None

    def test_getId(self):
        self.assertEquals(self.ct.getId(), "foo", "Could not get Category ID")

    def test_setItem(self):
        itm_1 = self.ct.setItem("bar")
        self.assertIsInstance(itm_1, Item, "setItem did not return Item")
        self.assertEqual(itm_1.id, "bar", "Item name not set correctly")

        itm_2 = Item("barfoo", self.ct)
        self.assertEqual(itm_2, self.ct.getItem("barfoo"), "Item not set by registration using object")

        itm_3 = self.ct.setItem(12345)
        self.assertIsNone(itm_3, "None expected but not returned")

        itm_4 = Item("bundy", parent=self.ct)
        itm_4.value = [0, 1, 2]
        self.ct.setItem(itm_4)
        self.assertIsInstance(itm_4, Item, "setItem did not return Item")

    def test_getItem(self):
        cat = self.ct.setItem("bar")
        self.assertIsInstance(self.ct.getItem("bar"), Item, "Get category did not return Item")
        self.assertEqual(cat, self.ct.getItem("bar"), "Item name not set correctly")

    def test_getItemNames(self):
        self.ct.setItem("bar")
        self.ct.setItem("barfoo")
        self.assertItemsEqual(["bar", "barfoo"], self.ct.getItemNames(), "getItemNames did not return expected values")

    def test_getItems(self):
        itm_1 = self.ct.setItem("bar")
        itm_2 = self.ct.setItem("barfoo")
        self.assertItemsEqual([itm_1, itm_2], self.ct.getItems(), "getItems did not return expected values")

    def test_remove(self):
        self.ct.remove()
        self.assertIsNone(self.db.categories.get("foo"), "did not remove Category as expected")
        self.assertIsNotNone(self.db.recycleBin.get("foo", None), "Category not moved to recycleBin as expected")
        self.assertEquals(self.db.recycleBin.get("foo"), self.ct, "Category expected in recycleBin but not found")

    def test_removeChildByString(self):
        msg = "Category.removeChild"

        itm_1 = self.ct.setItem("bar_removeChildByString")
        self.assertTrue(self.ct.removeChild("bar_removeChildByString"), msg+" did not return expected True")
        self.assertListEqual(self.ct.getItems(), [], msg+" items should be an empty list")
        self.assertIsInstance(self.ct.recycleBin.get("bar_removeChildByString"), Item, msg+" recycleBin should contain a Item instance")
        self.assertEquals(self.ct.recycleBin.get("bar_removeChildByString"), itm_1, msg+" recycleBin should contain the Item instance")

    def test_removeChildByObj(self):
        msg = "Category.removeChild"

        itm_1 = self.ct.setItem("bar_removeChildByObj")
        self.assertTrue(self.ct.removeChild(itm_1), msg+" did not return expected True")
        self.assertListEqual(self.ct.getItems(), [], msg+" items should be an empty list")
        self.assertIsInstance(self.ct.recycleBin.get("bar_removeChildByObj"), Item, msg+" recycleBin should contain a Item instance")
        self.assertEquals(self.ct.recycleBin.get("bar_removeChildByObj"), itm_1, msg+" recycleBin should contain the Item instance")

    def test_removeChildBadRef(self):
        msg = "Category.removeChild"
        self.ct.setItem("bar_removeChildBadRef")
        self.assertFalse(self.ct.removeChild("FAIL"), msg+" did not return expected False" )

if __name__ == '__main__':
    unittest.main()
