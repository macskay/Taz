__author__ = 'Max'


class Game(object):
    class GameStackEmptyError(Exception):
        def __init__(self):
            pass

    class NotAScenePushedOnStackError(Exception):
        def __init__(self):
            pass

    def __init__(self):
        self.scene_stack = []

    def is_stack_empty(self):
        return self.size_of_stack() == 0

    def size_of_stack(self):
        return len(self.scene_stack)

    def push_scene_on_stack(self, scene_to_push):
        if type(scene_to_push) is not Scene:
            raise Game.NotAScenePushedOnStackError
        self.scene_stack.insert(0, scene_to_push)

    def pop_scene_from_stack(self):
        if self.is_stack_empty():
            raise Game.GameStackEmptyError
        self.scene_stack.pop(0)

    def get_top_scene(self):
        return self.scene_stack[0]

    def get_name_of_top_scene(self):
        topscene = self.get_top_scene()
        return topscene.getIdentifier()

    # TODO: Register Scene


class Scene(object):
    def __init__(self, id):
        self.identifier = id

    def getIdentifier(self):
        return self.identifier

    # TODO: Initialize, Render, Update, Teardown

