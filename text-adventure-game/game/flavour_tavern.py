TAVERN_STATIC_INTERACTIONS = {
    ("use", "impossible drink", "bar", "tavern"): (
        "You set the Impossible Drink on the bar.",
        "For one second the wood grain bends subtly toward it.",
        'Bartender: "Keep causality off the varnish."',
    ),
    ("rub", "impossible drink", "bar", "tavern"): (
        "You rub the sealed Impossible Drink along the bar.",
        "A ring of condensation appears three inches ahead of it.",
        "The bartender quietly stops asking questions.",
    ),
    ("use", "impossible drink", "wall", "tavern"): (
        "You hold the Impossible Drink against the tavern wall.",
        "The stone becomes briefly uncertain whether it is indoors.",
    ),
    ("rub", "impossible drink", "wall", "tavern"): (
        "You polish the wall with the Impossible Drink.",
        "The damp patch you create is somehow on the other side.",
    ),
    ("use", "impossible drink", "sign", "tavern"): (
        "You present the Impossible Drink to the NO REFUNDS sign.",
        "The sign has no policy covering drinks issued by the universe.",
    ),
    ("rub", "impossible drink", "sign", "tavern"): (
        "You rub impossible condensation across the NO REFUNDS sign.",
        "For a heartbeat it reads NO REFUNDS AFTER THE THIRD DRINK.",
        "Then reality lawyers arrive and change it back.",
    ),
    ("use", "crumpled map", "sign", "tavern"): (
        "You compare the crumpled map with the NO REFUNDS sign.",
        "Neither contains useful directions. One is at least honest about it.",
    ),
    ("rub", "crumpled map", "sign", "tavern"): (
        "You rub the map against the sign.",
        "The map acquires a faint rectangular sense of authority.",
    ),
    ("use", "old key", "sign", "tavern"): (
        "You try the old key on the NO REFUNDS sign.",
        "Consumer protection remains tragically locked.",
    ),
    ("rub", "old key", "sign", "tavern"): (
        "You scrape the old key across the sign.",
        "The refund policy survives another legal challenge.",
    ),
    ("use", "sword", "sign", "tavern"): (
        "You point the sword at the NO REFUNDS sign.",
        "The sign has survived worse customers and appears unmoved.",
    ),
    ("rub", "sword", "sign", "tavern"): (
        "You polish the sword against the refund policy.",
        "Both emerge sharper in completely different senses.",
    ),
    ("use", "hidden treasure", "sign", "tavern"): (
        "You hold priceless treasure beside the NO REFUNDS sign.",
        "At last, sufficient funds. Still no refunds.",
    ),
    ("rub", "hidden treasure", "sign", "tavern"): (
        "You rub legendary treasure on the sign.",
        "The sign remains the most valuable thing here emotionally.",
    ),
    ("use", "beast drink", "sign", "tavern"): (
        "You show the reinforced beast mug to the NO REFUNDS sign.",
        "The mug has two handles and, apparently, better consumer rights.",
    ),
    ("rub", "beast drink", "bar", "tavern"): (
        "You drag the reinforced beast mug along the bar.",
        "It leaves a wet trail wide enough for small boats.",
    ),
    ("use", "coin", "chair", "tavern"): (
        "You place a coin on the chair.",
        "The chair has now earned more today than the raiders.",
    ),
    ("rub", "coin", "chair", "tavern"): (
        "You polish the chair with a coin.",
        "Furniture-backed currency remains a difficult market.",
    ),
    ("use", "crumpled map", "chair", "tavern"): (
        "You spread the crumpled map across the chair.",
        "For the first time, the map accurately depicts a seat.",
    ),
    ("rub", "crumpled map", "chair", "tavern"): (
        "You buff the chair with bad cartography.",
        "The chair is now approximately north.",
    ),
}


