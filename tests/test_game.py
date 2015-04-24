__author__ = 'Max'

from unittest import TestCase
from taz.game import Game, GameStackEmptyError, Scene, NotAScenePushedOnStackError


class TestGame(TestCase):
    def setUp(self):
        self.game = Game()
        self.sceneone = Scene("TestScene1")
        self.scenetwo = Scene("TestScene2")

    def test_if_stack_is_empty(self):
        self.assertTrue(self.game.is_stack_empty())

    def test_if_pushed_one_scene_size_of_stack_should_be_one(self):
        self.game.push_scene_on_stack(self.sceneone)
        self.assertEqual(self.game.size_of_stack(), 1)

    def test_if_pushed_one_scene_top_scene_should_be_one(self):
        self.game.push_scene_on_stack(self.sceneone)
        self.assertEqual(self.game.get_top_scene(), self.sceneone)

    def test_if_pushed_two_scene_top_scene_should_be_two(self):
        self.game.push_scene_on_stack(self.sceneone)
        self.game.push_scene_on_stack(self.scenetwo)
        self.assertEqual(self.game.get_top_scene(), self.scenetwo)

    def test_if_pushed_two_scenes_and_popped_one_top_should_be_one(self):
        self.game.push_scene_on_stack(self.sceneone)
        self.game.push_scene_on_stack(self.scenetwo)
        self.game.pop_scene_from_stack()
        self.assertEqual(self.game.get_top_scene(), self.sceneone)

    def test_if_pushed_two_scenes_and_popped_one_size_should_be_one(self):
        self.game.push_scene_on_stack(self.sceneone)
        self.game.push_scene_on_stack(self.scenetwo)
        self.game.pop_scene_from_stack()
        self.assertEqual(self.game.size_of_stack(), 1)

    def test_if_popped_empty_stack_raise_empty_error(self):
        self.assertRaises(GameStackEmptyError, self.game.pop_scene_from_stack)

    def test_name_of_top_scene(self):
        self.game.push_scene_on_stack(self.scenetwo)
        self.assertEqual(self.game.get_name_of_top_scene(), "TestScene2")

    def test_if_pushed_element_is_not_a_scene_raise_error(self):
        self.assertRaises(NotAScenePushedOnStackError, self.game.push_scene_on_stack, 1)
        self.assertRaises(NotAScenePushedOnStackError, self.game.push_scene_on_stack, "ThisIsNotAScene")


class TestScene(TestCase):
    def setUp(self):
        self.scene = Scene("TestScene")

    def test_if_you_can_get_identifier(self):
        self.assertEqual(self.scene.getIdentifier(), "TestScene")







