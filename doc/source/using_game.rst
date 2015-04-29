Using the "Game" class
======================
.. module:: taz.game

This sections is to present the Game class and its functionalities

What is the Game class
----------------------
The Game class is responsible for managing the scene stack
and running the game's main-loop. It is responsible for
calling the update- and render-functions of a scene and shuts down
the game if the last scene has been popped from the scene stack.

Instancing the Game class
-------------------------
To getting started with Taz you first have to create an object of
this class. The constructor takes two parameters, which are
the update_context and the render_context. The game passes
these contexts to the respective update- and render-function on each tick.
The contexts are represented as dictionaries holding specific items
you want every update- or render-function of your scenes to get on each tick.
You might be using the update_context to pass in the delta time or input events
for example. To see an example let's look at the following code block:

.. code-block:: python

    from taz import Game

    if __name__ == "__main__":
        update_context = {
            "input_fob" : sys.stdin
        }

        render_context = {
            "output_fob" : sys.stdout
        }

        game = Game(update_context, render_context)
        example_scene = ExampleScene("ExampleScene")
        game.register_new_scene(example_sccene)
        game.push_scene_on_stack("ExampleScene")
        game.enter_mainloop()
..

In this case the update and render context just hold the information which input and output to use. This method
is used in the integrationtest, which is represented as text-based adventure. So in this particular
example the render-function always writes to sys.stdout, while the update-function reads form sys.stdin.
You can setup these contexts to whatever needs you have in your application.

Registering scenes with the game
--------------------------------
Whenever a scene is created the game needs to know about it, thus is needs to be registered with the game.
The

<insert register scene here>

function gives you the possibility to register your scene object.
The registration of scenes needs to be done before the scene gets pushed to the stack, otherwise
a **Game.NoRegisteredSceneWithThisIDError** is raised.

Using the scene stack
---------------------
Using the scene stack is fairly simple. To push a scene on the you use the

<insert push function>

with the scene's identifier. Whenever a scene is pushed on the stack
its **initialize**- function is called. When you push a scene on top
another this scene gets paused.
To pop a scene you use the

<insert pop function>

Whenever you pop a scene, which is on top of another scene
that scene's **resume**-function is called in order to re-initiate
this scene.

When last scene of the stack is popped the game is closed.

Sharing data between all scenes
-------------------------------
TODO
