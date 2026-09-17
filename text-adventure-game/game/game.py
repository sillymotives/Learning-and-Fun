import json
import sys
from textwrap import dedent
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
        self.bartender_boot_stolen = False
        self.bartender_hostile = False
        self.bartender_defeated = False
        self.bartender_talk_counts = {}
        self.bartender_on_fire = False
        self.item_interaction_count = 0

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

        print(dedent(r"""
    .       .                 .              .         .                 .            .              .
       .         .       .          .              .        .       .          .               .
    /        /        /        /        /        /        /        /        /        /        /        /

                      T H E   S E C R E T   T H A T   W A S N ' T
                              A   C O M E D I C   T E X T   A D V E N T U R E

                                              (      )
                                               )    (
                                          .---'------'---.
                                         /              /|
                                ________/______________/ |
                         ______/_______________________/  |
                    ____/_____________________________/   |
                   /   /\                            /|   |
                  /___/  \__________________________/ |   |
                  |  |    |                          | |   |
                  |  |    |      .------------.      | |   |
                  |  |    |      |  THE END   |      | |   |
                  |  |    |      |   TAVERN   |      | |   |
                  |  |    |      '-----+------'      | |   |
                  |  |    |            |             | |   |
                  |  |    |       _____|_____        | |   |
                  |  |    |      /             \      | |   |
                  |  |    |     / .-----------. \     | |   |
                  |  |    |    |  | NO REFUNDS|  |    | |   |
                  |  |    |    |  | AFTER THE |  |    | |   |
                  |  |    |    |  |SECOND DRINK| |    | |   |
                  |  |    |     \ '-----------' /     | |   |
                  |  |    |      \_____________/      | |   |
                  |  |    |                          | |   |
              .---|--|----|--------------------------|-|---|---.
             /    |  |    |   .--------.  .--------. | |   |    \
            /     |  |    |   |  .--.  |  |  .--.  | | |   |     \
           /      |  |    |   |  |()|  |  |  |()|  | | |   |      \
          /_______|__|____|___|__'--'__|__|__'--'__|_|_|___|_______\
          |       |  |    |   |        |  |        | | |   |       |
          |   o   |  |    |   |  ////  |  |  \\\\  | | |   |   o   |
          |  /|\  |  |    |   |        |  |        | | |   |  /|\  |
          |   |   |  |    |   '--------'  '--------' | |   |   |   |
          |  / \  |  |    |                          | |   |  / \  |
          |       |  |    |       .------------.      | |   |       |
          |       |  |    |       |            |      | |   |       |
          |       |  |    |       |    __      |      | |   |       |
          |       |  |    |       |   /  \     |      | |   |       |
          |       |  |    |       |   |  |     |      | |   |       |
          |       |  |    |       |   |  |   o |      | |   |       |
          |       |  |    |       |   |  |     |      | |   |       |
          |_______|__|____|_______|___|__|_____|______|_|___|_______|
             _/____\_              _/________\_              _/____\_
         ___/________\____________/____________\____________/________\___

                  "A forgotten treasure. A suspicious tavern. A very bad secret."
                         Enter bravely. Explore carefully. Read the labels.

    /        /        /        /        /        /        /        /        /        /        /        /
""").strip())

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
        while True:
            self.start_game()
            while self.running:
                command = input("> ").strip().lower()
                if not command:
                    continue
                self.handle_command(command)

            replay = input("Would you like to play again? (yes/no) ").strip().lower()
            if replay not in {"yes", "y"}:
                return

            self.__init__()

    def show_current_room(self):
        room = self.rooms[self.current_room]
        print(f"\n{room.name}")
        print(room.description)

        visible_items = room.items
        if self.current_room == "forest_path" and not self.raiders_defeated:
            visible_items = [item for item in room.items if item.lower() != "hidden treasure"]

        if visible_items:
            print(f"You see: {', '.join(visible_items)}")

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

        if self.bartender_on_fire:
            state = "fire"
            lines = [
                'Bartender: "FINALLY. This place has been freezing for twenty years."',
                'Bartender: "Do not put me out. I have never felt better."',
                'Bartender: "I am beginning to understand candles."',
            ]

        elif self.bartender_defeated:
            state = "defeated"
            lines = [
                'Bartender: "You won. The chair did not."',
                'Bartender: "Take your victory and stop looking at my furniture."',
                'Bartender: "I am exercising my right to be unhelpful."',
            ]

        elif self.bartender_boot_stolen:
            state = "boot"
            lines = [
                'Bartender: "My boot."',
                'Bartender: "You stole footwear from a man serving suspicious liquor."',
                'Bartender: "I can see my sock. This conversation is over."',
            ]

        elif self.sword_taken:
            state = "sword"
            lines = [
                'Bartender: "The forest has been noisy lately. Very noisy."',
                'Bartender: "East has had a lot of shouting and suspicious cutlery."',
                'Bartender: "Anyone claiming they found something secret is probably lying."',
            ]

        elif self.torch_taken:
            state = "torch"
            lines = [
                'Bartender: "Light lets you see a bad idea. It does not make it a good weapon."',
                'Bartender: "Some things in the dark are less impressed by fire than you would hope."',
                'Bartender: "Protect whatever keeps you from being eaten in the dark."',
            ]

        elif self.bartender_key_given:
            state = "key"
            lines = [
                'Bartender: "The cellar is colder than the ale. That is all I am saying."',
                'Bartender: "Old locks rarely guard empty rooms."',
                'Bartender: "If you hear breathing below, try not to assume it is yours."',
            ]

        else:
            state = "early"
            lines = [
                'Bartender: "Secrets around here tend to go down before they go out."',
                'Bartender: "One coin buys one drink. Sometimes one drink buys something else."',
                'Bartender: "The End has doors that reward nosy people."',
            ]

        index = self.bartender_talk_counts.get(state, 0)
        print(lines[index % len(lines)])
        self.bartender_talk_counts[state] = index + 1


    def steal_from_bartender(self):
        if self.current_room != "tavern":
            print("There is no bartender here to steal from.")
            return

        if self.bartender_defeated:
            print("The bartender watches you carefully.")
            print("You have already won. Leave his remaining footwear alone.")
            return

        if self.bartender_boot_stolen:
            print("You already stole his left boot.")
            print("He has moved the right one somewhere secure.")
            return

        print("You lean casually across the bar.")
        print("Your hand disappears below the counter.")
        print("You steal the bartender's left boot.")
        print("He is still wearing it.")
        print("The fact that this works seems to upset reality itself.")

        self.player.add_item(
            Item(
                name="bartender's left boot",
                description=(
                    "A large, battered tavern boot acquired through "
                    "methods best described as geometrically suspicious."
                ),
            )
        )
        self.bartender_boot_stolen = True
        self.bartender_hostile = True

        print('Bartender: "..."')
        print('Bartender: "Did you just steal my boot?"')
        print('Bartender: "I was WEARING that."')
        print("The bartender is now extremely hostile.")


    def fight_bartender(self):
        if self.current_room != "tavern":
            print("There is no bartender here to fight.")
            return

        if self.bartender_defeated:
            print("The bartender has already surrendered.")
            if self.bartender_on_fire:
                print("He is also still on fire, apparently by choice.")
            else:
                print("He points meaningfully at the remains of the chair.")
            return

        if not self.sword_taken:
            if self.bartender_on_fire:
                print("You square up to the burning bartender.")
                print("He snaps the bar towel once.")
                print("The towel immediately catches fire.")
                print('Bartender: "EVEN BETTER."')
                print("This somehow improves his technique.")
                print("Three seconds later, he folds you like flaming tavern laundry.")
            else:
                print("You square up to the bartender.")
                print("He slowly puts down the mug.")
                print("He snaps the bar towel once.")
                print("This somehow becomes a complete martial art.")
                print("Three seconds later, he folds you like tavern laundry.")

            print("You lose.")
            self.bartender_hostile = True
            self.running = False
            self.state = "game over"
            return

        if self.bartender_on_fire:
            print("You draw your sword.")
            print("The bartender is still enthusiastically on fire.")
            print("He looks at the blade and grins.")
            print("He reaches beneath the bar.")
            print("He produces an entire wooden chair.")
            print("The chair catches fire immediately.")
            print('Bartender: "NOW THIS IS HOSPITALITY."')
        else:
            print("You draw your sword.")
            print("The bartender looks at the blade, then at you.")
            print("He sighs and reaches beneath the bar.")
            print("He produces an entire wooden chair.")
            print("You have several questions. None survive first contact.")

        print("")
        print("Sword meets chair.")
        print("Chair meets ceiling.")
        print("A mug achieves low orbit.")
        print("The bartender finally raises both hands.")
        print('Bartender: "Fine. FINE. You win."')

        self.bartender_defeated = True
        self.bartender_hostile = False

        has_key = any(
            item.name.lower() == "old key"
            for item in self.player.inventory
        )

        if not has_key:
            self.player.add_item(
                Item(
                    name="old key",
                    description="A rusted iron key. It smells of damp stone.",
                )
            )
            self.bartender_key_given = True
            print("He slides the old cellar key across the bar.")
            print('Bartender: "Take it. And leave my furniture alone."')
        else:
            print(
                "You already have the cellar key, so he surrenders "
                "the only thing he has left: dignity."
            )

        self.running = True


    def trigger_forest_raid(self):
        self.raiders_seen = True
        self.current_room = "forest_path"
        self.show_current_room()
        print("\nThe forest path beyond the tavern door is watched.")
        print("The raiders leap from the bushes, looking far too pleased with themselves.")
        print('Raider captain: "Good news! We found the secret treasure."')
        print('Second raider: "It was not very secret. It was practically labelled treasure."')
        if not self.sword_taken:
            print("You do not feel safe going back out there without a weapon.")
        else:
            print("The raiders raise their spoons, forks, and one extremely questionable sword.")
        print("")
        print("The raiders block the path.")
        print("You can: 'fight raiders' or 'turn back'")

    def handle_command(self, command):
        parts = command.split()
        verb = parts[0]

        if command == "turn back":
            if self.current_room == "forest_path":
                self.move("west")
            else:
                print("There is nothing to turn back from.")
            return

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

        if verb in {"steal", "rob", "nick"}:
            target = " ".join(parts[1:]).strip()
            valid_targets = {
                "",
                "bartender",
                "the bartender",
                "from bartender",
                "from the bartender",
                "barkeep",
                "from barkeep",
            }

            if target not in valid_targets:
                print(f"You cannot steal {target}.")
                return

            self.steal_from_bartender()
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

        if command in {"turn back", "go back", "retreat"}:
            if self.current_room == "forest_path":
                self.move("west")
                return
            print("There is nowhere to retreat from here.")
            return

        if verb in {"take", "pickup"}:
            if len(parts) < 2:
                print("What do you want to take?")
                return
            item_name = " ".join(parts[1:])
            self.take_item(item_name)
            return

        if verb in {"use", "rub"}:
            if len(parts) < 2:
                if verb == "rub":
                    print("Rub what on what?")
                else:
                    print("Use what?")
                return

            request = " ".join(parts[1:]).strip()

            if " on " in request:
                item_name, target_name = request.split(" on ", 1)

                self.use_item_on(
                    item_name,
                    target_name,
                    action=verb,
                )
                return

            if verb == "rub":
                print("Rub what on what? Try 'rub <item> on <target>'.")
                return

            self.use_item(request)
            return

        if verb == "unlock":
            if len(parts) < 2:
                print("Unlock with what?")
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
            target = " ".join(parts[1:]).strip()

            if target in {
                "bartender",
                "the bartender",
                "barkeep",
                "innkeeper",
            }:
                self.fight_bartender()
                return

            if (
                self.current_room == "forest_path"
                and target in {"", "raider", "raiders", "the raiders"}
            ):
                self.fight_raiders()
                return

            if (
                self.current_room == "cave_chamber"
                and target in {
                    "",
                    "beast",
                    "beasts",
                    "creature",
                    "creatures",
                    "cave beast",
                    "cave beasts",
                }
            ):
                self.resolve_cave_fight(use_torch=False)
                return

            if target:
                print(f"There is no {target} here to fight.")
            else:
                print("Fight whom? Try 'fight <target>'.")
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
            if self.raiders_defeated:
                print("The raiders are already behind you. Their spoons are safely confiscated.")
                return

            print("You raise your sword. The raiders raise their spoons.")
            print("It is less of a battle and more of a very tense picnic.")
            print("The raiders surrender and drop the treasure they definitely did not steal.")
            print('Raider captain: "Please tell everyone we discovered it first. Secretly."')
            self.raiders_defeated = True
            self.show_current_room()
            return

        print("You step into the path and the raiders rush at once.")
        print("You are outnumbered and underprepared.")
        print("They cut you down before you can reach the trees.")
        print("You lose.")
        self.running = False
        self.state = "game over"

    def _carried_interaction_item(self, item_name):
        normalized = item_name.lower().strip()

        aliases = {
            "boot": "bartender's left boot",
            "left boot": "bartender's left boot",
            "bartender's boot": "bartender's left boot",
            "bartender's left boot": "bartender's left boot",
            "key": "old key",
            "old key": "old key",
            "light": "torch",
            "torch": "torch",
            "blade": "sword",
            "sword": "sword",
            "coin": "coin",
        }

        canonical = aliases.get(normalized, normalized)

        if canonical == "coin" and self.player.coins > 0:
            return "coin"

        if canonical == "torch" and self.torch_taken:
            return "torch"

        if canonical == "sword" and self.sword_taken:
            return "sword"

        for carried in self.player.inventory:
            if carried.name.lower() == canonical:
                return carried.name.lower()

        return None


    def ignite_bartender(self):
        if self.current_room != "tavern":
            print("There is no bartender here to set on fire.")
            return

        if self.bartender_on_fire:
            print("The bartender is already on fire.")
            print('Bartender: "Do not be greedy."')
            return

        self.bartender_on_fire = True
        self.bartender_hostile = True

        print("You carefully introduce the torch to the bartender.")
        print("His apron catches.")
        print("Then his sleeve.")
        print("Then, somehow, the rest of him.")
        print("")
        print("The bartender looks down at the flames.")
        print("He considers the situation.")
        print('Bartender: "FINALLY. This place has been freezing for twenty years."')
        print("He straightens his burning apron and looks noticeably happier.")
        print("He is now on fire and alarmingly enthusiastic about it.")


    def use_item_on(self, item_name, target_name, action="use"):
        item = self._carried_interaction_item(item_name)
        target = target_name.lower().strip()

        if target.startswith("the "):
            target = target[4:].strip()

        if not target:
            print("Use it on what?")
            return

        if item is None:
            print(f"You are not carrying {item_name.strip()}.")
            return

        bartender_targets = {
            "bartender",
            "barkeep",
            "innkeeper",
        }

        boot_targets = {
            "boot",
            "left boot",
            "bartender's boot",
            "bartender's left boot",
        }

        wall_targets = {
            "wall",
            "walls",
            "stone wall",
            "tavern wall",
        }

        if target in bartender_targets:
            if self.current_room != "tavern":
                print("There is no bartender here.")
                return

            if item == "torch":
                self.ignite_bartender()
                return

            if item == "sword":
                print("You apply the sword to the bartender.")
                print("This is generally known as starting a fight.")
                self.fight_bartender()
                return

            if item == "bartender's left boot":
                print("You rub the bartender's stolen left boot against his apron.")
                print('Bartender: "That is NOT the same as giving it back."')
                self.bartender_hostile = True
                return

            if item == "old key":
                print("You press the old key against the bartender.")
                print("He looks at it for slightly too long.")
                print('Bartender: "I recognise nothing."')
                print("He very obviously recognises it.")
                return

            if item == "coin":
                print("You press a coin against the bartender.")
                print("His hand opens automatically.")
                print("You pull the coin back.")
                print('Bartender: "Cruel."')
                return

        if item == "torch" and target in boot_targets:
            print("You apply the torch to the boot.")
            print("The smell of hot leather immediately fills the room.")
            print("Every decision that led here becomes questionable at once.")
            return

        if item == "bartender's left boot" and target in wall_targets:
            print("You polish the wall with the bartender's stolen left boot.")
            print("The wall becomes marginally shinier.")
            print("The boot becomes spiritually worse.")
            return

        action_word = "rub" if action == "rub" else "use"

        responses = [
            (
                f"You {action_word} the {item} on the {target}. "
                "Nothing improves."
            ),
            (
                f"You {action_word} the {item} on the {target}. "
                "The universe quietly records the incident."
            ),
            (
                f"You {action_word} the {item} on the {target}. "
                "Against all expectations, this reveals absolutely nothing."
            ),
            (
                f"You {action_word} the {item} on the {target}. "
                "Somewhere, an adventure-game designer develops a headache."
            ),
            (
                f"You {action_word} the {item} on the {target}. "
                "The target endures this with remarkable professionalism."
            ),
        ]

        print(
            responses[
                self.item_interaction_count % len(responses)
            ]
        )

        self.item_interaction_count += 1


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
        print("  look                    inspect the current room")
        print("  go <direction>          move north, south, east, or west")
        print("  take <item>             pick up something you can see")
        print("  use <item>              use an item normally")
        print("  use <item> on <target>  use one thing on another")
        print("  rub <item> on <target>  same idea, less dignity")
        print("  inventory               show what you are carrying")
        print("  speak                   talk to someone nearby")
        print("  drink                   buy a drink at the tavern")
        print("  steal                   attempt an ill-advised theft")
        print("  fight <target>          fight someone or something")
        print("  turn back               retreat from the forest")
        print("  map                     show the world map")
        print("  help                    show this command list")
        print("  quit                    leave the game")


    def move(self, direction):
        room = self.rooms[self.current_room]

        if self.current_room == "tavern":
            if direction == "east":
                if not self.sword_taken or not self.raiders_defeated:
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
                if not self.raiders_defeated:
                    print("The raiders still have the treasure. Deal with them first.")
                    return
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

        if self.bartender_hostile and not self.bartender_defeated:
            if self.bartender_on_fire and self.bartender_boot_stolen:
                print(
                    'Bartender: "You stole my boot AND set me on fire. '
                    'One coin is still one coin."'
                )
            elif self.bartender_on_fire:
                print(
                    'Bartender: "I appear to be on fire. '
                    'One coin is still one coin."'
                )
            elif self.bartender_boot_stolen:
                print(
                    'Bartender: "I still want my boot back. '
                    'But one coin is one coin."'
                )

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