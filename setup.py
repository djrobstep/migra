#!/usr/bin/env python

import io

from setuptools import setup, find_packages

readme = io.open('README.rst').read()

setup(
    name='migra',
    version='0.1.1470919406',
    url='https://github.com/djrobstep/migra',
    description='Like diff but for PostgreSQL schemas',
    long_description=readme,
    author='Robert Lechte',
    author_email='robertlechte@gmail.com',
    install_requires=[
        'sqlbag',
        'six',
        'schemainspect'
    ],
    zip_safe=False,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha'
    ],
    entry_points={
        'console_scripts': [
            'migra = migra:do_command',
        ],
    },
    extras_require={'pg': ['psycopg2']}
)
