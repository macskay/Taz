# -*- encoding: UTF-8 -*-
from abc import ABCMeta, abstractmethod
import sys


class Game(object):
    """
    This class is the main game class.
    It contains the stack with all registered scenes and is managing the game loop.
    """
    class GameExitException(Exception):
        def __init__(self):
            sys.exit(0)

    class StackEmptyError(Exception):
        pass

    class SceneAlreadyRegisteredError(Exception):
        pass

    class NoRegisteredSceneWithThisIDError(Exception):
        pass

    def __init__(self, update_context, render_context):
        """
        :param update_context: This update_context is passed to the update-function of all scenes
        :param render_context: This render_context is passed to the render-function of all scenes

        To construct an instance of this class, a update_context
        and a render_context, depending on the used underlying
        engine is used. To ensure functionality call the base class' constructor when overriding the __init__-function.
        """
        self.scene_stack = []
        self.registered_scenes = {}

        self.update_context = update_context
        self.render_context = render_context

    def enter_mainloop(self):
        try:
            while True:
                self.get_top_scene().update()
                self.get_top_scene().render()
        except SystemExit:
            pass

    def register_new_scene(self, scene):
        """
        :param scene: This is the scene, which should get registered with the game
        :raises Game.SceneAlreadyRegisteredError: If a scene is registered multiple times an error is raised.

        Before a scene can be pushed on the game's stack it must be registered with the game.
        This method should be called right after a scene has been created.
        """
        if self.is_scene_already_registered(scene):
            raise Game.SceneAlreadyRegisteredError

        scene.game = self
        self.registered_scenes[scene.get_identifier()] = scene
        self.update_all_scenes()

    def is_scene_already_registered(self, scene):
        for scene_name in self.registered_scenes:
            if scene_name == scene.get_identifier():
                return True
        return False

    def update_all_scenes(self):
        for scene in self.registered_scenes.items():
            scene[1].registered_scenes = self.registered_scenes

    def size_of_stack(self):
        return len(self.scene_stack)

    def push_scene_on_stack(self, ident):
        """
        :param ident: This is the string-identifier of the scene.
        :raises Game.NoRegisteredSceneWithThisIDError: If the scene given hasn't been registered with the game this \
        function raises an error.

        This function pushes a given scene to the stack. The scene is given by its identifier and must have
        been registered with the game before it can be pushed on top of the state.
        """
        try:
            self.push_the_scene(ident)
        except KeyError:
            raise Game.NoRegisteredSceneWithThisIDError

    def pop_scene_from_stack(self):
        """
        :raises Game.StackEmptyError: If the stack is empty and this function is called an error is raised.
        :raises Game.GameExitException: If the last item of the active stack is popped an GameExitException is raised \
        and the game is shut down.

        This scene is used pop the current scene from the game's stack. When this is called,
        the scene's tear_down function will get called in order to destroy the scene.
        If the popped scene was on top of another scene, the other scene's resume-function is called,
        to re-initiate the state of this scene.
        """
        if self.is_stack_empty():
            raise Game.StackEmptyError
        if self.pop_last_scene():
            raise Game.GameExitException

        self.destroy_old_scene(self.scene_stack[0])
        self.scene_stack.pop(0)
        self.resume_new_scene(self.scene_stack[0])

    def push_the_scene(self, ident):
        self.pause_current_scene()
        scene_to_push = self.registered_scenes[ident]
        scene_to_push.paused = False
        scene_to_push.initialize_scene()
        self.scene_stack.insert(0, scene_to_push)

    def pause_current_scene(self):
        if not self.is_stack_empty():
            self.scene_stack[0].paused = True
            self.scene_stack[0].pause()

    def is_stack_empty(self):
        return self.size_of_stack() == 0

    def pop_last_scene(self):
        return self.size_of_stack() == 1

    @staticmethod
    def destroy_old_scene(oldscene):
        oldscene.paused = True
        oldscene.pause()

    @staticmethod
    def resume_new_scene(newscene):
        newscene.paused = False
        newscene.resume()

    def get_name_of_top_scene(self):
        topscene = self.get_top_scene()
        return topscene.get_identifier()

    def get_top_scene(self):
        if self.is_stack_empty():
            raise Game.StackEmptyError

        return self.scene_stack[0]


class Scene(object):
    """
    This is the abstract base class of all scenes.
    All Scenes must be derived from this and override the abstract methods.
    On each tick the render and update functions are called. They get passed the update_context and render_context
    passed to the Game object on creation.
    """
    __metaclass__ = ABCMeta

    def __init__(self, ident):
        """
        When creating an instance of this class a string-identifier must be passed to the constructor in order
        to be able to call the function through the game stack and identify it in the game's registered scenes.
        :param ident: This is the string-identifier of the Scene
        :return:
        """
        self.game = None

        self.identifier = ident
        self.paused = False
        self.registered_scenes = {}

    def get_identifier(self):
        """
        :return: This returns the string-identifier associated with this object
        """
        return self.identifier

    def is_paused(self):
        return self.paused

    @abstractmethod  # pragma: no cover
    def initialize_scene(self):
        """ This method builds up the scene """

    @abstractmethod  # pragma: no cover
    def update(self):
        """ This method updates the game's logic """

    @abstractmethod  # pragma: no cover
    def render(self):
        """ This method draws the game's screen """

    @abstractmethod  # pragma: no cover
    def tear_down(self):
        """ This method cleans up the scene before destroying it """

    @abstractmethod  # pragma: no cover
    def resume(self):
        """ This re-builds the state before pausing it (e.g. after returning from an options menu) """

    @abstractmethod  # pragma: no cover
    def pause(self):
        """  This function is called whenever a scene is pushed on top of the active one """