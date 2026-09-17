import json
import sys
from pathlib import Path

from .items import Item
from .player import Player
from .world import Room


class Game:
    def __init__(self):
        self.player = Player()
        self.running = True
        self.current_room = "tavern"
        self.rooms = self._load_rooms()
        self.state = "not started"
        self.treasure_found = False
        self.victory = False
        self.torch_taken = False
        self.sword_taken = False
        self.lock_open = False
        self.bartender_key_given = False
        self.drinks_bought = 0
        self.raiders_seen = False
        self.raiders_defeated = False
        self.cave_battle_done = False

    def _load_rooms(self):
        story_path = Path(__file__).resolve().parents[1] / "data" / "story.json"
        with open(story_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        rooms = {}
        for room_id, room_data in data["rooms"].items():
            rooms[room_id] = Room(
                name=room_data["name"],
                description=room_data["description"],
                exits=room_data.get("exits", {}),
                items=room_data.get("items", []),
            )
        return rooms

    def ask_player_name(self, provided_name=None):
        if provided_name:
            self.player.set_name(provided_name)
            return

        if not sys.stdin.isatty():
            self.player.set_name("Traveller")
            return

        while True:
            name = input("What is your name? ").strip()
            if name:
                self.player.set_name(name)
                return
            print('Bartender: "A name, if you please."')

    def start_game(self, player_name=None):
        self.state = "in progress"
        self.current_room = "tavern"

        print("\nThe rain hisses against the windows of a stone inn.")
        print("The walls are lined with cracked lanterns and old hunting trophies.")
        print("A burly barkeep wipes a mug with a weary stare.")
        print("")
        print('Bartender: "Ah, a traveller at last..."')
        print('Bartender: "Welcome to The End, friend."')
        self.ask_player_name(player_name)
        print(f'Bartender: "A fine name, {self.player.name}."')
        print('Bartender: "There is a hidden treasure beneath this place, sealed away by a forgotten vow."')
        print('Bartender: "Find it, and you may leave with more than gold. Fail, and the tavern may keep you forever."')
        print('Bartender: "Now... are you here for the truth, or just a drink?"')
        self.show_current_room()

    def start(self, player_name=None):
        self.start_game(player_name)

    def end(self):
        self.state = "game over"

    def run(self):
        self.start_game()
        while self.running:
            command = input("> ").strip().lower()
            if not command:
                continue
            self.handle_command(command)

    def show_current_room(self):
        room = self.rooms[self.current_room]
        print(f"\n{room.name}")
        print(room.description)

        if room.items:
            print(f"You see: {', '.join(room.items)}")

        if room.exits:
            exits = ", ".join(room.exits.keys())
            print(f"Exits: {exits}")

    def show_map(self):
        print("\nMap:")
        print("  [Tavern]")
        print("    |")
        print("    +-- [Forest Path] -- [Hidden Treasure]")
        print("    |")
        print("    +-- [Root Cellar] -- [Cave Entrance] -- [Cave Chamber]")
        print("         |")
        print("         +-- coin stash")
        print("")

    def speak_to_bartender(self):
        if self.current_room != "tavern":
            print("No one here is listening.")
            return

        print('Bartender: "If you want the cellar key, buy a drink. One coin."')
        print('Bartender: "The first drink is honest. The second is a mistake."')
        print('Bartender: "The cellar is below. The cave is deeper."')
        print('Bartender: "The key unlocks the old iron door beneath the tavern."')
        print('Bartender: "If you go into the cave without a light, it will eat you alive."')
        print('Bartender: "And if you think a torch is a weapon, the dark will claim you."')

    def trigger_forest_raid(self):
        self.raiders_seen = True
        print("\nThe forest path beyond the tavern door is watched.")
        print("You remember the men who followed you to the inn.")
        print("Their eyes are in the dark, waiting for you to step out.")
        print("You do not feel safe going back out there without a weapon.")
        print("")
        print("The raiders block the path.")
        print("You can: 'fight raiders' or 'turn back'")
        self.current_room = "forest_path"
        self.show_current_room()

    def handle_command(self, command):
        parts = command.split()
        verb = parts[0]

        if verb in {"quit", "exit"}:
            self.running = False
            self.state = "game over"
            print("The inn door swings shut behind you.")
            print("The tavern settles back into silence.")
            return

        if verb in {"help", "h"}:
            self.print_help()
            return

        if verb in {"map", "m"}:
            self.show_map()
            return

        if verb in {"speak", "talk", "chat"}:
            self.speak_to_bartender()
            return

        if verb in {"look", "l"}:
            self.show_current_room()
            return

        if verb in {"inventory", "inv", "i"}:
            self.player.show_inventory()
            return

        if verb in {"go", "move"}:
            if len(parts) < 2:
                print("Where do you want to go?")
                return
            self.move(parts[1])
            return

        if verb in {"take", "pickup"}:
            if len(parts) < 2:
                print("What do you want to take?")
                return
            item_name = " ".join(parts[1:])
            self.take_item(item_name)
            return

        if verb in {"use", "unlock"}:
            if len(parts) < 2:
                print("Use what?")
                return
            self.use_item(" ".join(parts[1:]))
            return

        if verb in {"torch", "key"}:
            self.use_item(verb)
            return

        if verb == "drink":
            self.drink_from_bar()
            return

        if verb in {"fight", "attack", "strike"}:
            if self.current_room == "forest_path" and not self.sword_taken:
                self.fight_raiders()
                return
            if self.current_room == "cave_chamber":
                self.resolve_cave_fight(use_torch=False)
                return
            print("There is nothing here to fight.")
            return

        if verb in {"pound", "gorilla", "chest"}:
            if self.current_room == "cave_chamber":
                self.resolve_cave_fight(use_torch=False)
                return
            print("That makes sense in the cave, not here.")
            return

        print("Unknown command. Type 'help' for options.")

    def fight_raiders(self):
        if self.current_room != "forest_path":
            print("No raiders are attacking here.")
            return

        if self.sword_taken:
            print("The raiders are already behind you. You are armed now.")
            return

        print("You step into the path and the raiders rush at once.")
        print("You are outnumbered and underprepared.")
        print("They cut you down before you can reach the trees.")
        print("You lose.")
        self.running = False
        self.state = "game over"

    def use_item(self, item_name):
        item = item_name.lower().strip()

        if item in {"key", "old key"}:
            if self.current_room != "root_cellar":
                print("There is no lock here to use the key on.")
                return

            if not any(i.name.lower() == "old key" for i in self.player.inventory):
                print("You do not have the key.")
                return

            if self.lock_open:
                print("The iron door is already open.")
                return

            self.lock_open = True
            self.current_room = "cave_entrance"
            print("You slip the key into the iron lock.")
            print("The iron door groans open.")
            self.show_current_room()
            return

        if item in {"torch", "light"}:
            if self.current_room != "cave_chamber":
                print("You don't have a use for that here.")
                return

            if not self.torch_taken:
                print("You don't have a torch.")
                return

            self.resolve_cave_fight(use_torch=True)
            return

        print(f"You can't use {item_name} here.")
        return

    def print_help(self):
        print("Commands:")
        print("  look       - inspect the room")
        print("  go <dir>   - move north, south, east, west")
        print("  take <item>- pick up an item")
        print("  inventory  - show your items")
        print("  speak      - talk to the bartender")
        print("  map        - show the world map")
        print("  drink      - buy a drink from the bartender")
        print("  use key    - unlock the cellar door")
        print("  use torch  - use the torch in the cave")
        print("  fight      - fight raiders or cave beasts")
        print("  help       - show this menu")
        print("  quit       - exit the game")

    def move(self, direction):
        room = self.rooms[self.current_room]

        if self.current_room == "tavern":
            if direction == "east":
                if not self.sword_taken:
                    self.trigger_forest_raid()
                    return
                self.current_room = "forest_path"
                self.show_current_room()
                return

            if direction == "north":
                self.current_room = "root_cellar"
                self.show_current_room()
                return

        if self.current_room == "root_cellar":
            if direction == "south":
                self.current_room = "tavern"
                self.show_current_room()
                return

            if direction == "north":
                if not self.lock_open:
                    print("A heavy iron door blocks the way.")
                    print("You need the key to unlock it.")
                    return
                self.current_room = "cave_entrance"
                self.show_current_room()
                if not self.torch_taken:
                    print("The cave looks very dark.")
                    print("You see glowing eyes in the black.")
                    print("If only you had some light...")
                return

        if self.current_room == "cave_entrance":
            if direction == "south":
                self.current_room = "root_cellar"
                self.show_current_room()
                return

            if direction == "north":
                if not self.torch_taken:
                    print("The cave is black as a grave.")
                    print("Glowing eyes blink in the dark.")
                    print("If only you had some light when you stepped in...")
                    print("The creatures surge from the dark and tear you apart.")
                    self.state = "game over"
                    self.running = False
                    return
                self.current_room = "cave_chamber"
                self.show_current_room()
                self.cave_fight()
                return

        if self.current_room == "cave_chamber":
            if direction == "south":
                self.current_room = "cave_entrance"
                self.show_current_room()
                return

            if direction == "east":
                if not self.sword_taken:
                    print("You cannot leave the cave without a weapon.")
                    return
                self.current_room = "tavern"
                self.show_current_room()
                return

        if self.current_room == "forest_path":
            if direction == "west":
                self.current_room = "tavern"
                self.show_current_room()
                return

        next_room = room.exits.get(direction)
        if not next_room:
            print("That way is closed to you.")
            return

        self.current_room = next_room
        self.show_current_room()

    def cave_fight(self):
        if self.current_room != "cave_chamber":
            return

        print("\nThe cave is alive with eyes and chittering teeth.")
        print("A beast lurches from the dark. Another follows.")
        print("You have a choice:")
        print("  - use torch")
        print("  - pound chest")
        print("The wrong choice will kill you.")
        print("The right choice is obvious to a fool with courage.")

    def resolve_cave_fight(self, use_torch=True):
        if self.current_room != "cave_chamber":
            print("There is no fight happening here.")
            return

        if use_torch:
            print("You swing the torch like a club.")
            print("The fire sputters and dies in your hand.")
            print("The creatures pounce in the smoke and darkness.")
            print("You die in the cave, surrounded by glowing eyes.")
            self.running = False
            self.state = "game over"
            return

        print("You throw out your chest and pound it like a gorilla.")
        print("The cave shakes with your raw, ridiculous confidence.")
        print("The creatures recoil, shriek, and collapse into the stone.")
        print("You find a sword resting in the beast's den.")
        self.cave_battle_done = True
        self.player.add_item(Item(name="sword", description="A heavy iron sword with an honest blade."))
        self.sword_taken = True
        self.current_room = "tavern"
        print("You drag yourself back to the tavern, breathless and victorious.")
        self.show_current_room()
        self.running = True

    def take_item(self, item_name):
        room = self.rooms[self.current_room]
        normalized = item_name.lower()

        if normalized == "old key":
            if self.current_room == "tavern":
                print("The key is not sitting in the room. The bartender keeps it.")
                return

        if normalized == "torch":
            if self.current_room == "root_cellar":
                if self.torch_taken:
                    print("You already took the torch.")
                    return
                self.torch_taken = True
                self.player.add_item(Item(name="torch", description="A rough timber torch. It burns with a steady orange flame."))
                room.items = [item for item in room.items if item.lower() != "torch"]
                print("You take the torch from the wall.")
                return

        if normalized == "coin":
            if self.current_room == "root_cellar":
                if any(item.name.lower() == "coin" for item in self.player.inventory):
                    print("You already took the coin.")
                    return
                self.player.add_item(Item(name="coin", description="A tarnished coin from a forgotten pocket."))
                self.player.add_coin(1)
                room.items = [item for item in room.items if item.lower() != "coin"]
                print("You pick up the coin and tuck it in your pocket.")
                print("A lucky little piece of metal.")
                return

        if normalized == "sword":
            if self.current_room == "cave_chamber":
                if self.sword_taken:
                    print("The sword is already yours.")
                    return
                self.player.add_item(Item(name="sword", description="A heavy iron sword with an honest blade."))
                self.sword_taken = True
                room.items = [item for item in room.items if item.lower() != "sword"]
                print("You lift the sword from the beast's den.")
                return

        if normalized == "hidden treasure":
            if self.current_room == "forest_path":
                self.treasure_found = True
                self.victory = True
                self.player.add_item(Item(name="hidden treasure", description="A gleaming relic, old as memory itself."))
                print("You uncover the hidden treasure at the end of the forest path.")
                print("The world exhales.")
                print("You win.")
                self.running = False
                self.state = "victory"
                return

        if normalized not in [item.lower() for item in room.items]:
            print(f"You cannot pick up {item_name}.")
            return

        room.items.remove(item_name)
        self.player.add_item(Item(name=item_name, description=item_name))
        print(f"You picked up {item_name}.")

    def drink_from_bar(self):
        if self.current_room != "tavern":
            print("There is no bar here.")
            return

        if self.player.coins <= 0:
            print('Bartender: "You have no coin left, friend."')
            print('Bartender: "The second drink is always the last one."')
            self.state = "game over"
            self.running = False
            return

        if self.drinks_bought == 0:
            if not self.player.spend_coin(1):
                print('Bartender: "No coin, no drink."')
                return

            self.drinks_bought += 1
            print('Bartender: "One drink, one favour. Here is the key."')
            self.player.add_item(Item(name="old key", description="A rusted iron key. It smells of damp stone."))
            self.bartender_key_given = True
            print("The bartender slides you a key beneath the bar.")
            print("You tuck it into your pocket and leave the glass on the counter.")
            return

        if self.drinks_bought >= 1:
            print('Bartender: "Ah. A second drink."')
            print('The room sways.')
            print('The bartender smiles too slowly.')
            print('The last thing you taste is iron and smoke.')
            print('You lose.')
            self.running = False
            self.state = "game over"
            return