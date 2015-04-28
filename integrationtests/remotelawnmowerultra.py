__author__ = 'Max'

import re
from StringIO import StringIO
from os import sys
from json import load, loads

from taz.game import Game, Scene


class Player(object):

    def __init__(self):
        self.room_id = None
        self.inventory = []

    def add_item_to_inventory(self, item):
        self.inventory.append(item)


class RoomScene(Scene):

    def __init__(self, identifier):
        super(RoomScene, self).__init__(identifier)
        self.output_buffer = None
        self.player = None
        self.commands = [(re.compile("^look$"), self.look_command),
                         (re.compile("^look at (?P<what>.+)$"), self.look_at_command),
                         (re.compile("^look (?P<what>.+)$"), self.look_at_command),
                         (re.compile("^go$"), self.go_command),
                         (re.compile("^go in (?P<direction>.+)$"), self.go_in_a_room_command),
                         (re.compile("^take$"), self.take_command),
                         (re.compile("^take (?P<item>.+)$"), self.take_an_item_command),
                         (re.compile("^build lawnmower$"), self.build_lawnmower_command),
                         (re.compile("^mow lawn"), self.mow_lawn_command),
                         ]

    def initialize_scene(self):
        pass

    def resume(self):
        pass

    def tear_down(self):
        pass

    def update(self, update_context):
        self.output_buffer = StringIO()
        self.process_command(update_context)
        self.output_buffer.seek(0)

    def process_command(self, update_context):
        commandText = update_context["input_fob"].readline().strip()
        for expression, command in self.commands:
            match = expression.match(commandText)
            if self.is_expression_valid(command, match, update_context):
                break
        else:
            self.write_invalid_command_to_buffer(update_context)

    @staticmethod
    def is_expression_valid(command, match, update_context):
        if match:
            command(update_context, match)
            return True
        return False

    def write_invalid_command_to_buffer(self, update_context):
        self.output_buffer.write(update_context["world_data"]["config"]["invalid_command"])

    def look_around(self, update_context):
        room = self.get_current_room(update_context)
        self.output_buffer.write(room["description"])

    def look_command(self, update_context, match):
        self.look_around(update_context)

    def look_at_command(self, update_context, match):
        room = self.get_current_room(update_context)
        what = match.group("what")
        try:
            self.look_up_and_write_object_to_buffer(room, what)
        except StopIteration:
            self.write_invalid_look_to_buffer(update_context)

    def go_command(self, update_context, match):
        self.output_buffer.write(update_context["world_data"]["config"]["default_go"])

    def go_in_a_room_command(self, update_context, match):
        current_room = self.get_current_room(update_context)
        room_to_go_to = match.group("direction")
        for key, value in current_room["exits"].items():
            if self.can_go_to_that_room(room_to_go_to, value):
                self.go_to_room(update_context, value)
                break
        else:
            self.write_invalid_room_to_buffer(room_to_go_to, update_context)

    def take_command(self, update_context, match):
        self.output_buffer.write(update_context["world_data"]["config"]["default_take"])

    def take_an_item_command(self, update_context, match):
        current_room = self.get_current_room(update_context)
        item_to_take = match.group("item")
        config = update_context["world_data"]["config"]
        for key, value in current_room["take_objects"].items():
            if self.can_take_item(key, item_to_take, update_context):
                if self.is_item_needed_for_lawnmower(item_to_take, config):
                    self.take_item_if_not_already_taken(key, item_to_take, update_context)
                else:
                    self.output_buffer.write(current_room["take_objects"][item_to_take])
                break
        else:
            config = update_context["world_data"]["config"]
            self.output_buffer.write(config["invalid_item"] % item_to_take)

    @staticmethod
    def is_item_needed_for_lawnmower(item_to_take, config):
        return item_to_take in config["all_items"].values()

    def build_lawnmower_command(self, update_context, match):
        config = update_context["world_data"]["config"]
        all_items_needed = config["all_items"]
        for key, item in all_items_needed.items():
            if self.is_item_not_in_inventory(item):
                self.output_buffer.write(config["item_missing"])
                break
        else:
            self.try_assembling_lawnmower(config)

    def mow_lawn_command(self, update_context, match):
        config = update_context["world_data"]["config"]
        current_room = self.get_current_room(update_context)
        lawn_room = config["lawn_room"]
        if self.is_lawnmower_in_inventory(config):
            if self.is_room_mowable(current_room["name"], lawn_room):
                self.output_buffer.write(config["start_mowing"])
            else:
                self.output_buffer.write(config["lawn_invalid_room"])
        else:
            self.output_buffer.write(config["no_mower"])

    @staticmethod
    def is_room_mowable(current_room, lawn_room):
        return current_room == lawn_room

    def is_lawnmower_in_inventory(self, config):
        return config["lawnmower"] in self.player.inventory

    def is_item_not_in_inventory(self, item):
        return item not in self.player.inventory

    def try_assembling_lawnmower(self, config):
        assemble_room = config["assemble_room"]
        if self.is_player_in_correct_room(assemble_room):
            self.output_buffer.write(config["start_assembling"])
            self.player.inventory = [config["lawnmower"]]
        else:
            self.output_buffer.write(config["wrong_room_to_assemble"])

    def is_player_in_correct_room(self, assemble_room):
        return self.player.room_id == assemble_room

    def take_item_if_not_already_taken(self, key, item_to_take, update_context):
        if item_to_take not in self.player.inventory:
            self.take_item(key, item_to_take, update_context)
        else:
            self.write_item_taken_twice_to_buffer(update_context)

    def write_item_taken_twice_to_buffer(self, update_context):
        config = update_context["world_data"]["config"]
        self.output_buffer.write(config["item_already_in_inv"])

    @staticmethod
    def is_item_in_room(key, item_to_take):
        return key == item_to_take

    def take_item(self, key, item_to_take, update_context):
        current_room = self.get_current_room(update_context)
        self.player.add_item_to_inventory(item_to_take)
        self.output_buffer.write(current_room["take_objects"][item_to_take])

    def can_take_item(self, key, item_to_take, update_context):
        if self.is_item_in_room(key, item_to_take):
            return True
        return False

    def write_invalid_room_to_buffer(self, room_to_go_to, update_context):
        config = update_context["world_data"]["config"]
        invalid_room = config["invalid_room"] % room_to_go_to
        self.output_buffer.write(invalid_room)

    @staticmethod
    def can_go_to_that_room(room_to_go_to, value):
        return room_to_go_to == value

    def go_to_room(self, update_context, value):
        self.player.room_id = value
        self.look_around(update_context)

    def look_up_and_write_object_to_buffer(self, room, what):
        obj = next((value for key, value in room["look_objects"].items() if key == what))
        self.output_buffer.write(obj)

    def write_invalid_look_to_buffer(self, update_context):
        look_cmd_not_valid = update_context["world_data"]["config"]["invalid_look"]
        self.output_buffer.write(look_cmd_not_valid)

    def get_current_room(self, update_context):
        rooms = update_context["world_data"]["rooms"]
        players_room_name = self.player.room_id
        return next((r for r in rooms if r["name"] == players_room_name))

    def render(self, render_context):
        output_fob = render_context["output_fob"]
        for line in self.output_buffer:
            output_fob.write(line)


class GameFactory(object):

    class MissingStartingRoom(Exception):
        pass

    def __init__(self, input_fob, output_fob, world_data):
        self.output_fob = output_fob
        self.input_fob = input_fob
        self.world_data = world_data

    def create(self):
        game = Game(self.get_update_context(), self.get_render_context())
        room_scene = RoomScene("room")
        game.register_new_scene(room_scene)
        game.push_scene_on_stack("room")
        room_scene.player = Player()
        self.set_starting_room(room_scene.player)
        return game

    def get_update_context(self):
        return {
            "world_data": self.world_data,
            "input_fob": self.input_fob
        }

    def get_render_context(self):
        return {
            "output_fob": self.output_fob
        }

    def set_starting_room(self, player):
        try:
            player.room_id = self.world_data["config"]["starting-room"]
        except KeyError:
            raise self.MissingStartingRoom()

if __name__ == "__main__":
    world_data = {}
    stdout = sys.stdout
    stdin = sys.stdin

    with open("rooms.json") as file:
        world_data = load(file)

    gameFactory = GameFactory(stdin, stdout, world_data)
    game = gameFactory.create()
