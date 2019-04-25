#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='pwman',
    version='2.0.1',
    description='Manage Nginx basic auth files. Think htpasswd as lib. Writes SSHA hashes.',
    long_description=long_description,
    author='Felix Hummel',
    author_email='felix@felixhummel.de',
    maintainer='Felix Hummel',
    maintainer_email='felix@felixhummel.de',
    url='https://github.com/felixhummel/pwman',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=['docopt', 'passlib', 'six'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pwman = pwman.tool:main'
        ]
    }
)
