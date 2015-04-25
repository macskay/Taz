# Welcome to Taz's documentation
This project is to aid people in getting started with their own Python based game.
Taz is a small library handling the switching of scenes and making sure your scenes get
updated and rendered on every tick.

The scenes will be organised in a game stack, which will automatically be updated
for all scenes whenever a new scene is registered with the Taz library. 
The user has the opportunity to force scene changes in pushing or popping from the game's
stack. Whenever the user pops the last stacked scene the game will come to an end.

Taz works independent of any python based game library.

# Usage

Learning to use Taz is nothing to be afraid of and pretty easy indeed.
All what has to be done is creating a subclass of the class Scene and registering it with the game's stack.

```python
from Taz import Game, Scene

render_context = {
	"screen": screen
	}

update_context = {
	"clock": clock,
	"get_events": get_events,
	"pump": pump
	}
	
class SubScene(Scene):
	def initialize_scene(self):
        return

    def resume(self):
        return

    def tear_down(self):
        return

    def update(self, update_context):
        return

    def render(self, render_context):
        return
	
	
if __name__ = "__main__":
	game = Game(update_context, render_context)
	my_first_scene = SubScene("MyFirstScene")
	game.register_new_scene(scene1)
	game.push_scene_on_stack("MyFirstScene")
```

After importing Taz into the program's code, the `render_context`and `update_context` ought to be set. In these two dictionaries you put any attribute, which your `update`- and `render`-function should get on each tick. An example for this would the `deltatime` since the last tick inside the `update_context`. The next step is to create a new subclass of `Scene` and all its abstract methods. The abstract methods, which all subclasses have to implement are `initialize_scene`, `tear_down`, `resume`, `update(update_context)` and `render(render_context)`. To build a new instance of the subclass you wrote you need to pass a string-identifier to the object's parameter on creation. In this example the identifier is `"MyFirstScene"`. Every time the scene should be pushed to the game's stack the string identifier is used to call it. After creating a new scene object it has to be registered (`game.register_new_scene(scene1)`) with the game, before you can push it onto the game's stack. After you've done that you can successfully push your new scene onto the using the identifier you chose for the scene (`game.push_scene_on_stack("MyFirstScene")`). Now your program is ready to launch.

The top scene of the stack is always the active scene, meaning it is the current scene to be updated and rendered by the program's mainloop. Every scene is aware of all registered scene's and is able to switch between them in using either `push_scene_on_stack("SceneName")` or `pop_scene_from_stack()`. Whenever a scene is pushed onto the stack the current scene's `paused`  is set to `True`, whereas the new scene's `paused` is set to `False`. When a scene is popped of the stack it does not get destroyed. It is still initialized in the game's `registered_scenes` dictionary, so it is still possible to push it back onto the game's stack by using the identifier of the scene.

