__author__ = 'Max'

from unittest import TestCase, skip
import json
from StringIO import StringIO

from remotelawnmowerultra import GameFactory, RoomScene, Player

from taz.game import Game


class PlayerTestCase(TestCase):

    def setUp(self):
        self.player = Player()

    def test_player_has_room_id(self):
        self.assertIsNone(self.player.room_id)

    def test_player_has_inventory(self):
        self.assertIsNotNone(self.player.inventory)

    def test_player_inventory_size_eq_1_when_item_is_put_into_inventory(self):
        self.player.add_item_to_inventory("Item")
        self.assertEqual(len(self.player.inventory), 1)


class GameFactoryTestCase(TestCase):
    def setUp(self):
        self.mock_stdout = StringIO()
        self.mock_stdin = StringIO()
        self.mock_stdin.write("some stuff\n")
        self.mock_stdin.seek(0)
        self.game = GameFactory(self.mock_stdin, self.mock_stdout, self.get_test_world_data()).create()

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

    def get_test_update_context(self):
        return {
            "input_fob": StringIO(),
            "world_data": self.get_test_world_data()
        }

    def get_test_world_data(self):
        return {
            "config": self.get_test_config(),
            "rooms": self.get_test_rooms()
        }

    def get_test_config(self):
        return {
            "starting-room": "room",
            "invalid_command": None
        }

    def get_test_rooms(self):
        return [{
            "name": "room",
            "description": "This is test room",
            "objects": dict()
        }]


class RoomSceneTestCase(TestCase):

    def setUp(self):
        self.scene = RoomScene("room")
        self.stdout = StringIO()
        self.context = {
            "output_fob": self.stdout 
        }
        self.update_context = self.get_test_update_context()
        self.scene.update(self.update_context)
        self.scene.output_buffer.write("line one\nline two")
        self.scene.output_buffer.seek(0)

    def test_render_should_write_to_output_buffer(self):
        self.scene.render(self.context)
        self.assertEqual("line one\nline two", self.stdout.getvalue())

    def test_output_buffer_should_not_accumulate(self):
        self.scene.render(self.context)
        self.scene.update(self.update_context)
        self.assertEqual(0, len(self.scene.output_buffer.getvalue()))

    def get_test_update_context(self):
        return {
            "input_fob": StringIO(),
            "world_data": self.get_test_world_data()
        }

    def get_test_world_data(self):
        return {
            "config": self.get_test_config(),
            "rooms": self.get_test_rooms()
        }

    def get_test_config(self):
        return {
            "starting-room": "room",
            "invalid_command": None,
            "default_go": "'Go where?!'"
        }

    def get_test_rooms(self):
        return [{
            "name": "room",
            "description": "This is test room",
            "objects": dict()
        }]


