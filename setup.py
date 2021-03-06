#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='sassily',
      version='0.2',
      description='Management commands for using sass and Django together.',
      author='Russell Kyle',
      author_email='russell.j.kyle@gmail.com',
      url='http://russellkyle.com/sassily/',
      download_url='https://github.com/russelljk/sassily/archive/master.zip',
      packages=find_packages(),
      include_package_data=True,
      zip_safe = False,
      keywords=['Django', 'SASS', 'CSS']
)
