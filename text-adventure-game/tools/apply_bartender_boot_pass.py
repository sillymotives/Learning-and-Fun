from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text, old, new, label):
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"{label} anchor not found")
    return text.replace(old, new, 1)


# Wire the dialogue engine and hidden flaming-boot cave route into Game.
path = ROOT / "game" / "game.py"
text = path.read_text(encoding="utf-8")

text = replace_once(
    text,
    '''from .interactions import (
    GENERIC_FALLBACKS,
    ROOM_FALLBACKS,
    ROOM_TARGETS,
    get_static_interaction,
    normalize_item,
    normalize_target,
    normalize_verb,
)
''',
    '''from .interactions import (
    GENERIC_FALLBACKS,
    ROOM_FALLBACKS,
    ROOM_TARGETS,
    get_static_interaction,
    normalize_item,
    normalize_target,
    normalize_verb,
)
from .bartender_dialogue import (
    BARTENDER_DIALOGUE_RULES,
    bartender_interaction_overlay,
    choose_modifier,
    match_dialogue_rule,
)
''',
    "dialogue imports",
)

text = replace_once(
    text,
    '''        self.bartender_talk_counts = {}
        self.bartender_on_fire = False
        self.bartender_extinguished = False
        self.item_interaction_count = 0
''',
    '''        self.bartender_talk_counts = {}
        self.bartender_dialogue_rules = BARTENDER_DIALOGUE_RULES
        self.bartender_on_fire = False
        self.bartender_extinguished = False
        self.bartender_was_extinguished = False
        self.boot_on_fire = False
        self.item_interaction_count = 0
''',
    "dialogue and boot state",
)

text = replace_once(
    text,
    '''    def speak_to_bartender(self):
        if self.current_room != "tavern":
            print("No one here is listening.")
            return
        if self.bartender_on_fire:
''',
    '''    def _bartender_flags(self):
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
        return frozenset(flags)

    def speak_to_bartender(self):
        if self.current_room != "tavern":
            print("No one here is listening.")
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
''',
    "dialogue engine wiring",
)

text = replace_once(
    text,
    '''            self.bartender_on_fire = False
            self.bartender_extinguished = True
            self.bartender_hostile = self.bartender_boot_stolen
''',
    '''            self.bartender_on_fire = False
            self.bartender_extinguished = True
            self.bartender_was_extinguished = True
            self.bartender_hostile = self.bartender_boot_stolen
''',
    "remember extinguish",
)

text = replace_once(
    text,
    '''        if self._handle_stateful_interaction(action, item, target):
            return

        if target == "bartender":
''',
    '''        if self._handle_stateful_interaction(action, item, target):
            return

        overlay = bartender_interaction_overlay(self._bartender_flags(), action, item, target)
        if overlay:
            self._print_interaction_lines(overlay)
            self._record_optional_interaction(action, item, target)
            return

        if target == "bartender":
''',
    "interaction overlay",
)

text = replace_once(
    text,
    '''        if item == "torch" and target in {"boot", "left boot", "bartender's boot", "bartender's left boot"}:
            print("You apply the torch to the boot.")
            print("The smell of hot leather immediately fills the room.")
            print("Every decision that led here becomes questionable at once.")
            self._record_optional_interaction(action, item, target)
            return
''',
    '''        if item == "torch" and target in {"boot", "left boot", "bartender's boot", "bartender's left boot"}:
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
''',
    "ignite boot",
)

text = replace_once(
    text,
    '''    def use_item(self, item_name):
        item = item_name.lower().strip()
        if item in {"key", "old key"}:
''',
    '''    def use_item(self, item_name):
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
''',
    "use boot route",
)

text = replace_once(
    text,
    '''    def resolve_cave_fight(self, use_torch=True):
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
        self.cave_battle_done = True
        if not any(item.name.lower() == "sword" for item in self.player.inventory):
            self.player.add_item(Item("sword", "A heavy iron sword with an honest blade."))
        self.sword_taken = True
        self.current_room = "tavern"
        print("You drag yourself back to the tavern, breathless and victorious.")
        self.show_current_room()
        self.running = True
''',
    '''    def _finish_cave_victory(self, return_line):
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
''',
    "cave boot resolution",
)

path.write_text(text, encoding="utf-8")


# Give the dialogue modifier layer awareness of the newly weaponized footwear.
path = ROOT / "game" / "bartender_dialogue.py"
text = path.read_text(encoding="utf-8")
text = replace_once(
    text,
    '''MODIFIER_LINES = {
    "treasure_found": (
''',
    '''MODIFIER_LINES = {
    "flaming_boot": (
        'Bartender: "My boot is on fire. I would like that entered into the complaint exactly as stated."',
        'Bartender: "You have weaponized my footwear. Hospitality was not designed for this."',
    ),
    "treasure_found": (
''',
    "flaming boot modifier",
)
path.write_text(text, encoding="utf-8")
