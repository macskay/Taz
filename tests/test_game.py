# -*- encoding: UTF-8 -*-
__author__ = 'Max'

from unittest import TestCase

from taz.game import Game, Scene


class TestGame(TestCase):
    def setUp(self):
        self.game = Game()
        self.sceneone = Scene("TestScene1")
        self.scenetwo = Scene("TestScene2")
        self.scenethree = Scene("TestScene3")

    def tearDown(self):
        self.game = 0
        self.sceneone = 0
        self.scenetwo = 0
        self.scenethree = 0

    def test_if_stack_is_empty(self):
        self.assertTrue(self.game.is_stack_empty())

    def test_if_pushed_one_scene_size_of_stack_should_be_one(self):
        self.game.push_scene_on_stack(self.sceneone)
        self.assertEqual(self.game.size_of_stack(), 1)

    def test_if_pushed_one_scene_top_scene_should_be_scene_one(self):
        self.game.push_scene_on_stack(self.sceneone)
        self.assertEqual(self.game.get_top_scene(), self.sceneone)

    def test_if_pushed_two_scene_top_scene_should_be_scene_two(self):
        self.game.push_scene_on_stack(self.sceneone)
        self.game.push_scene_on_stack(self.scenetwo)
        self.assertEqual(self.game.get_top_scene(), self.scenetwo)

    def test_if_pushed_two_scenes_and_popped_one_top_should_be_scene_one(self):
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
        self.assertRaises(Game.GameStackEmptyError, self.game.pop_scene_from_stack)

    def test_if_asked_for_top_scene_on_empty_stack_raise_error(self):
        self.assertRaises(Game.GameStackEmptyError, self.game.get_top_scene)

    def test_if_asked_for_top_scene_name_on_empty_stack_raise_error(self):
        self.assertRaises(Game.GameStackEmptyError, self.game.get_name_of_top_scene)

    def test_name_of_top_scene(self):
        self.game.push_scene_on_stack(self.scenetwo)
        self.assertEqual(self.game.get_name_of_top_scene(), "TestScene2")

    def test_if_pushed_element_is_not_a_scene_raise_error(self):
        self.assertRaises(Game.NotAScenePushedOnStackError, self.game.push_scene_on_stack, 1)
        self.assertRaises(Game.NotAScenePushedOnStackError, self.game.push_scene_on_stack, "ThisIsNotAScene")

    def test_if_scene_can_be_registered(self):
        self.assertTrue(self.game.register_new_scene(self.sceneone))
        self.assertRaises(Game.NotAScenePushedOnStackError, self.game.register_new_scene, "TestScene1")

    def test_if_one_scene_registered_len_should_be_one(self):
        self.game.register_new_scene(self.sceneone)
        self.assertEqual(len(self.game.registered_scenes), 1)

    def test_if_scene_is_registered_twice_raise_error(self):
        self.game.register_new_scene(self.sceneone)
        self.assertRaises(Game.SceneAlreadyRegisteredError, self.game.register_new_scene, self.sceneone)

    def test_if_active_scene_is_paused_if_another_scene_is_pushed_on_top(self):
        self.push_scenes()

        self.assertTrue(self.sceneone.is_paused())
        self.assertTrue(self.scenetwo.is_paused())
        self.assertFalse(self.scenethree.is_paused())

    def test_if_scene_is_unpaused_after_popped_higher_scene(self):
        self.push_scenes()
        self.game.pop_scene_from_stack()

        self.assertTrue(self.sceneone.is_paused())
        self.assertFalse(self.scenetwo.is_paused())
        self.assertTrue(self.scenethree.is_paused())

    def test_if_scenes_registered_scenes_get_updated_after_pushing_new_scenes(self):
        self.register_scenes()

        self.assertEqual(len(self.sceneone.registered_scenes), 3)
        self.assertEqual(len(self.scenetwo.registered_scenes), 3)
        self.assertEqual(len(self.scenethree.registered_scenes), 3)

    def register_scenes(self):
        self.game.register_new_scene(self.sceneone)
        self.game.register_new_scene(self.scenetwo)
        self.game.register_new_scene(self.scenethree)

    def push_scenes(self):
        self.game.push_scene_on_stack(self.sceneone)
        self.game.push_scene_on_stack(self.scenetwo)
        self.game.push_scene_on_stack(self.scenethree)


class TestScene(TestCase):
    def setUp(self):
        self.scene = Scene("TestScene")

    def tearDown(self):
        self.scene = 0

    def test_if_you_can_get_identifier(self):
        self.assertEqual(self.scene.get_identifier(), "TestScene")

    def test_if_scene_can_be_initialized(self):
        reg_scenes = {"SceneOne": Scene("SceneOne"), "SceneTwo": Scene("SceneTwo")}
        self.scene.init_scene(reg_scenes)

    def test_if_scene_gets_teared_down_paused_should_be_true(self):
        self.scene.tear_down()
        self.assertTrue(self.scene.is_paused())

    def test_if_scene_gets_resumed_paused_should_be_false(self):
        self.scene.tear_down()
        self.scene.resume()
        self.assertFalse(self.scene.is_paused())

    def test_update(self):
        # TODO: test if update works
        pass

    def test_render(self):
        # TODO: test if renderable
        pass










