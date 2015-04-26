__author__ = 'Max'

from taz.game import Game, Scene
from re import compile, match


class Player(object):
    def __init__(self, name):
        self.name = name
        self.current_room = 0
        self.inventory = []


class CommandProcessor(object):
    def __init__(self):
        pass

    def process(self, player, room, command_text):
        if self.is_room_backyard(room):
            run_backyard_command(command_text, player)

    def run_backyard_command(self, command_text, player):
        if self.is_looking_at_tools(command_text):
            player.inventory.append("Screw Driver")
            return "You look through the pile of tools. That screw driver might be useful. You take the Screw Driver"
        elif self.is_looking_at_gnomes(command_text):
            return "The gnomes play soccer and argue over a foul, which the referee-gnome not gave to the red-faced gnome."

    @staticmethod
    def is_looking_at_gnomes(command_text):
        a = compile("look\s*a?t?\s*gnomes?")
        if a.match(command_text):
            return True
        return False

    @staticmethod
    def is_looking_at_tools(command_text):
        a = compile("look\s*a?t?\s*p?i?l?e?\s*\w*\s*t?o?o?l?s?")
        if a.match(command_text):
            return True
        return False

    @staticmethod
    def is_room_backyard():
        return room == "Backyard"


class BackyardScene(Scene):
    def __init__(self):
        self.title = "Backyard"
        self.exits = {}
        self.item = "Screw Driver"
        self.objects_of_rooms = []
        self.commands_of_rooms = []

    def create_commands(self):
        self.commands_of_rooms.append("look at tools")
        self.commands_of_rooms.append("look at gnomes")
        self.commands_of_rooms.append("take tools")
        self.commands_of_rooms.append("take gnomes")
        self.commands_of_rooms.append("look west")
        self.commands_of_rooms.append("look east")
        self.commands_of_rooms.append("look north")
        self.commands_of_rooms.append("look south")
        self.commands_of_rooms.append("go west")
        self.commands_of_rooms.append("go east")
        self.commands_of_rooms.append("go north")
        self.commands_of_rooms.append("go south")

    def create_exits(self):
        self.exits["north"] = "Living Room"
        self.exits["south"] = "Storage Shed"
        self.exits["west"] = "Well, there is a big stone wall in front of you. No chance you are getting through that."
        self.exits["east"] = "You can't go there. Your neighbor is just waiting for an opportunity to get a hold of you."

    def create_objects(self):
        self.objects_of_rooms.append("Pile of Tools")
        self.objects_of_rooms.append("Gnomes")

    def update(self, update_context):
        pass

    def initialize_scene(self):
        print("You just stepped outside and are now standing on the backyard. " +
              "You look around and see two things, well except that hugely overgrown lawn, that stick out. " +
              "One is a Pile of Tools and the other is...a bunch of gnomes, which seem to argue?!")

    def render(self, render_context):
        pass

    def resume(self):
        pass

    def tear_down(self):
        pass


class StorageShedScene(Scene):
    def __init__(self):
        self.title = "Storage Shed"
        self.exits = {}
        self.item = "Armadillos"
        self.objectsOfRooms = []
        self.commands_of_room = []

    def create_exits(self):
        self.exits["north"] = "Backyard"
        self.exits["south"] = "You can't go there. There are only tools hanging on the wall."
        self.exits["west"] = "You can't climb through that window."
        self.exits["east"] = "You can't climb on the Grillmaster 3000"

    def create_commands(self):
        self.commands_of_room.append("look at hole")
        self.commands_of_room.append("look at grillmaster")
        self.commands_of_room.append("take armadillos")
        self.commands_of_room.append("take grillmaster")
        self.commands_of_room.append("look west")
        self.commands_of_room.append("look east")
        self.commands_of_room.append("look north")
        self.commands_of_room.append("look south")
        self.commands_of_room.append("go west")
        self.commands_of_room.append("go east")
        self.commands_of_room.append("go north")
        self.commands_of_room.append("go south")

    def create_objects(self):
        self.objectsOfRooms.append("Hole in the ground")
        self.objectsOfRooms.append("Grillmaster 3000")

    def update(self, update_context):
        pass

    def initialize_scene(self):
        print("You entered the shed! Wow, this is a tiny shed. Even though there is a hole in the ground," +
              "there is also the new Grillmaster 3000! That is the mothership of barbecue-grills.")

    def render(self, render_context):
        pass

    def resume(self):
        pass

    def tear_down(self):
        pass