class RoomSceneCommandTestCase(TestCase):

    def setUp(self):
        self.scene = RoomScene("room")
        self.scene.player = Player()
        self.scene.player.room_id = "room"
        self.stdin = StringIO()        
        self.stdout = StringIO()
        self.update_context = {
            "input_fob": self.stdin,
            "world_data": self.get_test_command_world_data()
        }
        self.render_context = {
            "output_fob": self.stdout            
        }

    def process_command(self, command):
        self.reset_render_context_output_fob()

        self.stdin.write(command + "\n")
        self.stdin.seek(0)
        self.scene.update(self.update_context)    
        self.scene.render(self.render_context)

        self.reset_update_context_input_fob()

    def reset_render_context_output_fob(self):
        self.stdout = StringIO()
        self.render_context["output_fob"] = self.stdout

    def reset_update_context_input_fob(self):
        self.stdin = StringIO()
        self.update_context["input_fob"] = self.stdin

    def assertOutputContains(self, message):
        self.assertEqual(message, self.stdout.getvalue())

    def test_look(self):
        self.process_command("look")
        self.assertOutputContains("This is test room")

    def test_look_at(self):
        self.process_command("look at Unit Test")
        self.assertOutputContains("It appears... useful")

    def test_look_at_nothing(self):
        self.process_command("look at nothing")
        self.assertOutputContains("'I will not look at that TDD!'")

    def test_no_good_command(self):
        self.process_command("foobar at foobar")
        self.assertOutputContains("'I can't do that! No Test is backing me up!'")

    def test_go(self):
        self.process_command("go")
        self.assertOutputContains("'Go where?!'")

    def test_go_in_room(self):
        self.process_command("go in room 2")
        self.assertOutputContains("This is the second test room")
        self.process_command("go in room")
        self.assertOutputContains("This is test room")

    def test_go_in_room_which_is_not_exit(self):
        self.process_command("go in unittest room")
        self.assertOutputContains("There is no spoon..oops..There is no unittest room")

    def test_take(self):
        self.process_command("take")
        self.assertOutputContains("'Take what?!'")

    def test_take_an_item(self):
        self.process_command("take Unit Test")
        self.assertOutputContains("Travis takes Unit Test and puts it in his inventory")
        self.assertEqual(len(self.scene.player.inventory), 1)

    def test_take_an_invalid_item(self):
        self.process_command("take non-TTDt program")
        self.assertOutputContains("There is no non-TTDt program, which Travis can put in his inventory")

    def test_if_item_taken_twice_raise_error(self):
        self.process_command("take Unit Test")
        self.process_command("take Unit Test")
        self.assertOutputContains("This item is already in Travis' inventory")

    def test_if_item_is_missing_for_building_lawnmower(self):
        self.process_command("take Unit Test")
        self.process_command("build lawnmower")
        self.assertOutputContains("Item missing")

    def test_if_lawnmower_can_be_build_with_all_items_and_correct_room(self):
        self.process_command("take Unit Test")
        self.process_command("go in room 2")
        self.process_command("take IRCbot")
        self.process_command("go in room")
        self.process_command("build lawnmower")
        self.assertOutputContains("Alright! Let's build Remote-Lawnmower-Ultra 3000 (TM)")
        self.assertEqual(self.scene.player.room_id, "room")
        self.assertIn("Remote-Lawnmower-Ultra 3000 (TM)", self.scene.player.inventory)

    def test_if_lawnmower_can_be_build_with_all_items_and_wrong_room(self):
        self.process_command("take Unit Test")
        self.process_command("go in room 2")
        self.process_command("take IRCbot")
        self.process_command("build lawnmower")
        self.assertOutputContains("Travis seem to have all the items he needs, but this is not the right place")

    def test_if_can_mow_without_lawnmower(self):
        self.process_command("mow lawn")
        self.assertOutputContains("You have no lawn mower")

    def test_if_can_mow_lawn_wrong_room(self):
        self.process_command("take Unit Test")
        self.process_command("go in room 2")
        self.process_command("take IRCbot")
        self.process_command("go in room")
        self.process_command("build lawnmower")
        self.process_command("mow lawn")
        self.assertOutputContains("The lawnmower is ready, but you can't mow in here")

    def test_start_mowing(self):
        self.process_command("take Unit Test")
        self.process_command("go in room 2")
        self.process_command("take IRCbot")
        self.process_command("go in room")
        self.process_command("build lawnmower")
        self.process_command("go in room 2")
        self.process_command("mow lawn")
        self.assertOutputContains("Alright! LET'S GET READY TO RUMBLE!")

    def get_test_command_world_data(self):
        return {
            "config": self.get_test_command_config(),
            "rooms": self.get_test_command_rooms()
        }

    def get_test_command_config(self):
        return {
            "starting-room": "room",
            "invalid_command": "'I can't do that! No Test is backing me up!'",
            "invalid_look": "'I will not look at that TDD!'",
            "invalid_room": "There is no spoon..oops..There is no %s",
            "invalid_item": "There is no %s, which Travis can put in his inventory",
            "default_go": "'Go where?!'",
            "default_take": "'Take what?!'",
            "take_item": "Travis takes %s and puts it in his inventory",
            "item_already_in_inv": "This item is already in Travis' inventory",
            "item_missing": "Item missing",
            "all_items_collected": "All items collected. Ready to build lawnmower",
            "start_assembling": "Alright! Let's build Remote-Lawnmower-Ultra 3000 (TM)",
            "assemble_room": "room",
            "wrong_room_to_assemble": "Travis seem to have all the items he needs, but this is not the right place",
            "lawnmower": "Remote-Lawnmower-Ultra 3000 (TM)",
            "lawn_room": "room 2",
            "lawn_invalid_room": "The lawnmower is ready, but you can't mow in here",
            "no_mower": "You have no lawn mower",
            "start_mowing": "Alright! LET'S GET READY TO RUMBLE!",
            "all_items": {
                1: "Unit Test",
                2: "IRCbot"
            }
        }

    def get_test_command_rooms(self):
        return [{
            "name": "room",
            "description": "This is test room",
            "objects": {
                "Unit Test": "It appears... useful"
            },
            "exits": {
                1: "room 2"
            }
        },  {
            "name": "room 2",
            "description": "This is the second test room",
            "objects": {
                "IRCbot": "It appears....not useful"
            },
            "exits": {
                1: "room"
            }
        }]