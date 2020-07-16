import unittest
from pdbecif.mmcif import CifFile, DataBlock, Category, Item
from .common import assert_equal


class CategoryTestCase(unittest.TestCase):
    def setUp(self):
        self.cf = CifFile("test.cif", preserve_token_order=True)
        self.db = DataBlock("TEST", parent=self.cf)
        self.ct = Category("_foo", parent=self.db)
        str(self.ct)

    #    def tearDown(self):
    #        self.foo.dispose()
    #        self.foo = None

    def test_getId(self):
        self.assertEqual(self.ct.getId(), "foo", "Could not get Category ID")

    def test_setItem(self):
        itm_1 = self.ct.setItem("bar")
        self.assertIsInstance(itm_1, Item, "setItem did not return Item")
        self.assertEqual(itm_1.id, "bar", "Item name not set correctly")

        itm_2 = Item("barfoo", self.ct)
        self.assertEqual(
            itm_2,
            self.ct.getItem("barfoo"),
            "Item not set by registration using object",
        )

        itm_3 = self.ct.setItem(12345)
        self.assertIsNone(itm_3, "None expected but not returned")

        itm_4 = Item("bundy", parent=self.ct)
        itm_4.value = [0, 1, 2]
        self.ct.setItem(itm_4)
        self.assertIsInstance(itm_4, Item, "setItem did not return Item")

    def test_getItem(self):
        cat = self.ct.setItem("bar")
        self.assertIsInstance(
            self.ct.getItem("bar"), Item, "Get category did not return Item"
        )
        self.assertEqual(cat, self.ct.getItem("bar"), "Item name not set correctly")

    def test_getItemNames(self):
        self.ct.setItem("bar")
        self.ct.setItem("barfoo")
        itemNames = self.ct.getItemNames()
        self.assertEqual(
            "bar",
            itemNames[0],
            "getItemNames did not return expected values - item names as string",
        )
        self.assertEqual(
            "barfoo",
            itemNames[1],
            "getItemNames did not return expected values - item names as string",
        )

    def test_getItems(self):
        itm_1 = self.ct.setItem("bar")
        itm_2 = self.ct.setItem("barfoo")
        items = self.ct.getItems()

        self.assertEqual(
            itm_1,
            items[0],
            "getItems did not return expected values - items by reference",
        )
        self.assertEqual(
            itm_2,
            items[1],
            "getItems did not return expected values - items by reference",
        )

    def test_remove(self):
        self.ct.remove()
        self.assertIsNone(
            self.db.categories.get("foo"), "did not remove Category as expected"
        )
        self.assertIsNotNone(
            self.db.recycleBin.get("foo", None),
            "Category not moved to recycleBin as expected",
        )
        self.assertEqual(
            self.db.recycleBin.get("foo"),
            self.ct,
            "Category expected in recycleBin but not found",
        )

    def test_removeChildByString(self):
        msg = "Category.removeChild"

        itm_1 = self.ct.setItem("bar_removeChildByString")
        self.assertTrue(
            self.ct.removeChild("bar_removeChildByString"),
            msg + " did not return expected True",
        )
        assert_equal(self.ct.getItems(), [], msg + " items should be an empty list")
        self.assertIsInstance(
            self.ct.recycleBin.get("bar_removeChildByString"),
            Item,
            msg + " recycleBin should contain a Item instance",
        )
        self.assertEqual(
            self.ct.recycleBin.get("bar_removeChildByString"),
            itm_1,
            msg + " recycleBin should contain the Item instance",
        )

    def test_removeChildByObj(self):
        msg = "Category.removeChild"

        itm_1 = self.ct.setItem("bar_removeChildByObj")
        self.assertTrue(
            self.ct.removeChild(itm_1), msg + " did not return expected True"
        )
        assert_equal(self.ct.getItems(), [], msg + " items should be an empty list")
        self.assertIsInstance(
            self.ct.recycleBin.get("bar_removeChildByObj"),
            Item,
            msg + " recycleBin should contain a Item instance",
        )
        self.assertEqual(
            self.ct.recycleBin.get("bar_removeChildByObj"),
            itm_1,
            msg + " recycleBin should contain the Item instance",
        )

    def test_removeChildBadRef(self):
        msg = "Category.removeChild"
        self.ct.setItem("bar_removeChildBadRef")
        self.assertFalse(
            self.ct.removeChild("FAIL"), msg + " did not return expected False"
        )


if __name__ == "__main__":
    unittest.main()
