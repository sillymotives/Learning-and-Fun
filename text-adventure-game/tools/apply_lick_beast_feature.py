from pathlib import Path


def replace_once(path, old, new):
    text = path.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected one anchor, found {count}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


interactions = Path('game/interactions.py')
replace_once(
    interactions,
    '''    "map": "crumpled map",
    "crumpled map": "crumpled map",
}
''',
    '''    "map": "crumpled map",
    "crumpled map": "crumpled map",
    "beast drink": "beast drink",
    "beast ale": "beast drink",
    "cave drink": "beast drink",
    "monster drink": "beast drink",
}
''',
)
replace_once(
    interactions,
    '''    "raider": "raiders", "raiders": "raiders", "the raiders": "raiders",
    "casks": "cask", "barrels": "cask", "barrel": "cask",
''',
    '''    "raider": "raiders", "raiders": "raiders", "the raiders": "raiders",
    "beast": "beasts", "beasts": "beasts", "the beast": "beasts", "the beasts": "beasts",
    "creature": "beasts", "creatures": "beasts", "cave beast": "beasts", "cave beasts": "beasts",
    "casks": "cask", "barrels": "cask", "barrel": "cask",
''',
)

bartender = Path('game/bartender_dialogue.py')
text = bartender.read_text(encoding='utf-8')
if 'BARTENDER_LICK_POOLS = {' in text:
    raise SystemExit('bartender lick pools already present')
