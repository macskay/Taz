#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from setuptools import setup

setup(name="Taz",
      version="1.0.0",
      description="Game Stack for managing Scenes",
      author="Max Klingmann <KlingmannM@gmail.com>",
      author_email="KlingmannM@gmail.com",
      packages=['taz'],
      license="GPLv3",
      url="https://github.com/mkli90/Taz",
      long_description="For a longer description see our GitHub-Page",
      package_data={
          'tmz': ['LICENSE', 'README.md']
      },
      classifiers=[
          "Intended Audience :: Developer",
          "Development Status :: 1.0.0",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Programming Language :: Python :: 2.7.x",
          "Topic :: Games/Entertainment",
          "Topic :: Software Development :: Libraries",
      ],
)