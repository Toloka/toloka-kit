#!/usr/bin/env python
# coding: utf8

import os

from setuptools import setup, find_packages

PREFIX = 'toloka'

setup_py_dir = os.path.dirname(__file__)
version_module_path = os.path.join(setup_py_dir, 'src', 'client', '__version__.py')
requirements_path = os.path.join(setup_py_dir, 'requirements.txt')
requirements_dev_path = os.path.join(setup_py_dir, 'requirements-dev.txt')

about = {}

with open(version_module_path) as f:
    exec(f.read(), about)

with open(requirements_path) as f:
    install_requires = f.read()

with open(requirements_dev_path) as f:
    install_requires_dev = f.read()

setup(
    name=about['__title__'],
    package_dir={PREFIX: 'src'},
    packages=[f'{PREFIX}.{package}' for package in find_packages('src')],
    version=about['__version__'],
    description='Toloka API client',
    license=about['__license__'],
    author='Vladimir Losev',
    author_email='losev@yandex-team.ru',
    python_requires='>=3.6.0',
    install_requires=install_requires,
    extras_require={'dev': install_requires_dev},
    include_package_data=True,
)
