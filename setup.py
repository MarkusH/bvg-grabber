import codecs
from os import path
from setuptools import setup, find_packages

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

setup(
	name='bvg-grabber',
	description='Display the upcoming departures of buses and subways in Berlin, Germany',
	long_description=read(path.join(path.dirname(__file__), 'README')),
	version='0.1a1',
	url='https://github.com/Markush2010/bvg-grabber',
	author='Christian Struck, Markus Holtermann',
	author_email='',
	license='BSD',
	packages=find_packages(exclude=['example']),
	include_package_data = True,
	classifiers = [
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
	],
)