TAVERN_STATE_INTERACTIONS = {
    (frozenset({"bootless"}), "pet", None, "bartender"): (
        "You pet the bootless bartender.",
        "He glances at his exposed sock and then at your hand.",
        'Bartender: "You stole my boot. Affection is not restitution."',
    ),
    (frozenset({"damp"}), "pet", None, "bartender"): (
        "You pat the damp bartender on the shoulder.",
        "Your palm comes away wetter and significantly less helpful.",
        'Bartender: "Please stop discovering new forms of towel."',
    ),
    (frozenset({"bootless", "damp"}), "pet", None, "bartender"): (
        "You cautiously pet the damp, bootless bartender.",
        "His wet sock squeaks as he takes one deliberate step away.",
        'Bartender: "You have discovered sympathy in the least useful format."',
    ),
    (frozenset({"fire"}), "pet", None, "bartender"): (
        "You attempt to pet the burning bartender.",
        "The heat negotiates directly with your fingerprints.",
        'Bartender: "Warm, isn\'t it?"',
    ),
    (frozenset({"defeated"}), "pet", None, "bartender"): (
        "You pet the defeated bartender.",
        "He accepts this with the exhausted dignity of a retired siege engine.",
        'Bartender: "Victory laps normally contain less touching."',
    ),
    (frozenset({"beasts_asleep"}), "pet", None, "bartender"): (
        "You pet the bartender after successfully petting the cave problem into submission.",
        'Bartender: "Do not generalise from the monsters."',
    ),
    (frozenset({"treasure_found"}), "pet", None, "bartender"): (
        "You pet the bartender while carrying legendary treasure.",
        'Bartender: "Rich, victorious, and still doing this."',
        "Success has not improved you.",
    ),
    (frozenset({"hostile"}), "pet", None, "bartender"): (
        "You reach toward the hostile bartender with petting intent.",
        "He raises one eyebrow with enough force to stop your hand.",
    ),
    (frozenset({"bootless"}), "inspect", None, "bartender"): (
        "You inspect the bootless bartender.",
        "One sock. One boot. Zero forgiveness.",
    ),
    (frozenset({"damp"}), "inspect", None, "bartender"): (
        "You inspect the damp bartender.",
        "His apron is steaming faintly and his expression is not.",
    ),
    (frozenset({"fire"}), "inspect", None, "bartender"): (
        "You inspect the burning bartender.",
        "He appears healthier than the furniture around him.",
        "This is medically unhelpful.",
    ),
    (frozenset({"defeated"}), "inspect", None, "bartender"): (
        "You inspect the defeated bartender.",
        "His pride is bruised. The chair is structurally worse.",
    ),
    (frozenset({"beasts_asleep"}), "inspect", None, "bartender"): (
        "You inspect the bartender after the peaceful cave victory.",
        "He looks exactly like a man reconsidering his ranking of local wildlife.",
    ),
    (frozenset({"treasure_found"}), "inspect", None, "bartender"): (
        "You inspect the bartender after finding the treasure.",
        "He looks annoyingly unsurprised that the secret was eventually found.",
    ),
    (frozenset({"bootless"}), "poke", None, "bartender"): (
        "You poke the bootless bartender.",
        "He points at the missing boot without saying a word.",
        "The silence contains an invoice.",
    ),
    (frozenset({"damp"}), "poke", None, "bartender"): (
        "You poke the damp bartender.",
        "Your finger makes a tiny wet squeak.",
        'Bartender: "Excellent. Diagnostics."',
    ),
    (frozenset({"fire"}), "poke", None, "bartender"): (
        "You poke the burning bartender.",
        "Your finger votes against a second measurement.",
    ),
    (frozenset({"defeated"}), "poke", None, "bartender"): (
        "You poke the defeated bartender.",
        'Bartender: "The fight ended. Your field study apparently did not."',
    ),
    (frozenset({"bootless"}), "kick", None, "bartender"): (
        "You consider kicking the bootless bartender.",
        "His remaining boot shifts half an inch toward you.",
        "You reconsider with admirable speed.",
    ),
    (frozenset({"fire"}), "kick", None, "bartender"): (
        "You attempt a warning kick at the burning bartender.",
        "Heat reaches your trouser cuff before courage reaches him.",
    ),
    (frozenset({"defeated"}), "kick", None, "bartender"): (
        "You mime a kick at the defeated bartender.",
        "He taps the ruined chair.",
        'Bartender: "We have already completed this module."',
    ),
    (frozenset({"bootless"}), "sit", None, "bartender"): (
        "You attempt to sit on the bootless bartender.",
        "He moves the exposed sock out of danger first.",
        "Priorities.",
    ),
    (frozenset({"fire"}), "sit", None, "bartender"): (
        "You consider sitting on the burning bartender.",
        "The narrator opens the fire-safety manual to a random page and points.",
    ),
    (frozenset({"defeated"}), "sit", None, "bartender"): (
        "You attempt to sit on the defeated bartender.",
        "He silently indicates the surviving chair.",
        "Even surrender has boundaries.",
    ),
    (frozenset({"beasts_asleep"}), "sit", None, "bartender"): (
        "You attempt to sit on the bartender after sitting beside sleeping cave beasts.",
        'Bartender: "The monsters have corrupted your understanding of furniture."',
    ),
    (frozenset(), "use", "impossible drink", "bartender"): (
        "You offer the bartender the Impossible Drink.",
        "He holds it up to the lantern light.",
        'Bartender: "I do not stock this. I resent the competition."',
    ),
    (frozenset({"bootless"}), "use", "impossible drink", "bartender"): (
        "You offer the bartender the Impossible Drink.",
        "He looks at reality's surrender, then at his exposed sock.",
        'Bartender: "The universe gave you a beverage before you gave me my boot back."',
    ),
    (frozenset({"fire"}), "use", "impossible drink", "bartender"): (
        "You offer the Impossible Drink to the burning bartender.",
        "Condensation crawls uphill on the bottle.",
        'Bartender: "Tempting. But I have finally found my preferred serving temperature."',
    ),
    (frozenset({"damp"}), "use", "impossible drink", "bartender"): (
        "You offer the Impossible Drink to the damp bartender.",
        "He stares at the condensation.",
        'Bartender: "I have had enough liquids applied to me today."',
    ),
    (frozenset({"defeated"}), "use", "impossible drink", "bartender"): (
        "You offer the Impossible Drink to the defeated bartender.",
        'Bartender: "No. I have already lost one contest with you today."',
    ),
    (frozenset({"beasts_asleep"}), "use", "impossible drink", "bartender"): (
        "You show the bartender the Impossible Drink after hydrating the cave beasts.",
        'Bartender: "Of course reality serves you after I comp the wildlife."',
    ),
    (frozenset(), "rub", "impossible drink", "bartender face"): (
        "You gently press the cold Impossible Drink to the bartender's cheek.",
        "For a moment his reflection appears on the wrong side of the bottle.",
        'Bartender: "I liked lager skincare better."',
    ),
    (frozenset({"bootless"}), "rub", "impossible drink", "bartender face"): (
        "You moisturize the bootless bartender with impossible condensation.",
        'Bartender: "My footwear is missing and causality is now on my face."',
    ),
    (frozenset({"fire"}), "rub", "impossible drink", "bartender face"): (
        "You press the Impossible Drink to the burning bartender's cheek.",
        "The bottle stays cold. The fire stays lit. Physics resigns.",
        'Bartender: "Now THAT is refreshing."',
    ),
    (frozenset({"damp", "bootless"}), "rub", "impossible drink", "bartender face"): (
        "You apply impossible condensation to the damp, bootless bartender.",
        "Nothing about the moisture budget improves.",
        'Bartender: "I am begging you to discover towels."',
    ),
    (frozenset({"bootless"}), "use", "beast drink", "bartender"): (
        "You offer the beast drink back to the bootless bartender.",
        'Bartender: "That is for the monsters. My monster is apparently footwear theft."',
    ),
    (frozenset({"damp"}), "rub", "crumpled map", "bartender"): (
        "You dab the damp bartender with the crumpled map.",
        "The map absorbs water and loses another county.",
        'Bartender: "At last. Cartographic towelling."',
    ),
    (frozenset({"bootless"}), "use", "hidden treasure", "bartender"): (
        "You present the legendary treasure to the bootless bartender.",
        "He looks at the treasure. Then at his sock.",
        'Bartender: "Buy me a boot."',
    ),
    (frozenset({"fire"}), "rub", "beast drink", "bartender face"): (
        "You hold the reinforced beast mug near the burning bartender's face.",
        "The surface begins to steam.",
        'Bartender: "Do not waste the monsters\' drink on climate control."',
    ),
}
