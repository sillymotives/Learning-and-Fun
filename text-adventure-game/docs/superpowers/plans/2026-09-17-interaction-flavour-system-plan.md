# Interaction and Flavour System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a scalable, state-aware flavour interaction engine with 80-120 bespoke interactions, standalone curiosity verbs, contextual tavern objects, cosmetic achievements, rotating fallbacks, and quest-integrity regression coverage.

**Architecture:** Move static interaction content and alias normalization into `game/interactions.py`; keep state-changing reactions as small `Game` methods selected by handler names. Add `game/achievements.py` for cosmetic achievement metadata. `Game` remains the owner of mutable state, parser routing, contextual availability, and output, while the new data modules remain side-effect free.

**Tech Stack:** Python 3, pytest, existing `Game`/`Player`/`Item` classes, standard library only.

**Spec:** `docs/superpowers/specs/2026-09-17-interaction-flavour-system-design.md`

## Global Constraints

- The first implementation batch must contain roughly **80-120 bespoke interactions** plus reusable fallbacks.
- Quest-critical inventory items are never consumed by flavour interactions.
- `use <item> on <target>` must not silently replace existing critical-path `use <item>` behaviour.
- Optional interactions must not permanently remove the bartender, raiders, exits, key, torch, sword, or treasure unless an already-designed quest outcome does so.
- Optional comedy state must not block access to the key, cave, sword, forest, or treasure.
- Generic fallbacks never mutate quest state.
- Achievements never mutate quest state.
- Potentially destructive jokes such as torch-on-forest are flavour only unless separately designed.
- Flavour rotation must be deterministic so tests do not rely on randomness.
- No third-party dependencies.

---

## File Structure

- Create `game/interactions.py`: aliases, room targets, static exact interactions, room fallbacks, generic fallbacks, and pure normalization/look-up helpers.
- Create `game/achievements.py`: immutable achievement metadata.
- Create `tests/test_interactions.py`: focused parser, resolver, achievement, state-aware flavour, interaction-count, and quest-integrity tests.
- Modify `game/game.py`: import new data/helpers; add cosmetic state; add contextual-object resolution; add standalone flavour verbs; route exact static/stateful interactions; keep existing quest methods intact.
- Leave `adventure_game.py`, `game/items.py`, `game/player.py`, `game/world.py`, and `data/story.json` unchanged.

---

### Task 1: Pure interaction data and normalization

**Files:**
- Create: `game/interactions.py`
- Create: `tests/test_interactions.py`

**Interfaces:**
- Produces: `normalize_item(name: str) -> str`
- Produces: `normalize_target(name: str) -> str`
- Produces: `normalize_verb(name: str) -> str`
- Produces: `get_static_interaction(verb: str, item: str | None, target: str, room_id: str) -> tuple[str, ...] | None`
- Produces: constants `ITEM_ALIASES`, `TARGET_ALIASES`, `VERB_ALIASES`, `ROOM_TARGETS`, `STATIC_INTERACTIONS`, `ROOM_FALLBACKS`, `GENERIC_FALLBACKS`

- [ ] **Step 1: Write failing normalization tests**

Create `tests/test_interactions.py` with:

```python
from game.interactions import (
    STATIC_INTERACTIONS,
    normalize_item,
    normalize_target,
    normalize_verb,
)


def test_interaction_alias_normalization():
    assert normalize_item("left boot") == "bartender's left boot"
    assert normalize_item("blade") == "sword"
    assert normalize_target("the barkeep") == "bartender"
    assert normalize_target("stone walls") == "wall"
    assert normalize_verb("examine") == "inspect"
    assert normalize_verb("stroke") == "pet"


def test_static_interaction_pack_is_large_enough():
    assert 80 <= len(STATIC_INTERACTIONS) <= 120
```

- [ ] **Step 2: Run tests to verify RED**

Run:

```bash
pytest -q tests/test_interactions.py
```

Expected: import failure because `game.interactions` does not exist.

- [ ] **Step 3: Create normalization tables and helpers**

Create `game/interactions.py` with these exact normalization maps and pure helpers:

