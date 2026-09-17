from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text, old, new, label):
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"{label} anchor not found")
    return text.replace(old, new, 1)


# 1. Item aliases: "map" must resolve to the actual carried item name.
path = ROOT / "game" / "interactions.py"
text = path.read_text(encoding="utf-8")
old = '''    "hidden treasure": "hidden treasure",
}'''
new = '''    "hidden treasure": "hidden treasure",
    "map": "crumpled map",
    "crumpled map": "crumpled map",
}'''
text = replace_once(text, old, new, "map alias")
path.write_text(text, encoding="utf-8")


# 2. Bespoke map-on-bartender flavour.
path = ROOT / "game" / "flavour_expansion.py"
text = path.read_text(encoding="utf-8")
old = '''    ("rub", "drink", "bartender", "tavern"): (
        "You rub a little ale into the bartender's sleeve.",
        "He looks down at the spreading stain.",
        'Bartender: "At least commit to the face if you are going to be strange."',
    ),
    ("use", "coin", "bartender face", "tavern"): ('''
new = '''    ("rub", "drink", "bartender", "tavern"): (
        "You rub a little ale into the bartender's sleeve.",
        "He looks down at the spreading stain.",
        'Bartender: "At least commit to the face if you are going to be strange."',
    ),
    ("use", "crumpled map", "bartender", "tavern"): (
        "You hold the crumpled map up to the bartender for professional review.",
        "He squints at it upside down for several seconds.",
        'Bartender: "Looks accurate."',
        "This is not reassuring.",
    ),
    ("rub", "crumpled map", "bartender", "tavern"): (
        "You rub the map against the bartender's apron.",
        "The map gains an ale stain exactly where a scale bar might have gone.",
        'Bartender: "Improved it."',
    ),
    ("use", "coin", "bartender face", "tavern"): ('''
text = replace_once(text, old, new, "map bartender flavour")
path.write_text(text, encoding="utf-8")


# 3. Reshape the actual world graph into a zig-zag.
path = ROOT / "data" / "story.json"
data = json.loads(path.read_text(encoding="utf-8"))
rooms = data["rooms"]
rooms["root_cellar"]["description"] = (
    "A cold cellar full of dust and old casks. Torch brackets line the stone wall, "
    "and a locked iron door waits to the east. The stairs climb south back to the tavern."
)
rooms["root_cellar"]["exits"] = {"south": "tavern", "east": "cave_entrance"}
rooms["cave_entrance"]["description"] = (
    "The tunnel bends east into a grim cave mouth. Everything smells of wet stone and old blood. "
    "The cellar lies west, while a thin trail of pale light leads north and deeper into the dark."
)
rooms["cave_entrance"]["exits"] = {"west": "root_cellar", "north": "cave_chamber"}
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


# 4. Stateful bartender, map layout, and navigation flavour.
path = ROOT / "game" / "game.py"
text = path.read_text(encoding="utf-8")

text = replace_once(
    text,
    '''        self.bartender_on_fire = False
        self.item_interaction_count = 0''',
    '''        self.bartender_on_fire = False
        self.bartender_extinguished = False
        self.item_interaction_count = 0''',
    "extinguished state",
)

old = '''        print("\\nCrumpled Map:")
        vertical = ["cave_chamber", "cave_entrance", "root_cellar", "tavern"]
        for index, room_id in enumerate(vertical[:-1]):
            if room_id not in visible:
                continue
            print(f"      {node(room_id)}")
            lower = vertical[index + 1]
            if lower in visible:
                print("          |")
        tavern_line = node("tavern")
        if "forest_path" in visible:
            tavern_line += f" -- {node('forest_path')}"
        print(tavern_line)
        if self.treasure_found:
            print("* Treasure discovered on the Forest Path.")'''
new = '''        print("\\nCrumpled Map:")
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
            print("* Treasure discovered on the Forest Path.")'''
text = replace_once(text, old, new, "map layout")

old = '''        if self.bartender_on_fire:
            state = "fire"
            lines = [
                'Bartender: "FINALLY. This place has been freezing for twenty years."',
                'Bartender: "Do not put me out. I have never felt better."',
                'Bartender: "I am beginning to understand candles."',
            ]
        elif self.bartender_defeated:'''
