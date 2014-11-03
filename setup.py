# -*- coding: utf-8 -*
"""
Setup script for beehive.

USAGE:
    python setup.py install
    python setup.py beehive_test     # -- XFAIL on Windows (currently).
    python setup.py nosetests
"""

import sys
import os.path

HERE0 = os.path.dirname(__file__) or os.curdir
os.chdir(HERE0)
HERE = os.curdir
sys.path.insert(0, HERE)

from setuptools import find_packages, setup
from setuptools_beehive import beehive_test

# -----------------------------------------------------------------------------
# CONFIGURATION:
# -----------------------------------------------------------------------------
python_version = float("%s.%s" % sys.version_info[:2])
requirements = ["parse>=1.6.3"]
if python_version < 2.7 or 3.0 <= python_version <= 3.1:
    requirements.append("argparse")
if python_version < 2.7:
    requirements.append("ordereddict")
if python_version < 2.6:
    requirements.append("simplejson")

BEEHIVE = os.path.join(HERE, "beehive")
README = os.path.join(HERE, "README.md")
description = "".join(open(README).readlines()[4:])


# -----------------------------------------------------------------------------
# UTILITY:
# -----------------------------------------------------------------------------
def find_packages_by_root_package(where):
    """
    Better than excluding everything that is not needed,
    collect only what is needed.
    """
    root_package = os.path.basename(where)
    packages = ["%s.%s" % (root_package, sub_package)
                for sub_package in find_packages(where)]
    packages.insert(0, root_package)
    return packages


# -----------------------------------------------------------------------------
# SETUP:
# -----------------------------------------------------------------------------
setup(
    name="beehive",
    version="1.1",
    description="beehive is behaviour-driven development, Python style",
    long_description=description,
    author="Benno Rice, Richard Jones, Jens Engel, Vadim Rutkovsky",
    author_email="roignac@gmail.com",
    url="http://github.com/vrutkovs/beehive",
    provides=["beehive", "setuptools_beehive"],
    packages=find_packages_by_root_package(BEEHIVE),
    py_modules=["setuptools_beehive"],
    entry_points={
        "console_scripts": [
            "beehive = beehive.__main__:main"
        ],
        "distutils.commands": [
            "beehive_test = setuptools_beehive:beehive_test"
        ]
    },
    install_requires=requirements,
    test_suite="nose.collector",
    tests_require=["nose>=1.3", "mock>=1.0", "PyHamcrest>=1.8"],
    cmdclass={
        "beehive_test": beehive_test,
    },
    use_2to3=bool(python_version >= 3.0),
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: Jython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: BSD License",
    ],
)
