BEAST_STATIC_INTERACTIONS = {
    ("use", "impossible drink", "darkness", "cave_entrance"): (
        "You hold the Impossible Drink toward the darkness.",
        "The darkness reflects a tiny cold glint from somewhere it should not have a surface.",
    ),
    ("rub", "impossible drink", "darkness", "cave_entrance"): (
        "You attempt to rub the Impossible Drink on the darkness.",
        "For once, the darkness appears to move away from you.",
    ),
    ("use", "impossible drink", "wall", "cave_entrance"): (
        "You press the Impossible Drink to the cave wall.",
        "A circle of frost appears, then remembers caves do not work like that.",
    ),
    ("rub", "impossible drink", "wall", "cave_entrance"): (
        "You polish ancient stone with an impossible beverage.",
        "Geology declines to cite this experiment.",
    ),
    ("use", "impossible drink", "stone", "cave_chamber"): (
        "You balance the Impossible Drink on a black cave stone.",
        "The stone looks ordinary. The shadow beneath the bottle does not.",
    ),
    ("rub", "impossible drink", "stone", "cave_chamber"): (
        "You rub the Impossible Drink over the cave stone.",
        "The stone becomes cold enough to reconsider magma retroactively.",
    ),
    ("use", "crumpled map", "bones", "cave_chamber"): (
        "You lay the crumpled map over the old bones.",
        "The resulting diagram is anatomically and geographically wrong.",
    ),
    ("rub", "crumpled map", "bones", "cave_chamber"): (
        "You dust the bones with the map.",
        "Several crumbs of bad geography fall off.",
    ),
    ("use", "hidden treasure", "beast den", "cave_chamber"): (
        "You place the legendary treasure in the beast den.",
        "For one moment the secret treasure is secret again.",
    ),
    ("rub", "hidden treasure", "stone", "cave_chamber"): (
        "You polish cave stone with legendary treasure.",
        "Somewhere, an archaeologist wakes up furious.",
    ),
    ("use", "beast drink", "bones", "cave_chamber"): (
        "You offer the beast drink to the bones.",
        "They remain impressively committed to sobriety.",
    ),
    ("rub", "beast drink", "wall", "cave_chamber"): (
        "You smear a little beast drink on the cave wall.",
        "The wall now smells faintly more social.",
    ),
    ("use", "old key", "bones", "cave_chamber"): (
        "You try the old key against a rib bone.",
        "The skeleton contains no visible keyhole and several implied objections.",
    ),
    ("rub", "old key", "stone", "cave_chamber"): (
        "You scrape the old key across black stone.",
        "The key remains old. The stone remains smug.",
    ),
}


