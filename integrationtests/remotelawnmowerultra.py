__author__ = 'Max'

import re
from StringIO import StringIO

from taz.game import Game, Scene


class Player(object):

    def __init__(self):
        self.room_id = None  # TODO: rename to room_name


class RoomScene(Scene):

    def __init__(self, identifier):
        super(RoomScene, self).__init__(identifier)
        self.output_buffer = None
        self.player = None
        self.commands = [(re.compile("^look$"), self.look_command),
                         (re.compile("^look at (?P<what>.+)$"), self.look_at_command),
                         (re.compile("^look (?P<what>.+)$"), self.look_at_command)]

    def initialize_scene(self):
        pass

    def resume(self):
        pass

    def tear_down(self):
        pass

    def update(self, update_context):
        self.output_buffer = StringIO()
        commandText = update_context["input_fob"].readline().strip()
        for expression, command in self.commands:
            match = expression.match(commandText)
            if match:
                command(update_context, match)
                break
        self.output_buffer.seek(0)

    def look_command(self, update_context, match):
        room = self.get_current_room(update_context)
        self.output_buffer.write(room["description"])

    def look_at_command(self, update_context, match):
        room = self.get_current_room(update_context)
        what = match.group("what")
        obj = next((value for key, value in room["objects"].items() if key == what))
        self.output_buffer.write(obj)

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
