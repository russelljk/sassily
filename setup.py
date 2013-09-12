#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='sassily',
      version='0.1',
      description='Management commands for using sass and Django together.',
      author='Russell Kyle',
      author_email='russell.j.kyle@gmail.com',
      url='http://russellkyle.com/sassily/',
      download_url='https://github.com/russelljk/sassily/archive/master.zip',
      packages=['sassily'],
      include_package_data=True,
      keywords=['Django', 'SASS', 'CSS']
)
