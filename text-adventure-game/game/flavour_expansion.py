EXTRA_INTERACTIONS = {
    # Bartender: every obvious standalone verb deserves a real answer.
    ("inspect", None, "bartender", "tavern"): (
        "You inspect the bartender properly.",
        "His apron has survived ale, smoke, violence, and apparently you.",
        'Bartender: "Find what you were looking for?"',
    ),
    ("poke", None, "bartender", "tavern"): (
        "You poke the bartender with one experimental finger.",
        "He looks at the finger, then at you.",
        'Bartender: "That finger has made a choice."',
    ),
    ("kick", None, "bartender", "tavern"): (
        "You attempt a small, exploratory kick at the bartender's shin.",
        "He moves exactly two inches and your foot encounters the bar instead.",
        'Bartender: "A masterful campaign."',
    ),
    ("lick", None, "bartender", "tavern"): (
        "You lick the bartender.",
        "Your tongue reports ale, smoke, and immediate professional consequences.",
        'Bartender: "I am going to pretend that was a medical emergency."',
    ),
    ("sit", None, "bartender", "tavern"): (
        "You attempt to sit on the bartender's lap.",
        "He catches you under the arms and places you on the nearest chair like misplaced luggage.",
        'Bartender: "Furniture. We have furniture."',
    ),

    # Bartender: common item abuse.
    ("use", "coin", "bartender", "tavern"): (
        "You press the coin into the bartender's palm, then refuse to let go.",
        "For three silent seconds you are both holding the world's least impressive hostage negotiation.",
    ),
    ("rub", "coin", "bartender", "tavern"): (
        "You rub the coin against the bartender's sleeve.",
        'Bartender: "If you are trying to polish me, start with the personality."',
    ),
    ("use", "mug", "bartender", "tavern"): (
        "You hand the bartender his own mug with ceremonial gravity.",
        "He takes it, waits, then hands it back.",
        'Bartender: "A complete economic cycle."',
    ),
    ("use", "drink", "bartender", "tavern"): (
        "You offer the bartender a taste of the drink he poured.",
        'Bartender: "I know what it does."',
        "That answer raises several excellent new questions.",
    ),
    ("rub", "drink", "bartender", "tavern"): (
        "You rub a little ale into the bartender's sleeve.",
        "He looks down at the spreading stain.",
        'Bartender: "At least commit to the face if you are going to be strange."',
    ),
    ("use", "coin", "bartender face", "tavern"): (
        "You hold the coin against the bartender's forehead.",
        'Bartender: "Do I look coin-operated?"',
    ),
    ("rub", "coin", "bartender face", "tavern"): (
        "You polish the bartender's cheek with currency.",
        "His expression appreciates neither monetary policy nor exfoliation.",
    ),
    ("use", "old key", "bartender face", "tavern"): (
        "You hold the old key beneath the bartender's nose.",
        'Bartender: "Yes. Still a key."',
    ),
    ("rub", "mug", "bartender face", "tavern"): (
        "You gently rub the mug against the bartender's cheek.",
        'Bartender: "The mug was happier before it met you."',
    ),
    ("use", "bartender's left boot", "bartender face", "tavern"): (
        "You present the stolen boot inches from the bartender's face.",
        'Bartender: "I know what my own boot smells like."',
        'Bartender: "Put it DOWN."',
    ),

    # Tavern scenery: the safety net should almost never catch the obvious nouns.
    ("inspect", None, "wall", "tavern"): ("The tavern wall is smoke-stained stone decorated by generations of badly aimed chairs.",),
    ("poke", None, "wall", "tavern"): ("You poke the wall. Centuries of masonry remain unmoved by peer review.",),
    ("kick", None, "wall", "tavern"): ("You kick the wall. The wall accepts your foot as a very brief donation.",),
    ("pet", None, "wall", "tavern"): ("You pet the wall. It is rough, cold, and emotionally consistent.",),
    ("sit", None, "wall", "tavern"): ("You attempt to sit on the wall. Architecture declines to provide the necessary horizontal component.",),
    ("poke", None, "sign", "tavern"): ("You poke the NO REFUNDS sign. The policy remains legally undefeated.",),
    ("kick", None, "sign", "tavern"): ("You kick the sign. It swings once and continues judging your purchasing decisions.",),
    ("lick", None, "sign", "tavern"): ("You lick the sign. The refund policy now applies to your tongue as well.",),
    ("pet", None, "sign", "tavern"): ("You stroke the sign reassuringly. Its terms and conditions soften by zero percent.",),
    ("sit", None, "sign", "tavern"): ("You consider sitting on the sign. The bartender points at the chair without looking up.",),
    ("poke", None, "lantern", "tavern"): ("You poke a cracked lantern. It flickers in what may be fear or poor maintenance.",),
    ("pet", None, "lantern", "tavern"): ("You pet the lantern carefully. Warm glass is a demanding friendship.",),

    # Root cellar.
    ("inspect", None, "wall", "root_cellar"): ("The cellar wall is damp enough to have opinions about mould.",),
    ("poke", None, "wall", "root_cellar"): ("You poke the wet stone. Moisture wins initiative.",),
    ("kick", None, "wall", "root_cellar"): ("You kick the cellar wall. Dust falls down purely to make your decision feel consequential.",),
    ("pet", None, "wall", "root_cellar"): ("You pet the damp wall. Your hand returns colder and somehow older.",),
    ("sit", None, "wall", "root_cellar"): ("You lean so aggressively against the cellar wall that it almost counts as sitting.",),
    ("inspect", None, "cellar door", "root_cellar"): ("The iron door is thick, old, and built by someone who considered subtlety a security vulnerability.",),
    ("lick", None, "cellar door", "root_cellar"): ("You lick the iron door. Metallic, damp, and catastrophically unnecessary.",),
    ("pet", None, "cellar door", "root_cellar"): ("You pat the iron door. It remains locked but may now feel supported.",),
    ("sit", None, "cellar door", "root_cellar"): ("You sit against the iron door. For a moment you become part of the locking mechanism.",),
    ("inspect", None, "stairs", "root_cellar"): ("The cellar stairs are worn smooth by feet belonging to people with better reasons to be down here.",),
    ("poke", None, "stairs", "root_cellar"): ("You poke a stair. It passes the stair inspection with flying colours.",),
    ("kick", None, "stairs", "root_cellar"): ("You kick the stairs. Somewhere above, the tavern hears your engineering review.",),

    # Cave entrance.
    ("inspect", None, "wall", "cave_entrance"): ("The cave wall glistens with moisture and an unreasonable quantity of geological confidence.",),
    ("poke", None, "wall", "cave_entrance"): ("You poke the cave wall. The mountain declines to react on your timescale.",),
    ("kick", None, "wall", "cave_entrance"): ("You kick the cave wall. The cave keeps the point.",),
    ("pet", None, "wall", "cave_entrance"): ("You pet the cave wall. It has the comforting texture of a place that could collapse on you.",),
    ("sit", None, "wall", "cave_entrance"): ("You sit with your back to the cave wall. The glowing eyes appreciate the stationary target.",),
    ("inspect", None, "darkness", "cave_entrance"): ("You inspect the darkness. It contains several pairs of eyes and no customer-service desk.",),
    ("poke", None, "darkness", "cave_entrance"): ("You poke a hand into the darkness. Something politely pokes back from farther away.",),
    ("sit", None, "darkness", "cave_entrance"): ("You sit in the darkness. The darkness immediately feels more populated.",),
    ("pet", None, "glowing eyes", "cave_entrance"): ("You reach toward the glowing eyes with petting intent. The eyes decide proximity was overrated.",),

    # Cave chamber.
    ("kick", None, "bones", "cave_chamber"): ("You kick a loose bone. It skitters away with more purpose than your current plan.",),
    ("lick", None, "bones", "cave_chamber"): ("You decline, at the last possible moment, to lick the ancient bones. Character growth.",),
    ("pet", None, "bones", "cave_chamber"): ("You pat the bones gently. Whatever owned them has no feedback at this time.",),
    ("sit", None, "bones", "cave_chamber"): ("You sit beside the bones rather than on them. Even you have discovered a line.",),
    ("poke", None, "beast den", "cave_chamber"): ("You poke the beast den. The den does not poke back, which is currently the best possible result.",),
    ("kick", None, "beast den", "cave_chamber"): ("You kick the edge of the beast den. Dust rises like a tiny, disappointed ghost.",),
    ("lick", None, "beast den", "cave_chamber"): ("You consider licking the beast den. The narrator exercises emergency editorial powers.",),
    ("pet", None, "beast den", "cave_chamber"): ("You pet the beast den. This is technically pet-adjacent, which is the closest you should get.",),
    ("inspect", None, "stone", "cave_chamber"): ("The stone is jagged, black, and completely innocent of whatever story you are projecting onto it.",),
    ("poke", None, "stone", "cave_chamber"): ("You poke the stone. It remains the strongest conversationalist in the chamber.",),

    # Forest path.
    ("inspect", None, "raiders", "forest_path"): ("The raiders are armed with picnic cutlery and the confidence of men who have never met consequences.",),
    ("kick", None, "raiders", "forest_path"): ("You mime a warning kick toward the raiders. Several spoons are raised defensively.",),
    ("lick", None, "raiders", "forest_path"): ("You announce an intention to lick a raider. Their formation breaks immediately.",),
    ("pet", None, "raiders", "forest_path"): ("You pat the nearest raider on the shoulder. He looks genuinely confused by the tactical doctrine.",),
    ("sit", None, "raiders", "forest_path"): ("You attempt to sit among the raiders. They shuffle aside with the awkward courtesy of a bus stop.",),
    ("inspect", None, "grass", "forest_path"): ("The grass is wet, flattened, and carrying more evidence than the raiders realise.",),
    ("poke", None, "grass", "forest_path"): ("You poke the grass. A beetle relocates without filing paperwork.",),
    ("kick", None, "grass", "forest_path"): ("You kick through the grass and achieve almost one full second of dramatic rustling.",),
    ("lick", None, "grass", "forest_path"): ("You taste one blade of grass. The forest receives your resignation from civilisation.",),
    ("pet", None, "grass", "forest_path"): ("You brush the grass flat with your palm. It springs back with admirable boundaries.",),
    ("inspect", None, "path", "forest_path"): ("The path is muddy, narrow, and suspiciously committed to leading toward trouble.",),
    ("poke", None, "path", "forest_path"): ("You poke the path. Navigation remains unchanged.",),
}
