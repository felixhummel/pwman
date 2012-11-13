#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pwman',
      version='0.0.3',
      description='Simple command line client to manage nginx basic auth files. Think htpasswd (but not quite) as lib. Writes SSHA hashes.',
      author='Felix Hummel',
      author_email='felix@felixhummel.de',
      maintainer='Felix Hummel',
      maintainer_email='felix@felixhummel.de',
      url='http://felixhummel.de/pwman',
      package_dir = {'':'src'},
      packages=find_packages('src'),
      install_requires=['distribute', 'docopt', 'passlib'],
      entry_points = {
          'console_scripts': [
              'pwman = pwman.tool:main'
          ]
      }
)

