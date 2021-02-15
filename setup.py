#!/usr/bin/python3

import pkgconfig
from setuptools import setup, Extension

if pkgconfig.installed("picnic", ">=3.0.1"):
    flags = pkgconfig.parse("picnic")
    define_macros = flags["define_macros"]
    include_dirs = flags["include_dirs"]
    library_dirs = flags["library_dirs"]
    libraries = flags["libraries"]
else:
    raise EnvironmentError("Required picnic version not available")

ext_modules = [
    Extension(
        "picnic._picnic",
        ["picnic/_picnic.pyx"],
        define_macros=define_macros,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
    )
]


setup(
    ext_modules=ext_modules,
    packages=["picnic"],
    package_data={
        "picnic": ["_picnic.pyi", "py.typed"]
    },
    test_suite="picnic.tests",
)
