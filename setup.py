#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='happymongo',
    version='0.1',
    description=('Python module for making it easy and consistent to '
                 'connect to mongoDB via PyMongo either in Flask or in'
                 ' a non-flask application'),
    author='Matt Martz',
    author_email='matt@sivel.net',
    url='https://github.com/sivel/happymongo',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    install_requires=['pymongo']
)
