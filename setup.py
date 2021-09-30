#!/usr/bin/env python
# coding: utf8

import os

from setuptools import setup, find_packages

PREFIX = 'toloka'

setup_py_dir = os.path.dirname(__file__)
version_module_path = os.path.join(setup_py_dir, 'src', '__version__.py')

about = {}

with open(version_module_path) as f:
    exec(f.read(), about)

with open('README.md') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    package_dir={PREFIX: 'src'},
    packages=['toloka', *(f'{PREFIX}.{package}' for package in find_packages('src'))],
    version=about['__version__'],
    description='Toloka API client',
    long_description=readme,
    long_description_content_type='text/markdown',
    license=about['__license__'],
    author='Vladimir Losev',
    author_email='losev@yandex-team.ru',
    python_requires='>=3.6.0',
    install_requires=[
        'attrs >= 20.3.0',
        'cattrs == 1.0.0 ; python_version < "3.7.0"',
        'cattrs >= 1.1.1; python_version >= "3.7.0"',
        'cached-property; python_version < "3.8.0"',
        'backports-datetime-fromisoformat; python_version < "3.7.0"',
        'requests',
        'urllib3',
        'pandas',
        'simplejson',
        'docstring-parser',
        'ipyplot',
        'jupyter-dash',
    ],
    extras_require={'dev': ['requests-mock']},
    include_package_data=True,
    project_urls={
        'Documentation': 'https://yandex.com/dev/toloka/toloka-kit/doc/',
        'Source': 'https://github.com/Toloka/toloka-kit',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Typing :: Typed',
    ],
)