lick_code = r'''BARTENDER_LICK_POOLS = {
    "normal": (
        ("You lick the bartender.", "Your tongue reports ale, smoke, and immediate professional consequences.", 'Bartender: "I am going to pretend that was a medical emergency."'),
        ("You lick the bartender again.", "He stops polishing the mug very slowly.", 'Bartender: "Once was evidence. Twice is a policy decision."'),
    ),
    "bootless": (
        ("You lick the bootless bartender.", "He looks down at his exposed sock, then back at you.", 'Bartender: "You stole my boot. Was that not enough intimacy for one evening?"'),
        ("You lick the bartender.", "His socked foot retreats half an inch on principle.", 'Bartender: "My boot is missing and somehow my tongue-related problems are increasing."'),
    ),
    "hostile": (
        ("You lick the hostile bartender.", "He becomes so still that the room develops weather.", 'Bartender: "That was your final complimentary boundary violation."'),
        ("You lick him despite the unmistakable hostility.", "His eye twitches once.", 'Bartender: "Customer service has ended. So has licking."'),
    ),
    "defeated": (
        ("You lick the defeated bartender.", "He looks toward the ruined chair as if asking it for strength.", 'Bartender: "I surrendered the fight. I did not surrender surface rights."'),
        ("You lick him after winning the fight.", "Victory has apparently taught you nothing.", 'Bartender: "The chair died for less than this."'),
    ),
    "damp": (
        ("You lick the damp bartender.", "Your tongue reports ale, rainwater, and a rapidly deteriorating social contract.", 'Bartender: "I was already wet. This is not assistance."'),
        ("You lick the bartender while he is still damp.", "This adds no useful moisture data.", 'Bartender: "Please stop quality-testing the weather on me."'),
    ),
    "fire": (
        ("You lick the burning bartender.", "This is immediately educational and extremely hot.", 'Bartender: "GOOD. Perhaps pain will teach you boundaries."'),
        ("You attempt to lick a man who is actively on fire.", "Your tongue files an urgent thermal complaint.", 'Bartender: "I admire the commitment. Not the judgement."'),
    ),
    "was_extinguished": (
        ("You lick the bartender.", "He remembers the extinguishing. Somehow this is now part of the same grievance.", 'Bartender: "You put me out once. Do not attempt temperature control with your mouth."'),
        ("You lick him with the confidence of someone who has already managed his fire badly.", 'Bartender: "I remember summer. I also remember you ending it."'),
    ),
    "flaming_boot": (
        ("You lick the bartender while holding his flaming boot.", "He watches the burning footwear instead of your tongue.", 'Bartender: "There are two emergencies here. You picked the wrong one."'),
        ("You lick him. His stolen boot continues burning nearby.", 'Bartender: "My shoe is on fire and somehow YOU are still the least normal object in the room."'),
    ),
    "map_owned": (
        ("You lick the bartender while carrying his terrible map.", 'Bartender: "Does the map show a route away from my face?"'),
        ("You lick him.", "The crumpled map offers no guidance for this encounter.", 'Bartender: "Cartography has failed us both."'),
    ),
    "cave_done": (
        ("You lick the bartender after surviving the cave.", 'Bartender: "The beasts let you live and this is what you did with the opportunity."'),
        ("You lick him with the confidence of a cave survivor.", 'Bartender: "Whatever was underground showed remarkable restraint."'),
    ),
    "treasure_found": (
        ("You lick the bartender while carrying legendary treasure.", 'Bartender: "Wealth has not improved you."'),
        ("You lick him after finding the treasure.", "Gold glints nearby. Dignity does not.", 'Bartender: "Rich enough to retire. Still licking staff."'),
    ),
    "beasts_thirsty": (
        ("You lick the bartender while thinking about the thirsty cave beasts.", 'Bartender: "Do not sample me while planning animal hydration."'),
        ("You lick him.", 'Bartender: "If this is how you diagnosed the cave creatures, I do not want the methodology."'),
    ),
    "beast_drink_given": (
        ("You lick the bartender after he gives you the beast drink.", 'Bartender: "I gave you wildlife refreshments. That was not permission."'),
        ("You lick him while carrying the cave animals' drink.", 'Bartender: "The mug is for them. Your tongue can remain unemployed."'),
    ),
    "beasts_asleep": (
        ("You lick the bartender after peacefully putting the cave beasts to sleep.", 'Bartender: "Kind to monsters. Like this to hospitality workers. Fascinating."'),
        ("You lick him.", "Somewhere below, two enormous beasts are sleeping more politely than you behave.", 'Bartender: "They are my favourite customers now."'),
    ),
    "raiders_defeated": (
        ("You lick the bartender after defeating the raiders.", 'Bartender: "The spoon people lost to this. Humiliating."'),
        ("You lick him.", 'Bartender: "Apparently combat success creates very strange confidence."'),
    ),
    "sword_taken": (
        ("You lick the bartender while armed with a sword.", 'Bartender: "Weapon on your hip. Tongue on staff. Heroism is complicated."'),
        ("You lick him.", "He checks where the sword is before deciding how offended to be.", 'Bartender: "At least you chose the less sharp implement."'),
    ),
    "torch_taken": (
        ("You lick the bartender while carrying the torch.", 'Bartender: "Given your history with fire, I am calling the tongue the safer tool."'),
        ("You lick him.", "He watches the torch suspiciously throughout.", 'Bartender: "One hazard at a time, please."'),
    ),
    "key_given": (
        ("You lick the bartender who trusted you with a cellar key.", 'Bartender: "I gave you access to the plot. This is my reward."'),
        ("You lick him.", 'Bartender: "Return to the locked-door portion of our relationship."'),
    ),
    "drank": (
        ("You lick the bartender after sampling his ale.", 'Bartender: "The drink was meant to satisfy the tasting requirement."'),
        ("You lick him.", "He gestures toward the bar full of things designed to be consumed.", 'Bartender: "So many beverages. One bartender. An extraordinary choice."'),
    ),
    "map_offered": (
        ("You lick the bartender while a map is still technically on offer.", 'Bartender: "The map costs one coin. Licking the vendor does not unlock a discount."'),
        ("You lick him.", 'Bartender: "This has not improved your purchasing position."'),
    ),
    "damp_bootless_flaming": (
        ("You lick the damp bartender.", "He glances at the flaming boot you stole from him.", 'Bartender: "You are holding my burning shoe. Why am I the thing being tasted?"'),
        ("You lick a cold, wet, one-boot-short bartender while his stolen boot burns nearby.", "His face passes through several kinds of disbelief.", 'Bartender: "This complaint no longer fits on one form."'),
    ),
    "fire_bootless_flaming": (
        ("You lick the burning, bootless bartender while his stolen boot is also on fire.", 'Bartender: "At last. A complete inventory of bad decisions."'),
        ("You lick him. Both bartender and boot continue burning.", 'Bartender: "There are TWO fires and you chose mouth contact."'),
    ),
    "damp_bootless": (
        ("You lick the damp, bootless bartender.", "Your tongue reports ale, rainwater, and sock-adjacent despair.", 'Bartender: "You stole my boot, soaked me, and now you are checking the seasoning?"'),
        ("You lick him while he stands wet and asymmetrically shod.", 'Bartender: "This evening has acquired a distressingly specific texture."'),
    ),
    "fire_bootless": (
        ("You lick the burning, bootless bartender.", "He looks offended that the flames did not deter you.", 'Bartender: "GOOD. Perhaps pain will teach you where my boot belongs."'),
        ("You lick him despite the fire and the missing footwear.", 'Bartender: "Hot, furious, one boot short, and somehow still serving you."'),
    ),
    "bootless_flaming": (
        ("You lick the bartender while holding his flaming stolen boot.", 'Bartender: "My footwear is burning in your possession and this is your follow-up?"'),
        ("You lick him. The burning boot crackles nearby.", 'Bartender: "Return shoe. Extinguish shoe. Stop tasting staff. Pick any order."'),
    ),
    "fire_was_extinguished": (
        ("You lick the bartender after setting him on fire again.", 'Bartender: "Last time you put me out. I see we are varying the technique."'),
        ("You lick the reignited bartender.", 'Bartender: "I remembered summer. I did not miss this part."'),
    ),
    "defeated_bootless": (
        ("You lick the defeated, bootless bartender.", 'Bartender: "You won the fight and stole the boot. There was no bonus objective here."'),
        ("You lick him.", "He looks at the ruined chair, then his exposed sock.", 'Bartender: "Victory has made you unbearable."'),
    ),
    "cave_bootless": (
        ("You lick the bartender after surviving the cave with his boot still missing.", 'Bartender: "The beasts showed better boundaries, and they have chittering teeth."'),
        ("You lick him.", 'Bartender: "You navigated a monster cave but cannot navigate my boot home."'),
    ),
    "treasure_bootless": (
        ("You lick the bartender while rich and still in possession of stolen-footwear history.", 'Bartender: "Legendary treasure. Missing boot. Licked employee. A heroic record."'),
        ("You lick him.", 'Bartender: "Gold does not reimburse socks."'),
    ),
    "beast_drink_bootless": (
        ("You lick the bartender after he gives you a drink for the beasts whose cave you entered with his boot.", 'Bartender: "I am helping the wildlife. You stole my shoe. Reflect on the moral hierarchy."'),
        ("You lick him while carrying the beast drink.", 'Bartender: "They tip badly. You behave worse. Somehow they are ahead."'),
    ),
}

BARTENDER_LICK_COMBINATIONS = (
    ("damp_bootless_flaming", frozenset({"damp", "bootless", "flaming_boot"})),
    ("fire_bootless_flaming", frozenset({"fire", "bootless", "flaming_boot"})),
    ("damp_bootless", frozenset({"damp", "bootless"})),
    ("fire_bootless", frozenset({"fire", "bootless"})),
    ("bootless_flaming", frozenset({"bootless", "flaming_boot"})),
    ("fire_was_extinguished", frozenset({"fire", "was_extinguished"})),
    ("defeated_bootless", frozenset({"defeated", "bootless"})),
    ("cave_bootless", frozenset({"cave_done", "bootless"})),
    ("treasure_bootless", frozenset({"treasure_found", "bootless"})),
    ("beast_drink_bootless", frozenset({"beast_drink_given", "bootless"})),
)

BARTENDER_LICK_PRIORITY = (
    "beasts_asleep",
    "fire",
    "damp",
    "flaming_boot",
    "bootless",
    "defeated",
    "hostile",
    "was_extinguished",
    "treasure_found",
    "cave_done",
    "beast_drink_given",
    "beasts_thirsty",
    "map_owned",
    "raiders_defeated",
    "sword_taken",
    "torch_taken",
    "key_given",
    "map_offered",
    "drank",
)


def bartender_lick_pool(flags):
    flags = frozenset(flags)
    for key, required in BARTENDER_LICK_COMBINATIONS:
        if required <= flags:
            return key, BARTENDER_LICK_POOLS[key]
    for key in BARTENDER_LICK_PRIORITY:
        if key in flags:
            return key, BARTENDER_LICK_POOLS[key]
    return "normal", BARTENDER_LICK_POOLS["normal"]
'''
if not text.rstrip().endswith('return None'):
    raise SystemExit('bartender_dialogue.py: unexpected file ending')
