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
    use_scm_version=True,
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
    python_requires='>=3.5',
    setup_requires=['setuptools_scm'],
    install_requires=[
        'pytest-reporter>=0.3.0',
        'Jinja2',
        'ansi2html>=1.3.0',
        'htmlmin',
        'docutils',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Topic :: Text Processing :: Markup :: HTML',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'reporter_html1 = pytest_reporter_html1.plugin',
        ],
    },
)