class LivingRoomScene(Scene):
    def __init__(self):
        self.title = "Living Room"
        self.exits = {}
        self.item = "Antenna"
        self.objectsOfRooms = []

    def create_commands(self):
        self.commands_of_room.append("look at wife")
        self.commands_of_room.append("look at tv")
        self.commands_of_room.append("look at n64")
        self.commands_of_room.append("take tv")
        self.commands_of_room.append("take n64")
        self.commands_of_room.append("take wife")
        self.commands_of_room.append("look west")
        self.commands_of_room.append("look east")
        self.commands_of_room.append("look north")
        self.commands_of_room.append("look south")
        self.commands_of_room.append("go west")
        self.commands_of_room.append("go east")
        self.commands_of_room.append("go north")
        self.commands_of_room.append("go south")

    def create_exits(self):
        self.exits["north"] = "Kitchen"
        self.exits["south"] = "Backyard"
        self.exits["west"] = "Bedroom"
        self.exits["east"] = "Your wife is sitting in front of the TV. If you don't want to through her and the TV out of the way and break through the wall behind, there is no chance of walking this way."

    def create_objects(self):
        self.objectsOfRooms.append("Wife")
        self.objectsOfRooms.append("TV")
        self.objectsOfRooms.append("N64")

    def update(self, update_context):
        pass

    def initialize_scene(self):
        print("You stepped into the living room. Your wife is eyeing you suspiciously, while the TV runs another episode of 'The Prince of Bel Air.'")

    def render(self, render_context):
        pass

    def resume(self):
        pass

    def tear_down(self):
        pass


class KitchenScene(Scene):
    def __init__(self):
        self.title = "Kitchen"
        self.exits = {}
        self.item = "Battery"
        self.objectsOfRooms = []

    def create_commands(self):
        self.commands_of_room.append("look at sink")
        self.commands_of_room.append("look at microwave")
        self.commands_of_room.append("take sink")
        self.commands_of_room.append("take microwave")
        self.commands_of_room.append("look west")
        self.commands_of_room.append("look east")
        self.commands_of_room.append("look north")
        self.commands_of_room.append("look south")
        self.commands_of_room.append("go west")
        self.commands_of_room.append("go east")
        self.commands_of_room.append("go north")
        self.commands_of_room.append("go south")

    def create_exits(self):
        self.exits["north"] = "Garage"
        self.exits["south"] = "Living Room"
        self.exits["west"] = "Office"
        self.exits["east"] = "There is a huge pile of dishes in front of that window, so you can definitely not go there."

    def create_objects(self):
        self.objectsOfRooms.append("Sink")
        self.objectsOfRooms.append("Microwave")

    def update(self, update_context):
        pass

    def initialize_scene(self):
        print("You just entered the kitchen. You better get out of here quick, " +
              "otherwise you might have to do all the dishes in the sink." +
              "Get your food and RUN!")

    def render(self, render_context):
        pass

    def resume(self):
        pass

    def tear_down(self):
        pass


