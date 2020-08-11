#!/usr/bin/python3

import os.path
import pkgconfig
import sys
from Cython.Build import cythonize
from setuptools import setup, Extension


if pkgconfig.installed("picnic", ">=3.0.1"):
    flags = pkgconfig.parse("picnic")
    define_macros = flags["define_macros"]
    include_dirs = flags["include_dirs"]
    library_dirs = flags["library_dirs"]
    libraries = list(flags["libraries"])
else:
    raise EnvironmentError("Required picnic version not available")


def read(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return f.read()


setup(
    name="python-picnic",
    version="1.0",
    description="Python bindings for picnic",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Sebastian Ramacher",
    author_email="sebastian.ramacher@ait.ac.at",
    url="https://github.com/sebastinas/python-picnic",
    license="Expat",
    ext_modules=cythonize(
        [
            Extension(
                "picnic._picnic",
                ["picnic/_picnic.pyx"],
                define_macros=define_macros,
                include_dirs=include_dirs,
                library_dirs=library_dirs,
                libraries=libraries,
            )
        ],
        language_level=3,
    ),
    packages=["picnic"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
    ],
    test_suite="picnic.tests",
    setup_requires=["pkgconfig", "cython >= 0.28"],
)
