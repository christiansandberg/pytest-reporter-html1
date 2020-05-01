#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-reporter-html1',
    version='0.1.0',
    author='Christian Sandberg',
    author_email='christiansandberg@me.com',
    maintainer='Christian Sandberg',
    maintainer_email='christiansandberg@me.com',
    license='MIT',
    url='https://github.com/christiansandberg/pytest-reporter-html1',
    description='A basic HTML report template for Pytest',
    long_description=read('README.rst'),
    packages=find_packages(),
    package_data={'pytest_reporter_html1': ['templates/html1/*']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'pytest-reporter>=0.1.0',
        'Jinja2',
        'htmlmin',
        'docutils',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'reporter_html1 = pytest_reporter_html1.plugin',
        ],
    },
)
