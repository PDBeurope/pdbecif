# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest

import CifFileTest
import DataBlockTest
import SaveFrameTest
import CategoryTest
import CIFWrapperTest
import CIFWrapperTableTest
import CifFileReaderTest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    PDBeCIF_Suite = loader.loadTestsFromModule(CifFileTest)
    PDBeCIF_Suite.addTests(loader.loadTestsFromModule(DataBlockTest))
    PDBeCIF_Suite.addTests(loader.loadTestsFromModule(SaveFrameTest))
    PDBeCIF_Suite.addTests(loader.loadTestsFromModule(CategoryTest))
    PDBeCIF_Suite.addTests(loader.loadTestsFromModule(CIFWrapperTest))
    PDBeCIF_Suite.addTests(loader.loadTestsFromModule(CIFWrapperTableTest))
    PDBeCIF_Suite.addTests(loader.loadTestsFromModule(CifFileReaderTest))
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(PDBeCIF_Suite)
