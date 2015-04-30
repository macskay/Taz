__author__ = 'Max'

import re

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
    
from os import sys
from json import load
from argparse import ArgumentParser
from os.path import abspath, join, split

SCRIPT_DIR = abspath(split(__file__)[0])
INSTRUCTIONS_FILE_PATH = join(SCRIPT_DIR, u"instructions.txt")
ROOMS_FILE_PATH = join(SCRIPT_DIR, u"rooms.json")
WELCOME_FILE_PATH = join(SCRIPT_DIR, u"welcome.json")

sys.path.append(abspath(join(SCRIPT_DIR, u"..")))

from taz.game import Game, Scene


class GameFactory(object):
    
    class MissingStartingRoom(Exception):
        pass

    def __init__(self, input_fob, output_fob, world_data):
        self.output_fob = output_fob
        self.input_fob = input_fob
        self.world_data = world_data
        self.InstructionReaderClass = InstructionReader

    def create(self, start_scene_name):
        instructions_file = self.InstructionReaderClass()
        game = Game(self.get_update_context(), self.get_render_context())
        title_scene = TitleScene(start_scene_name, instructions_file)
        game.register_new_scene(title_scene)
        game.push_scene_on_stack(start_scene_name)
        return game

    def get_update_context(self):
        return {
            u"world_data": self.world_data,
            u"input_fob": self.input_fob
        }

    def get_render_context(self):
        return {
            u"output_fob": self.output_fob
        }


class Player(object):
    def __init__(self):
        self.room_id = None
        self.inventory = []

    def add_item_to_inventory(self, item):
        self.inventory.append(item)


