import json
import sys
from pathlib import Path
from textwrap import dedent

from .items import Item
from .player import Player
from .world import Room
from .achievements import ACHIEVEMENTS
from .interactions import (
    GENERIC_FALLBACKS,
    ROOM_FALLBACKS,
    ROOM_TARGETS,
    TAVERN_STATE_INTERACTIONS,
    get_state_interaction,
    get_static_interaction,
    normalize_item,
    normalize_target,
    normalize_verb,
)
from .bartender_dialogue import (
    BARTENDER_DIALOGUE_RULES,
    bartender_interaction_overlay,
    bartender_lick_pool,
    choose_modifier,
    match_dialogue_rule,
)


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
        self.failed_drink_attempts = 0
        self.visited_rooms = {"tavern"}
        self.map_offer_made = False
        self.raiders_seen = False
        self.raiders_defeated = False
        self.cave_battle_done = False
        self.bartender_boot_stolen = False
        self.bartender_hostile = False
        self.bartender_defeated = False
        self.bartender_talk_counts = {}
        self.bartender_dialogue_rules = BARTENDER_DIALOGUE_RULES
        self.bartender_on_fire = False
        self.bartender_extinguished = False
        self.bartender_was_extinguished = False
        self.boot_on_fire = False
        self.beast_pet_count = 0
        self.beasts_thirsty = False
        self.beast_drink_given = False
        self.beasts_asleep = False
        self.item_interaction_count = 0
        self.optional_interaction_count = 0
        self.flavour_counts = {}
        self.interaction_targets_seen = set()
        self.achievements = set()
        self.boot_targets_seen = set()

    def _load_rooms(self):
        story_path = Path(__file__).resolve().parents[1] / "data" / "story.json"
        with open(story_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return {
            room_id: Room(
                name=room_data["name"],
                description=room_data["description"],
                exits=room_data.get("exits", {}),
                items=room_data.get("items", []),
            )
            for room_id, room_data in data["rooms"].items()
        }

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
                   /   /\\                            /|   |
                  /___/  \\__________________________/ |   |
                  |  |    |                          | |   |
                  |  |    |      .------------.      | |   |
                  |  |    |      |  THE END   |      | |   |
                  |  |    |      |   TAVERN   |      | |   |
                  |  |    |      '-----+------'      | |   |
                  |  |    |            |             | |   |
                  |  |    |       _____|_____        | |   |
                  |  |    |      /             \\      | |   |
                  |  |    |     / .-----------. \\     | |   |
                  |  |    |    |  | NO REFUNDS|  |    | |   |
                  |  |    |    |  | AFTER THE |  |    | |   |
                  |  |    |    |  |SECOND DRINK| |    | |   |
                  |  |    |     \\ '-----------' /     | |   |
                  |  |    |      \\_____________/      | |   |
                  |  |    |                          | |   |
              .---|--|----|--------------------------|-|---|---.
             /    |  |    |   .--------.  .--------. | |   |    \\
            /     |  |    |   |  .--.  |  |  .--.  | | |   |     \\
           /      |  |    |   |  |()|  |  |  |()|  | | |   |      \\
          /_______|__|____|___|__'--'__|__|__'--'__|_|_|___|_______\\
          |       |  |    |   |        |  |        | | |   |       |
          |   o   |  |    |   |  ////  |  |  \\\\\\  | | |   |   o   |
          |  /|\\  |  |    |   |        |  |        | | |   |  /|\\  |
          |   |   |  |    |   '--------'  '--------' | |   |   |   |
          |  / \\  |  |    |                          | |   |  / \\  |
          |       |  |    |       .------------.      | |   |       |
          |       |  |    |       |            |      | |   |       |
          |       |  |    |       |    __      |      | |   |       |
          |       |  |    |       |   /  \\     |      | |   |       |
          |       |  |    |       |   |  |     |      | |   |       |
          |       |  |    |       |   |  |   o |      | |   |       |
          |       |  |    |       |   |  |     |      | |   |       |
          |_______|__|____|_______|___|__|_____|______|_|___|_______|
             _/____\\_              _/________\\_              _/____\\_
         ___/________\\____________/____________\\____________/________\\___

                  "A forgotten treasure. A suspicious tavern. A very bad secret."
                         Enter bravely. Explore carefully. Read the labels.

    /        /        /        /        /        /        /        /        /        /        /        /
""").strip())
        print("\nThe rain hisses against the windows of a stone inn.")
        print("The walls are lined with cracked lanterns and old hunting trophies.")
        print("A burly barkeep wipes a mug with a weary stare.")
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
                if command:
                    self.handle_command(command)
            replay = input("Would you like to play again? (yes/no) ").strip().lower()
            if replay not in {"yes", "y"}:
                return
            self.__init__()

    def _owns_map(self):
        return any(item.name.lower() == "crumpled map" for item in self.player.inventory)

    def _has_inventory_item(self, name):
        wanted = name.lower()
        return any(item.name.lower() == wanted for item in self.player.inventory)

    def _maybe_offer_map(self):
        if (
            self.current_room != "tavern"
            or self.map_offer_made
            or self._owns_map()
            or self.drinks_bought < 1
            or self.player.coins < 1
        ):
            return
        self.map_offer_made = True
        print('Bartender: "Found another coin, did you?"')
        print('Bartender: "One coin gets you another drink..."')
        print("He produces a badly folded scrap of paper from beneath the bar.")
        print('Bartender: "...or a map."')
        print('Bartender: "Both contain information. One is considerably wetter."')
        print("You can: 'buy map' or 'drink'")

    def show_current_room(self):
        self.visited_rooms.add(self.current_room)
        room = self.rooms[self.current_room]
        print(f"\n{room.name}")
        print(room.description)
        visible_items = room.items
        if self.current_room == "forest_path" and not self.raiders_defeated:
            visible_items = [item for item in room.items if item.lower() != "hidden treasure"]
        if visible_items:
            print(f"You see: {', '.join(visible_items)}")
        if room.exits:
            print(f"Exits: {', '.join(room.exits.keys())}")
        self._maybe_offer_map()

    def show_map(self):
        if not self._owns_map():
            print("You do not have a map. Apparently cartography is a paid feature.")
            return

        visible = set(self.visited_rooms)
        for room_id in tuple(self.visited_rooms):
            visible.update(self.rooms[room_id].exits.values())

        names = {
            "tavern": "Tavern",
            "root_cellar": "Root Cellar",
            "cave_entrance": "Cave Entrance",
            "cave_chamber": "Cave Chamber",
            "forest_path": "Forest Path",
        }

        def node(room_id):
            if room_id not in visible:
                return ""
            if room_id not in self.visited_rooms:
                return "[?]"
            return f"[{names[room_id]}]"

        print("\nCrumpled Map:")
        if "cave_chamber" in visible:
            print(f"                    {node('cave_chamber')}")
            if "cave_entrance" in visible:
                print("                         |")
        if "root_cellar" in visible or "cave_entrance" in visible:
            left = node("root_cellar") if "root_cellar" in visible else ""
            right = node("cave_entrance") if "cave_entrance" in visible else ""
            if left and right:
                print(f"{left} -- {right}")
            else:
                print(left or right)
            if "tavern" in visible and "root_cellar" in visible:
                print("     |")
        tavern_line = node("tavern")
        if "forest_path" in visible:
            tavern_line += f" -- {node('forest_path')}"
        print(tavern_line)
        if self.treasure_found:
            print("* Treasure discovered on the Forest Path.")

    def buy_map(self):
        if self.current_room != "tavern":
            print("There is nobody here selling maps.")
            return
        if self._owns_map():
            print('Bartender: "You already bought the map. I admire the enthusiasm, not the accounting."')
            return
        if self.drinks_bought < 1:
            print('Bartender: "Buy a drink first. I need to establish your standards."')
            return
        if not self.player.spend_coin(1):
            print('Bartender: "One coin. Maps remain tragically non-charitable."')
            return
        self.player.add_item(Item(
            "crumpled map",
            "A cheaply drawn map. Someone has aggressively erased a section marked 'TREASURE'.",
        ))
        print("The bartender slides a badly folded map across the bar.")
        print('Bartender: "Do not blame me for the scale."')

    def _bartender_flags(self):
        flags = set()
        if self.bartender_on_fire:
            flags.add("fire")
        if self.bartender_extinguished:
            flags.add("damp")
        if self.bartender_was_extinguished:
            flags.add("was_extinguished")
        if self.bartender_boot_stolen:
            flags.add("bootless")
        if self.bartender_defeated:
            flags.add("defeated")
        if self.bartender_hostile:
            flags.add("hostile")
        if self.bartender_key_given:
            flags.add("key_given")
        if self._owns_map():
            flags.add("map_owned")
        if self.map_offer_made:
            flags.add("map_offered")
        if self.drinks_bought:
            flags.add("drank")
        if self.torch_taken:
            flags.add("torch_taken")
        if self.sword_taken:
            flags.add("sword_taken")
        if self.raiders_defeated:
            flags.add("raiders_defeated")
        if self.cave_battle_done:
            flags.add("cave_done")
        if self.treasure_found:
            flags.add("treasure_found")
        if self.boot_on_fire:
            flags.add("flaming_boot")
        if self.beasts_thirsty:
            flags.add("beasts_thirsty")
        if self.beast_drink_given:
            flags.add("beast_drink_given")
        if self.beasts_asleep:
            flags.add("beasts_asleep")
        return frozenset(flags)

    def speak_to_bartender(self):
        if self.current_room != "tavern":
            print("No one here is listening.")
            return

        if self.beasts_thirsty and not self.beast_drink_given:
            print('Bartender: "For the cave things?"')
            print('Bartender: "Take this drink. They are awful tippers, but better customers than you."')
            if self.bartender_boot_stolen:
                print('Bartender: "You stole my boot, and I am still helping the wildlife. Reflect on that."')
            elif self.bartender_on_fire:
                print('Bartender: "Take it before I accidentally warm it."')
            self.player.add_item(Item(
                "beast drink",
                "A heavy mug of suspiciously animal-friendly tavern drink. The bartender insists it is not the second drink.",
            ))
            self.beast_drink_given = True
            print("He slides a reinforced mug across the bar. It has two handles and no dignity.")
            return

        flags = self._bartender_flags()
        rule = match_dialogue_rule(flags)
        if rule is not None:
            index = self.bartender_talk_counts.get(rule.key, 0)
            print(rule.lines[index % len(rule.lines)])
            modifier = choose_modifier(flags, rule.required, index)
            if modifier:
                print(modifier)
            self.bartender_talk_counts[rule.key] = index + 1
            return

        if self.bartender_on_fire:
            state = "fire"
            lines = [
                'Bartender: "FINALLY. This place has been freezing for twenty years."',
                'Bartender: "Do not put me out. I have never felt better."',
                'Bartender: "I am beginning to understand candles."',
            ]
        elif self.bartender_extinguished:
            state = "damp"
            lines = [
                'Bartender: "I was warm."',
                'Bartender: "For one beautiful minute, I understood summer."',
                'Bartender: "Please stop helping. I am damp now."',
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
        self.player.add_item(Item("bartender's left boot", "A large, battered tavern boot acquired through geometrically suspicious methods."))
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
            print("He is also still on fire, apparently by choice." if self.bartender_on_fire else "He points meaningfully at the remains of the chair.")
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
        print("Sword meets chair.")
        print("Chair meets ceiling.")
        print("A mug achieves low orbit.")
        print("The bartender finally raises both hands.")
        print('Bartender: "Fine. FINE. You win."')
        self.bartender_defeated = True
        self.bartender_hostile = False
        if not any(item.name.lower() == "old key" for item in self.player.inventory):
            self.player.add_item(Item("old key", "A rusted iron key. It smells of damp stone."))
            self.bartender_key_given = True
            print("He slides the old cellar key across the bar.")
            print('Bartender: "Take it. And leave my furniture alone."')
        else:
            print("You already have the cellar key, so he surrenders the only thing he has left: dignity.")
        self.running = True

    def trigger_forest_raid(self):
        self.raiders_seen = True
        self.current_room = "forest_path"
        self.show_current_room()
        print("\nThe forest path beyond the tavern door is watched.")
        print("The raiders leap from the bushes, looking far too pleased with themselves.")
        print('Raider captain: "Good news! We found the secret treasure."')
        print('Second raider: "It was not very secret. It was practically labelled treasure."')
        print("You do not feel safe going back out there without a weapon." if not self.sword_taken else "The raiders raise their spoons, forks, and one extremely questionable sword.")
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
            self.print_help(); return
        if verb in {"map", "m"}:
            self.show_map(); return
        if verb in {"buy", "purchase"}:
            target = " ".join(parts[1:]).strip()
            if target in {"map", "the map", "crumpled map"}:
                self.buy_map(); return
            print("Buy what? Try 'buy map'."); return
        if verb in {"speak", "talk", "chat"}:
            self.speak_to_bartender(); return
        if verb in {"steal", "rob", "nick"}:
            target = " ".join(parts[1:]).strip()
            valid = {"", "bartender", "the bartender", "from bartender", "from the bartender", "barkeep", "from barkeep"}
            if target not in valid:
                print(f"You cannot steal {target}."); return
            self.steal_from_bartender(); return
        if verb in {"look", "l"}:
            self.show_current_room(); return
        if verb in {"inventory", "inv", "i"}:
            self.player.show_inventory(); return
        if verb in {"go", "move"}:
            if len(parts) < 2:
                print("Where do you want to go?"); return
            self.move(parts[1]); return
        if command in {"turn back", "go back", "retreat"}:
            if self.current_room == "forest_path":
                self.move("west"); return
            print("There is nowhere to retreat from here."); return
        if verb in {"inspect", "examine", "poke", "prod", "kick", "lick", "taste", "pet", "pat", "stroke", "sit"}:
            if verb == "sit" and len(parts) == 1:
                self.flavour_action("sit", "floor")
                return
            target = " ".join(parts[1:]).strip()
            if target.startswith("on "):
                target = target[3:].strip()
            if not target:
                print(f"{normalize_verb(verb).capitalize()} what?")
                return
            self.flavour_action(verb, target)
            return

        if verb in {"take", "pickup"}:
            if len(parts) < 2:
                print("What do you want to take?"); return
            self.take_item(" ".join(parts[1:])); return
        if verb in {"use", "rub"}:
            if len(parts) < 2:
                print("Rub what on what?" if verb == "rub" else "Use what?"); return
            request = " ".join(parts[1:]).strip()
            if " on " in request:
                item_name, target_name = request.split(" on ", 1)
                self.use_item_on(item_name, target_name, action=verb); return
            if verb == "rub":
                print("Rub what on what? Try 'rub <item> on <target>'."); return
            self.use_item(request); return
        if verb == "unlock":
            if len(parts) < 2:
                print("Unlock with what?"); return
            self.use_item(" ".join(parts[1:])); return
        if verb in {"torch", "key"}:
            self.use_item(verb); return
        if verb == "drink" and len(parts) > 1:
            requested = normalize_item(" ".join(parts[1:]))
            if requested == "impossible drink":
                self.drink_impossible_drink()
                return
        if verb == "drink":
            self.drink_from_bar(); return
        if verb in {"fight", "attack", "strike"}:
            target = " ".join(parts[1:]).strip()
            if target in {"bartender", "the bartender", "barkeep", "innkeeper"}:
                self.fight_bartender(); return
            if self.current_room == "forest_path" and target in {"", "raider", "raiders", "the raiders"}:
                self.fight_raiders(); return
            if self.current_room == "cave_chamber" and target in {"", "beast", "beasts", "creature", "creatures", "cave beast", "cave beasts"}:
                self.resolve_cave_fight(use_torch=False); return
            print(f"There is no {target} here to fight." if target else "Fight whom? Try 'fight <target>'."); return
        if verb in {"pound", "gorilla", "chest"}:
            if self.current_room == "cave_chamber":
                self.resolve_cave_fight(use_torch=False); return
            print("That makes sense in the cave, not here."); return
        print("Unknown command. Type 'help' for options.")

    def fight_raiders(self):
        if self.current_room != "forest_path":
            print("No raiders are attacking here."); return
        if self.sword_taken:
            if self.raiders_defeated:
                print("The raiders are already behind you. Their spoons are safely confiscated."); return
            print("You raise your sword. The raiders raise their spoons.")
            print("It is less of a battle and more of a very tense picnic.")
            print("The raiders surrender and drop the treasure they definitely did not steal.")
            print('Raider captain: "Please tell everyone we discovered it first. Secretly."')
            self.raiders_defeated = True
            self.show_current_room(); return
        print("You step into the path and the raiders rush at once.")
        print("You are outnumbered and underprepared.")
        print("They cut you down before you can reach the trees.")
        print("You lose.")
        self.running = False
        self.state = "game over"

    def _print_interaction_lines(self, lines):
        for line in lines:
            print(line)

    def _unlock_achievement(self, key):
        if key in self.achievements:
            return
        self.achievements.add(key)
        print(f"[Achievement unlocked: {ACHIEVEMENTS[key]}]")
        if key == "training_arc":
            print("100 pushups. 100 situps. A 10 km run. Every single day. Probably.")

    def _evaluate_interaction_achievements(self, verb, item, target):
        if verb == "rub" and item == "drink" and target == "bartender face":
            self._unlock_achievement("bartender_moisturized")
        if verb == "lick" and target == "wall":
            self._unlock_achievement("wall_licked")
        if item == "coin" and target == "wall":
            self._unlock_achievement("attempted_capitalism_on_stone")
        if item == "bartender's left boot":
            self.boot_targets_seen.add(target)
            if len(self.boot_targets_seen) >= 5:
                self._unlock_achievement("applied_science")
        if self.optional_interaction_count >= 100:
            self._unlock_achievement("training_arc")

    def _record_optional_interaction(self, verb, item, target):
        self.optional_interaction_count += 1
        if item:
            self.interaction_targets_seen.add((item, target))
        self._evaluate_interaction_achievements(verb, item, target)

    def _interaction_fallback(self, verb, item, target):
        room_lines = ROOM_FALLBACKS.get(self.current_room, ())
        pool = room_lines + GENERIC_FALLBACKS
        key = (
            normalize_verb(verb),
            normalize_item(item) if item else None,
            normalize_target(target),
            self.current_room,
            "fallback",
        )
        index = self.flavour_counts.get(key, 0)
        prefix = f"You {normalize_verb(verb)}"
        if item:
            prefix += f" the {normalize_item(item)} on the {normalize_target(target)}."
        else:
            prefix += f" the {normalize_target(target)}."
        print(prefix)
        print(pool[index % len(pool)])
        self.flavour_counts[key] = index + 1
        self._record_optional_interaction(
            normalize_verb(verb),
            normalize_item(item) if item else None,
            normalize_target(target),
        )

    def _beast_death(self, *lines):
        for line in lines:
            print(line)
        print("You lose.")
        self.running = False
        self.state = "game over"

    def _handle_beast_flavour(self, verb, target):
        if self.current_room != "cave_chamber" or target != "beasts":
            return False

        if self.beasts_asleep:
            sleepy = {
                "inspect": (
                    "The two enormous cave beasts are curled together in the corner, fast asleep.",
                    "One has a paw draped over the other's nose.",
                    "They are infuriatingly sweet and adorable.",
                ),
                "pet": (
                    "You gently scratch one sleeping beast behind the ear.",
                    "Its back foot thumps once. The other beast snuggles closer without waking.",
                ),
                "poke": (
                    "You poke one sleeping beast very gently.",
                    "It sleepily pulls the other closer with one paw. Your experiment becomes wholesome against its will.",
                ),
                "lick": (
                    "You consider licking a sleeping beast.",
                    "The narrator notices your recent personal growth and quietly closes that option.",
                ),
                "kick": (
                    "You raise a foot toward the sleeping beasts.",
                    "No. They are adorable now. Character development has limits, but it does have limits.",
                ),
                "sit": (
                    "You sit beside the sleeping beasts.",
                    "One enormous tail settles across your boots like a furry safety bar.",
                ),
            }
            lines = sleepy.get(verb)
            if lines:
                self._print_interaction_lines(lines)
                self._record_optional_interaction(verb, None, target)
                return True
            return False

        if self.cave_battle_done:
            print("The live beasts are no longer here to bother. The cave remembers them with several dents.")
            self._record_optional_interaction(verb, None, target)
            return True

        if verb == "inspect":
            print("You study the two cave beasts instead of immediately making a worse decision.")
            print("Too many teeth. Too many bright eyes. Huge paws. Dry tongues.")
            print("One of them watches your hands with suspicious concentration.")
            self._record_optional_interaction(verb, None, target)
            return True

        if verb == "pet":
            if self.beast_pet_count == 0:
                self.beast_pet_count = 1
                print("You extend a cautious hand toward the nearest beast.")
                print("It sniffs your fingers. The chittering pauses.")
                print("Then, impossibly, it leans its enormous head into your palm.")
                print("The second beast looks offended that it did not think of this first.")
            elif self.beast_pet_count == 1:
                self.beast_pet_count = 2
                self.beasts_thirsty = True
                print("You pet the beast again.")
                print("This time both of them crowd around your hands, bumping each other aside.")
                print("One nudges your empty palm, then stares pointedly at its own dry tongue.")
                print("The other does the same.")
                print("Oh. They are thirsty.")
                print("The monster problem has become a hydration problem.")
                print("Perhaps the bartender has something suitable.")
            else:
                print("You pet the beasts again. They accept this as established policy.")
                print("Both stare at your empty hands. Yes. Still thirsty.")
            self._record_optional_interaction(verb, None, target)
            return True

        if verb == "poke":
            self._record_optional_interaction(verb, None, target)
            self._beast_death(
                "You poke the nearest beast.",
                "It looks down at your finger.",
                "Then at you.",
                "Experiment concluded.",
                "Peer review is immediate and involves mauling.",
            )
            return True

        if verb == "lick":
            self._record_optional_interaction(verb, None, target)
            self._beast_death(
                "You lick the nearest cave beast.",
                "The beast freezes.",
                "It looks genuinely offended.",
                "The second beast appears embarrassed on your behalf.",
                "Then they maul you together, having found common ground.",
            )
            return True

        if verb == "kick":
            self._record_optional_interaction(verb, None, target)
            self._beast_death(
                "You kick a cave beast.",
                "For a heartbeat, nothing happens.",
                "Then the cave produces a practical demonstration of why kicking apex predators is poor methodology.",
                "You are mauled with excellent footwork.",
            )
            return True

        if verb == "sit":
            self._record_optional_interaction(verb, None, target)
            self._beast_death(
                "You attempt to sit on a cave beast.",
                "The beast objects to becoming furniture.",
                "The objection is upheld by teeth.",
                "Your seating experiment ends in a mauling.",
            )
            return True

        return False

    def _handle_beast_item_interaction(self, verb, item, target):
        if self.current_room != "cave_chamber" or target != "beasts":
            return False

        if self.beasts_asleep:
            print(f"You carefully {verb} the {item} near the sleeping beasts.")
            print("Neither wakes. One tiny ear flicks, which is more response than this plan deserves.")
            self._record_optional_interaction(verb, item, target)
            return True

        if self.cave_battle_done:
            print("The beasts are gone. Your item has missed its audience.")
            self._record_optional_interaction(verb, item, target)
            return True

        if item == "bartender's left boot":
            self.resolve_cave_boot()
            return True

        if item == "crumpled map":
            print("You hold the crumpled map out to the beasts.")
            print("One sniffs it, takes the corner delicately between its teeth, and chews.")
            print("It has eaten the least accurate piece of geography on the page.")
            print("The map may actually have improved.")
            self._record_optional_interaction(verb, item, target)
            return True

        if item == "beast drink":
            if not self.beasts_thirsty:
                print("You offer the reinforced mug to the beasts.")
                print("They sniff it suspiciously. Apparently even monsters dislike unsolicited beverages.")
                self._record_optional_interaction(verb, item, target)
                return True
            print("You set the reinforced mug down between the beasts.")
            print("The first beast sniffs it.")
            print("The second shoves its face in beside it.")
            print("There is aggressive slurping.")
            print("Then less aggressive slurping.")
            print("Then a pair of enormous, satisfied sighs.")
            print("Both beasts circle twice and curl up together in the corner.")
            print("One puts a paw over the other's nose.")
            print("They are, infuriatingly, sweet and adorable.")
            print("The battle is over. You win through hydration.")
            print("A heavy iron sword lies beside their nest. You take it without waking them.")
            self.player.remove_item("beast drink")
            self.beasts_thirsty = False
            self.beasts_asleep = True
            self._record_optional_interaction(verb, item, target)
            self._finish_cave_victory("You return to the tavern carrying a sword and the knowledge that the monsters were just thirsty.")
            return True

        if item == "torch":
            self.resolve_cave_fight(use_torch=True)
            return True

        if item == "old key":
            print("You offer the old key to the beasts.")
            print("One sniffs it and sneezes. Locksmithing remains unavailable as a dialogue option.")
            self._record_optional_interaction(verb, item, target)
            return True

        if item == "coin":
            print("You offer a coin to the beasts.")
            print("One paws it once, decides it has terrible nutritional value, and returns to considering you instead.")
            self._record_optional_interaction(verb, item, target)
            return True

        return False

    def flavour_action(self, verb, target_name):
        verb = normalize_verb(verb)
        target = normalize_target(target_name)
        if not target:
            print(f"{verb.capitalize()} what?")
            return
        if self._handle_beast_flavour(verb, target):
            return
        if verb == "lick" and target in {"bartender", "bartender face"} and self.current_room == "tavern":
            lick_key, pool = bartender_lick_pool(self._bartender_flags())
            counter_key = ("bartender_lick", lick_key)
            index = self.flavour_counts.get(counter_key, 0)
            self._print_interaction_lines(pool[index % len(pool)])
            self.flavour_counts[counter_key] = index + 1
            self._record_optional_interaction(verb, None, target)
            return
        if self.current_room == "tavern" and target in {"bartender", "bartender face"}:
            lines = get_state_interaction(
                TAVERN_STATE_INTERACTIONS,
                self._bartender_flags(),
                verb,
                None,
                target,
            )
            if lines:
                self._print_interaction_lines(lines)
                self._record_optional_interaction(verb, None, target)
                return
        if target in {"map", "crumpled map"}:
            if not self._owns_map():
                print("You do not have a map to bother.")
                return
            if verb == "inspect":
                print("The map has clearly been drawn by someone who knew the area well and cartography poorly.")
                print("Someone has aggressively erased a section marked 'TREASURE'. Subtle.")
                self._record_optional_interaction(verb, None, "map")
                return
            if verb == "lick":
                print("You lick the map.")
                print("It tastes faintly of ale and administrative negligence.")
                self._record_optional_interaction(verb, None, "map")
                return
        lines = get_static_interaction(verb, None, target, self.current_room)
        if lines:
            self._print_interaction_lines(lines)
            self._record_optional_interaction(verb, None, target)
            return
        self._interaction_fallback(verb, None, target)

    def _available_interaction_item(self, item_name):
        canonical = normalize_item(item_name)
        if canonical == "drink":
            if self.current_room == "tavern" and self.drinks_bought >= 1:
                return "drink"
            return None
        if canonical == "mug":
            if self.current_room == "tavern":
                return "mug"
            return None
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
            print("There is no bartender here to set on fire."); return
        if self.bartender_on_fire:
            print("The bartender is already on fire.")
            print('Bartender: "Do not be greedy."'); return
        self.bartender_on_fire = True
        self.bartender_extinguished = False
        self.bartender_hostile = True
        print("You carefully introduce the torch to the bartender.")
        print("His apron catches.")
        print("Then his sleeve.")
        print("Then, somehow, the rest of him.")
        print("The bartender looks down at the flames.")
        print("He considers the situation.")
        print('Bartender: "FINALLY. This place has been freezing for twenty years."')
        print("He straightens his burning apron and looks noticeably happier.")
        print("He is now on fire and alarmingly enthusiastic about it.")

    def _handle_stateful_interaction(self, verb, item, target):
        if self._handle_beast_item_interaction(verb, item, target):
            return True
        if self.current_room != "tavern":
            return False
        if (
            item == "bartender's left boot"
            and target == "bartender"
            and self.boot_on_fire
            and self.bartender_extinguished
        ):
            print("You offer the bartender his left boot.")
            print("It is on fire.")
            print("He looks at the boot.")
            print("He looks at you.")
            print("He looks back at the boot.")
            print('Bartender: "That is not what restitution means."')
            print("The cuff brushes his apron.")
            print("FWOOMPH.")
            self.bartender_on_fire = True
            self.bartender_extinguished = False
            self.bartender_hostile = True
            print("He closes his eyes.")
            print('Bartender: "...warm."')
            print('Bartender: "I hate that this helped."')
            self._record_optional_interaction(verb, item, target)
            return True
        if item == "torch" and target == "bartender":
            self.ignite_bartender()
            return True
        if item == "sword" and target == "bartender":
            print("You apply the sword to the bartender.")
            print("This is generally known as starting a fight.")
            self.fight_bartender()
            return True
        if verb == "rub" and item == "drink" and target in {"bartender", "bartender face"} and self.bartender_on_fire:
            print("You rub ale across the burning bartender.")
            print("The ale hisses across him as the flames collapse into a cloud of extremely disappointed steam.")
            self.bartender_on_fire = False
            self.bartender_extinguished = True
            self.bartender_was_extinguished = True
            self.bartender_hostile = self.bartender_boot_stolen
            print('Bartender: "..."')
            print('Bartender: "I was warm."')
            if self.bartender_boot_stolen:
                print('Bartender: "You stole my boot, set me on fire, and now you put me out."')
                print('Bartender: "I miss normal customers."')
            else:
                print('Bartender: "Refreshing. I hate it."')
                print('Bartender: "For one beautiful minute, I understood summer."')
            self._record_optional_interaction(verb, item, target)
            return True
        if verb == "rub" and item == "drink" and target == "bartender face" and self.bartender_boot_stolen:
            print('Bartender: "You stole my boot and now you are moisturizing me with lager."')
            print('Bartender: "There are easier ways to become memorable."')
            self._record_optional_interaction(verb, item, target)
            return True
        return False

    def use_item_on(self, item_name, target_name, action="use"):
        requested = normalize_item(item_name)
        item = self._available_interaction_item(item_name)
        target = normalize_target(target_name)
        action = normalize_verb(action)

        if not target:
            print("Use it on what?")
            return
        if item is None:
            if requested in {"drink", "mug"}:
                print(f"That {requested} is not available here.")
            else:
                print(f"You are not carrying {item_name.strip()}.")
            return

        if self._handle_stateful_interaction(action, item, target):
            return

        if self.current_room == "tavern" and target in {"bartender", "bartender face"}:
            lines = get_state_interaction(
                TAVERN_STATE_INTERACTIONS,
                self._bartender_flags(),
                action,
                item,
                target,
            )
            if lines:
                self._print_interaction_lines(lines)
                self._record_optional_interaction(action, item, target)
                return

        overlay = bartender_interaction_overlay(self._bartender_flags(), action, item, target)
        if overlay:
            self._print_interaction_lines(overlay)
            self._record_optional_interaction(action, item, target)
            return

        if target == "bartender":
            if self.current_room != "tavern":
                print("There is no bartender here.")
                return
            if item == "bartender's left boot":
                print("You rub the bartender's stolen left boot against his apron.")
                print('Bartender: "That is NOT the same as giving it back."')
                self.bartender_hostile = True
                self._record_optional_interaction(action, item, target)
                return

        if item == "torch" and target in {"boot", "left boot", "bartender's boot", "bartender's left boot"}:
            if not any(carried.name.lower() == "bartender's left boot" for carried in self.player.inventory):
                print("You do not currently possess a boot worthy of ignition.")
                return
            print("You apply the torch to the bartender's stolen left boot.")
            print("The leather catches with appalling enthusiasm.")
            print("The boot is now on fire.")
            print("Against every principle of footwear, this feels useful.")
            self.boot_on_fire = True
            self._record_optional_interaction(action, item, target)
            return

        lines = get_static_interaction(action, item, target, self.current_room)
        if lines:
            self._print_interaction_lines(lines)
            self._record_optional_interaction(action, item, target)
            return

        self._interaction_fallback(action, item, target)

    def use_item(self, item_name):
        item = item_name.lower().strip()
        canonical = normalize_item(item_name)
        if canonical == "bartender's left boot":
            if not any(carried.name.lower() == "bartender's left boot" for carried in self.player.inventory):
                print("You do not have the bartender's boot.")
                return
            if self.current_room == "cave_chamber":
                self.resolve_cave_boot()
                return
            if self.boot_on_fire:
                print("You brandish the flaming stolen boot.")
                print("Nothing nearby is prepared to acknowledge this as a normal object.")
            else:
                print("You brandish the stolen boot with unjustified confidence.")
            return
        if item in {"key", "old key"}:
            if self.current_room != "root_cellar":
                print("There is no lock here to use the key on."); return
            if not any(i.name.lower() == "old key" for i in self.player.inventory):
                print("You do not have the key."); return
            if self.lock_open:
                print("The iron door is already open."); return
            self.lock_open = True
            self.current_room = "cave_entrance"
            print("You slip the key into the iron lock.")
            print("The iron door groans open.")
            self.show_current_room(); return
        if item in {"torch", "light"}:
            if self.current_room != "cave_chamber":
                print("You don't have a use for that here."); return
            if not self.torch_taken:
                print("You don't have a torch."); return
            self.resolve_cave_fight(use_torch=True); return
        if item in {"map", "crumpled map"}:
            self.show_map(); return
        print(f"You can't use {item_name} here.")

    def print_help(self):
        print("Commands:")
        print("  look                    inspect the current room")
        print("  go <direction>          move north, south, east, or west")
        print("  take <item>             pick up something you can see")
        print("  use <item>              use an item normally")
        print("  use <item> on <target>  use one thing on another")
        print("  rub <item> on <target>  same idea, less dignity")
        print("  inspect <target>        examine scenery or people")
        print("  poke/kick/lick <target> bother the scenery")
        print("  pet <target>            attempt diplomacy through touching")
        print("  sit [on <target>]       sit somewhere questionable")
        print("  inventory               show what you are carrying")
        print("  speak                   talk to someone nearby")
        print("  drink                   buy a drink at the tavern")
        print("  buy map                 spend a spare coin on suspicious cartography")
        print("  steal                   attempt an ill-advised theft")
        print("  fight <target>          fight someone or something")
        print("  turn back               retreat from the forest")
        print("  map                     read your map, once you own one")
        print("  help                    show this command list")
        print("  quit                    leave the game")

    def _blocked_direction(self, direction):
        lines = {
            "tavern": {
                "south": "You consider walking behind the bar. The bartender's stare closes that route more effectively than a door.",
                "west": "The west wall offers a hunting trophy, damp stone, and a complete absence of doorway.",
            },
            "root_cellar": {
                "north": "You head north and meet a regiment of old casks. They refuse to form a corridor.",
                "west": "The cellar wall is cold, damp, and insufficiently interested in becoming an exit.",
            },
            "cave_entrance": {
                "east": "You try east. Wet stone has already occupied the position.",
                "south": "South is mostly rock and the growing suspicion that caves do not respect compass symmetry.",
            },
            "cave_chamber": {
                "east": "The eastern wall is jagged stone with enough claw marks to discourage further negotiation.",
                "west": "West ends immediately in geology. Geology declines your appeal.",
            },
            "forest_path": {
                "north": "The pines close ranks to the north. Apparently the forest has zoning laws.",
                "south": "South becomes mud, brambles, and a firm suggestion to use the actual path.",
                "east": "The path frays into trees to the east. None of them appear interested in being a road.",
            },
        }
        fallback = f"You try {direction}. The scenery has other plans."
        print(lines.get(self.current_room, {}).get(direction, fallback))

    def move(self, direction):
        room = self.rooms[self.current_room]
        if self.current_room == "tavern":
            if direction == "east":
                if not self.sword_taken or not self.raiders_defeated:
                    self.trigger_forest_raid(); return
                self.current_room = "forest_path"; self.show_current_room(); return
            if direction == "north":
                self.current_room = "root_cellar"; self.show_current_room(); return
        if self.current_room == "root_cellar":
            if direction == "south":
                self.current_room = "tavern"; self.show_current_room(); return
            if direction == "east":
                if not self.lock_open:
                    print("A heavy iron door blocks the way east.")
                    print("You need the key to unlock it."); return
                self.current_room = "cave_entrance"; self.show_current_room()
                if not self.torch_taken:
                    print("The cave looks very dark.")
                    print("You see glowing eyes in the black.")
                    print("If only you had some light...")
                return
        if self.current_room == "cave_entrance":
            if direction == "west":
                self.current_room = "root_cellar"; self.show_current_room(); return
            if direction == "north":
                if not self.torch_taken:
                    print("The cave is black as a grave.")
                    print("Glowing eyes blink in the dark.")
                    print("If only you had some light when you stepped in...")
                    print("The creatures surge from the dark and tear you apart.")
                    self.state = "game over"; self.running = False; return
                self.current_room = "cave_chamber"; self.show_current_room()
                if self.beasts_asleep:
                    print("The two cave beasts remain curled together, sleeping off their drink.")
                    print("One paw is still draped over the other's nose. Ridiculous.")
                    return
                if self.cave_battle_done:
                    print("The beast den is quiet now. Whatever happened here has stayed happened.")
                    return
                self.cave_fight(); return
        if self.current_room == "cave_chamber":
            if direction == "south":
                self.current_room = "cave_entrance"; self.show_current_room(); return
            if direction == "east":
                if not self.sword_taken:
                    print("You cannot leave the cave without a weapon."); return
                self.current_room = "tavern"; self.show_current_room(); return
        if self.current_room == "forest_path" and direction == "west":
            self.current_room = "tavern"; self.show_current_room(); return
        next_room = room.exits.get(direction)
        if not next_room:
            self._blocked_direction(direction); return
        self.current_room = next_room
        self.show_current_room()

    def cave_fight(self):
        if self.current_room != "cave_chamber":
            return
        if self.cave_battle_done:
            if self.beasts_asleep:
                print("The beasts are asleep in a warm, improbable heap. There is no fight left to have.")
            else:
                print("The beast den is quiet now. There is no fight left to have.")
            return
        print("\nThe cave is alive with eyes and chittering teeth.")
        print("A beast lurches from the dark. Another follows.")
        print("You have a choice:")
        print("  - use torch")
        print("  - pound chest")
        print("The wrong choice will kill you.")
        print("The right choice is obvious to a fool with courage.")

    def _finish_cave_victory(self, return_line):
        self.cave_battle_done = True
        if not any(item.name.lower() == "sword" for item in self.player.inventory):
            self.player.add_item(Item("sword", "A heavy iron sword with an honest blade."))
        self.sword_taken = True
        self.current_room = "tavern"
        print(return_line)
        self.show_current_room()
        self.running = True

    def resolve_cave_boot(self):
        if self.current_room != "cave_chamber":
            print("There is no cave fight here requiring experimental footwear.")
            return
        if not self.boot_on_fire:
            print("You raise the bartender's left boot like a sacred weapon.")
            print("The beasts stop.")
            print("One of them grimaces.")
            print("The other looks genuinely disappointed in you.")
            print("For one magnificent second, you think this is working.")
            print("Then they maul you.")
            print("Carefully avoiding the boot.")
            print("You lose.")
            self.running = False
            self.state = "game over"
            return
        print("You thrust the flaming boot into the darkness.")
        print("The cave fills with the smell of burning leather, old ale, and decisions.")
        print("The chittering stops.")
        print("One beast recoils. The other swallows hard.")
        print("They look at the boot. They look at you. They look at each other.")
        print("One of them makes a tiny, deeply unhappy noise.")
        print("The beasts leave.")
        print("Not frightened. Just... unwell.")
        print("They abandon a sword, presumably because nausea has priorities.")
        self._finish_cave_victory("You return to the tavern carrying victory and one still-burning boot.")

    def resolve_cave_fight(self, use_torch=True):
        if self.current_room != "cave_chamber":
            print("There is no fight happening here."); return
        if use_torch:
            print("You swing the torch like a club.")
            print("The fire sputters and dies in your hand.")
            print("The creatures pounce in the smoke and darkness.")
            print("You die in the cave, surrounded by glowing eyes.")
            self.running = False; self.state = "game over"; return
        print("You throw out your chest and pound it like a gorilla.")
        print("The cave shakes with your raw, ridiculous confidence.")
        print("The creatures recoil, shriek, and collapse into the stone.")
        print("You find a sword resting in the beast's den.")
        self._finish_cave_victory("You drag yourself back to the tavern, breathless and victorious.")

    def take_item(self, item_name):
        room = self.rooms[self.current_room]
        normalized = item_name.lower()
        if normalized == "old key" and self.current_room == "tavern":
            print("The key is not sitting in the room. The bartender keeps it."); return
        if normalized == "torch" and self.current_room == "root_cellar":
            if self.torch_taken:
                print("You already took the torch."); return
            self.torch_taken = True
            self.player.add_item(Item("torch", "A rough timber torch. It burns with a steady orange flame."))
            room.items = [item for item in room.items if item.lower() != "torch"]
            print("You take the torch from the wall."); return
        if normalized == "coin" and self.current_room == "root_cellar":
            if "coin" not in [item.lower() for item in room.items]:
                print("You already took the coin."); return
            self.player.add_coin(1)
            room.items = [item for item in room.items if item.lower() != "coin"]
            print("You pick up the coin and tuck it in your pocket.")
            print("A lucky little piece of metal."); return
        if normalized == "sword" and self.current_room == "cave_chamber":
            if self.sword_taken:
                print("The sword is already yours."); return
            self.player.add_item(Item("sword", "A heavy iron sword with an honest blade."))
            self.sword_taken = True
            room.items = [item for item in room.items if item.lower() != "sword"]
            print("You lift the sword from the beast's den."); return
        if normalized == "hidden treasure" and self.current_room == "forest_path":
            if not self.raiders_defeated:
                print("The raiders still have the treasure. Deal with them first."); return
            self.treasure_found = True
            self.victory = True
            self.player.add_item(Item("hidden treasure", "A gleaming relic, old as memory itself."))
            print("You uncover the hidden treasure at the end of the forest path.")
            print("The world exhales.")
            print("You win.")
            self.running = False
            self.state = "victory"; return
        if normalized not in [item.lower() for item in room.items]:
            print(f"You cannot pick up {item_name}."); return
        room.items.remove(item_name)
        self.player.add_item(Item(item_name, item_name))
        print(f"You picked up {item_name}.")

    def _handle_drink_obsession_milestone(self, attempt):
        if attempt == 5:
            print("[Drink obsession milestone] Five attempts. This is becoming a pattern.")
            return
        if attempt == 10:
            print("[Drink obsession milestone] Ten attempts. This has officially become a habit.")
            return
        if attempt == 20:
            print("[Drink obsession milestone] Twenty attempts. Reality has filed a complaint.")
            print("There is a small pop.")
            if not self._has_inventory_item("impossible drink"):
                self.player.add_item(Item(
                    "Impossible Drink",
                    "A sealed drink summoned by repeated refusal to accept local beverage availability.",
                ))
            print("A sealed drink appears in your hand.")
            print("It is cold. It is real.")
            print("The universe has capitulated.")
            return
        if attempt == 50:
            print("[Drink obsession milestone] Fifty attempts.")
            if self._has_inventory_item("impossible drink"):
                print("You are carrying a perfectly valid ending.")
                print("You have chosen instead to keep trying to drink the atmosphere.")
            else:
                print("Somewhere, the bartender feels a disturbance in the ale.")
            return
        if attempt == 100:
            print("[Drink obsession milestone] Attempt 100.")
            if self._has_inventory_item("impossible drink"):
                print("You still have a perfectly valid ending in your pocket.")
            print("This is no longer thirst.")
            print("This is a completed research programme.")
            self._unlock_achievement("longitudinal_study")

    def _drink_in_wrong_place(self):
        self.failed_drink_attempts += 1
        attempt = self.failed_drink_attempts

        openings = (
            "You reach for a glass that is emphatically not here.",
            "You raise an imaginary pint to absolutely nobody.",
            "You stare hopefully at your empty hand.",
            "You mime taking a long drink from the surrounding atmosphere.",
            "You check the immediate area for emergency ale. Again.",
            "You perform the ancient ritual of looking thirsty at architecture.",
        )
        thoughts = (
            '"Am I an alcoholic?"',
            '"Damn... was there something else in that first drink? Kind of want to, er... drink."',
            '"This is becoming less of a request and more of a lifestyle."',
            '"I do understand that drinks normally require... drinks, right?"',
            '"Maybe the tavern has ruined beverages everywhere else for me."',
            '"I am beginning to miss that deeply suspicious ale."',
            '"At some point thirst became a side quest."',
        )
        room_lines = {
            "root_cellar": "The cellar contains several liquids. Every single one is a terrible candidate.",
            "cave_entrance": "The cave entrance offers darkness, damp stone, and absolutely no table service.",
            "cave_chamber": "The cave contains monsters, bones, and no functioning bar staff.",
            "forest_path": "The forest remains stubbornly unlicensed.",
        }
        print(f"Attempt {attempt}: {openings[(attempt - 1) % len(openings)]}")
        print(thoughts[(attempt - 1) % len(thoughts)])
        print(room_lines.get(self.current_room, "The universe declines to provide a drink here."))
        self._handle_drink_obsession_milestone(attempt)

    def drink_impossible_drink(self):
        if not self._has_inventory_item("impossible drink"):
            print("You do not have an Impossible Drink.")
            return

        print("You break the seal.")
        print("It tastes like every drink you tried to summon and none of them.")
        print("Rain. Smoke. Ale. Cold stone. Something faintly impossible.")
        print("The tavern, the cave, the forest, the treasure... all of it seems suddenly very far away.")
        print("You were never looking for the secret.")
        print("You were thirsty.")
        print("And now you are not.")
        print("You win.")
        self.player.remove_item("Impossible Drink")
        self.victory = True
        self.state = "victory"
        self.running = False

    def drink_from_bar(self):
        if self.current_room != "tavern":
            self._drink_in_wrong_place(); return
        if self.bartender_hostile and not self.bartender_defeated:
            if self.bartender_on_fire and self.bartender_boot_stolen:
                print('Bartender: "You stole my boot AND set me on fire. One coin is still one coin."')
            elif self.bartender_on_fire:
                print('Bartender: "I appear to be on fire. One coin is still one coin."')
            elif self.bartender_boot_stolen:
                print('Bartender: "I still want my boot back. But one coin is one coin."')
        if not self.player.spend_coin(1):
            print('Bartender: "You have no coin left, friend."')
            if self.drinks_bought:
                print('Bartender: "The second drink may be the last one, but I am not running a tab."')
            else:
                print('Bartender: "Come back when your pockets make a more convincing argument."')
            return
        if self.drinks_bought == 0:
            self.drinks_bought += 1
            print('Bartender: "One drink, one favour. Here is the key."')
            self.player.add_item(Item("old key", "A rusted iron key. It smells of damp stone."))
            self.bartender_key_given = True
            print("The bartender slides you a key beneath the bar.")
            print("You tuck it into your pocket and leave the glass on the counter.")
            self._maybe_offer_map(); return
        self.drinks_bought += 1
        print('Bartender: "Ah. A second drink."')
        print("The room sways.")
        print("The bartender smiles too slowly.")
        print("The last thing you taste is iron and smoke.")
        print("You lose.")
        self.running = False
        self.state = "game over"
