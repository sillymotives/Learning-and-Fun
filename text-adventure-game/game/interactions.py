ITEM_ALIASES = {
    "ale": "drink",
    "beer": "drink",
    "booze": "drink",
    "drink": "drink",
    "mug": "mug",
    "cup": "mug",
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
    "treasure": "hidden treasure",
    "hidden treasure": "hidden treasure",
}

TARGET_ALIASES = {
    "bartender": "bartender", "the bartender": "bartender", "barkeep": "bartender",
    "the barkeep": "bartender", "innkeeper": "bartender",
    "bartender face": "bartender face", "bartender's face": "bartender face",
    "his face": "bartender face", "face": "bartender face",
    "walls": "wall", "stone wall": "wall", "stone walls": "wall",
    "tavern wall": "wall", "cellar wall": "wall", "cave wall": "wall",
    "trees": "tree", "forest": "forest", "woods": "forest", "bushes": "bush",
    "raider": "raiders", "raiders": "raiders", "the raiders": "raiders",
    "casks": "cask", "barrels": "cask", "barrel": "cask",
    "iron door": "cellar door", "cellar door": "cellar door", "door": "door",
    "glowing eyes": "glowing eyes", "eyes": "glowing eyes",
    "beast den": "beast den", "den": "beast den", "bones": "bones",
    "floor": "floor", "ground": "floor", "chair": "chair", "bar": "bar",
    "counter": "bar", "sign": "sign", "trophy": "trophies", "trophies": "trophies",
    "lantern": "lantern", "lanterns": "lantern", "torch bracket": "torch bracket",
    "stairs": "stairs", "damp stone": "damp stone", "darkness": "darkness",
    "stone": "stone", "path": "path", "grass": "grass", "mud": "mud",
    "spoon": "spoon", "spoons": "spoon", "fork": "fork", "forks": "fork",
}

VERB_ALIASES = {
    "look": "inspect", "examine": "inspect", "inspect": "inspect",
    "prod": "poke", "poke": "poke", "kick": "kick", "lick": "lick",
    "taste": "lick", "stroke": "pet", "pat": "pet", "pet": "pet",
    "sit": "sit", "use": "use", "rub": "rub",
}


def _clean(text):
    return " ".join(text.lower().strip().split())


def normalize_item(name):
    value = _clean(name)
    return ITEM_ALIASES.get(value, value)


def normalize_target(name):
    value = _clean(name)
    if value.startswith("the ") and value not in TARGET_ALIASES:
        value = value[4:]
    return TARGET_ALIASES.get(value, value)


def normalize_verb(name):
    value = _clean(name)
    return VERB_ALIASES.get(value, value)


