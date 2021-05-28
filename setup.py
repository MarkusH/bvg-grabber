# -*- coding: utf-8 -*-
import codecs

from os import path
from setuptools import setup, find_packages

BASEDIR = path.dirname(__file__)

open = lambda filepath: codecs.open(filepath, 'r', 'utf-8')

description = open(path.join(BASEDIR, 'README.rst')).read()

setup(
    name='bvg-grabber',
    description='Querying the upcoming public transport departures in Berlin',
    long_description=description,
    version='0.2.1',
    url='https://github.com/MarkusH/bvg-grabber',
    author='Christian Struck, Markus Holtermann',
    author_email='info@markusholtermann.eu',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4>=4.4.1',
        'python-dateutil>=2.1',
        'requests>=1.2.3',
        'six>=1.3.0',
    ],
    test_suite="tests",
    scripts=['bvg-grabber.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
