# Welcome to Taz's documentation
This project is to aid people in getting started with their own Python based game.
Taz is a small library handling the switching of scenes and making sure your scenes get
updated and rendered on every tick.

The scenes will be organised in a game stack, which will automatically be updated
for all scenes whenever a new scene is registered with the Taz library. 
The user has the opportunity to force scene changes in pushing or popping from the game's
stack. Whenever the user pops the last stacked scene the game will come to an end.

Taz works independent of any python based game library.

Master-Branch: ![Travis-CI Build](https://travis-ci.org/mkli90/Taz.svg?branch=master)

To get to the documentation of Taz please follow this link:
http://taz.readthedocs.org/en/latest/

Documentation: [![Documentation Status](https://readthedocs.org/projects/taz/badge/?version=latest)](https://readthedocs.org/projects/taz/?badge=latest)




