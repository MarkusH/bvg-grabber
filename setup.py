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
    version='0.1.0',
    url='https://github.com/Markush2010/bvg-grabber',
    author='Christian Struck, Markus Holtermann',
    author_email='',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'beautifulsoup4>=4.2.1',
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
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