STATIC_INTERACTIONS = {
    # Tavern item-on-target
    ("rub", "drink", "bartender face", "tavern"): (
        "You scoop up a heroic quantity of ale and rub it directly into the bartender's face.",
        "He stands perfectly still.",
        'Bartender: "Was there a reason?"',
        "You consider lying.",
        'Bartender: "I watched you do it."',
    ),
    ("use", "drink", "bartender face", "tavern"): ("You apply the drink to the bartender's face with the confidence of a trained professional.", 'Bartender: "That sentence contained no medicine."'),
    ("rub", "mug", "bartender", "tavern"): ("You rub the mug against the bartender's sleeve.", 'Bartender: "We have cloths for this."'),
    ("use", "coin", "wall", "tavern"): ("You press a coin against the tavern wall and wait for capitalism to happen.", "The wall declines the transaction."),
    ("rub", "coin", "wall", "tavern"): ("You polish the wall with money.", "The economy remains unstable."),
    ("use", "sword", "mug", "tavern"): ("You introduce the mug to the sword.", "The mug becomes two smaller, less useful mugs."),
    ("rub", "sword", "mug", "tavern"): ("You hone the sword on a mug.", "The mug loses this argument immediately."),
    ("use", "old key", "bartender", "tavern"): ("You hold the old key up to the bartender.", "He develops an urgent interest in a completely different wall."),
    ("rub", "old key", "bartender", "tavern"): ("You rub the key against the bartender's apron.", 'Bartender: "That is not how doors work."'),
    ("use", "bartender's left boot", "wall", "tavern"): ("You polish the wall with the bartender's stolen left boot.", "The wall becomes marginally shinier.", "The boot becomes spiritually worse."),
    ("rub", "bartender's left boot", "wall", "tavern"): ("You polish the wall with the bartender's stolen left boot.", "The wall becomes marginally shinier.", "The boot becomes spiritually worse."),
    ("rub", "bartender's left boot", "chair", "tavern"): ("You buff the chair with the stolen boot.", "The chair now smells like consequences."),
    ("rub", "bartender's left boot", "bar", "tavern"): ("You polish the bar with the stolen boot.", "The bartender watches a hygiene law die behind his eyes."),
    ("use", "old key", "bartender's left boot", "tavern"): ("You try the old key on the boot.", "The footwear remains tragically unlocked."),
    ("use", "torch", "chair", "tavern"): ("You lower the torch toward the chair.", "The narrator physically removes your hand from the decision.", "One burning bartender is already enough paperwork."),
    ("use", "torch", "wall", "tavern"): ("You warm the tavern wall with the torch.", "Centuries of dampness remain emotionally unavailable."),
    ("rub", "torch", "bartender's left boot", "tavern"): ("You rub a burning torch against the stolen boot.", "Hot leather answers a question nobody asked."),
    ("use", "hidden treasure", "bartender", "tavern"): ("You present the legendary treasure to the bartender.", 'Bartender: "Lovely. Put it somewhere that is not my bar."'),
    ("rub", "hidden treasure", "bartender", "tavern"): ("You rub priceless treasure against the bartender's apron.", 'Bartender: "You make wealth look exhausting."'),

    # Tavern standalone
    ("inspect", None, "chair", "tavern"): ("It is a sturdy wooden chair with combat experience it refuses to discuss.",),
    ("inspect", None, "bar", "tavern"): ("The bar is scarred by mugs, coins, and several decisions that became case law.",),
    ("inspect", None, "sign", "tavern"): ("The sign says NO REFUNDS AFTER THE SECOND DRINK. It has the confidence of precedent.",),
    ("inspect", None, "trophies", "tavern"): ("The hunting trophies stare down with the exhausted dignity of former side quests.",),
    ("inspect", None, "lantern", "tavern"): ("The cracked lanterns produce enough light to identify mistakes, not prevent them.",),
    ("poke", None, "chair", "tavern"): ("You poke the chair. Somewhere, the bartender's combat instincts wake briefly.",),
    ("poke", None, "trophies", "tavern"): ("You poke a trophy. Dust files a formal complaint.",),
    ("kick", None, "bar", "tavern"): ("You kick the bar. The bar wins on points.",),
    ("kick", None, "chair", "tavern"): ("You kick the chair. It remembers the bartender and seems encouraged.",),
    ("lick", None, "wall", "tavern"): ("You lick the tavern wall. It tastes of stone, smoke, and poor boundaries.",),
    ("lick", None, "bar", "tavern"): ("You lick the bar. The bartender stops polishing the mug and starts polishing his expectations downward.",),
    ("pet", None, "chair", "tavern"): ("You pet the chair. It is the gentlest interaction this furniture has had all week.",),
    ("pet", None, "bartender", "tavern"): ("You reach out and pet the bartender once. He looks at your hand, then at you. No further guidance is offered.",),
    ("sit", None, "chair", "tavern"): ("You sit in the chair. For once, the chair is used according to manufacturer intent.",),
    ("sit", None, "floor", "tavern"): ("You sit on the tavern floor. The bartender quietly upgrades you from customer to local feature.",),
    ("sit", None, "bar", "tavern"): ("You sit on the bar. The bartender moves every glass two inches farther away.",),

    # Cellar item-on-target
    ("use", "old key", "torch", "root_cellar"): ("You touch the key to the torch. Neither object reveals a secret secondary profession.",),
    ("rub", "old key", "torch", "root_cellar"): ("You rub iron against burning timber. The smell is mostly confidence.",),
    ("use", "bartender's left boot", "cellar door", "root_cellar"): ("You present the stolen boot to the iron door. The door remains class-conscious.",),
    ("rub", "bartender's left boot", "cellar door", "root_cellar"): ("You polish the iron door with stolen footwear. Security is unchanged; presentation improves slightly.",),
    ("use", "coin", "cask", "root_cellar"): ("You offer a coin to the cask. The cask is not licensed for retail.",),
    ("rub", "coin", "cask", "root_cellar"): ("You rub the coin on the cask. It is now a slightly more alcoholic currency.",),
    ("use", "torch", "cask", "root_cellar"): ("You consider introducing fire to an unidentified cask. Survival instinct finally clocks in.",),
    ("rub", "bartender's left boot", "cask", "root_cellar"): ("You rub the stolen boot over the cask. The cellar acquires another smell it did not request.",),
    ("use", "coin", "wall", "root_cellar"): ("You attempt commerce with the cellar wall. The wall offers zero percent interest and no liquidity.",),

    # Cellar standalone
    ("inspect", None, "damp stone", "root_cellar"): ("The damp stone has spent centuries perfecting the colour 'basement'.",),
    ("inspect", None, "torch bracket", "root_cellar"): ("The bracket is empty once the torch is taken and somehow looks accusatory about it.",),
    ("inspect", None, "cask", "root_cellar"): ("The casks are old, sealed, and labelled in handwriting that became illegal several alphabets ago.",),
    ("poke", None, "cellar door", "root_cellar"): ("You poke the iron door. It responds with premium-grade door behaviour.",),
    ("poke", None, "damp stone", "root_cellar"): ("You poke the damp stone. It is exactly as damp as advertised.",),
    ("kick", None, "cellar door", "root_cellar"): ("You kick the iron door. Your foot learns about iron.",),
    ("kick", None, "cask", "root_cellar"): ("You kick a cask. Something inside sloshes with legal ambiguity.",),
    ("lick", None, "wall", "root_cellar"): ("You lick the cellar wall. Mineral notes. Damp finish. Regret-forward bouquet.",),
    ("pet", None, "torch", "root_cellar"): ("You pet the torch with extreme logistical caution. Warm.",),
    ("pet", None, "cask", "root_cellar"): ("You pat the cask affectionately. It gives nothing away.",),
    ("sit", None, "cask", "root_cellar"): ("You sit on a cask. Somewhere inside it, a liquid judges your weight distribution.",),
    ("sit", None, "stairs", "root_cellar"): ("You sit on the stairs and briefly become the obstacle the dungeon was missing.",),

    # Cave item-on-target
    ("use", "coin", "wall", "cave_entrance"): ("You offer the cave wall a coin. Geology remains defiantly pre-capitalist.",),
    ("rub", "coin", "wall", "cave_entrance"): ("You rub money on the cave wall. The wall's net worth is unaffected.",),
    ("use", "sword", "stone", "cave_chamber"): ("You strike stone with the sword. The stone wins by being a stone.",),
    ("rub", "sword", "stone", "cave_chamber"): ("You scrape the blade over stone. It gains a new edge and loses several opinions of you.",),
    ("rub", "bartender's left boot", "sword", "cave_chamber"): ("You polish the sword with the stolen boot. The blade is now technically shined and spiritually compromised.",),
    ("use", "bartender's left boot", "bones", "cave_chamber"): ("You place the boot among the bones. For one terrible second it looks archaeologically plausible.",),
    ("use", "torch", "darkness", "cave_entrance"): ("You use the torch on the darkness. For once, object-oriented programming accurately describes the situation.",),

    # Cave standalone
    ("inspect", None, "bones", "cave_chamber"): ("The bones belong to creatures that either fought bravely or failed a very similar tutorial.",),
    ("inspect", None, "glowing eyes", "cave_entrance"): ("The glowing eyes inspect you back. The review is not favourable.",),
    ("inspect", None, "beast den", "cave_chamber"): ("The beast den contains scratches, bones, and a conspicuously sword-shaped absence.",),
    ("poke", None, "glowing eyes", "cave_entrance"): ("You reach toward the glowing eyes. The glowing eyes move closer. Experiment concluded.",),
    ("poke", None, "bones", "cave_chamber"): ("You poke a bone. It contributes nothing to the conversation.",),
    ("kick", None, "stone", "cave_chamber"): ("You kick a cave stone. The cave records another victory over footwear.",),
    ("lick", None, "wall", "cave_entrance"): ("You lick the cave wall. It tastes older than your insurance coverage.",),
    ("lick", None, "wall", "cave_chamber"): ("You lick the cave wall. Somewhere, geology withdraws consent from the scientific method.",),
    ("pet", None, "darkness", "cave_entrance"): ("You pet the darkness. Something in it appears to appreciate the gesture. This is worse.",),
    ("sit", None, "beast den", "cave_chamber"): ("You sit in the beast den. It is surprisingly ergonomic and deeply concerning.",),
    ("sit", None, "floor", "cave_chamber"): ("You sit on the cave floor. Adventure waits with visible impatience.",),

    # Forest item-on-target
    ("use", "torch", "forest", "forest_path"): ("You raise the torch toward the forest.", "Narrator: No.", "You lower the torch."),
    ("rub", "torch", "tree", "forest_path"): ("You move the burning torch toward a tree. The narrator clears their throat with legal force.",),
    ("use", "coin", "tree", "forest_path"): ("You offer a coin to the tree. It is already heavily invested in timber.",),
    ("rub", "coin", "tree", "forest_path"): ("You rub currency into the bark. The tree remains outside the banking system.",),
    ("use", "bartender's left boot", "tree", "forest_path"): ("You place the stolen boot against a tree. The tree has seen storms, axes, and now this.",),
    ("rub", "bartender's left boot", "tree", "forest_path"): ("You polish bark with stolen footwear. Both surfaces get worse.",),
    ("rub", "hidden treasure", "raiders", "forest_path"): ("You rub the treasure on the defeated raiders. Nobody learns anything from this victory.",),
    ("use", "sword", "spoon", "forest_path"): ("You cross sword and spoon. The spoon retires undefeated in spirit.",),
    ("use", "sword", "fork", "forest_path"): ("You duel a fork with a sword. It is technically four points to one.",),

    # Forest standalone
    ("inspect", None, "spoon", "forest_path"): ("The raider spoon is polished, threatening, and absolutely unsuitable for war.",),
    ("inspect", None, "fork", "forest_path"): ("The fork has four points and the tactical doctrine of a picnic.",),
    ("inspect", None, "mud", "forest_path"): ("The mud contains footprints, rainwater, and the shattered remains of several dignities.",),
    ("inspect", None, "bush", "forest_path"): ("The bush looks exactly like somewhere a raider would hide. This proves nothing and everything.",),
    ("poke", None, "raiders", "forest_path"): ("You poke a raider. He looks at his captain for policy guidance.",),
    ("poke", None, "bush", "forest_path"): ("You poke the bush. The bush rustles in a manner legally distinct from foreshadowing.",),
    ("kick", None, "tree", "forest_path"): ("You kick the tree. The tree has rings older than your entire argument.",),
    ("kick", None, "mud", "forest_path"): ("You kick the mud. Congratulations, you have invented trousers with spots.",),
    ("lick", None, "tree", "forest_path"): ("You lick the tree. Bark. Literally and culinarily.",),
    ("lick", None, "mud", "forest_path"): ("You consider licking the mud. The narrator quietly marks this boundary as non-negotiable.",),
    ("pet", None, "tree", "forest_path"): ("You pet the tree. After everything else today, this is unexpectedly wholesome.",),
    ("pet", None, "bush", "forest_path"): ("You pet the bush. It accepts this with leafy professionalism.",),
    ("sit", None, "bush", "forest_path"): ("You sit in the bush. You are now tactically indistinguishable from a low-budget raider.",),
    ("sit", None, "grass", "forest_path"): ("You sit in the grass. The quest remains available whenever your knees are ready.",),
}

