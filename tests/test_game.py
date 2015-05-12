# -*- encoding: UTF-8 -*-
__author__ = 'Max'

from unittest import TestCase
from logging import getLogger, basicConfig, INFO
from taz.game import Game, Scene
from mock import patch

logger = getLogger(__name__)
basicConfig(level=INFO, format=' Log: - %(message)s')


class TestGame(TestCase):
    def setUp(self):
        self.dict = {}
        self.game = Game(self.dict, self.dict)
        self.sceneone = MockUpScene("TestScene1")
        self.scenetwo = MockUpScene("TestScene2")
        self.scenethree = MockUpScene("TestScene3")

    def tearDown(self):
        self.game = 0
        self.sceneone = 0
        self.scenetwo = 0
        self.scenethree = 0

    def test_if_game_can_be_created(self):
        self.assertIsNotNone(Game(self.dict, self.dict))

    def test_if_stack_is_empty(self):
        self.assertTrue(self.game.is_stack_empty())

    def test_if_pushed_one_scene_size_of_stack_should_be_one(self):
        self.game.register_new_scene(self.sceneone)
        self.game.push_scene_on_stack(self.sceneone.get_identifier())
        self.assertEqual(self.game.size_of_stack(), 1)

    def test_if_pushed_one_scene_top_scene_should_be_scene_one(self):
        self.game.register_new_scene(self.sceneone)
        self.game.push_scene_on_stack(self.sceneone.get_identifier())

        self.assertEqual(self.game.get_top_scene(), self.sceneone)

    def test_if_pushed_two_scene_top_scene_should_be_scene_two(self):
        self.game.register_new_scene(self.sceneone)
        self.game.register_new_scene(self.scenetwo)
        self.game.push_scene_on_stack(self.sceneone.get_identifier())
        self.game.push_scene_on_stack(self.scenetwo.get_identifier())

        self.assertEqual(self.game.get_top_scene(), self.scenetwo)

    def test_if_pushed_two_scenes_and_popped_one_top_should_be_scene_one(self):
        self.game.register_new_scene(self.sceneone)
        self.game.register_new_scene(self.scenetwo)

        self.game.push_scene_on_stack(self.sceneone.get_identifier())
        self.game.push_scene_on_stack(self.scenetwo.get_identifier())

        self.game.pop_scene_from_stack()

        self.assertEqual(self.game.get_top_scene(), self.sceneone)

    def test_if_pushed_two_scenes_and_popped_one_size_should_be_one(self):
        self.game.register_new_scene(self.sceneone)
        self.game.register_new_scene(self.scenetwo)
        self.game.push_scene_on_stack(self.sceneone.get_identifier())
        self.game.push_scene_on_stack(self.scenetwo.get_identifier())
        self.game.pop_scene_from_stack()

        self.assertEqual(self.game.size_of_stack(), 1)

    def test_if_popped_empty_stack_raise_empty_error(self):
        self.assertRaises(Game.StackEmptyError, self.game.pop_scene_from_stack)

    def test_if_asked_for_top_scene_on_empty_stack_raise_error(self):
        self.assertRaises(Game.StackEmptyError, self.game.get_top_scene)

    def test_if_asked_for_top_scene_name_on_empty_stack_raise_error(self):
        self.assertRaises(Game.StackEmptyError, self.game.get_name_of_top_scene)

    def test_if_last_scene_popped_raises_exit_exception(self):
        self.game.register_new_scene(self.sceneone)
        self.game.register_new_scene(self.scenetwo)
        self.game.push_scene_on_stack(self.sceneone.get_identifier())
        self.game.push_scene_on_stack(self.scenetwo.get_identifier())

        self.game.pop_scene_from_stack()
        self.assertRaises(SystemExit, self.game.pop_scene_from_stack)

    def test_name_of_top_scene(self):
        self.game.register_new_scene(self.scenetwo)
        self.game.push_scene_on_stack(self.scenetwo.get_identifier())
        self.assertEqual(self.game.get_name_of_top_scene(), "TestScene2")

    def test_if_one_scene_registered_len_should_be_one(self):
        self.game.register_new_scene(self.sceneone)
        self.assertEqual(len(self.game.registered_scenes), 1)

    def test_if_scene_is_registered_twice_raise_error(self):
        self.game.register_new_scene(self.sceneone)
        self.assertRaises(Game.SceneAlreadyRegisteredError, self.game.register_new_scene, self.sceneone)

    def test_if_scene_gets_pushed_without_registration_raise_error(self):
        self.assertRaises(Game.NoRegisteredSceneWithThisIDError,
                          self.game.push_scene_on_stack, self.sceneone.get_identifier())

    def test_is_scenes_can_be_pushed_on_the_stack(self):
        self.game.register_new_scene(self.sceneone)
        self.game.push_scene_on_stack(self.sceneone.get_identifier())
        self.assertTrue(self.game.size_of_stack, 1)

    def test_if_active_scene_is_paused_if_another_scene_is_pushed_on_top(self):
        self.register_scenes()
        self.push_scenes()

        self.assertTrue(self.sceneone.is_paused())
        self.assertTrue(self.scenetwo.is_paused())
        self.assertFalse(self.scenethree.is_paused())

    def test_if_scene_is_unpaused_after_popped_higher_scene(self):
        self.register_scenes()
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

    @patch("taz.game.Scene.initialize")
    def test_when_scene_initialization_fails_raise_exception(self, mock_initialize):
        scene_fail = MockUpScene("scene_fail")
        self.game.register_new_scene(scene_fail)
        self.assertRaises(Game.SceneInitializationFailed, self.game.try_scene_initialization, scene_fail.get_identifier)

    def register_scenes(self):
        self.game.register_new_scene(self.sceneone)
        self.game.register_new_scene(self.scenetwo)
        self.game.register_new_scene(self.scenethree)

    def push_scenes(self):
        self.game.push_scene_on_stack(self.sceneone.get_identifier())
        self.game.push_scene_on_stack(self.scenetwo.get_identifier())
        self.game.push_scene_on_stack(self.scenethree.get_identifier())


