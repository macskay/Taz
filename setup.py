#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

setup(name="tazlib",
      version="1.0.0",
      description="Taz - Game Loop and Scene Stack Manager",
      author="Max Klingmann <KlingmannM@gmail.com>",
      author_email="KlingmannM@gmail.com",
      packages=['taz'],
      license="GPLv3",
      url="https://github.com/mkli90/Taz",
      download_url = "https://github.com/mkli90/Taz/tarball/1.0.0",
      long_description="http://taz.readthedocs.org/en/latest/index.html",
      package_data={
          'tmz': ['LICENSE']
      },
      classifiers=[
          "Intended Audience :: Developers",
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Natural Language :: English",
          "Programming Language :: Python :: 2.7",
          "Topic :: Games/Entertainment",
          "Topic :: Software Development :: Libraries",
      ],
)
