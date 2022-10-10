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

EXTRAS_REQUIRE = {
    'dev': ['requests-mock'],
    'pandas': ['pandas'],
    'autoquality': ['crowd-kit >= 1.0.0'],
    's3': ['boto3 >= 1.4.7'],
    'zookeeper': ['kazoo >= 2.6.1'],
    'jupyter-metrics': ['plotly', 'ipyplot', 'jupyter-dash'],
}
EXTRAS_REQUIRE['all'] = sum(EXTRAS_REQUIRE.values(), [])

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
    python_requires='>=3.7.0',
    install_requires=[
        'attrs >= 20.3.0',
        'cattrs >= 1.1.1, < 22.2.0',
        'cached-property; python_version < "3.8.0"',
        'filelock >= 3.2.0',
        'requests',
        'typing-extensions',
        'urllib3 >= 1.26.0',
        'simplejson',
        'docstring-parser',
        'tqdm',
    ],
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
    project_urls={
        'Documentation': 'https://toloka.ai/en/docs/toloka-kit',
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Typing :: Typed',
    ],
)
