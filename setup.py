__author__ = "Glen van Ginkel (Protein Data Bank in Europe; http://pdbe.org)"
__date__ = "$17-Aug-2013 12:39:18$"

import os
from setuptools import setup, find_packages

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup (
        name='PDBeCif',
        version='1.3.5',
        author='Glen van Ginkel (Protein Data Bank in Europe; PDBe)',
        author_email='pdbe@ebi.ac.uk',
        package_dir = {'': 'src'},
        packages = find_packages(
            'src',
            exclude = [
                '*.test',
                '*.test.*',
                'test.*',
                'test',
                ]),
        test_suite = 'test',
      	include_package_data=True,
        setup_requires=['pytest-runner'],
        tests_require=[
            'pytest>=3.2',
            'pytest-cov',
        ],
        package_data={
            '': [
                '*.txt',
                '*.rst',
                '*.md',
            ],
            'test': [
                'data/usage-example.cif',
                'data/usage-example.dic',
            ],
        },
        scripts=[],
        url='http://pypi.python.org/pypi/PDBeCIF/',
        license=read('LICENSE'),
        description='A lightweight pure python package for reading, writing and manipulating mmCIF files distributed by the wwPDB',
        long_description=read('README.md'),
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Operating System :: Unix",
            "Operating System :: MacOS",
            "Operating System :: POSIX",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Topic :: Scientific/Engineering :: Bio-Informatics",
        ],
        keywords='STAR CIF mmCIF PDB PDBe parsing parser API',
        install_requires=[],
       )