class RoomScene(Scene):

    def __init__(self, identifier, welcome_data, instructions_file):
        super(RoomScene, self).__init__(identifier)
        self.output_buffer = StringIO()
        self.player = None
        self.commands = []
        self.append_all_regex_to_commands()
        self.welcome_data = welcome_data
        self.instructions_file = instructions_file

    def append_all_regex_to_commands(self):
        self.append_look_regex_to_commands()
        self.append_go_regex_to_commands()
        self.append_take_regex_to_commands()
        self.append_lawnmower_regex_to_commands()
        self.append_inventory_regex_to_commands()
        self.append_help_quit_exits_regex_to_commands()

    def append_look_regex_to_commands(self):
        self.commands.append((re.compile(u"^look$"), self.look_command))
        self.commands.append((re.compile(u"^look at (?P<what>.+)$"), self.look_at_command))
        self.commands.append((re.compile(u"^look (?P<what>.+)$"), self.look_at_command))

    def append_go_regex_to_commands(self):
        self.commands.append((re.compile(u"^go$"), self.go_command))
        self.commands.append((re.compile(u"^go in (?P<direction>.+)$"), self.go_in_a_room_command))

    def append_take_regex_to_commands(self):
        self.commands.append((re.compile(u"^take$"), self.take_command))
        self.commands.append((re.compile(u"^take (?P<item>.+)$"), self.take_an_item_command))

    def append_lawnmower_regex_to_commands(self):
        self.commands.append((re.compile(u"^build lawnmower$"), self.build_lawnmower_command))
        self.commands.append((re.compile(u"^mow lawn$"), self.mow_lawn_command))

    def append_inventory_regex_to_commands(self):
        self.commands.append((re.compile(u"^show inv$"), self.show_inventory_command))
        self.commands.append((re.compile(u"^show inventory$"), self.show_inventory_command))

    def append_help_quit_exits_regex_to_commands(self):
        self.commands.append((re.compile(u"^quit game$"), self.quit_game_command))
        self.commands.append((re.compile(u"^help$$"), self.help_command))
        self.commands.append((re.compile(u"^show exits$"), self.show_exits_command))

    def initialize_scene(self):
        self.player = Player()
        self.player.room_id = self.welcome_data[u"starting_room"]
        print(self.welcome_data[u"intro"])

    def resume(self):
        pass

    def tear_down(self):
        pass

    def update(self, update_context):
        self.output_buffer = StringIO()
        update_context[u"input_fob"] = StringIO()
        command = u"#"
        while command.startswith(u"#"):
            command = self.instructions_file.readline().strip()
        print(u"Travis-CI Command: u"+command)
        update_context[u"input_fob"].write(command)
        self.process_command(update_context)
        self.output_buffer.write(u"\n")
        self.output_buffer.seek(0)

    def process_command(self, update_context):
        update_context[u"input_fob"].seek(0)
        command_text = update_context[u"input_fob"].readline().strip()
        for expression, command in self.commands:
            match = expression.match(command_text)
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
        self.output_buffer.write(update_context[u"world_data"][u"config"][u"invalid_command"])

    def look_around(self, update_context):
        room = self.get_current_room(update_context)
        self.output_buffer.write(room[u"description"])

    def look_command(self, update_context, match):
        self.look_around(update_context)

    def look_at_command(self, update_context, match):
        room = self.get_current_room(update_context)
        what = match.group(u"what")
        try:
            self.look_up_and_write_object_to_buffer(room, what)
        except StopIteration:
            self.write_invalid_look_to_buffer(update_context)

    def go_command(self, update_context, match):
        self.output_buffer.write(update_context[u"world_data"][u"config"][u"default_go"])

    def go_in_a_room_command(self, update_context, match):
        current_room = self.get_current_room(update_context)
        room_to_go_to = match.group(u"direction")
        for key_value in current_room[u"exits"].items():

            if self.can_go_to_that_room(room_to_go_to, key_value[1]):
                self.go_to_room(update_context, key_value[1])
                break
        else:
            self.write_invalid_room_to_buffer(room_to_go_to, update_context)

    def take_command(self, update_context, match):
        self.output_buffer.write(update_context[u"world_data"][u"config"][u"default_take"])

    def take_an_item_command(self, update_context, match):
        current_room = self.get_current_room(update_context)
        item_to_take = match.group(u"item")
        config = update_context[u"world_data"][u"config"]
        for key_value in current_room[u"take_objects"].items():
            if self.can_take_item(key_value[0], item_to_take, update_context):
                if self.is_item_needed_for_lawnmower(item_to_take, config):
                    self.take_item_if_not_already_taken(key_value[0], item_to_take, update_context)
                else:
                    self.output_buffer.write(current_room[u"take_objects"][item_to_take])
                break
        else:
            config = update_context[u"world_data"][u"config"]
            self.output_buffer.write(config[u"invalid_item"] % item_to_take)

    @staticmethod
    def is_item_needed_for_lawnmower(item_to_take, config):
        return item_to_take in config[u"all_items"].values()

    def build_lawnmower_command(self, update_context, match):
        config = update_context[u"world_data"][u"config"]
        all_items_needed = config[u"all_items"]
        for key, item in all_items_needed.items():
            if self.is_item_not_in_inventory(item):
                self.output_buffer.write(config[u"item_missing"])
                break
        else:
            self.try_assembling_lawnmower(config)

    def mow_lawn_command(self, update_context, match):
        config = update_context[u"world_data"][u"config"]
        current_room = self.get_current_room(update_context)
        lawn_room = config[u"lawn_room"]
        if self.is_lawnmower_in_inventory(config):
            if self.is_room_mowable(current_room[u"name"], lawn_room):
                self.output_buffer.write(config[u"start_mowing"])
                game_over_scene = GameOverScene(u"GameOver")
                game.register_new_scene(game_over_scene)
                game.push_scene_on_stack(game_over_scene.get_identifier())
            else:
                self.output_buffer.write(config[u"lawn_invalid_room"])
        else:
            self.output_buffer.write(config[u"no_mower"])

    def show_inventory_command(self, update_context, match):
        self.output_buffer.write(str(self.player.inventory))

    @staticmethod
    def quit_game_command(update_context, match):
        raise Game.GameExitException

    def help_command(self, update_context, match):
        self.output_buffer.write(update_context[u"world_data"][u"config"][u"help"])

    def show_exits_command(self, update_context, match):
        current_room = self.get_current_room(update_context)
        list_of_exits = []
        for key, value in current_room[u"exits"].items():
            list_of_exits.append(str(value))
        self.output_buffer.write(update_context[u"world_data"][u"config"][u"can_go_to"] % str(list_of_exits))



    @staticmethod
    def is_room_mowable(current_room, lawn_room):
        return current_room == lawn_room

    def is_lawnmower_in_inventory(self, config):
        return config[u"lawnmower"] in self.player.inventory

    def is_item_not_in_inventory(self, item):
        return item not in self.player.inventory

    def try_assembling_lawnmower(self, config):
        assemble_room = config[u"assemble_room"]
        if self.is_player_in_correct_room(assemble_room):
            self.output_buffer.write(config[u"start_assembling"])
            self.player.inventory = [config[u"lawnmower"]]
        else:
            self.output_buffer.write(config[u"wrong_room_to_assemble"])

    def is_player_in_correct_room(self, assemble_room):
        return self.player.room_id == assemble_room

    def take_item_if_not_already_taken(self, key, item_to_take, update_context):
        if item_to_take not in self.player.inventory:
            self.take_item(key, item_to_take, update_context)
        else:
            self.write_item_taken_twice_to_buffer(update_context)

    def write_item_taken_twice_to_buffer(self, update_context):
        config = update_context[u"world_data"][u"config"]
        self.output_buffer.write(config[u"item_already_in_inv"])

    @staticmethod
    def is_item_in_room(key, item_to_take):
        return key == item_to_take

    def take_item(self, key, item_to_take, update_context):
        current_room = self.get_current_room(update_context)
        self.player.add_item_to_inventory(item_to_take)
        self.output_buffer.write(current_room[u"take_objects"][item_to_take])

    def can_take_item(self, key, item_to_take, update_context):
        if self.is_item_in_room(key, item_to_take):
            return True
        return False

    def write_invalid_room_to_buffer(self, room_to_go_to, update_context):
        config = update_context[u"world_data"][u"config"]
        invalid_room = config[u"invalid_room"] % room_to_go_to
        self.output_buffer.write(invalid_room)

    @staticmethod
    def can_go_to_that_room(room_to_go_to, value):
        return room_to_go_to == value

    def go_to_room(self, update_context, value):
        self.player.room_id = value
        self.look_around(update_context)

    def look_up_and_write_object_to_buffer(self, room, what):
        obj = next((value for key, value in room[u"look_objects"].items() if key == what))
        self.output_buffer.write(obj)

    def write_invalid_look_to_buffer(self, update_context):
        look_cmd_not_valid = update_context[u"world_data"][u"config"][u"invalid_look"]
        self.output_buffer.write(look_cmd_not_valid)

    def get_current_room(self, update_context):
        rooms = update_context[u"world_data"][u"rooms"]
        players_room_name = self.player.room_id
        return next((r for r in rooms if r[u"name"] == players_room_name))

    def render(self, render_context):
        output_fob = render_context[u"output_fob"]
        for line in self.output_buffer:
            output_fob.write(line)


