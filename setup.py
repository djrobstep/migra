#!/usr/bin/env python
import io

from setuptools import setup, find_packages

readme = io.open("README.md").read()
setup(
    name="migra",
    version="1.0.1535509978",
    url="https://github.com/djrobstep/migra",
    description="Like diff but for PostgreSQL schemas",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Robert Lechte",
    author_email="robertlechte@gmail.com",
    install_requires=["sqlbag", "six", "schemainspect"],
    zip_safe=False,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={"console_scripts": ["migra = migra:do_command"]},
    extras_require={"pg": ["psycopg2-binary"]},
)
