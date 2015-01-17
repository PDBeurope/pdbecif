__author__ = "Glen van Ginkel (Protein Data Bank in Europe; http://pdbe.org)"
__date__ = "$17-Aug-2013 12:39:18$"

import os
from setuptools import setup, find_packages

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup (
        name='PDBeCif',
        version='1.2.0',
        author='Glen van Ginkel (Protein Data Bank in Europe; PDBe)',
        author_email='pdbe@ebi.ac.uk',
        packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
        include_package_data=True,
        package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md'],
        },
        scripts=[],
        url='http://pypi.python.org/pypi/PDBeCIF/',
        license='../LICENSE',
        description='A lightweight pure python package for reading, writing and manipulating mmCIF files distributed by the wwPDB',
        long_description=read('../README.md'),
        classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        ],
        keywords='STAR CIF mmCIF PDB PDBe parsing parser API',
        test_suite='../test',
        install_requires=[],
       )
