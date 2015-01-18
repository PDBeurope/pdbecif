# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest

from test import (
    ItemTest, 
    DataBlockTest, 
    SaveFrameTest, 
    CategoryTest, 
    CIFWrapperTest, 
    CIFWrapperTableTest, 
    CifFileTest, 
    CifFileReaderTest, 
    CifFileIOTest,
    )

@unittest.skip("This is not a unittest")
class PDBeCIFSuite(unittest.TestCase):
    
    def __init__(self, verbosity=0):
        self.verbosity = verbosity
        self._suite = self._create_test_suite()

    def _create_test_suite(self):
        loader = unittest.TestLoader()

        PDBeCIF_Suite = unittest.TestSuite()
        PDBeCIF_Suite = loader.loadTestsFromModule(ItemTest)
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(CategoryTest))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(SaveFrameTest))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(DataBlockTest))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(CifFileTest))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(CIFWrapperTest))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(CIFWrapperTableTest))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(CifFileIOTest))
        PDBeCIF_Suite.addTests(loader.loadTestsFromModule(CifFileReaderTest))
        return PDBeCIF_Suite 

    def _run(self):
        result = unittest.TextTestRunner(verbosity=self.verbosity).run(self._suite)

    def run_all_tests(self):
        self._run()

if __name__ == '__main__':
    suite = PDBeCIFSuite(verbosity=2)
    suite.run_all_tests()
    

