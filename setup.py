__author__ = "Glen van Ginkel (Protein Data Bank in Europe; http://pdbe.org)"
__date__ = "$17-Aug-2013 12:39:18$"

import os

import pdbecif
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="PDBeCif",
    version=pdbecif.__version__,
    author="Glen van Ginkel (Protein Data Bank in Europe; PDBe)",
    author_email="pdbe@ebi.ac.uk",
    test_suite="test",
    include_package_data=True,
    setup_requires=["pytest-runner"],
    tests_require=["tox", "pytest>=3.2", "pytest-cov"],
    package_dir = {'': 'src'},
        packages = find_packages(
            'src',
            exclude = [
                '*.test',
                '*.test.*',
                'test.*',
                'test',
                ]),    scripts=[],
    url="http://pypi.python.org/pypi/PDBeCIF/",
    # license=read("LICENSE"),
    description="A lightweight pure python package for reading, writing and manipulating mmCIF files distributed by the wwPDB.",
    project_urls={
        "Source code": "https://github.com/PDBeurope/pdbecif",
        "Documentation": "https://pdbeurope.github.io/pdbecif/",
    },
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="STAR CIF mmCIF PDB PDBe parsing parser API",
    install_requires=[],
)