ROOM_TARGETS = {
    "tavern": {"bartender", "bartender face", "mug", "bar", "chair", "wall", "floor", "sign", "trophies", "lantern", "door"},
    "root_cellar": {"wall", "torch", "torch bracket", "coin", "cask", "cellar door", "stairs", "damp stone", "floor"},
    "cave_entrance": {"wall", "darkness", "glowing eyes", "stone", "floor"},
    "cave_chamber": {"wall", "beast den", "bones", "sword", "stone", "darkness", "torch", "floor"},
    "forest_path": {"forest", "tree", "path", "grass", "hidden treasure", "raiders", "spoon", "fork", "mud", "bush", "floor"},
}

ROOM_FALLBACKS = {
    "tavern": ("The bartender notices. He chooses not to encourage you.", "The tavern absorbs this event into its already difficult history."),
    "root_cellar": ("The cellar is damp, silent, and somehow more judgmental now.", "Something drips in the darkness with suspiciously comic timing."),
    "cave_entrance": ("The cave answers with the ancient language of absolutely nothing useful.", "The glowing eyes remain professionally ominous."),
    "cave_chamber": ("The cave tolerates your experiment without endorsing it.", "A distant pebble falls, possibly in embarrassment."),
    "forest_path": ("The forest has witnessed stranger things, but not recently.", "A bird leaves. It does not explain whether this is related."),
}

GENERIC_FALLBACKS = (
    "Nothing improves.",
    "The universe quietly records the incident.",
    "Against all expectations, this reveals absolutely nothing.",
    "Somewhere, an adventure-game designer develops a headache.",
    "The target endures this with remarkable professionalism.",
)


def get_static_interaction(verb, item, target, room_id):
    key = (
        normalize_verb(verb),
        normalize_item(item) if item is not None else None,
        normalize_target(target),
        room_id,
    )
    return STATIC_INTERACTIONS.get(key) or STATIC_INTERACTIONS.get((key[0], key[1], key[2], None))
