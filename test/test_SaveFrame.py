import unittest
from pdbecif.mmcif import CifFile, DataBlock, SaveFrame, Category


class SaveFrameTestCase(unittest.TestCase):
    def setUp(self):
        self.cf = CifFile("test.cif", preserve_token_order=True)
        self.db = DataBlock("TEST", parent=self.cf)
        self.sf = SaveFrame("_saveframe.test", parent=self.db)
        str(self.sf)

    #    def tearDown(self):
    #        self.foo.dispose()
    #        self.foo = None

    def test_updateId(self):
        self.sf.updateId("FOOBAR")
        self.assertEqual(self.sf.id, "FOOBAR", "Could not change saveframe ID")
        self.sf.updateId("_saveframe.test")

    def test_getId(self):
        self.assertEqual(
            self.sf.getId(), "_saveframe.test", "Could not get saveframe ID"
        )

    def test_setCategory(self):
        cat_1 = self.sf.setCategory("_foo")
        self.assertIsInstance(cat_1, Category, "Set category did not return Category")
        self.assertEqual(cat_1.id, "foo", "Category name not set correctly")

        cat_2 = Category("_bar", self.sf)
        self.assertEqual(
            cat_2,
            self.sf.getCategory("_bar"),
            "Category not set by registration using object",
        )

        cat_3 = self.sf.setCategory(Category("_bundy", self.sf))
        self.assertIsInstance(cat_3, Category, "Set category did not return Category")

    def test_getCategory(self):
        cat = self.sf.setCategory("_foo")
        self.assertIsInstance(
            self.sf.getCategory("_foo"),
            Category,
            "Get category did not return Category",
        )
        self.assertEqual(
            cat, self.sf.getCategory("_foo"), "Category name not set correctly"
        )

    def test_getCategoryIds(self):
        self.sf.setCategory("_foo")
        self.sf.setCategory("foo")
        self.sf.setCategory("bar")

        categories = self.sf.getCategoryIds()

        self.assertEqual(
            "foo",
            categories[0],
            "getCategoryIds did not return expected values - id as string",
        )
        self.assertEqual(
            "bar",
            categories[1],
            "getCategoryIds did not return expected values - id as string",
        )

    def test_getCategories(self):
        foo = self.sf.setCategory("_foo")
        self.sf.setCategory("foo")
        bar = self.sf.setCategory("bar")

        categories = self.sf.getCategories()

        self.assertEqual(
            foo,
            categories[0],
            "getCategories did not return expected values - id as reference",
        )
        self.assertEqual(
            bar,
            categories[1],
            "getCategories did not return expected values - id as reference",
        )

    def test_remove(self):
        self.sf.remove()
        self.assertIsNone(
            self.db.saveFrames.get("_saveframe.test"),
            "did not remove SaveFrame as expected",
        )
        self.assertIsNotNone(
            self.db.recycleBin.get("_saveframe.test", None),
            "SaveFrame not moved to recycleBin as expected",
        )
        self.assertEqual(
            self.db.recycleBin.get("_saveframe.test"),
            self.sf,
            "SaveFrame expected in recycleBin but not found",
        )

    def test_removeChildByString(self):
        msg = "SaveFrame.removeChild"

        cat_foo = self.sf.setCategory("foo")
        self.assertTrue(
            self.sf.removeChild("foo"), msg + " did not return expected True"
        )
        self.assertListEqual(
            self.sf.getCategories(), [], msg + " categories should be an empty list"
        )
        self.assertIsInstance(
            self.sf.recycleBin.get("foo"),
            Category,
            msg + " recycleBin should contain a Category instance",
        )
        self.assertEqual(
            self.sf.recycleBin.get("foo"),
            cat_foo,
            msg + " recycleBin should contain the Category instance",
        )

    def test_removeChildByObj(self):
        msg = "SaveFrame.removeChild"

        cat_foo = self.sf.setCategory("_foo")
        self.assertTrue(
            self.sf.removeChild(cat_foo), msg + " did not return expected True"
        )
        self.assertListEqual(
            self.sf.getCategories(), [], msg + " categories should be an empty list"
        )
        self.assertIsInstance(
            self.sf.recycleBin.get("foo"),
            Category,
            msg + " recycleBin should contain a Category instance",
        )
        self.assertEqual(
            self.sf.recycleBin.get("foo"),
            cat_foo,
            msg + " recycleBin should contain the Category instance",
        )

    def test_removeChildBadRef(self):
        msg = "SaveFrame.removeChild"
        self.sf.setCategory("foo")
        self.assertFalse(
            self.sf.removeChild("FAIL"), msg + " did not return expected False"
        )


if __name__ == "__main__":
    unittest.main()