```python
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
    "bartender": "bartender",
    "the bartender": "bartender",
    "barkeep": "bartender",
    "the barkeep": "bartender",
    "innkeeper": "bartender",
    "bartender face": "bartender face",
    "bartender's face": "bartender face",
    "his face": "bartender face",
    "face": "bartender face",
    "walls": "wall",
    "stone wall": "wall",
    "stone walls": "wall",
    "tavern wall": "wall",
    "cellar wall": "wall",
    "cave wall": "wall",
    "trees": "tree",
    "forest": "forest",
    "woods": "forest",
    "bushes": "bush",
    "raider": "raiders",
    "raiders": "raiders",
    "the raiders": "raiders",
    "casks": "cask",
    "barrels": "cask",
    "barrel": "cask",
    "iron door": "cellar door",
    "door": "door",
    "glowing eyes": "glowing eyes",
    "eyes": "glowing eyes",
    "beast den": "beast den",
    "den": "beast den",
    "bones": "bones",
    "floor": "floor",
    "ground": "floor",
    "chair": "chair",
    "bar": "bar",
    "counter": "bar",
    "sign": "sign",
    "trophy": "trophies",
    "trophies": "trophies",
    "lantern": "lantern",
    "lanterns": "lantern",
    "torch bracket": "torch bracket",
    "stairs": "stairs",
    "damp stone": "damp stone",
    "darkness": "darkness",
    "stone": "stone",
    "path": "path",
    "grass": "grass",
    "mud": "mud",
    "spoon": "spoon",
    "spoons": "spoon",
    "fork": "fork",
    "forks": "fork",
}

VERB_ALIASES = {
    "look": "inspect",
    "examine": "inspect",
    "inspect": "inspect",
    "prod": "poke",
    "poke": "poke",
    "kick": "kick",
    "lick": "lick",
    "taste": "lick",
    "stroke": "pet",
    "pat": "pet",
    "pet": "pet",
    "sit": "sit",
    "use": "use",
    "rub": "rub",
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
```

- [ ] **Step 4: Add the exact static interaction registry**

Use tuple keys `(verb, item_or_none, target, room_or_none)`. A `None` room means all rooms. Each value is a tuple of printable lines. These 95 keys form the first curated pack:

```python
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
    key = (normalize_verb(verb), normalize_item(item) if item is not None else None, normalize_target(target), room_id)
    return STATIC_INTERACTIONS.get(key) or STATIC_INTERACTIONS.get((key[0], key[1], key[2], None))
```

- [ ] **Step 5: Run pure-data tests**

Run `pytest -q tests/test_interactions.py`. Expected: both tests pass and registry count is within 80-120.

- [ ] **Step 6: Commit Task 1**

```bash
git add game/interactions.py tests/test_interactions.py
git commit -m "Add interaction flavour data registry"
```

---

### Task 2: Parser routing and generic standalone flavour verbs

**Files:**
- Modify: `game/game.py`
- Modify: `tests/test_interactions.py`

**Interfaces:**
- Consumes Task 1 helpers.
- Produces `Game.flavour_action(verb, target_name)`, `_print_interaction_lines(lines)`, `_interaction_fallback(verb, item, target)`, `flavour_counts`, and `optional_interaction_count`.

- [ ] **Step 1: Write failing parser tests**

```python
from game.game import Game


def test_standalone_flavour_verbs_are_routed(capsys):
    game = Game()
    game.handle_command("inspect chair")
    first = capsys.readouterr().out.lower()
    game.handle_command("pet chair")
    second = capsys.readouterr().out.lower()
    game.handle_command("sit on chair")
    third = capsys.readouterr().out.lower()
    assert "combat experience" in first
    assert "gentlest interaction" in second
    assert "manufacturer intent" in third


def test_malformed_standalone_flavour_command_is_helpful(capsys):
    game = Game()
    game.handle_command("poke")
    assert "poke what" in capsys.readouterr().out.lower()


def test_unknown_flavour_target_uses_rotating_fallback(capsys):
    game = Game()
    game.handle_command("inspect chandelier")
    first = capsys.readouterr().out
    game.handle_command("inspect chandelier")
    second = capsys.readouterr().out
    assert first != second
```

