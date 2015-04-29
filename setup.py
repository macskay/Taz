#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

setup(name="Taz",
      version="1.0.0b1",
      description="Game Stack for managing Scenes",
      author="Max Klingmann <KlingmannM@gmail.com>",
      author_email="KlingmannM@gmail.com",
      packages=['taz'],
      license="GPLv3",
      url="https://github.com/mkli90/Taz",
      download_url = "https://github.com/mkli90/Taz/tarball/1.0.0",
      long_description="For a longer description see our GitHub-Page",
      package_data={
          'tmz': ['LICENSE']
      },
      classifiers=[
          "Intended Audience :: Developer",
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Natural Language :: English",
          "Programming Language :: Python :: 2.7",
          "Topic :: Games/Entertainment",
          "Topic :: Software Development :: Libraries",
      ],
)
