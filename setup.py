#!/usr/bin/env python

import setuptools

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name='happymongo',
    version='0.1.1',
    description=('Python module for making it easy and consistent to '
                 'connect to MongoDB via PyMongo either in Flask or in'
                 ' a non-flask application'),
    long_description=long_description,
    author='Matt Martz',
    author_email='matt@sivel.net',
    url='https://github.com/sivel/happymongo',
    license='Apache License, Version 2.0',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    install_requires=['pymongo']
)