- [ ] **Step 2: Run RED tests**

Run `pytest -q tests/test_interactions.py -k 'standalone or malformed or unknown_flavour'`. Expected: failures because these verbs are unknown.

- [ ] **Step 3: Import helpers and add state**

Import `GENERIC_FALLBACKS`, `ROOM_FALLBACKS`, `ROOM_TARGETS`, `get_static_interaction`, `normalize_item`, `normalize_target`, and `normalize_verb`. In `__init__`, keep `item_interaction_count` for backward compatibility and add:

```python
self.optional_interaction_count = 0
self.flavour_counts = {}
self.interaction_targets_seen = set()
```

- [ ] **Step 4: Add printing/fallback helpers**

```python
def _print_interaction_lines(self, lines):
    for line in lines:
        print(line)


def _record_optional_interaction(self, verb, item, target):
    self.optional_interaction_count += 1
    if item:
        self.interaction_targets_seen.add((item, target))


def _interaction_fallback(self, verb, item, target):
    room_lines = ROOM_FALLBACKS.get(self.current_room, ())
    pool = room_lines + GENERIC_FALLBACKS
    key = (normalize_verb(verb), normalize_item(item) if item else None, normalize_target(target), self.current_room, "fallback")
    index = self.flavour_counts.get(key, 0)
    prefix = f"You {normalize_verb(verb)}"
    if item:
        prefix += f" the {normalize_item(item)} on the {normalize_target(target)}."
    else:
        prefix += f" the {normalize_target(target)}."
    print(prefix)
    print(pool[index % len(pool)])
    self.flavour_counts[key] = index + 1
    self._record_optional_interaction(normalize_verb(verb), normalize_item(item) if item else None, normalize_target(target))


def flavour_action(self, verb, target_name):
    verb = normalize_verb(verb)
    target = normalize_target(target_name)
    if not target:
        print(f"{verb.capitalize()} what?")
        return
    lines = get_static_interaction(verb, None, target, self.current_room)
    if lines:
        self._print_interaction_lines(lines)
        self._record_optional_interaction(verb, None, target)
        return
    self._interaction_fallback(verb, None, target)
```

- [ ] **Step 5: Route standalone verbs**

Before `take` handling in `handle_command`, add:

```python
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
```

Leave existing bare `look` room-description behaviour unchanged.

- [ ] **Step 6: Update help**

Add exact lines:

```python
print("  inspect <target>        examine scenery or people")
print("  poke/kick/lick <target> bother the scenery")
print("  pet <target>            attempt diplomacy through touching")
print("  sit [on <target>]       sit somewhere questionable")
```

- [ ] **Step 7: Run targeted and full tests**

Run `pytest -q tests/test_interactions.py` then `pytest -q`. Expected: all pass.

- [ ] **Step 8: Commit Task 2**

```bash
git add game/game.py tests/test_interactions.py
git commit -m "Add standalone flavour command routing"
```

---

### Task 3: Contextual items and static item-on-target resolver

**Files:**
- Modify: `game/game.py`
- Modify: `tests/test_interactions.py`

**Interfaces:**
- Produces `Game._available_interaction_item(item_name)`.
- Contextual `drink` is available in the tavern only after the first purchase; contextual `mug` is always available in the tavern.

- [ ] **Step 1: Write failing tests**

```python
def test_drink_becomes_contextual_after_first_purchase(capsys):
    game = Game()
    game.drink_from_bar()
    capsys.readouterr()
    game.handle_command("rub drink on bartender face")
    assert "watched you do it" in capsys.readouterr().out.lower()


def test_drink_is_unavailable_before_purchase(capsys):
    game = Game()
    game.handle_command("rub drink on bartender face")
    assert "not available" in capsys.readouterr().out.lower()


def test_tavern_mug_is_contextual(capsys):
    game = Game()
    game.handle_command("rub mug on bartender")
    assert "cloths" in capsys.readouterr().out.lower()


def test_static_item_interaction_does_not_consume_quest_item(capsys):
    game = Game()
    game.torch_taken = True
    game.handle_command("use torch on wall")
    capsys.readouterr()
    assert game.torch_taken is True
```

