# -*- coding: utf-8 -*-

"""
SeleniumTestability
"""

from os.path import abspath, dirname, join
from setuptools import setup, find_packages

LIBRARY_NAME = "SeleniumTestability"
CWD = abspath(dirname(__file__))
VERSION_PATH = join(CWD, 'src', LIBRARY_NAME, 'version.py')
exec(compile(open(VERSION_PATH).read(), VERSION_PATH, 'exec'))

with open(join(CWD, 'requirements.txt'), encoding="utf-8") as f:
    REQUIREMENTS = f.read().splitlines()

# Get the long description from the README file
with open(join(CWD, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

CLASSIFIERS = '''
Development Status :: 3 - Alpha
Topic :: Software Development :: Testing
Operating System :: OS Independent
License :: OSI Approved :: Apache Software License
Programming Language :: Python
Programming Language :: Python :: 3
Topic :: Software Development :: Testing
Framework :: Robot Framework
Framework :: Robot Framework :: Library
'''.strip().splitlines()

setup(
    name='robotframework-%s' % LIBRARY_NAME.lower(),
    version=VERSION,  # noqa: F821
    description='SeleniunTestability library that helps speed up tests with'
                'asyncronous evens',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/salabs/robotframework-%s' % LIBRARY_NAME.lower(),
    author='Jani Mikkonen',
    author_email='jani.mikkonen@siili.com',
    license='Apache License 2.0',
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    keywords='robot framework testing automation selenium seleniumlibrary'
             'testability async javascript softwaretesting',
    platforms='any',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['js/*.*']}
)
