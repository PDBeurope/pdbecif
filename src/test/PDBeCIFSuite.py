# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest

from test import (
    test_Item,
    test_DataBlock,
    test_SaveFrame,
    test_Category,
    test_CIFWrapper,
    test_CIFWrapperTable,
    test_CifFile,
    test_CifFileReader,
    test_CifFileIO,
)


@unittest.skip("This is not a unittest")
class PDBeCIFSuite(unittest.TestCase):
    def __init__(self, verbosity=0):
        self.verbosity = verbosity
        self._suite = self._create_test_suite()

    def _create_test_suite(self):
        loader = unittest.TestLoader()

        PDBeCIF_Suite = unittest.TestSuite()
        PDBeCIF_Suite = loader.loadTestsFromModule(test_Item)
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(test_Category))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(test_SaveFrame))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(test_DataBlock))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(test_CifFile))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(test_CIFWrapper))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(test_CIFWrapperTable))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(test_CifFileIO))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(test_CifFileReader))
        return PDBeCIF_Suite

    def _run(self):
        result = unittest.TextTestRunner(verbosity=self.verbosity).run(self._suite)

    def run_all_tests(self):
        self._run()


if __name__ == "__main__":
    suite = PDBeCIFSuite(verbosity=2)
    suite.run_all_tests()