- [ ] **Step 2: Run RED tests**

Run `pytest -q tests/test_interactions.py -k 'contextual or unavailable or consume'`.

- [ ] **Step 3: Replace `_carried_interaction_item` with `_available_interaction_item`**

Normalize with `normalize_item`. Retain existing coin, torch, sword, and inventory logic. Add:

```python
if canonical == "drink":
    if self.current_room == "tavern" and self.drinks_bought >= 1:
        return "drink"
    return None
if canonical == "mug":
    if self.current_room == "tavern":
        return "mug"
    return None
```

- [ ] **Step 4: Refactor `use_item_on`**

Normalize item, target, and action. Keep state-mutating routes before the static lookup. Then:

```python
lines = get_static_interaction(action, item, target, self.current_room)
if lines:
    self._print_interaction_lines(lines)
    self._record_optional_interaction(action, item, target)
    return
self._interaction_fallback(action, item, target)
```

For unavailable contextual items print `That <item> is not available here.`; for inventory items retain `You are not carrying ...`. Remove old static special-case branches only after their equivalent registry entries exist.

- [ ] **Step 5: Run tests**

Run `pytest -q tests/test_interactions.py` then `pytest -q`.

- [ ] **Step 6: Commit Task 3**

```bash
git add game/game.py tests/test_interactions.py
git commit -m "Add contextual item interaction resolver"
```

---

### Task 4: Cosmetic achievements

**Files:**
- Create: `game/achievements.py`
- Modify: `game/game.py`
- Modify: `tests/test_interactions.py`

**Interfaces:**
- Produces `ACHIEVEMENTS`, `Game.achievements`, `Game.boot_targets_seen`, `_unlock_achievement`, and `_evaluate_interaction_achievements`.

- [ ] **Step 1: Write failing achievement tests**

```python
def test_bartender_moisturized_unlocks_once(capsys):
    game = Game()
    game.drink_from_bar()
    capsys.readouterr()
    game.handle_command("rub drink on bartender face")
    first = capsys.readouterr().out.lower()
    game.handle_command("rub drink on bartender face")
    second = capsys.readouterr().out.lower()
    assert "achievement unlocked" in first
    assert "bartender moisturized" in first
    assert "achievement unlocked" not in second


def test_wall_licked_is_cosmetic(capsys):
    game = Game()
    before = (game.current_room, game.lock_open, game.victory, game.running)
    game.handle_command("lick wall")
    output = capsys.readouterr().out.lower()
    after = (game.current_room, game.lock_open, game.victory, game.running)
    assert "wall licked" in output
    assert before == after


def test_attempted_capitalism_on_stone(capsys):
    game = Game()
    game.handle_command("use coin on wall")
    assert "attempted capitalism on stone" in capsys.readouterr().out.lower()


def test_training_arc_unlocks_at_100_optional_interactions(capsys):
    game = Game()
    for _ in range(100):
        game.handle_command("inspect chandelier")
    output = capsys.readouterr().out.lower()
    assert "training arc" in output
    assert "100 pushups" in output
    assert "100 situps" in output
    assert "10 km run" in output
```

- [ ] **Step 2: Run RED tests**

Run `pytest -q tests/test_interactions.py -k 'moisturized or wall_licked or capitalism or training_arc'`.

- [ ] **Step 3: Create metadata**

`game/achievements.py`:

```python
ACHIEVEMENTS = {
    "bartender_moisturized": "Bartender Moisturized",
    "wall_licked": "Wall Licked",
    "attempted_capitalism_on_stone": "Attempted Capitalism On Stone",
    "applied_science": "Applied Science",
    "training_arc": "Training Arc",
}
```

- [ ] **Step 4: Add state and evaluation**

In `__init__`:

```python
self.achievements = set()
self.boot_targets_seen = set()
```

Add:

```python
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
```

