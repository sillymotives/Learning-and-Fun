from dataclasses import dataclass


@dataclass(frozen=True)
class DialogueRule:
    key: str
    required: frozenset[str]
    lines: tuple[str, ...]


def _rule(key, required, *lines):
    return DialogueRule(key, frozenset(required), tuple(lines))


BARTENDER_DIALOGUE_RULES = (
    _rule("reignited_memory", {"fire", "was_extinguished"},
          'Bartender: "No. You put me out last time. I remember summer now."',
          'Bartender: "I know how this ends. Warmth, betrayal, then lager."'),
    _rule("reignited_memory_boot", {"fire", "was_extinguished", "bootless"},
          'Bartender: "You put me out last time and you still have my boot. Pick a grievance."',
          'Bartender: "Fire again? Fine. My sock was getting cold."'),
    _rule("reignited_memory_map", {"fire", "was_extinguished", "map_owned"},
          'Bartender: "Check the map. Does it mark where you extinguished my happiness last time?"',
          'Bartender: "I remember summer. Your map remembers nothing useful."'),
    _rule("reignited_memory_defeated", {"fire", "was_extinguished", "defeated"},
          'Bartender: "You beat me, put me out, then set me alight again. This is not a customer journey."',
          'Bartender: "I surrendered once. Apparently the weather did not."'),
    _rule("reignited_memory_sword", {"fire", "was_extinguished", "sword_taken"},
          'Bartender: "You have the sword and I have fire again. I dislike this sequel already."',
          'Bartender: "Last time you put me out. This time keep the blade away from the upholstery."'),
    _rule("reignited_memory_treasure", {"fire", "was_extinguished", "treasure_found"},
          'Bartender: "You found legendary treasure and still came back to relight me. Priorities."',
          'Bartender: "Rich, victorious, and somehow still managing my temperature badly."'),
    _rule("damp_boot_map", {"damp", "bootless", "map_owned"},
          'Bartender: "I am cold, wet, and missing a boot. I need you to understand how specific my hatred has become."',
          'Bartender: "The map says tavern. My sock says marshland. You caused both."'),
    _rule("fire_boot_map", {"fire", "bootless", "map_owned"},
          'Bartender: "The map says this is a tavern. Does it mention the part where I am on fire and missing a boot?"',
          'Bartender: "If that map has a route to my left boot, now would be an excellent time."'),
    _rule("defeated_boot_map", {"defeated", "bootless", "map_owned"},
          'Bartender: "You beat me, stole my boot, then bought my map. Most people just leave a bad review."',
          'Bartender: "The map was one coin. My dignity appears to have been complimentary."'),
    _rule("sword_boot_map", {"sword_taken", "bootless", "map_owned"},
          'Bartender: "Sword. Map. My boot. You have assembled the worst adventuring kit I have ever seen."',
          'Bartender: "One of those belongs to me. Hint: it is not the sword, unfortunately."'),
    _rule("treasure_boot_map", {"treasure_found", "bootless", "map_owned"},
          'Bartender: "You found the treasure. Wonderful. My boot remains the greater mystery."',
          'Bartender: "Gold, map, stolen footwear. Your inventory tells a troubling story."'),
    _rule("damp_defeated_boot", {"damp", "defeated", "bootless"},
          'Bartender: "First violence. Then theft. Then moisture. You fight like weather."',
          'Bartender: "I surrendered. My boot surrendered. Apparently dryness did not survive either."'),
    _rule("fire_defeated_boot", {"fire", "defeated", "bootless"},
          'Bartender: "I lost the fight, the boot, and now several workplace fire regulations."',
          'Bartender: "Defeated and burning. Still technically open for business."'),
    _rule("damp_sword_boot", {"damp", "sword_taken", "bootless"},
          'Bartender: "Put the sword down. Return the boot. Bring me a towel. In that order."',
          'Bartender: "You look armed. I look damp. Somehow I am still the professional here."'),
    _rule("fire_sword_boot", {"fire", "sword_taken", "bootless"},
          'Bartender: "You have a sword, my boot, and access to fire. I have made staffing mistakes."',
          'Bartender: "Do not wave the sword. I am already providing enough dramatic lighting."'),
    _rule("damp_map_sword", {"damp", "map_owned", "sword_taken"},
          'Bartender: "The map is wet, I am wet, and you have a sword. Cartography has become threatening."',
          'Bartender: "If you cut the map in half, you will have two equally bad maps."'),
    _rule("fire_map_sword", {"fire", "map_owned", "sword_taken"},
          'Bartender: "Keep the map away from me unless you want considerably less map."',
          'Bartender: "Sword in one hand, flammable cartography in the other. Adventuring."'),
    _rule("defeated_map_sword", {"defeated", "map_owned", "sword_taken"},
          'Bartender: "You won the fight. The map still lost the argument with scale."',
          'Bartender: "I surrendered to the sword, not to your navigation skills."'),
    _rule("treasure_map_sword", {"treasure_found", "map_owned", "sword_taken"},
          'Bartender: "So the sword worked, the map worked, and somehow my business model survives."',
          'Bartender: "You found the treasure. I am taking partial credit for the paper."'),
    _rule("damp_treasure_map", {"damp", "treasure_found", "map_owned"},
          'Bartender: "You found treasure and brought me back dampness. I preferred the gold part."',
          'Bartender: "Apparently the map led you to riches and me to pneumonia."'),
    _rule("fire_treasure_map", {"fire", "treasure_found", "map_owned"},
          'Bartender: "Legendary treasure, cheap map, burning innkeeper. A complete tourism package."',
          'Bartender: "Please admire your treasure from a fire-safe distance."'),
    _rule("defeated_treasure_map", {"defeated", "treasure_found", "map_owned"},
          'Bartender: "You beat me and found the treasure. I am thrilled to be a useful sequence of setbacks."',
          'Bartender: "Keep the gold. I am charging extra for emotional damages next time."'),
    _rule("damp_key_map", {"damp", "key_given", "map_owned"},
          'Bartender: "I gave you a key and sold you a map. You gave me hypothermia."',
          'Bartender: "This exchange has become economically difficult to defend."'),
    _rule("fire_key_map", {"fire", "key_given", "map_owned"},
          'Bartender: "Key, map, fire. One of those services was not advertised."',
          'Bartender: "The map is non-refundable. The flames are apparently also non-refundable."'),
    _rule("boot_key_map", {"bootless", "key_given", "map_owned"},
          'Bartender: "I gave you the key, sold you the map, and somehow paid with a boot."',
          'Bartender: "This transaction has drifted well outside standard hospitality."'),
    _rule("defeated_key_map", {"defeated", "key_given", "map_owned"},
          'Bartender: "You fought me for a key you already had access to and still bought the map."',
          'Bartender: "I admire commitment. From over here."'),
    _rule("damp_torch_boot", {"damp", "torch_taken", "bootless"},
          'Bartender: "You have the torch, my boot, and I am somehow the wet one."',
          'Bartender: "Do not solve the dampness with the torch. We have data on that now."'),
    _rule("fire_torch_boot", {"fire", "torch_taken", "bootless"},
          'Bartender: "That torch started this. My missing boot merely makes it personal."',
          'Bartender: "You are holding the ignition source and my footwear. Evidence everywhere."'),
    _rule("defeated_torch_boot", {"defeated", "torch_taken", "bootless"},
          'Bartender: "You defeated me while carrying fire and stolen footwear. Heroic branding."',
          'Bartender: "I would applaud, but I am guarding the remaining boot."'),
    _rule("damp_torch_map", {"damp", "torch_taken", "map_owned"},
          'Bartender: "Torch, wet map, wet bartender. Please do not attempt science."',
          'Bartender: "If your next idea is drying the map over me, the answer is no."'),
    _rule("fire_torch_map", {"fire", "torch_taken", "map_owned"},
          'Bartender: "You still have the torch. The prosecution rests."',
          'Bartender: "Keep the map away from the flames. I already know where the tavern is."'),
    _rule("defeated_torch_map", {"defeated", "torch_taken", "map_owned"},
          'Bartender: "The map survived, the torch survived, the chair did not."',
          'Bartender: "Somewhere an insurance clerk just woke up screaming."'),
    _rule("sword_torch_boot", {"sword_taken", "torch_taken", "bootless"},
          'Bartender: "Sword, torch, stolen boot. Are you adventuring or emptying my lost property box?"',
          'Bartender: "The weapon is yours. The fire is arguable. The boot is absolutely mine."'),
    _rule("sword_torch_map", {"sword_taken", "torch_taken", "map_owned"},
          'Bartender: "Sword, torch, map. Finally, an adventuring kit with only one obvious liability."',
          'Bartender: "The liability is you. The equipment is doing its best."'),
    _rule("defeated_sword_torch", {"defeated", "sword_taken", "torch_taken"},
          'Bartender: "You brought sword and fire to a chair fight. I still nearly respect the chair."',
          'Bartender: "I surrendered. The furniture union has not."'),
    _rule("treasure_sword_boot", {"treasure_found", "sword_taken", "bootless"},
          'Bartender: "You slew danger, found treasure, and stole one boot from a civilian."',
          'Bartender: "History books are going to edit that last part, I assume."'),
    _rule("treasure_defeated_boot", {"treasure_found", "defeated", "bootless"},
          'Bartender: "Treasure found, bartender beaten, boot missing. Your victory lap is very specific."',
          'Bartender: "Please celebrate farther away from my remaining shoe."'),
    _rule("treasure_damp_boot", {"treasure_found", "damp", "bootless"},
          'Bartender: "You return rich. I remain damp and asymmetrically shod."',
          'Bartender: "Money truly cannot buy happiness. Or apparently return footwear."'),
    _rule("treasure_fire_boot", {"treasure_found", "fire", "bootless"},
          'Bartender: "You have treasure. I have fire. You also have my boot. Wealth distribution is broken."',
          'Bartender: "Congratulations on the gold. Condolences on your ethics."'),
    _rule("raiders_sword_map", {"raiders_defeated", "sword_taken", "map_owned"},
          'Bartender: "So you beat the spoon people. Did the map mention cutlery warfare?"',
          'Bartender: "I should add raiders to the legend. That would require knowing where anything is."'),
    _rule("raiders_boot_map", {"raiders_defeated", "bootless", "map_owned"},
          'Bartender: "You defeated armed raiders yet my boot remains beyond recovery."',
          'Bartender: "Fearsome warrior outside. Petty thief indoors. Range."'),
    _rule("raiders_defeated_sword", {"raiders_defeated", "defeated", "sword_taken"},
          'Bartender: "You beat the raiders and me. The chair requests a rematch."',
          'Bartender: "At this point the sword has a more stable social life than I do."'),
    _rule("cave_torch_sword", {"cave_done", "torch_taken", "sword_taken"},
          'Bartender: "You went into the cave with a torch and returned with a sword. Concerning exchange rate."',
          'Bartender: "Whatever you did underground, keep the demonstration underground."'),
    _rule("cave_boot_sword", {"cave_done", "bootless", "sword_taken"},
          'Bartender: "You survived the cave but cannot navigate a boot back to its owner."',
          'Bartender: "The beast had better manners, and I never even met it."'),
    _rule("cave_map_sword", {"cave_done", "map_owned", "sword_taken"},
          'Bartender: "You survived the cave. I assume the map was present in a ceremonial capacity."',
          'Bartender: "Useful sword, decorative map. Balanced equipment load."'),
    _rule("cave_defeated_sword", {"cave_done", "defeated", "sword_taken"},
          'Bartender: "You conquered the cave, then used your growth arc on me. Inspiring."',
          'Bartender: "Next heroic journey, try defeating something that does not pour your drinks."'),
    _rule("map_offer_drank", {"map_offered", "drank"},
          'Bartender: "The offer remains one coin: map or drink. One improves survival. Allegedly."',
          'Bartender: "I can sell you geography or consequences. Same price."'),
    _rule("map_offer_boot", {"map_offered", "bootless"},
          'Bartender: "You can buy the map. You cannot pay with my own boot."',
          'Bartender: "One coin for the map. Returning stolen footwear remains free."'),
    _rule("hostile_boot_key", {"hostile", "bootless", "key_given"},
          'Bartender: "I gave you a key and you took a boot. Hospitality has failed as a concept."',
          'Bartender: "Use the key. Return the boot. We may then renegotiate eye contact."'),
    _rule("hostile_fire_boot", {"hostile", "fire", "bootless"},
          'Bartender: "You stole my boot and set me on fire. I am running out of escalation vocabulary."',
          'Bartender: "For clarity, I am warm, furious, and still one boot short."'),
)