BEAST_STATE_INTERACTIONS = {
    (frozenset({"beasts_hostile"}), "inspect", None, "beasts"): (
        "You inspect the hostile cave beasts.",
        "Their eyes follow every movement. Their teeth appear to have formed a committee.",
        "The committee is not in your favour.",
    ),
    (frozenset({"beasts_hostile"}), "use", "impossible drink", "beasts"): (
        "You offer the Impossible Drink to the hostile beasts.",
        "They sniff reality's concession and recoil from the smell of impossible weather.",
        "They remain hostile. Apparently metaphysics is not hydration.",
    ),
    (frozenset({"beasts_hostile"}), "rub", "impossible drink", "beasts"): (
        "You move the Impossible Drink toward the hostile beasts with rubbing intent.",
        "Both beasts bare their teeth.",
        "Even reality has limits and this appears to be one.",
    ),
    (frozenset({"beasts_thirsty"}), "inspect", None, "beasts"): (
        "You inspect the thirsty beasts.",
        "The teeth are still enormous, but both dry tongues keep appearing between them.",
        "One stares at your hands with the focus of a customer awaiting table service.",
    ),
    (frozenset({"beasts_thirsty"}), "poke", None, "beasts"): (
        "You poke the nearer thirsty beast.",
        "It opens one eye, licks a very dry nose, and nudges your hand toward its mouth.",
        "This has become less a threat display and more a hydration complaint.",
    ),
    (frozenset({"beasts_thirsty"}), "lick", None, "beasts"): (
        "You consider licking a thirsty beast.",
        "It considers licking you first.",
        "Its tongue is visibly dry. You both decide this exchange would solve nothing.",
    ),
    (frozenset({"beasts_thirsty"}), "kick", None, "beasts"): (
        "You lift a foot toward the thirsty beasts.",
        "One places a huge paw on your boot and gently pushes it back down.",
        "The message is surprisingly diplomatic: drink first, violence never.",
    ),
    (frozenset({"beasts_thirsty"}), "sit", None, "beasts"): (
        "You sit beside the thirsty beasts.",
        "Both immediately crowd closer and stare at your empty hands.",
        "You have accidentally opened a very large waiting room.",
    ),
    (frozenset({"beasts_thirsty"}), "use", "impossible drink", "beasts"): (
        "You offer the thirsty beasts the Impossible Drink.",
        "They sniff it. Both dry tongues retract at once.",
        "Reality smells too strong. They want an actual drink, not a philosophical incident.",
    ),
    (frozenset({"beasts_thirsty"}), "rub", "impossible drink", "beasts"): (
        "You wave impossible condensation near the thirsty beasts.",
        "They track every droplet until each one vanishes upward.",
        "Their disappointment is enormous and very dry.",
    ),
    (frozenset({"beasts_thirsty"}), "use", "sword", "beasts"): (
        "You show the thirsty beasts a sword.",
        "One sniffs the blade and looks back at your empty hand.",
        "Weapons are not beverages. Progress.",
    ),
    (frozenset({"beasts_thirsty"}), "rub", "sword", "beasts"): (
        "You cautiously present the flat of the sword near a thirsty beast.",
        "It licks the metal once, grimaces, and looks betrayed by chemistry.",
    ),
    (frozenset({"beasts_thirsty"}), "use", "hidden treasure", "beasts"): (
        "You offer legendary treasure to the thirsty beasts.",
        "One noses the relic aside and stares meaningfully at its dry tongue.",
        "Capital has failed where hydration might succeed.",
    ),
    (frozenset({"beasts_thirsty"}), "rub", "hidden treasure", "beasts"): (
        "You rub the treasure against a thirsty beast's fur.",
        "It tolerates this only because it still believes your other hand may contain a drink.",
    ),
    (frozenset({"beasts_asleep"}), "inspect", None, "beasts"): (
        "The two enormous cave beasts are curled together, fast asleep.",
        "One paw covers the other's nose. A tail twitches with tiny dream violence.",
        "They are offensively adorable.",
    ),
    (frozenset({"beasts_asleep"}), "poke", None, "beasts"): (
        "You gently poke one sleeping beast.",
        "It sleepily hooks a paw around the other and pulls it closer.",
        "Your experiment becomes cuddling against its will.",
    ),
    (frozenset({"beasts_asleep"}), "lick", None, "beasts"): (
        "You lean toward a sleeping beast with a familiar terrible idea.",
        "The narrator lowers an invisible barrier.",
        "You have grown. Do not ruin the paperwork.",
    ),
    (frozenset({"beasts_asleep"}), "kick", None, "beasts"): (
        "You raise a foot toward the sleeping beasts.",
        "No.",
        "They have tiny sleepy ear twitches now. You are outvoted.",
    ),
    (frozenset({"beasts_asleep"}), "sit", None, "beasts"): (
        "You sit beside the sleeping beasts.",
        "A huge tail flops across your lap without waking its owner.",
        "You have been assigned blanket duty.",
    ),
    (frozenset({"beasts_asleep"}), "pet", None, "beasts"): (
        "You scratch one sleeping beast behind the ear.",
        "Its back foot thumps twice.",
        "The other beast buries its face deeper under the first one's paw.",
    ),
    (frozenset({"beasts_asleep"}), "use", "impossible drink", "beasts"): (
        "You set the Impossible Drink beside the sleeping beasts.",
        "One nose twitches.",
        "Neither wakes. Reality has been successfully ignored.",
    ),
    (frozenset({"beasts_asleep"}), "rub", "impossible drink", "beasts"): (
        "You let cold impossible condensation touch the fur of a sleeping beast.",
        "It shivers once and steals more of the other beast's warmth.",
    ),
    (frozenset({"beasts_asleep"}), "use", "crumpled map", "beasts"): (
        "You drape the crumpled map over the sleeping beasts.",
        "It covers approximately one shoulder.",
        "Cartography has become a blanket industry.",
    ),
    (frozenset({"beasts_asleep"}), "rub", "crumpled map", "beasts"): (
        "You gently fan the sleeping beasts with the map.",
        "One ear flicks. The scale remains inaccurate.",
    ),
    (frozenset({"beasts_asleep"}), "use", "coin", "beasts"): (
        "You place a coin near one sleeping paw.",
        "The paw closes over it reflexively.",
        "You have accidentally paid the monster.",
    ),
    (frozenset({"beasts_asleep"}), "rub", "coin", "beasts"): (
        "You rub a coin gently over sleeping fur.",
        "The beast does not wake, but capitalism feels ashamed.",
    ),
    (frozenset({"beasts_asleep"}), "use", "old key", "beasts"): (
        "You place the old key beside the sleeping beasts.",
        "One whisker brushes it. No doors open.",
    ),
    (frozenset({"beasts_asleep"}), "rub", "old key", "beasts"): (
        "You scratch behind a sleeping ear with the old key.",
        "The beast leans into it without waking.",
        "The key has finally found a practical purpose.",
    ),
    (frozenset({"beasts_asleep"}), "use", "sword", "beasts"): (
        "You hold the sword near the sleeping beasts.",
        "Then you remember you won this encounter with a drink and feel faintly embarrassed.",
    ),
    (frozenset({"beasts_asleep"}), "rub", "sword", "beasts"): (
        "You very carefully avoid rubbing a sword on a sleeping animal.",
        "The narrator awards one invisible point for judgment.",
    ),
    (frozenset({"beasts_asleep"}), "use", "torch", "beasts"): (
        "You hold the torch well away from the sleeping beasts.",
        "Warm light catches their paws. Neither wakes.",
    ),
    (frozenset({"beasts_asleep"}), "rub", "torch", "beasts"): (
        "You begin moving the torch toward sleeping fur.",
        "The narrator removes the torch from the experiment before biology becomes chemistry.",
    ),
    (frozenset({"beasts_asleep"}), "use", "bartender's left boot", "beasts"): (
        "You place the stolen boot beside the sleeping beasts.",
        "One beast sleepily rests its chin on it.",
        "The bartender would find this development spiritually expensive.",
    ),
    (frozenset({"beasts_asleep"}), "rub", "bartender's left boot", "beasts"): (
        "You gently buff sleeping fur with stolen footwear.",
        "The beast sighs contentedly.",
        "The boot's moral condition worsens.",
    ),
    (frozenset({"beasts_asleep"}), "use", "hidden treasure", "beasts"): (
        "You place the hidden treasure beside the sleeping beasts.",
        "For a moment it looks less valuable than the paw pile.",
    ),
    (frozenset({"beasts_asleep"}), "rub", "hidden treasure", "beasts"): (
        "You brush the treasure lightly against sleeping fur.",
        "Legendary wealth acquires one enormous hair.",
    ),
    (frozenset({"beasts_asleep"}), "use", "beast drink", "beasts"): (
        "You show the sleeping beasts another beast drink.",
        "One nose twitches. The bar is closed.",
    ),
    (frozenset({"beasts_asleep"}), "rub", "beast drink", "beasts"): (
        "You move the reinforced mug near the sleeping heap.",
        "A tiny sleepy slurp happens without either beast opening its eyes.",
    ),
}
