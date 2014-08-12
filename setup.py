#!/usr/bin/env python

import os
import re
import codecs

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


# Read the version number from a source file.
# Why read it, and not import?
# see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Get the long description from the relevant file
try:
    f = codecs.open('README.rst', encoding='utf-8')
    long_description = f.read()
    f.close()
except:
    long_description = ''

setup(
    name='happymongo',
    version=find_version('happymongo', '__init__.py'),
    description=('Python module for making it easy and consistent to '
                 'connect to MongoDB via PyMongo either in Flask or in'
                 ' a non-flask application'),
    long_description=long_description,
    author='Matt Martz',
    author_email='matt@sivel.net',
    url='https://github.com/sivel/happymongo',
    license='Apache License, Version 2.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['pymongo']
)
