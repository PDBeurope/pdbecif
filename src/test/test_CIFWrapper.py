import sys
import unittest

from mmcif.mmcif import CIFWrapper, CIFWrapperTable

from .common import assert_equal

try:
    from collections import OrderedDict
except ImportError:
    # fallback: try to use the ordereddict backport when using python 2.6
    try:
        from ordereddict import OrderedDict
    except ImportError:
        # backport not installed: use local OrderedDict
        from mmCif.ordereddict import OrderedDict


class CIFWrapperTestCase(unittest.TestCase):
    def setUp(self):
        self.raw_dictionary = OrderedDict(
            (
                (
                    "TEST_BLOCK_1",
                    {
                        "_test_category_1": {
                            "test_value_1": 1,
                            "test_value_2": 2,
                            "test_value_3": 3,
                        },
                        "_test_category_2": {  # Loop/table
                            "test_value_1": [1, 2, 3, 4],
                            "test_value_2": ["Sleepy", "Dopey", "Bashful", "Grumpy"],
                            "test_value_3": [
                                "A ->\nLINE = A",
                                "B ->\nLINE = B",
                                "C ->\nLINE = C",
                                "D ->\nLINE = D",
                            ],
                        },
                    },
                ),
                ("TEST_BLOCK_2", {"_test_category_1": {"test_value_1": [1, 2, 3, 4]}}),
            )
        )

    def test_init_3_level_dictionary(self):
        """ preserve_token_order=True ensures deterministic unittests otherwise CIF data is random access """
        cif_wrapper = CIFWrapper(self.raw_dictionary, preserve_token_order=True)
        self.assertIsInstance(
            cif_wrapper,
            CIFWrapper,
            "Failed to instantiate CIFWrapper from 3-level mmCIF-like dictionary",
        )
        sys.stdout.write(cif_wrapper.data_id)
        self.assertEqual(
            cif_wrapper.data_id,
            "TEST_BLOCK_1",
            "'TEST_BLOCK_1' not set correctly as datablock ID",
        )

    def test_init_2_level_dictionary(self):
        cif_wrapper = CIFWrapper(
            self.raw_dictionary["TEST_BLOCK_1"], preserve_token_order=True
        )
        self.assertIsInstance(
            cif_wrapper,
            CIFWrapper,
            "Failed to instantiate CIFWrapper from 2-level mmCIF-like dictionary",
        )
        assert_equal(cif_wrapper.data_id, "", "datablock ID should be ''")

    def test_init_2_level_dictionary_new_id(self):
        cif_wrapper = CIFWrapper(
            self.raw_dictionary["TEST_BLOCK_2"], "NEW_ID", preserve_token_order=True
        )
        self.assertIsInstance(
            cif_wrapper,
            CIFWrapper,
            "Failed to instantiate CIFWrapper from 2-level mmCIF-like dictionary",
        )
        assert_equal(
            cif_wrapper.data_id, "NEW_ID", "'NEW_ID' not set correctly as datablock ID"
        )

    def test_wrapper_contains(self):
        cif_wrapper = CIFWrapper(
            self.raw_dictionary["TEST_BLOCK_2"], "NEW_ID", preserve_token_order=True
        )
        self.assertIsInstance(
            cif_wrapper,
            CIFWrapper,
            "Failed to instantiate CIFWrapper from 2-level mmCIF-like dictionary",
        )
        assert_equal(
            cif_wrapper.data_id, "NEW_ID", "'NEW_ID' not set correctly as datablock ID"
        )
        self.assertFalse("bogus" in cif_wrapper, "__contains__ not returning boolean")
        self.assertTrue(
            "_test_category_1" in cif_wrapper, "__contains__ not returning boolean"
        )

    def test_wrapper_getattr(self):
        cif_wrapper = CIFWrapper(
            self.raw_dictionary["TEST_BLOCK_2"], "NEW_ID", preserve_token_order=True
        )
        self.assertIsNone(
            cif_wrapper._bogus,
            "__getattr__ not returning None for uninitialized attribute",
        )
        self.assertIsInstance(
            cif_wrapper._test_category_1,
            CIFWrapperTable,
            "__getattr__ not returning CIFWrapperTable",
        )

    def test_wrapper_delItem(self):
        cif_wrapper = CIFWrapper(
            self.raw_dictionary["TEST_BLOCK_2"], "NEW_ID", preserve_token_order=True
        )
        self.assertIsNone(
            cif_wrapper._bogus,
            "__getattr__ not returning None for uninitialized attribute",
        )
        self.assertIsInstance(
            cif_wrapper._test_category_1,
            CIFWrapperTable,
            "__getattr__ not returning CIFWrapperTable",
        )
        del cif_wrapper["_test_category_1"]
        self.assertIsNone(
            cif_wrapper._test_category_1, "__delitem__ failed (dot notation)"
        )
        self.assertIsNone(
            cif_wrapper["_test_category_1"], "__delitem__ failed (dict notation)"
        )
        self.assertIsNone(
            cif_wrapper._DATA.get("_test_category_1", None),
            "__delitem__ failed (direct access)",
        )

    def test_unwrap(self):
        cif_wrapper = CIFWrapper(
            self.raw_dictionary["TEST_BLOCK_2"], "NEW_ID", preserve_token_order=True
        )
        assert_equal(
            cif_wrapper.unwrap(),
            {"NEW_ID": {"_test_category_1": {"test_value_1": [1, 2, 3, 4]}}},
            "CIFWrapper to dictionary conversion failed",
        )
        cif_wrapper = CIFWrapper(
            self.raw_dictionary["TEST_BLOCK_2"], preserve_token_order=True
        )
        for unique_id, data in list(cif_wrapper.unwrap().items()):
            self.assertNotEqual(unique_id, "", "No unique datablock id was assigned")
            assert_equal(
                data,
                {"_test_category_1": {"test_value_1": [1, 2, 3, 4]}},
                "CIFWrapper to dictionary conversion failed",
            )

    def test_listContents(self):
        cif_wrapper = CIFWrapper(
            self.raw_dictionary["TEST_BLOCK_1"], preserve_token_order=True
        )
        categories = cif_wrapper.contents()
        categories.sort()
        assert_equal(
            categories,
            ["_test_category_1", "_test_category_2"],
            "Item list for the category is incorrect",
        )


if __name__ == "__main__":
    unittest.main()
