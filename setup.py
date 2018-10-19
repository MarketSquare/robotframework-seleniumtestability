#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SeleniumTestability
"""

import codecs
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

LIBRARY_NAME = 'SeleniumTestability'
CWD = abspath(dirname(__file__))
VERSION_PATH = join(CWD, 'src', LIBRARY_NAME, 'version.py')
exec(compile(open(VERSION_PATH).read(), VERSION_PATH, 'exec'))

with codecs.open(join(CWD, 'README.md'), encoding='utf-8') as reader:
    LONG_DESCRIPTION = reader.read()

setup(
    name='robotframework-%s' % LIBRARY_NAME.lower(),
    version=VERSION,
    description='SeleniunTestability library that helps speed up tests with'
                'asyncronous evens',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/omenia/robotframework-%s' % LIBRARY_NAME.lower(),
    author='Jani Mikkonen',
    author_email='jani.mikkonen@siili.com',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Robot Framework',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    keywords='robot framework testing automation selenium seleniumlibrary'
             'testability async javascript softwaretesting',
    platforms='any',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['selenium >= 2.46.1', 'robotframework-seleniumlibrary >= 3.2.0']
)