MODIFIER_LINES = {
    "flaming_boot": (
        'Bartender: "My boot is on fire. I would like that entered into the complaint exactly as stated."',
        'Bartender: "You have weaponized my footwear. Hospitality was not designed for this."',
    ),
    "treasure_found": (
        'Bartender: "And apparently you found the treasure. Of course you did."',
        'Bartender: "The treasure does not cancel any of the above."',
    ),
    "bootless": (
        'Bartender: "Also, I remain one boot below acceptable staffing levels."',
        'Bartender: "My left sock would like its own grievance procedure."',
    ),
    "damp": (
        'Bartender: "The floor is wetter than my mood."',
        'Bartender: "I am still damp, in case the atmosphere was too subtle."',
    ),
    "fire": (
        'Bartender: "For the record, this is the warmest shift I have had."',
        'Bartender: "Yes, I am still on fire. No, that is not the urgent part."',
    ),
    "defeated": (
        'Bartender: "The chair and I are not discussing the incident."',
        'Bartender: "I surrendered, not emotionally, but technically."',
    ),
    "map_owned": (
        'Bartender: "I still maintain the map was worth one coin."',
        'Bartender: "Do not look at me about the scale. We covered this."',
    ),
    "sword_taken": (
        'Bartender: "Please keep the sword on your side of the bar."',
        'Bartender: "The blade is making the glassware nervous."',
    ),
    "torch_taken": (
        'Bartender: "I have developed opinions about that torch."',
        'Bartender: "Keep the torch where I can see it. Actually, no, that was worse."',
    ),
    "raiders_defeated": (
        'Bartender: "The spoon people have been unusually quiet."',
        'Bartender: "I heard about the raiders. The spoons were a bold choice."',
    ),
    "cave_done": (
        'Bartender: "Whatever happened in the cave, the cave can keep the paperwork."',
        'Bartender: "You smell faintly of cave and avoidable confidence."',
    ),
    "map_offered": (
        'Bartender: "The map offer remains valid. My judgement does not."',
        'Bartender: "One coin. Map or drink. Try not to make this philosophically difficult."',
    ),
    "hostile": (
        'Bartender: "We are not, to be clear, friends."',
        'Bartender: "Customer service has ended. Vocabulary continues."',
    ),
    "key_given": (
        'Bartender: "I regret the key on several administrative levels."',
        'Bartender: "That key has caused more plot than metal should."',
    ),
    "drank": (
        'Bartender: "You have already demonstrated your standards in beverages."',
        'Bartender: "The first drink remains legally your decision."',
    ),
}

