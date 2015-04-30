[![Travis-CI Build](https://travis-ci.org/mkli90/Taz.svg??style=flat-square&branch=master)](https://travis-ci.org/mkli90/Taz)
[![Coverage Status](https://coveralls.io/repos/mkli90/Taz/badge.svg?style=flat-square&branch=master)](https://coveralls.io/r/mkli90/Taz/badge.svg?branch=master)
[![PyPI version](https://badge.fury.io/py/tazlib.svg?style=flat-square)](http://badge.fury.io/py/tazlib)
[![Python Versions](https://img.shields.io/badge/python-2.7%2C%203.4-blue.svg?style=flat-square)](https://pypi.python.org/pypi/tazlib/1.0.0)
[![License](https://img.shields.io/badge/license-GPLv3-blue.svg?style=flat-square)](https://pypi.python.org/pypi/tazlib/1.0.0)
[![Code Health](https://landscape.io/github/mkli90/Taz/master/landscape.svg?style=flat-square)](https://landscape.io/github/mkli90/Taz/master)

# Taz: Game Loop and Scene Stack
This project is to aid people in getting started with their own Python based game.
Taz is a small library handling the switching of scenes and making sure your scenes get
updated and rendered on every tick.

The scenes will be organised in a game stack, which will automatically be updated
for all scenes whenever a new scene is registered with the Taz library. 
The user has the opportunity to force scene changes in pushing or popping from the game's
stack. Whenever the user pops the last stacked scene the game will come to an end.

Taz works independent of any python based game library.

# Documentation

To get to the documentation of Taz please follow this link:
http://taz.readthedocs.org/en/latest/

Documentation-Status: [![Documentation Status](https://readthedocs.org/projects/taz/badge/?version=latest)](https://readthedocs.org/projects/taz/?badge=latest)




