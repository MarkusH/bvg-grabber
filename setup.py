# -*- coding: utf-8 -*-
import codecs
from os import path
from setuptools import setup, find_packages

BASEDIR = path.dirname(__file__)

open = lambda filepath: codecs.open(filepath, 'r', 'utf-8')

description = open(path.join(BASEDIR, 'README.rst')).read()
requirements = [line for line in open(path.join(BASEDIR, 'requirements.txt'))]

setup(
    name='bvg-grabber',
    description='Display the upcoming departures of buses and subways in Berlin, Germany',
    long_description=description,
    version='0.1a1',
    url='https://github.com/Markush2010/bvg-grabber',
    author='Christian Struck, Markus Holtermann',
    author_email='',
    license='BSD',
    packages=find_packages(exclude=['example', 'tests']),
    include_package_data=True,
    install_requires=requirements,
    test_suite="tests",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