class GameOverScene(Scene):
    def __init__(self, identifier):
        super(GameOverScene, self).__init__(identifier)
        self.welcome_data = None

    def tear_down(self):
        pass

    def render(self, render_context):
        pass

    def initialize_scene(self):
        with open(WELCOME_FILE_PATH) as f:
            welcome_data = load(f)
        print(welcome_data[u"outro"])

    def resume(self):
        pass

    def update(self, update_context):
        self.quit_game_command(update_context, None)

    @staticmethod
    def quit_game_command(update_context, match):
        raise Game.GameExitException


class TitleScene(Scene):
    def __init__(self, identifier, instructions_file):
        super(TitleScene, self).__init__(identifier)
        self.commands = [(re.compile(u"^quit game$"), self.quit_game_command),
                         (re.compile(u"^1$"), self.start_game),
                         ]
        self.output_buffer = StringIO()
        self.welcome_data = None
        self.instructions_file = instructions_file

    @staticmethod
    def quit_game_command(update_context, match):
        raise Game.GameExitException

    def tear_down(self):
        pass

    def render(self, render_context):
        output_fob = render_context[u"output_fob"]
        for line in self.output_buffer:
            output_fob.write(line)

    def initialize_scene(self):
        with open(WELCOME_FILE_PATH) as f:
            welcome_data = load(f)
        self.welcome_data = welcome_data
        self.show_welcome_message(welcome_data)

    def resume(self):
        pass

    def update(self, update_context):
        self.output_buffer = StringIO()
        command = u"#"
        while command.startswith(u"#"):
            command = self.instructions_file.readline().strip()
        print(command)
        update_context[u"input_fob"].write(command)
        self.process_command(update_context)
        self.output_buffer.write(u"\n")
        self.output_buffer.seek(0)

    def process_command(self, update_context):
        update_context[u"input_fob"].seek(0)
        commandText = update_context[u"input_fob"].readline().strip()
        for expression, command in self.commands:
            match = expression.match(commandText)
            if self.is_expression_valid(command, match, update_context):
                break
        else:
            self.output_buffer.write(self.welcome_data[u"invalid_command"])

    def start_game(self, update_context, match):
        print(self.welcome_data[u"game_start"])
        room = RoomScene(u"RoomScene", self.welcome_data, self.instructions_file)
        game.register_new_scene(room)
        game.push_scene_on_stack(room.get_identifier())

    @staticmethod
    def show_welcome_message(welcome_data):
        print(welcome_data[u"welcome"])

    @staticmethod
    def is_expression_valid(command, match, update_context):
        if match:
            command(update_context, match)
            return True
        return False


class InstructionReader(object):
    
    def __init__(self):
        self.instruction_file = self.open_instruction_file()

    @staticmethod
    def open_instruction_file():
        return open(INSTRUCTIONS_FILE_PATH, u"r")

    def readline(self):
        return self.instruction_file.readline()


class StdinReader(object):

    def readline(self):
        return sys.stdin.readline()


def get_arguments():
    parser = get_argument_parser()
    return parser.parse_args()


def get_argument_parser():
    parser = ArgumentParser(u"remotelawnmowerultra.py")
    parser.add_argument(u"--manual", action="store_true", default=False)
    return parser

def set_reader(game_factory):
    args = get_arguments()
    if args.manual:
        game_factory.InstructionReaderClass = StdinReader
    else:
        game_factory.InstructionReaderClass = InstructionReader
    

if __name__ == u"__main__":
    world_data = {}
    stdout = sys.stdout
    stdin = StringIO()

    with open(ROOMS_FILE_PATH) as f:
        world_data = load(f)

    game_factory = GameFactory(stdin, stdout, world_data)
    set_reader(game_factory)
        
    game = game_factory.create(u"TitleScreen")
    game.enter_mainloop()
