Examples
========

Example Usage with PyGame
-------------------------

..code-block:: python

    from taz.game import Game, Scene
    import pygame
    
    class MyScene(Scene):
        def __init__(self, identifier, color):
            super(MyScene, self).__init__(identifier)
    
            self.color = color
            self.screen = None
    
        def initialize(self):
            self.screen = self.game.render_context["screen"]
    
        def update(self):
            self.handle_inputs()
    
        def render(self):
            pygame.display.flip()
    
            self.screen.fill(self.color)
    
        def handle_inputs(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   raise Game.GameExitException
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if "Green" in self.identifier:
                            game.pop_scene_from_stack()
                        else:
                            game.push_scene_on_stack("Green-Scene")
    
    
    if __name__ == "__main__":
        pygame.init()
    
        update_context = {
        }
    
        render_context = {
                "screen": pygame.display.set_mode((800, 600))
        }
    
    
        game = Game(update_context, render_context)
    
        scene_one = MyScene("Red-Scene", pygame.Color("red"))
        scene_two = MyScene("Green-Scene", pygame.Color("green"))
        game.register_new_scene(scene_one)
        game.register_new_scene(scene_two)
    
        game.push_scene_on_stack("Red-Scene")
        game.enter_mainloop()



In this example two scenes are registered and the scene filling the background with the color red is pushed first. Upon pressing the "Return"-Key on the keyboard the "Green-Scene" is pushed to the game-stack and from then on its render and update methods are called. When Return is pressed again the scene pops itself from the stack. An example Use Case for this scenario would be the opening of an Options menu.