MODIFIER_ORDER = tuple(MODIFIER_LINES)


def match_dialogue_rule(flags):
    flags = frozenset(flags)
    best = None
    for rule in BARTENDER_DIALOGUE_RULES:
        if rule.required <= flags:
            if best is None or len(rule.required) > len(best.required):
                best = rule
    return best


def choose_modifier(flags, consumed, index):
    remaining = frozenset(flags) - frozenset(consumed)
    for state in MODIFIER_ORDER:
        if state in remaining:
            lines = MODIFIER_LINES[state]
            return lines[index % len(lines)]
    return None


def bartender_interaction_overlay(flags, verb, item, target):
    flags = frozenset(flags)
    if target not in {"bartender", "bartender face"}:
        return None

    if "damp" in flags and item == "crumpled map" and verb in {"use", "rub"}:
        return (
            "The wet bartender looks at the increasingly wet map.",
            'Bartender: "Excellent. Now neither of us knows where we are."',
        )

    if "damp" in flags and "bootless" in flags and item == "bartender's left boot":
        return (
            "You offer the boot to the damp bartender.",
            "He looks at the boot. He looks at his wet sock.",
            'Bartender: "Now? NOW you discover restitution?"',
        )

    if "fire" in flags and item == "crumpled map" and verb in {"use", "rub"}:
        return (
            "You move the paper map toward the burning bartender.",
            'Bartender: "There are several bad maps. Do not make this one shorter."',
        )

    if "defeated" in flags and item == "bartender's left boot":
        return (
            "You offer the stolen boot after winning the fight.",
            'Bartender: "That is the closest thing to an apology I expect from you."',
        )

    if "treasure_found" in flags and item == "crumpled map":
        return (
            "You show the map to the bartender after finding the treasure.",
            'Bartender: "It worked?"',
            "That sounded much more surprised than he intended.",
        )

    return None


BARTENDER_LICK_POOLS = {
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
