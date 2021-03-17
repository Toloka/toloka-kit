#!/usr/bin/env python
# coding: utf8

import os

from setuptools import setup, find_packages

PREFIX = 'toloka'

setup_py_dir = os.path.dirname(__file__)
version_module_path = os.path.join(setup_py_dir, 'src', 'client', '__version__.py')

about = {}

with open(version_module_path) as f:
    exec(f.read(), about)

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
    install_requires=[
        'attrs >= 20.3.0',
        'cattrs == 1.0.0 ; python_version < "3.7.0"',
        'cattrs >= 1.1.1; python_version >= "3.7.0"',
        'backports-datetime-fromisoformat; python_version < "3.7.0"',
        'requests',
        'urllib3',
        'pandas',
        'simplejson',
    ],
    extras_require={'dev': ['requests-mock']},
    include_package_data=True,
)