class BedroomScene(Scene):
    def __init__(self):
        self.title = "Bedroom"
        self.exits = {}
        self.item = "N64 Controller"
        self.objectsOfRooms = []

    def create_commands(self):
        self.commands_of_room.append("look at alarm clock")
        self.commands_of_room.append("look at closet")
        self.commands_of_room.append("take alarm clock")
        self.commands_of_room.append("look west")
        self.commands_of_room.append("look east")
        self.commands_of_room.append("look north")
        self.commands_of_room.append("look south")
        self.commands_of_room.append("go west")
        self.commands_of_room.append("go east")
        self.commands_of_room.append("go north")
        self.commands_of_room.append("go south")

    def create_exits(self):
        self.exits["north"] = "Garage"
        self.exits["south"] = "You can't go there. There are only tools hanging on the wall."
        self.exits["west"] = "Office"
        self.exits["east"] = "You can't climb on the Grillmaster 3000"

    def create_objects(self):
        self.objectsOfRooms.append("Alarm Clock")
        self.objectsOfRooms.append("Closet")

    def update(self, update_context):
        pass

    def initialize_scene(self):
        print("You just woke up and realize you are in the bedroom. That dream, though! You definitely need " +
              "a new lawnmower. 'I will just build it myself...I got all the stuff at home. I better get going'." +
              "But, you should get dressed first.")

    def render(self, render_context):
        pass

    def resume(self):
        pass

    def tear_down(self):
        pass


class GarageScene(Scene):
    def __init__(self):
        self.title = "Garage"
        self.exits = {}
        self.item = "Duct Tape"
        self.objectsOfRooms = []

    def create_commands(self):
        self.commands_of_room.append("look at car")
        self.commands_of_room.append("look at ladder")
        self.commands_of_room.append("take car")
        self.commands_of_room.append("take ladder")
        self.commands_of_room.append("look west")
        self.commands_of_room.append("look east")
        self.commands_of_room.append("look north")
        self.commands_of_room.append("look south")
        self.commands_of_room.append("go west")
        self.commands_of_room.append("go east")
        self.commands_of_room.append("go north")
        self.commands_of_room.append("go south")

    def create_exits(self):
        self.exits["north"] = "You can't go on the streets in your stained boxers. Get dressed and shower you filth!"
        self.exits["south"] = "Kitchen"
        self.exits["west"] = "There's an awesome Audi A8 blocking your way....Stop staring, get back to work!"
        self.exits["east"] = "There's a ladder hanging on the wall, but you can't climb it."

    def create_objects(self):
        self.objectsOfRooms.append("Car")
        self.objectsOfRooms.append("Ladder")

    def update(self, update_context):
        pass

    def initialize_scene(self):
        print("You are in the garage now! There it is! Your eye-candy, your sweet-heart, your little cutie. The new Audi A8." +
              "What a sight! But enough, that lawn is waiting for you to keep growing.")

    def render(self, render_context):
        pass

    def resume(self):
        pass

    def tear_down(self):
        pass


class OfficeScene(Scene):
    def __init__(self):
        self.title = "Office"
        self.exits = {}
        self.item = "Hot Glue"
        self.objectsOfRooms = []

    def create_commands(self):
        self.commands_of_room.append("look at computer")
        self.commands_of_room.append("look at megan fox")
        self.commands_of_room.append("take computer")
        self.commands_of_room.append("take megan fox")
        self.commands_of_room.append("look west")
        self.commands_of_room.append("look east")
        self.commands_of_room.append("look north")
        self.commands_of_room.append("look south")
        self.commands_of_room.append("go west")
        self.commands_of_room.append("go east")
        self.commands_of_room.append("go north")
        self.commands_of_room.append("go south")

    def create_exits(self):
        self.exits["north"] = "There is a computer on there. 'Wow! Pygame2, I've been waiting for that for ages.' Now turn around!"
        self.exits["south"] = "Bedroom"
        self.exits["west"] = "There's a sexy picture of Megan Fox. But now is not the time to go there!"
        self.exits["east"] = "Kitchen"

    def create_objects(self):
        self.objectsOfRooms.append("Computer")
        self.objectsOfRooms.append("Megan Fox Poster")

    def update(self, update_context):
        pass

    def initialize_scene(self):
        print("You enter the office and your computer is still running. You look at the wall and get reminded why you better make sure your wife doesn't get into this room.")

    def render(self, render_context):
        pass

    def resume(self):
        pass

    def tear_down(self):
        pass