class TestScene(TestCase):
    def setUp(self):
        self.scene = MockUpScene("TestScene")

    def tearDown(self):
        self.scene = 0

    def test_if_you_can_get_identifier(self):
        self.assertEqual(self.scene.get_identifier(), "TestScene")

    def test_if_scene_can_be_initialized(self):
        self.scene.initialize()

    def test_if_scene_gets_resumed_paused_should_be_false(self):
        self.scene.tear_down()
        self.scene.resume()
        self.assertFalse(self.scene.is_paused())

    def test_if_coupling_between_scene_and_game_works(self):
            game = self.setup_mock_up_scene()
            game.enter_mainloop()

    def setup_mock_up_scene(self):
        update_context, render_context = self.setup_contexts()
        game = Game(update_context, render_context)
        scene1, scene2 = self.create_mock_up_scene_objects()

        self.create_mock_up_scene_objects()
        self.register_mock_up_scenes_with_game(game, scene1, scene2)
        self.push_mock_up_scenes_on_game_stack(game)

        return game

    def setup_contexts(self):
        rc = {
            "screen": 0
        }

        uc = {
            "clock": 0,
            "get_events": 0,
            "pump": 0
        }
        return uc, rc

    def create_mock_up_scene_objects(self):
        scene1 = MockUpScene("FirstMockUpScene")
        scene2 = MockUpScene("SecondMockUpScene")

        return scene1, scene2

    def register_mock_up_scenes_with_game(self, game, scene1, scene2):
        game.register_new_scene(scene1)
        game.register_new_scene(scene2)

    def push_mock_up_scenes_on_game_stack(self, game):
        game.push_scene_on_stack("FirstMockUpScene")
        game.push_scene_on_stack("SecondMockUpScene")


class MockUpScene(Scene):
    def initialize(self):
        pass

    def resume(self):
        pass

    def tear_down(self):
        pass

    def update(self):
        self.game.pop_scene_from_stack()

    def render(self):
        pass

    def pause(self):
        pass