new = '''        if self.bartender_on_fire:
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
        elif self.bartender_defeated:'''
text = replace_once(text, old, new, "sad bartender dialogue")

old = '''        self.bartender_on_fire = True
        self.bartender_hostile = True
        print("You carefully introduce the torch to the bartender.")'''
new = '''        self.bartender_on_fire = True
        self.bartender_extinguished = False
        self.bartender_hostile = True
        print("You carefully introduce the torch to the bartender.")'''
text = replace_once(text, old, new, "reignite state")

old = '''        if item == "sword" and target == "bartender":
            print("You apply the sword to the bartender.")
            print("This is generally known as starting a fight.")
            self.fight_bartender()
            return True
        if verb == "rub" and item == "drink" and target == "bartender face":
            if self.bartender_on_fire and self.bartender_boot_stolen:
                print("The ale hisses against the bartender's burning face.")
                print('Bartender: "You stole my boot, set me on fire, and now you are moisturizing me with lager."')
                print('Bartender: "I miss normal customers."')
                self._record_optional_interaction(verb, item, target)
                return True
            if self.bartender_on_fire:
                print("The ale hisses against the bartender's face.")
                print('Bartender: "Refreshing."')
                self._record_optional_interaction(verb, item, target)
                return True
            if self.bartender_boot_stolen:
                print('Bartender: "You stole my boot and now you are moisturizing me with lager."')
                print('Bartender: "There are easier ways to become memorable."')
                self._record_optional_interaction(verb, item, target)
                return True
        return False'''
new = '''        if item == "sword" and target == "bartender":
            print("You apply the sword to the bartender.")
            print("This is generally known as starting a fight.")
            self.fight_bartender()
            return True
        if verb == "rub" and item == "drink" and target in {"bartender", "bartender face"} and self.bartender_on_fire:
            print("You rub ale across the burning bartender.")
            print("The flames hiss out in a cloud of extremely disappointed steam.")
            self.bartender_on_fire = False
            self.bartender_extinguished = True
            self.bartender_hostile = self.bartender_boot_stolen
            print('Bartender: "..."')
            print('Bartender: "I was warm."')
            if self.bartender_boot_stolen:
                print('Bartender: "And you still have my boot."')
            else:
                print('Bartender: "For one beautiful minute, I understood summer."')
            self._record_optional_interaction(verb, item, target)
            return True
        if verb == "rub" and item == "drink" and target == "bartender face" and self.bartender_boot_stolen:
            print('Bartender: "You stole my boot and now you are moisturizing me with lager."')
            print('Bartender: "There are easier ways to become memorable."')
            self._record_optional_interaction(verb, item, target)
            return True
        return False'''
text = replace_once(text, old, new, "drink extinguishes bartender")

old = '''    def move(self, direction):
        room = self.rooms[self.current_room]'''
new = '''    def _blocked_direction(self, direction):
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
        room = self.rooms[self.current_room]'''
text = replace_once(text, old, new, "blocked direction flavour")

old = '''        if self.current_room == "root_cellar":
            if direction == "south":
                self.current_room = "tavern"; self.show_current_room(); return
            if direction == "north":
                if not self.lock_open:
                    print("A heavy iron door blocks the way.")
                    print("You need the key to unlock it."); return
                self.current_room = "cave_entrance"; self.show_current_room()
                if not self.torch_taken:
                    print("The cave looks very dark.")
                    print("You see glowing eyes in the black.")
                    print("If only you had some light...")
                return
        if self.current_room == "cave_entrance":
            if direction == "south":
                self.current_room = "root_cellar"; self.show_current_room(); return'''
new = '''        if self.current_room == "root_cellar":
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
                self.current_room = "root_cellar"; self.show_current_room(); return'''
text = replace_once(text, old, new, "zig-zag movement")

old = '''        next_room = room.exits.get(direction)
        if not next_room:
            print("That way is closed to you."); return'''
new = '''        next_room = room.exits.get(direction)
        if not next_room:
            self._blocked_direction(direction); return'''
text = replace_once(text, old, new, "blocked direction fallback")

path.write_text(text, encoding="utf-8")