Call evaluation exactly once from `_record_optional_interaction` after incrementing.

- [ ] **Step 5: Run tests**

Run targeted achievement tests then `pytest -q`.

- [ ] **Step 6: Commit Task 4**

```bash
git add game/achievements.py game/game.py tests/test_interactions.py
git commit -m "Add cosmetic interaction achievements"
```

---

### Task 5: Stateful bartender flavour combinations

**Files:**
- Modify: `game/game.py`
- Modify: `tests/test_interactions.py`

**Interfaces:**
- Produces `Game._handle_stateful_interaction(verb, item, target) -> bool`.
- Preserves existing bartender ignition and sword-combat behaviour.

- [ ] **Step 1: Write failing state tests**

```python
def _buy_drink(game, capsys):
    game.drink_from_bar()
    capsys.readouterr()


def test_burning_bartender_calls_face_ale_refreshing(capsys):
    game = Game()
    _buy_drink(game, capsys)
    game.torch_taken = True
    game.handle_command("use torch on bartender")
    capsys.readouterr()
    game.handle_command("rub drink on bartender face")
    output = capsys.readouterr().out.lower()
    assert "hisses" in output
    assert "refreshing" in output


def test_bootless_bartender_objects_to_lager_moisturizer(capsys):
    game = Game()
    _buy_drink(game, capsys)
    game.handle_command("steal from bartender")
    capsys.readouterr()
    game.handle_command("rub drink on bartender face")
    output = capsys.readouterr().out.lower()
    assert "stole my boot" in output
    assert "moistur" in output


def test_burning_bootless_bartender_misses_normal_customers(capsys):
    game = Game()
    _buy_drink(game, capsys)
    game.handle_command("steal from bartender")
    capsys.readouterr()
    game.torch_taken = True
    game.handle_command("use torch on bartender")
    capsys.readouterr()
    game.handle_command("rub drink on bartender face")
    output = capsys.readouterr().out.lower()
    assert "stole my boot" in output
    assert "set me on fire" in output
    assert "normal customers" in output
```

- [ ] **Step 2: Run RED tests**

Run `pytest -q tests/test_interactions.py -k 'refreshing or moisturizer or normal_customers'`.

- [ ] **Step 3: Add stateful dispatcher**

```python
def _handle_stateful_interaction(self, verb, item, target):
    if self.current_room != "tavern":
        return False
    if item == "torch" and target == "bartender":
        self.ignite_bartender()
        return True
    if item == "sword" and target == "bartender":
        print("You apply the sword to the bartender.")
        print("This is generally known as starting a fight.")
        self.fight_bartender()
        return True
    if verb == "rub" and item == "drink" and target == "bartender face":
        if self.bartender_on_fire and self.bartender_boot_stolen:
            print("The ale hisses against the bartender's burning face.")
            print('Bartender: "You stole my boot, set me on fire, and now you are moisturizing me with lager."')
            print('Bartender: "I miss normal customers."')
            return True
        if self.bartender_on_fire:
            print("The ale hisses against the bartender's face.")
            print('Bartender: "Refreshing."')
            return True
        if self.bartender_boot_stolen:
            print('Bartender: "You stole my boot and now you are moisturizing me with lager."')
            print('Bartender: "There are easier ways to become memorable."')
            return True
    return False
```

Call before static lookup. Record optional interaction once for the three drink-on-face flavour states, but do not count torch ignition or sword combat as optional flavour.

- [ ] **Step 4: Run tests**

Run targeted bartender tests then `pytest -q`.

- [ ] **Step 5: Commit Task 5**

```bash
git add game/game.py tests/test_interactions.py
git commit -m "Add state-aware bartender flavour reactions"
```

---

### Task 6: Quest-integrity regression tests

**Files:**
- Modify: `tests/test_interactions.py`

**Interfaces:**
- Produces explicit proof that optional flavour cannot consume critical items or block a complete victory route.

- [ ] **Step 1: Add integrity tests**