bartender.write_text(text.rstrip() + '\n\n\n' + lick_code + '\n', encoding='utf-8')


game = Path('game/game.py')
replace_once(
    game,
    '''    BARTENDER_DIALOGUE_RULES,
    bartender_interaction_overlay,
    choose_modifier,
    match_dialogue_rule,
)
''',
    '''    BARTENDER_DIALOGUE_RULES,
    bartender_interaction_overlay,
    bartender_lick_pool,
    choose_modifier,
    match_dialogue_rule,
)
''',
)
replace_once(
    game,
    '''        self.boot_on_fire = False
        self.item_interaction_count = 0
''',
    '''        self.boot_on_fire = False
        self.beast_pet_count = 0
        self.beasts_thirsty = False
        self.beast_drink_given = False
        self.beasts_asleep = False
        self.item_interaction_count = 0
''',
)
replace_once(
    game,
    '''        if self.boot_on_fire:
            flags.add("flaming_boot")
        return frozenset(flags)
''',
    '''        if self.boot_on_fire:
            flags.add("flaming_boot")
        if self.beasts_thirsty:
            flags.add("beasts_thirsty")
        if self.beast_drink_given:
            flags.add("beast_drink_given")
        if self.beasts_asleep:
            flags.add("beasts_asleep")
        return frozenset(flags)
''',
)
replace_once(
    game,
    '''    def speak_to_bartender(self):
        if self.current_room != "tavern":
            print("No one here is listening.")
            return

        flags = self._bartender_flags()
''',
    '''    def speak_to_bartender(self):
        if self.current_room != "tavern":
            print("No one here is listening.")
            return

        if self.beasts_thirsty and not self.beast_drink_given:
            print('Bartender: "For the cave things?"')
            print('Bartender: "Take this. They are awful tippers, but better customers than you."')
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
''',
)

