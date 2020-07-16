import unittest
from pdbecif.mmcif import CifFile, DataBlock, Category, SaveFrame
from .common import assert_equal


class DataBlockTestCase(unittest.TestCase):
    def setUp(self):
        self.cf = CifFile("test.cif", preserve_token_order=True)
        self.db = DataBlock("TEST", parent=self.cf)
        str(self.db)

    #    def tearDown(self):
    #        self.foo.dispose()
    #        self.foo = None

    def test_updateId(self):
        self.db.updateId("FOOBAR")
        self.assertEqual(self.db.id, "FOOBAR", "Could not change datablock ID")
        self.db.updateId("TEST")

    def test_getId(self):
        self.assertEqual(self.db.getId(), "TEST", "Could not get datablock ID")

    def test_setCategory(self):
        cat_1 = self.db.setCategory("_foo")
        self.assertIsInstance(cat_1, Category, "Set category did not return Category")
        self.assertEqual(cat_1.id, "foo", "Category name not set correctly")

        cat_2 = Category("_bar", self.db)
        self.assertEqual(
            cat_2,
            self.db.getCategory("_bar"),
            "Category not set by registration using object",
        )

        cat_3 = self.db.setCategory(Category("_bundy", self.db))
        self.assertIsInstance(cat_3, Category, "Set category did not return Category")

    def test_getCategory(self):
        cat = self.db.setCategory("_foo")
        self.assertIsInstance(
            self.db.getCategory("_foo"),
            Category,
            "Get category did not return Category",
        )
        self.assertEqual(
            cat, self.db.getCategory("_foo"), "Category name not set correctly"
        )

    def test_getCategoryIds(self):
        self.db.setCategory("_foo")
        self.db.setCategory("foo")
        self.db.setCategory("bar")

        categoryIds = self.db.getCategoryIds()

        self.assertEqual(
            "foo",
            categoryIds[0],
            "getCategoryIds did not return expected values - id as string",
        )
        self.assertEqual(
            "bar",
            categoryIds[1],
            "getCategoryIds did not return expected values - id as string",
        )

    def test_getCategories(self):
        foo = self.db.setCategory("_foo")
        self.db.setCategory("foo")
        bar = self.db.setCategory("bar")

        categories = self.db.getCategories()

        self.assertEqual(
            foo,
            categories[0],
            "getCategories did not return expected values - category as reference",
        )
        self.assertEqual(
            bar,
            categories[1],
            "getCategories did not return expected values - category as reference",
        )

    # SAVEFRAMES
    def test_setSaveFrame(self):
        save_1 = self.db.setSaveFrame("_foo")
        self.assertIsInstance(
            save_1, SaveFrame, "setSaveFrame did not return SaveFrame"
        )
        self.assertEqual(save_1.id, "_foo", "SaveFrame name not set correctly")

        save_2 = SaveFrame("_bar", self.db)
        self.assertEqual(
            save_2,
            self.db.getSaveFrame("_bar"),
            "SaveFrame not set by registration using object",
        )

        save_3 = self.db.setSaveFrame(SaveFrame("_bundy", self.db))
        self.assertIsInstance(
            save_3, SaveFrame, "setSaveFrame did not return SaveFrame"
        )

    def test_getSaveFrame(self):
        save = self.db.setSaveFrame("_foo")
        self.assertIsInstance(
            self.db.getSaveFrame("_foo"),
            SaveFrame,
            "getSaveFrame did not return SaveFrame",
        )
        self.assertEqual(
            save, self.db.getSaveFrame("_foo"), "SaveFrame name not set correctly"
        )

    def test_getSaveFrameIds(self):
        self.db.setSaveFrame("_foo")
        self.db.setSaveFrame("foo")
        self.db.setSaveFrame("bar")
        assert_equal(
            ["_foo", "foo", "bar"],
            self.db.getSaveFrameIds(),
            "getSaveFrameIds did not return expected values",
        )

    def test_getSaveFrames(self):
        _foo = self.db.setSaveFrame("_foo")
        foo = self.db.setSaveFrame("foo")
        bar = self.db.setSaveFrame("bar")
        assert_equal(
            [_foo, foo, bar],
            self.db.getSaveFrames(),
            "getSaveFrames did not return expected values",
        )

    def test_remove(self):
        self.db.remove()
        self.assertIsNone(
            self.cf.data_blocks.get("TEST"), "did not remove DataBlock as expected"
        )
        self.assertIsNotNone(
            self.cf.recycleBin.get("TEST", None),
            "DataBlock not moved to recycleBin as expected",
        )
        self.assertEqual(
            self.cf.recycleBin.get("TEST"),
            self.db,
            "DataBlock expected in recycleBin but not found",
        )

    def test_removeChildByString(self):
        msg = "DataBlock.removeChild"

        cat_foo = self.db.setCategory("foo")
        self.assertTrue(
            self.db.removeChild("foo"), msg + " did not return expected True"
        )
        self.assertListEqual(
            self.db.getCategories(), [], msg + " categories should be an empty list"
        )
        self.assertIsInstance(
            self.db.recycleBin.get("foo"),
            Category,
            msg + " recycleBin should contain a Category instance",
        )
        self.assertEqual(
            self.db.recycleBin.get("foo"),
            cat_foo,
            msg + " recycleBin should contain the Category instance",
        )

        save_bar = self.db.setSaveFrame("_bar")
        self.assertTrue(
            self.db.removeChild("_bar"), msg + " did not return expected True"
        )
        self.assertListEqual(
            self.db.getSaveFrames(), [], msg + " saveframes shoud be an empty list"
        )
        self.assertIsInstance(
            self.db.recycleBin.get("_bar"),
            SaveFrame,
            msg + " recycleBin should contain a SaveFrame instance",
        )
        self.assertEqual(
            self.db.recycleBin.get("_bar"),
            save_bar,
            msg + " recycleBin should contain the SaveFrame instance",
        )

    def test_removeChildByObj(self):
        msg = "DataBlock.removeChild"

        cat_foo = self.db.setCategory("_foo")
        self.assertTrue(
            self.db.removeChild(cat_foo), msg + " did not return expected True"
        )
        self.assertListEqual(
            self.db.getCategories(), [], msg + " categories should be an empty list"
        )
        self.assertIsInstance(
            self.db.recycleBin.get("foo"),
            Category,
            msg + " recycleBin should contain a Category instance",
        )
        self.assertEqual(
            self.db.recycleBin.get("foo"),
            cat_foo,
            msg + " recycleBin should contain the Category instance",
        )

        save_bar = self.db.setSaveFrame("_bar")
        self.assertTrue(
            self.db.removeChild(save_bar), msg + " did not return expected True"
        )
        self.assertListEqual(
            self.db.getSaveFrames(), [], msg + " saveframes should be an empty list"
        )
        self.assertIsInstance(
            self.db.recycleBin.get("_bar"),
            SaveFrame,
            msg + " recycleBin should contain a SaveFrame instance",
        )
        self.assertEqual(
            self.db.recycleBin.get("_bar"),
            save_bar,
            msg + " recycleBin should contain the SaveFrame instance",
        )

    def test_removeChildBadRef(self):
        msg = "DataBlock.removeChild"
        self.db.setCategory("foo")
        self.assertFalse(
            self.db.removeChild("FAIL"), msg + " did not return expected False"
        )


#    def test_removeChild(self):
#
#        cat_foo = self.db.setCategory("foo")
#        cat_bar = self.db.setCategory("bar")
#        self.assertIsInstance(self.db.getCategory("_foo"), Category, "Get category did not return Category (setCategory must have failed)")
#        self.assertEqual(cat_foo, self.db.getCategory("_foo"), "Category name not set correctly")
#
#        self.assertTrue(self.db.removeChild(cat_foo), "did not remove Category(given object) as expected")
#        self.assertTrue(self.db.removeChild(cat_bar.id), "did not remove Category(given string) as expected")
#        self.assertFalse(self.db.removeChild("foo_bar"), "did not False for removing dummy value as expected")
#        print self.db.categories
#        self.assertEquals(self.db.categories, {}, "did not return expected {} value for categories")
#        print self.db.recycleBin
#        self.assertEquals(self.db.recycleBin, {'foo': cat_foo, 'bar': cat_bar}, "removed categories were not moved to recycleBin")

if __name__ == "__main__":
    unittest.main()
