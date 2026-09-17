from pathlib import Path

path = Path(__file__).resolve().parents[1] / "game" / "game.py"
text = path.read_text(encoding="utf-8")

old = '''        self.drinks_bought = 0
        self.failed_drink_attempts = 0
'''
new = '''        self.drinks_bought = 0
        self.failed_drink_attempts = 0
        self.visited_rooms = {"tavern"}
        self.map_offer_made = False
'''
if new not in text:
    if old not in text:
        raise SystemExit("state anchor not found")
    text = text.replace(old, new, 1)

old = '''    def show_current_room(self):
        room = self.rooms[self.current_room]
        print(f"\\n{room.name}")
        print(room.description)
        visible_items = room.items
        if self.current_room == "forest_path" and not self.raiders_defeated:
            visible_items = [item for item in room.items if item.lower() != "hidden treasure"]
        if visible_items:
            print(f"You see: {', '.join(visible_items)}")
        if room.exits:
            print(f"Exits: {', '.join(room.exits.keys())}")

    def show_map(self):
        print("\\nMap:")
        print("  [Tavern]")
        print("    |")
        print("    +-- [Forest Path] -- [Hidden Treasure]")
        print("    |")
        print("    +-- [Root Cellar] -- [Cave Entrance] -- [Cave Chamber]")
        print("         |")
        print("         +-- coin stash")
'''
new = '''    def _owns_map(self):
        return any(item.name.lower() == "crumpled map" for item in self.player.inventory)

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
        print(f"\\n{room.name}")
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

        print("\\nCrumpled Map:")
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
'''
if "    def _owns_map(self):\n" not in text:
    if old not in text:
        raise SystemExit("map block anchor not found")
    text = text.replace(old, new, 1)

old = '''        if verb in {"map", "m"}:
            self.show_map(); return
        if verb in {"speak", "talk", "chat"}:
'''
new = '''        if verb in {"map", "m"}:
            self.show_map(); return
        if verb in {"buy", "purchase"}:
            target = " ".join(parts[1:]).strip()
            if target in {"map", "the map", "crumpled map"}:
                self.buy_map(); return
            print("Buy what? Try 'buy map'."); return
        if verb in {"speak", "talk", "chat"}:
'''
if new not in text:
    if old not in text:
        raise SystemExit("command anchor not found")
    text = text.replace(old, new, 1)

old = '''    def flavour_action(self, verb, target_name):
        verb = normalize_verb(verb)
        target = normalize_target(target_name)
        if not target:
            print(f"{verb.capitalize()} what?")
            return
        lines = get_static_interaction(verb, None, target, self.current_room)
'''
new = '''    def flavour_action(self, verb, target_name):
        verb = normalize_verb(verb)
        target = normalize_target(target_name)
        if not target:
            print(f"{verb.capitalize()} what?")
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
'''
if new not in text:
    if old not in text:
        raise SystemExit("flavour anchor not found")
    text = text.replace(old, new, 1)

old = '''        if item in {"torch", "light"}:
            if self.current_room != "cave_chamber":
                print("You don't have a use for that here."); return
            if not self.torch_taken:
                print("You don't have a torch."); return
            self.resolve_cave_fight(use_torch=True); return
        print(f"You can't use {item_name} here.")
'''
new = '''        if item in {"torch", "light"}:
            if self.current_room != "cave_chamber":
                print("You don't have a use for that here."); return
            if not self.torch_taken:
                print("You don't have a torch."); return
            self.resolve_cave_fight(use_torch=True); return
        if item in {"map", "crumpled map"}:
            self.show_map(); return
        print(f"You can't use {item_name} here.")
'''
if new not in text:
    if old not in text:
        raise SystemExit("use item anchor not found")
    text = text.replace(old, new, 1)

old = '        print("  drink                   buy a drink at the tavern")\n'
new = old + '        print("  buy map                 spend a spare coin on suspicious cartography")\n'
if new not in text:
    if old not in text:
        raise SystemExit("help drink anchor not found")
    text = text.replace(old, new, 1)

old = '        print("  map                     show the world map")\n'
new = '        print("  map                     read your map, once you own one")\n'
if new not in text:
    if old not in text:
        raise SystemExit("help map anchor not found")
    text = text.replace(old, new, 1)

old = '''        if normalized == "coin" and self.current_room == "root_cellar":
            if any(item.name.lower() == "coin" for item in self.player.inventory):
                print("You already took the coin."); return
            self.player.add_item(Item("coin", "A tarnished coin from a forgotten pocket."))
            self.player.add_coin(1)
            room.items = [item for item in room.items if item.lower() != "coin"]
            print("You pick up the coin and tuck it in your pocket.")
            print("A lucky little piece of metal."); return
'''
new = '''        if normalized == "coin" and self.current_room == "root_cellar":
            if "coin" not in [item.lower() for item in room.items]:
                print("You already took the coin."); return
            self.player.add_coin(1)
            room.items = [item for item in room.items if item.lower() != "coin"]
            print("You pick up the coin and tuck it in your pocket.")
            print("A lucky little piece of metal."); return
'''
if new not in text:
    if old not in text:
        raise SystemExit("coin anchor not found")
    text = text.replace(old, new, 1)

old = '''            self.bartender_key_given = True
            print("The bartender slides you a key beneath the bar.")
            print("You tuck it into your pocket and leave the glass on the counter."); return
'''
new = '''            self.bartender_key_given = True
            print("The bartender slides you a key beneath the bar.")
            print("You tuck it into your pocket and leave the glass on the counter.")
            self._maybe_offer_map(); return
'''
if new not in text:
    if old not in text:
        raise SystemExit("first drink anchor not found")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