beast_methods = r'''    def _beast_death(self, *lines):
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

'''
replace_once(
    game,
    '''    def flavour_action(self, verb, target_name):
''',
    beast_methods + '''    def flavour_action(self, verb, target_name):
''',
)
replace_once(
    game,
    '''        if not target:
            print(f"{verb.capitalize()} what?")
            return
        if target in {"map", "crumpled map"}:
''',
    '''        if not target:
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
        if target in {"map", "crumpled map"}:
''',
)
replace_once(
    game,
    '''    def _handle_stateful_interaction(self, verb, item, target):
        if self.current_room != "tavern":
            return False
''',
    '''    def _handle_stateful_interaction(self, verb, item, target):
        if self._handle_beast_item_interaction(verb, item, target):
            return True
        if self.current_room != "tavern":
            return False
''',
)
replace_once(
    game,
    '''                self.current_room = "cave_chamber"; self.show_current_room(); self.cave_fight(); return
''',
    '''                self.current_room = "cave_chamber"; self.show_current_room()
                if self.beasts_asleep:
                    print("The two cave beasts remain curled together, sleeping off their drink.")
                    print("One paw is still draped over the other's nose. Ridiculous.")
                    return
                if self.cave_battle_done:
                    print("The beast den is quiet now. Whatever happened here has stayed happened.")
                    return
                self.cave_fight(); return
''',
)
replace_once(
    game,
    '''    def cave_fight(self):
        if self.current_room != "cave_chamber":
            return
        print("\\nThe cave is alive with eyes and chittering teeth.")
''',
    '''    def cave_fight(self):
        if self.current_room != "cave_chamber":
            return
        if self.cave_battle_done:
            if self.beasts_asleep:
                print("The beasts are asleep in a warm, improbable heap. There is no fight left to have.")
            else:
                print("The beast den is quiet now. There is no fight left to have.")
            return
        print("\\nThe cave is alive with eyes and chittering teeth.")
''',
)

print('PASS: lick states and beast drink feature patch applied')