```python
def test_flavour_spam_preserves_critical_inventory_and_state(capsys):
    game = Game()
    game.player.coins = 5
    game.drink_from_bar()
    capsys.readouterr()
    game.current_room = "root_cellar"
    game.take_item("torch")
    capsys.readouterr()
    for command in ["use coin on wall", "rub key on torch", "lick wall", "kick cask", "pet torch", "sit on cask"]:
        game.handle_command(command)
        capsys.readouterr()
    assert game.running is True
    assert game.torch_taken is True
    assert any(item.name.lower() == "old key" for item in game.player.inventory)


def test_normal_win_route_survives_optional_interaction_spam(capsys):
    game = Game()
    game.player.coins = 5
    for command in ["inspect chair", "lick wall", "pet bartender", "kick bar"]:
        game.handle_command(command)
        capsys.readouterr()
    game.drink_from_bar(); capsys.readouterr()
    game.move("north"); capsys.readouterr()
    game.handle_command("use coin on wall"); capsys.readouterr()
    game.take_item("torch"); capsys.readouterr()
    game.use_item("key"); capsys.readouterr()
    game.move("north"); capsys.readouterr()
    game.resolve_cave_fight(use_torch=False); capsys.readouterr()
    game.move("east"); capsys.readouterr()
    game.handle_command("fight raiders"); capsys.readouterr()
    game.take_item("hidden treasure"); capsys.readouterr()
    assert game.victory is True
    assert game.state == "victory"
```

- [ ] **Step 2: Run targeted tests**

Run `pytest -q tests/test_interactions.py -k 'preserves_critical or normal_win_route'`. Expected: PASS.

- [ ] **Step 3: Run complete suite and source checks**

```bash
python -m py_compile adventure_game.py game/*.py
pytest -q
git diff --check
```

- [ ] **Step 4: Verify curated count and required phrases**

```bash
python - <<'PY'
from game.interactions import STATIC_INTERACTIONS
assert 80 <= len(STATIC_INTERACTIONS) <= 120, len(STATIC_INTERACTIONS)
print(f"Bespoke static interactions: {len(STATIC_INTERACTIONS)}")
PY

grep -R "Bartender Moisturized" -n game tests
grep -R "100 pushups" -n game tests
```

- [ ] **Step 5: Commit Task 6**

```bash
git add tests/test_interactions.py
git commit -m "Protect quest route from flavour interactions"
```

---

### Task 7: Final help text and smoke verification

**Files:**
- Modify: `game/game.py` only if help copy needs alignment.
- Modify: `tests/test_interactions.py`

- [ ] **Step 1: Add help assertion**

```python
def test_help_lists_flavour_commands(capsys):
    game = Game()
    game.print_help()
    output = capsys.readouterr().out.lower()
    assert "inspect <target>" in output
    assert "poke/kick/lick <target>" in output
    assert "pet <target>" in output
    assert "sit [on <target>]" in output
```

- [ ] **Step 2: Run help test**

Run `pytest -q tests/test_interactions.py::test_help_lists_flavour_commands`. Expected: PASS after Task 2; if it fails, modify only `print_help` to match the four exact strings.

- [ ] **Step 3: Run final automated verification**

```bash
python -m py_compile adventure_game.py game/*.py
pytest -q
git diff --check
git status --short
```

Expected: no test failures, no compile errors, no whitespace errors, and only intended changes before any final commit.

- [ ] **Step 4: Manual smoke test**

Run `python adventure_game.py` and exercise:

```text
inspect chair
pet bartender
lick wall
drink
rub drink on bartender face
steal from bartender
rub boot on wall
use torch on bartender
fight bartender
```

Confirm new parser forms work, achievements announce once, and quest commands retain existing behaviour.

- [ ] **Step 5: Commit final help/test alignment if changed**

```bash
git add game/game.py tests/test_interactions.py
git commit -m "Polish interaction flavour command help"
```

Skip if Task 7 produces no file changes.

- [ ] **Step 6: Final history review**

```bash
git status -sb
git log -8 --oneline --decorate
```

Expected: clean feature branch containing interaction-data, parser, contextual-item, achievement, bartender-state, and quest-integrity commits.
