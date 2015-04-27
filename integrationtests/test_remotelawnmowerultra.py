__author__ = 'Max'

from unittest import TestCase, skip
import json
from StringIO import StringIO

from remotelawnmowerultra import GameFactory, RoomScene, Player

from taz.game import Game


class PlayerTestCase(TestCase):

    def test_player_has_room_id(self):
        player = Player()
        self.assertIsNone(player.room_id)


class GameFactoryTestCase(TestCase):

    def setUp(self):
        self.mock_stdout = StringIO()
        self.mock_stdin = StringIO()
        self.mock_stdin.write("some stuff\n")
        self.mock_stdin.seek(0)
        self.game = GameFactory(self.mock_stdin, self.mock_stdout, {
            "config": {"starting-room": "room"},
            "rooms": [{
                "name": "room",
                "description": "This is test room",
                "objects": dict()
            }]}).create()

    def test_new_game_should_have_one_scene(self):
        self.assertEqual(len(self.game.registered_scenes), 1)

    def test_game_has_room_scene(self):
        self.assertEqual(self.game.get_name_of_top_scene(), "room")

    def test_game_has_file_like_object_in_render_context(self):
        fob = self.game.render_context["output_fob"]
        message = "hello world\n"
        fob.write(message)
        self.assertIn(message, fob.getvalue())

    def test_game_has_file_like_object_in_update_context(self):
        fob = self.game.update_context["input_fob"]
        self.assertTrue(hasattr(fob, "readline"))
        self.assertEqual("some stuff\n", fob.readline())

    def test_update_context_contains_world_data(self):
        world_data = self.game.update_context["world_data"]
        self.assertEqual(len(world_data["rooms"]), 1)
        first_room = world_data["rooms"][0]
        self.assertIn("name", first_room)
        self.assertIn("objects", first_room)

    def test_should_put_a_player_instance_on_the_room_scene(self):
        self.assertIsNotNone(self.game.registered_scenes["room"].player)

    def test_game_factory_raises_if_missing_starting_room(self):
        with self.assertRaises(GameFactory.MissingStartingRoom):
            game = GameFactory(None, None, dict()).create()


class RoomSceneTestCase(TestCase):

    def setUp(self):
        self.scene = RoomScene("room")
        self.stdout = StringIO()
        self.context = {
            "output_fob": self.stdout 
        }
        self.scene.update({
            "input_fob": StringIO()
        })
        self.scene.output_buffer.write("line one\nline two")
        self.scene.output_buffer.seek(0)

    def test_render_should_write_to_output_buffer(self):
        self.scene.render(self.context)
        self.assertEqual("line one\nline two", self.stdout.getvalue())

    def test_output_buffer_should_not_accumulate(self):
        self.scene.render(self.context)
        self.scene.update({
            "input_fob": StringIO()
        })
        self.assertEqual(0, len(self.scene.output_buffer.getvalue()))


class RoomSceneLookTestCase(TestCase):

    def setUp(self):
        self.scene = RoomScene("room")
        self.scene.player = Player()
        self.scene.player.room_id = "room"
        self.stdin = StringIO()        
        self.stdout = StringIO()
        self.update_context = {
            "input_fob": self.stdin,
            "world_data": {
                "config": {"starting-room": "room"},
                "rooms": [{
                    "name": "room",
                    "description": "This is test room",
                    "objects": {
                        "Unit Test": "It appears... useful"
                    }
                }]}
        }
        self.render_context = {
            "output_fob": self.stdout            
        }

    def process_command(self, command):
        self.stdin.write(command + "\n")
        self.stdin.seek(0)
        self.scene.update(self.update_context)    
        self.scene.render(self.render_context)
        self.stdin = StringIO()

    def assertOutputContains(self, message):
        self.assertIn(message, self.stdout.getvalue())

    @skip("TODO")
    def test_no_good_command(self):
        pass

    def test_look(self):
        self.process_command("look")
        self.assertOutputContains("This is test room")

    def test_look_at(self):
        self.process_command("look at Unit Test")
        self.assertOutputContains("It appears... useful")

    @skip("TODO")
    def test_look_at_nothing(self):
        pass
