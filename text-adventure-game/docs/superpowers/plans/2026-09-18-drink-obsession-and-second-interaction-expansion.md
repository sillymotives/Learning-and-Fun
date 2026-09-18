# Drink Obsession and Second Interaction Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a 5/10/20/50/100 drink-obsession arc with an Impossible Drink alternate ending, plus at least 100 new bespoke interaction rules organized into focused flavour packs.

**Architecture:** Keep `game/interactions.py` as the normalization and lookup hub. Add four focused content packs for tavern, beasts/cave, cellar, and forest; static rules use the existing tuple-key registry, while bartender and beast state variants use small state-aware tables selected by named handlers in `Game`. The Impossible Drink is a real inventory item, but only the explicit `drink impossible drink` command consumes it and ends the run.

**Tech Stack:** Python 3, pytest, existing tuple-key interaction registry, existing `Game` state model.

**Spec:** `docs/superpowers/specs/2026-09-18-drink-obsession-and-second-interaction-expansion-design.md`

## Global Constraints

- Failed-drink milestones occur at exactly **5 / 10 / 20 / 50 / 100**.
- Attempt 20 awards exactly one inventory item named **Impossible Drink**.
- `drink impossible drink` is the only action that consumes the Impossible Drink.
- Drinking the Impossible Drink sets `victory = True`, `state = "victory"`, and `running = False`.
- Attempt 100 unlocks the cosmetic achievement **Longitudinal Study**.
- The implementation adds at least **100 new bespoke interaction rule keys** beyond the current interaction registries.
- Multiple alternate lines for one rule key do not increase the rule count.
- Static flavour must not consume quest-critical inventory.
- The normal treasure route, beast-drink route, and flaming-boot cave route must remain completable.
- Existing bartender lick-state behavior remains authoritative unless a new rule is deliberately more specific.
- Existing lethal hostile-beast actions remain lethal unless the beast is in a more specific thirsty or sleeping state.
- `game/flavour_expansion.py` remains intact unless a compatibility change is strictly necessary.
- No new generic rules DSL and no parser rewrite.

---

### Task 1: Drink obsession milestones, Impossible Drink, and alternate victory

**Files:**
- Modify: `game/game.py`
- Modify: `game/interactions.py`
- Modify: `game/achievements.py`
- Modify: `tests/test_economy.py`

**Interfaces:**
- Consumes: existing `Game.failed_drink_attempts`, `Player.add_item(Item(...))`, `Player.remove_item(name)`, `normalize_item(name)`, `Game._unlock_achievement(key)`.
- Produces:
  - item alias `normalize_item("impossible") == "impossible drink"`
  - `Game._has_inventory_item(name: str) -> bool`
  - `Game._handle_drink_obsession_milestone(attempt: int) -> None`
  - `Game.drink_impossible_drink() -> None`
  - achievement key `"longitudinal_study"`

- [ ] **Step 1: Write failing milestone and reward tests**

Add to `tests/test_economy.py`:

```python
import pytest

from game.items import Item


@pytest.mark.parametrize(
    ("start", "expected"),
    [
        (4, "pattern"),
        (9, "habit"),
        (19, "reality"),
        (49, "fifty"),
        (99, "attempt 100"),
    ],
)
def test_wrong_place_drink_milestones_are_5_10_20_50_100(capsys, start, expected):
    game = Game()
    game.current_room = "forest_path"
    game.failed_drink_attempts = start

    game.drink_from_bar()
    output = capsys.readouterr().out.lower()

    assert expected in output


def test_old_25_drink_milestone_is_gone(capsys):
    game = Game()
    game.current_room = "forest_path"
    game.failed_drink_attempts = 24

    game.drink_from_bar()
    output = capsys.readouterr().out.lower()

    assert "milestone" not in output
    assert "twenty-five" not in output


def test_attempt_20_awards_exactly_one_impossible_drink(capsys):
    game = Game()
    game.current_room = "root_cellar"
    game.failed_drink_attempts = 19

    game.drink_from_bar()
    first = capsys.readouterr().out.lower()

    assert "universe has capitulated" in first
    assert sum(item.name.lower() == "impossible drink" for item in game.player.inventory) == 1

    game.failed_drink_attempts = 19
    game.drink_from_bar()
    capsys.readouterr()

    assert sum(item.name.lower() == "impossible drink" for item in game.player.inventory) == 1
```

- [ ] **Step 2: Run the milestone tests and confirm RED**

Run:

```bash
pytest -q tests/test_economy.py::test_wrong_place_drink_milestones_are_5_10_20_50_100 tests/test_economy.py::test_old_25_drink_milestone_is_gone tests/test_economy.py::test_attempt_20_awards_exactly_one_impossible_drink
```

Expected: failures because the current milestones are 10/25/50/100 and no Impossible Drink exists.

- [ ] **Step 3: Add the Impossible Drink aliases and achievement name**

In `game/interactions.py`, extend `ITEM_ALIASES`:

```python
    "impossible": "impossible drink",
    "impossible drink": "impossible drink",
```

In `game/achievements.py`:

```python
    "longitudinal_study": "Longitudinal Study",
```

- [ ] **Step 4: Implement inventory and milestone helpers**

In `Game`, add:

```python
    def _has_inventory_item(self, name):
        wanted = name.lower()
        return any(item.name.lower() == wanted for item in self.player.inventory)

    def _handle_drink_obsession_milestone(self, attempt):
        if attempt == 5:
            print("[Drink obsession milestone] Five attempts. This is becoming a pattern.")
            return
        if attempt == 10:
            print("[Drink obsession milestone] Ten attempts. This has officially become a habit.")
            return
        if attempt == 20:
            print("[Drink obsession milestone] Twenty attempts. Reality has filed a complaint.")
            print("There is a small pop.")
            if not self._has_inventory_item("impossible drink"):
                self.player.add_item(Item(
                    "Impossible Drink",
                    "A sealed drink summoned by repeated refusal to accept local beverage availability.",
                ))
            print("A sealed drink appears in your hand.")
            print("It is cold. It is real.")
            print("The universe has capitulated.")
            return
        if attempt == 50:
            print("[Drink obsession milestone] Fifty attempts.")
            if self._has_inventory_item("impossible drink"):
                print("You are carrying a perfectly valid ending.")
                print("You have chosen instead to keep trying to drink the atmosphere.")
            else:
                print("Somewhere, the bartender feels a disturbance in the ale.")
            return
        if attempt == 100:
            print("[Drink obsession milestone] Attempt 100.")
            if self._has_inventory_item("impossible drink"):
                print("You still have a perfectly valid ending in your pocket.")
            print("This is no longer thirst.")
            print("This is a completed research programme.")
            self._unlock_achievement("longitudinal_study")
```

Replace the inline `milestones = {...}` block in `_drink_in_wrong_place()` with:

```python
        self._handle_drink_obsession_milestone(attempt)
```

and remove the old `if attempt in milestones` print.

- [ ] **Step 5: Run milestone tests and confirm GREEN**

Run:

```bash
pytest -q tests/test_economy.py::test_wrong_place_drink_milestones_are_5_10_20_50_100 tests/test_economy.py::test_old_25_drink_milestone_is_gone tests/test_economy.py::test_attempt_20_awards_exactly_one_impossible_drink
```

Expected: PASS.

- [ ] **Step 6: Write failing alternate-victory and capstone tests**

Add to `tests/test_economy.py`:

```python
def test_drink_impossible_drink_requires_inventory(capsys):
    game = Game()

    game.handle_command("drink impossible drink")
    output = capsys.readouterr().out.lower()

    assert "do not have" in output
    assert game.running is True
    assert game.victory is False


def test_impossible_alias_routes_to_same_inventory_drink(capsys):
    game = Game()
    game.player.add_item(Item("Impossible Drink", "Reality gave up."))

    game.handle_command("drink impossible")
    capsys.readouterr()

    assert game.victory is True
    assert not game._has_inventory_item("impossible drink")


def test_drinking_impossible_drink_is_real_alternate_victory(capsys):
    game = Game()
    game.state = "in progress"
    game.player.add_item(Item("Impossible Drink", "Reality gave up."))

    game.handle_command("drink impossible drink")
    output = capsys.readouterr().out.lower()

    assert "you were thirsty" in output
    assert "you win" in output
    assert game.victory is True
    assert game.state == "victory"
    assert game.running is False
    assert not game._has_inventory_item("impossible drink")


def test_50_and_100_notice_unused_winning_drink(capsys):
    game = Game()
    game.current_room = "forest_path"
    game.player.add_item(Item("Impossible Drink", "Reality gave up."))

    game.failed_drink_attempts = 49
    game.drink_from_bar()
    fifty = capsys.readouterr().out.lower()

    game.failed_drink_attempts = 99
    game.drink_from_bar()
    hundred = capsys.readouterr().out.lower()

    assert "valid ending" in fifty
    assert "valid ending" in hundred
    assert "longitudinal study" in hundred
    assert "longitudinal_study" in game.achievements
```

- [ ] **Step 7: Run alternate-victory tests and confirm RED**

Run:

```bash
pytest -q tests/test_economy.py::test_drink_impossible_drink_requires_inventory tests/test_economy.py::test_drinking_impossible_drink_is_real_alternate_victory tests/test_economy.py::test_50_and_100_notice_unused_winning_drink
```

Expected: failures because `drink impossible drink` currently routes to ordinary tavern/environment drinking.

- [ ] **Step 8: Implement explicit Impossible Drink command handling**

Add to `Game`:

```python
    def drink_impossible_drink(self):
        if not self._has_inventory_item("impossible drink"):
            print("You do not have an Impossible Drink.")
            return

        print("You break the seal.")
        print("It tastes like every drink you tried to summon and none of them.")
        print("Rain. Smoke. Ale. Cold stone. Something faintly impossible.")
        print("The tavern, the cave, the forest, the treasure... all of it seems suddenly very far away.")
        print("You were never looking for the secret.")
        print("You were thirsty.")
        print("And now you are not.")
        print("You win.")
        self.player.remove_item("impossible drink")
        self.victory = True
        self.state = "victory"
        self.running = False
```

In `handle_command()`, route the inventory form before the existing plain-drink branch:

```python
        if verb == "drink" and len(parts) > 1:
            requested = normalize_item(" ".join(parts[1:]))
            if requested == "impossible drink":
                self.drink_impossible_drink()
                return
        if verb == "drink":
            self.drink_from_bar()
            return
```

- [ ] **Step 9: Run Task 1 focused tests**

Run:

```bash
pytest -q tests/test_economy.py
```

Expected: PASS, including the existing second-drink and wrong-place behavior tests.

- [ ] **Step 10: Commit Task 1**

```bash
git add game/game.py game/interactions.py game/achievements.py tests/test_economy.py
git commit -m "Add impossible drink obsession ending"
```

---

### Task 2: Tavern pack and bartender state-aware lookup

**Files:**
- Create: `game/flavour_tavern.py`
- Modify: `game/interactions.py`
- Modify: `game/game.py`
- Modify: `tests/test_interactions.py`

**Interfaces:**
- Consumes: normalized verb/item/target values, `Game._bartender_flags() -> frozenset[str]`, existing `bartender_interaction_overlay()`.
- Produces:
  - `TAVERN_STATIC_INTERACTIONS: dict[tuple[str, str | None, str, str], tuple[str, ...]]`
  - `TAVERN_STATE_INTERACTIONS: dict[tuple[frozenset[str], str, str | None, str], tuple[str, ...]]`
  - `get_state_interaction(rules, flags, verb, item, target) -> tuple[str, ...] | None`
  - at least 45 new tavern rule keys, with at least 30 bartender/bartender-face keys and at least 15 tavern-scenery keys

- [ ] **Step 1: Write failing state-lookup and tavern-density tests**

Add imports to `tests/test_interactions.py`:

```python
from game.flavour_tavern import TAVERN_STATIC_INTERACTIONS, TAVERN_STATE_INTERACTIONS
from game.interactions import get_state_interaction
```

Add tests:

```python
def test_tavern_second_wave_has_45_new_rules():
    assert len(TAVERN_STATIC_INTERACTIONS) + len(TAVERN_STATE_INTERACTIONS) >= 45


def test_state_interaction_prefers_most_specific_flags():
    rules = {
        (frozenset({"bootless"}), "pet", None, "bartender"): ("bootless",),
        (frozenset({"bootless", "damp"}), "pet", None, "bartender"): ("specific",),
    }

    lines = get_state_interaction(
        rules,
        frozenset({"bootless", "damp", "was_extinguished"}),
        "pet",
        None,
        "bartender",
    )

    assert lines == ("specific",)


def test_damp_bootless_bartender_pet_beats_generic_pet(capsys):
    game = Game()
    game.bartender_boot_stolen = True
    game.bartender_extinguished = True
    game.bartender_was_extinguished = True

    game.handle_command("pet bartender")
    output = capsys.readouterr().out.lower()

    assert "boot" in output or "sock" in output
    assert "damp" in output or "wet" in output
    assert "reach out and pet" not in output


def test_impossible_drink_on_bartender_is_bespoke_and_preserved(capsys):
    game = Game()
    game.player.add_item(Item("Impossible Drink", "Reality gave up."))

    game.handle_command("use impossible drink on bartender")
    output = capsys.readouterr().out.lower()

    assert "impossible" in output or "reality" in output
    assert game._has_inventory_item("impossible drink")
```

Import `Item` in this test file from `game.items`.

- [ ] **Step 2: Run the new tavern tests and confirm RED**

Run:

```bash
pytest -q tests/test_interactions.py::test_tavern_second_wave_has_45_new_rules tests/test_interactions.py::test_state_interaction_prefers_most_specific_flags tests/test_interactions.py::test_damp_bootless_bartender_pet_beats_generic_pet tests/test_interactions.py::test_impossible_drink_on_bartender_is_bespoke_and_preserved
```

Expected: import or assertion failures because the pack and lookup helper do not exist.

- [ ] **Step 3: Create the state lookup helper**

In `game/interactions.py` add:

```python
def get_state_interaction(rules, flags, verb, item, target):
    matches = []
    for (required, rule_verb, rule_item, rule_target), lines in rules.items():
        if rule_verb != verb or rule_item != item or rule_target != target:
            continue
        if required <= flags:
            matches.append((len(required), lines))
    if not matches:
        return None
    matches.sort(key=lambda pair: pair[0], reverse=True)
    return matches[0][1]
```

Inputs are already normalized before this helper is called. Do not normalize again inside the helper.

- [ ] **Step 4: Create `flavour_tavern.py` with the first 45 new rule keys**

Use this exact module shape:

```python
TAVERN_STATIC_INTERACTIONS = {
    # At least 15 new tavern-scenery or item-on-scenery keys.
}

TAVERN_STATE_INTERACTIONS = {
    # At least 30 bartender or bartender-face keys.
    # Key: (frozenset(required_flags), verb, item_or_none, target)
}
```

Content requirements:

- at least 30 bartender/bartender-face state-aware keys
- at least 15 tavern scenery keys
- 8 to 12 Impossible Drink interactions across the full feature, with several beginning here
- do not duplicate existing bartender lick-pool keys
- do not duplicate existing `STATIC_INTERACTIONS` keys
- include combinations such as damp+bootless, fire+bootless, defeated+bootless, beasts_asleep, beast_drink_given, and treasure_found
- every value is a non-empty tuple of printable strings
- no rule mutates game state

Representative required entries:

```python
TAVERN_STATE_INTERACTIONS = {
    (
        frozenset({"damp", "bootless"}),
        "pet",
        None,
        "bartender",
    ): (
        "You cautiously pet the damp, bootless bartender.",
        "His wet sock squeaks as he takes one deliberate step away.",
        'Bartender: "You have discovered sympathy in the least useful format."',
    ),
    (
        frozenset({"bootless"}),
        "use",
        "impossible drink",
        "bartender",
    ): (
        "You offer the bartender the Impossible Drink.",
        "He looks at reality's surrender, then at his exposed sock.",
        'Bartender: "The universe gave you a beverage before you gave me my boot back."',
    ),
}
```

- [ ] **Step 5: Merge static tavern content into the registry**

In `game/interactions.py`:

```python
from .flavour_tavern import TAVERN_STATIC_INTERACTIONS, TAVERN_STATE_INTERACTIONS

STATIC_INTERACTIONS.update(TAVERN_STATIC_INTERACTIONS)
```

Place the import/update after the existing `flavour_expansion` update so the second-wave pack is clearly separate.

- [ ] **Step 6: Route bartender state content without breaking existing consequences**

In `Game.flavour_action()`, after the existing bartender lick special case and before static lookup:

```python
        if self.current_room == "tavern" and target in {"bartender", "bartender face"}:
            lines = get_state_interaction(
                TAVERN_STATE_INTERACTIONS,
                self._bartender_flags(),
                verb,
                None,
                target,
            )
            if lines:
                self._print_interaction_lines(lines)
                self._record_optional_interaction(verb, None, target)
                return
```

In `Game.use_item_on()`, preserve this precedence:

1. `_handle_stateful_interaction()`
2. new `TAVERN_STATE_INTERACTIONS`
3. existing `bartender_interaction_overlay()`
4. static registry
5. fallback

Add the state table lookup between steps 1 and 3:

```python
        if self.current_room == "tavern" and target in {"bartender", "bartender face"}:
            lines = get_state_interaction(
                TAVERN_STATE_INTERACTIONS,
                self._bartender_flags(),
                action,
                item,
                target,
            )
            if lines:
                self._print_interaction_lines(lines)
                self._record_optional_interaction(action, item, target)
                return
```

Import `TAVERN_STATE_INTERACTIONS` and `get_state_interaction` into `game.py`.

- [ ] **Step 7: Run tavern-focused tests and existing bartender tests**

Run:

```bash
pytest -q tests/test_interactions.py tests/test_bartender_dialogue.py tests/test_lick_states_and_beasts.py
```

Expected: PASS.

- [ ] **Step 8: Commit Task 2**

```bash
git add game/flavour_tavern.py game/interactions.py game/game.py tests/test_interactions.py
git commit -m "Add second-wave tavern interactions"
```

---

### Task 3: Beast and cave pack with hostile/thirsty/sleeping specificity

**Files:**
- Create: `game/flavour_beasts.py`
- Modify: `game/interactions.py`
- Modify: `game/game.py`
- Modify: `tests/test_lick_states_and_beasts.py`

**Interfaces:**
- Consumes: `get_state_interaction()`, `Game.beasts_thirsty`, `Game.beasts_asleep`, `Game.beast_pet_count`, existing explicit lethal and victory handlers.
- Produces:
  - `BEAST_STATIC_INTERACTIONS`
  - `BEAST_STATE_INTERACTIONS`
  - `Game._beast_flavour_flags() -> frozenset[str]`
  - at least 35 new beast/cave rule keys, with at least 25 beast-state keys and at least 10 cave/cave-entrance static keys

- [ ] **Step 1: Write failing beast-state and pack-density tests**

Add to `tests/test_lick_states_and_beasts.py`:

```python
from game.flavour_beasts import BEAST_STATIC_INTERACTIONS, BEAST_STATE_INTERACTIONS


def test_beast_second_wave_has_35_new_rules():
    assert len(BEAST_STATIC_INTERACTIONS) + len(BEAST_STATE_INTERACTIONS) >= 35


def test_poke_beast_changes_across_hostile_thirsty_sleeping_states(capsys):
    hostile = Game()
    put_in_live_beast_cave(hostile)
    hostile.handle_command("poke beast")
    hostile_output = capsys.readouterr().out.lower()
    assert hostile.running is False
    assert "maul" in hostile_output or "lose" in hostile_output

    thirsty = Game()
    put_in_live_beast_cave(thirsty)
    thirsty.beasts_thirsty = True
    thirsty.beast_pet_count = 2
    thirsty.handle_command("poke beast")
    thirsty_output = capsys.readouterr().out.lower()
    assert thirsty.running is True
    assert "thirst" in thirsty_output or "dry" in thirsty_output or "water" in thirsty_output

    sleeping = Game()
    put_in_live_beast_cave(sleeping)
    sleeping.cave_battle_done = True
    sleeping.beasts_asleep = True
    sleeping.handle_command("poke beast")
    sleeping_output = capsys.readouterr().out.lower()
    assert sleeping.running is True
    assert "sleep" in sleeping_output or "cuddle" in sleeping_output or "paw" in sleeping_output


def test_impossible_drink_on_thirsty_beasts_is_bespoke_but_not_the_beast_drink_win(capsys):
    game = Game()
    put_in_live_beast_cave(game)
    game.beasts_thirsty = True
    game.beast_pet_count = 2
    game.player.add_item(Item("Impossible Drink", "Reality gave up."))

    game.handle_command("use impossible drink on beast")
    output = capsys.readouterr().out.lower()

    assert "impossible" in output or "reality" in output
    assert game.cave_battle_done is False
    assert game._has_inventory_item("impossible drink")
```

- [ ] **Step 2: Run the new beast tests and confirm RED**

Run:

```bash
pytest -q tests/test_lick_states_and_beasts.py::test_beast_second_wave_has_35_new_rules tests/test_lick_states_and_beasts.py::test_poke_beast_changes_across_hostile_thirsty_sleeping_states tests/test_lick_states_and_beasts.py::test_impossible_drink_on_thirsty_beasts_is_bespoke_but_not_the_beast_drink_win
```

Expected: import failures and thirsty `poke beast` still taking the hostile lethal path.

- [ ] **Step 3: Create `flavour_beasts.py`**

Use this module shape:

```python
BEAST_STATIC_INTERACTIONS = {
    # At least 10 new cave or cave-entrance static keys.
}

BEAST_STATE_INTERACTIONS = {
    # At least 25 state-aware beast keys.
    # Key: (frozenset(required_flags), verb, item_or_none, target)
}
```

Required state names:

- `beasts_hostile`
- `beasts_thirsty`
- `beasts_asleep`
- optional `beasts_petted` when `beast_pet_count > 0`

Representative entries:

```python
BEAST_STATE_INTERACTIONS = {
    (
        frozenset({"beasts_thirsty"}),
        "poke",
        None,
        "beasts",
    ): (
        "You poke the nearer beast.",
        "It opens one eye, licks a very dry nose, and nudges your hand toward its mouth.",
        "This has become less a threat display and more a customer complaint.",
    ),
    (
        frozenset({"beasts_asleep"}),
        "poke",
        None,
        "beasts",
    ): (
        "You gently poke one sleeping beast.",
        "It sleepily hooks a paw around the other and pulls it closer.",
        "Your experiment becomes cuddling against its will.",
    ),
}
```

Do not redefine the actual `beast drink` victory, flaming-boot victory, plain-boot death, or torch death as static content.

- [ ] **Step 4: Add beast flags and route state tables before hostile deaths**

In `Game`:

```python
    def _beast_flavour_flags(self):
        flags = set()
        if self.beasts_asleep:
            flags.add("beasts_asleep")
        elif self.beasts_thirsty:
            flags.add("beasts_thirsty")
        else:
            flags.add("beasts_hostile")
        if self.beast_pet_count > 0:
            flags.add("beasts_petted")
        return frozenset(flags)
```

Refactor `_handle_beast_flavour()` to use this exact precedence:

1. If `beasts_asleep`, query `BEAST_STATE_INTERACTIONS` first and return on a match. Sleeping actions must never fall into live-beast pet progression or hostile deaths.
2. If `cave_battle_done` and the beasts are not asleep, keep the existing “beasts are gone” response.
3. If `verb == "pet"` and the beasts are live, preserve the existing pet progression because it mutates `beast_pet_count` and `beasts_thirsty`.
4. For live beasts, query `BEAST_STATE_INTERACTIONS`. This gives thirsty variants precedence over hostile behavior.
5. Preserve the existing hostile `inspect` response and lethal `poke/lick/kick/sit` branches as the fallback for live, non-thirsty beasts.
6. If none match, return `False` and allow the normal interaction system to continue.

Use this lookup in steps 1 and 4:

```python
        lines = get_state_interaction(
            BEAST_STATE_INTERACTIONS,
            self._beast_flavour_flags(),
            verb,
            None,
            target,
        )
        if lines:
            self._print_interaction_lines(lines)
            self._record_optional_interaction(verb, None, target)
            return True
```

- [ ] **Step 5: Route beast item state content after explicit consequence items**

In `_handle_beast_item_interaction()`, preserve explicit consequence precedence:

1. beast drink victory
2. plain/flaming boot route
3. torch route
4. existing map/key/coin behaviors where already bespoke
5. new state table
6. static/fallback path

For new state lookup:

```python
        lines = get_state_interaction(
            BEAST_STATE_INTERACTIONS,
            self._beast_flavour_flags(),
            verb,
            item,
            target,
        )
        if lines:
            self._print_interaction_lines(lines)
            self._record_optional_interaction(verb, item, target)
            return True
```

- [ ] **Step 6: Merge cave static content**

In `game/interactions.py`:

```python
from .flavour_beasts import BEAST_STATIC_INTERACTIONS, BEAST_STATE_INTERACTIONS

STATIC_INTERACTIONS.update(BEAST_STATIC_INTERACTIONS)
```

- [ ] **Step 7: Run all beast and cave regression tests**

Run:

```bash
pytest -q tests/test_lick_states_and_beasts.py tests/test_cave_boot.py
```

Expected: PASS, including the original hostile deaths, beast-drink peaceful victory, and flaming-boot route.

- [ ] **Step 8: Commit Task 3**

```bash
git add game/flavour_beasts.py game/interactions.py game/game.py tests/test_lick_states_and_beasts.py
git commit -m "Deepen beast and cave interactions"
```

---

### Task 4: Cellar second-wave pack

**Files:**
- Create: `game/flavour_cellar.py`
- Modify: `game/interactions.py`
- Modify: `tests/test_interactions.py`

**Interfaces:**
- Consumes: existing static tuple-key registry and normalization.
- Produces: `CELLAR_STATIC_INTERACTIONS` with at least 10 new non-duplicating rule keys.

- [ ] **Step 1: Write failing cellar pack tests**

Add:

```python
from game.flavour_cellar import CELLAR_STATIC_INTERACTIONS


def test_cellar_second_wave_has_10_new_rules():
    assert len(CELLAR_STATIC_INTERACTIONS) >= 10


def test_cellar_impossible_drink_interaction_is_bespoke(capsys):
    game = Game()
    game.current_room = "root_cellar"
    game.player.add_item(Item("Impossible Drink", "Reality gave up."))

    game.handle_command("use impossible drink on cask")
    output = capsys.readouterr().out.lower()

    assert "impossible" in output or "cask" in output or "reality" in output
    assert game._has_inventory_item("impossible drink")
```

- [ ] **Step 2: Run the cellar tests and confirm RED**

Run:

```bash
pytest -q tests/test_interactions.py::test_cellar_second_wave_has_10_new_rules tests/test_interactions.py::test_cellar_impossible_drink_interaction_is_bespoke
```

Expected: import failure.

- [ ] **Step 3: Create 10 or more new cellar rules**

Use:

```python
CELLAR_STATIC_INTERACTIONS = {
    # At least 10 unique keys not already present in STATIC_INTERACTIONS.
}
```

Prioritize:

- Impossible Drink on cask / damp stone / cellar door
- map on cask / stairs
- sword on cask or cellar door
- beast drink on cask or wall
- treasure on damp stone
- boot on torch bracket
- key on cask

Every rule is flavour-only and must preserve the item.

- [ ] **Step 4: Merge cellar pack into `STATIC_INTERACTIONS`**

In `game/interactions.py`:

```python
from .flavour_cellar import CELLAR_STATIC_INTERACTIONS

STATIC_INTERACTIONS.update(CELLAR_STATIC_INTERACTIONS)
```

- [ ] **Step 5: Run cellar and inventory-preservation tests**

Run:

```bash
pytest -q tests/test_interactions.py::test_cellar_second_wave_has_10_new_rules tests/test_interactions.py::test_cellar_impossible_drink_interaction_is_bespoke tests/test_interactions.py::test_flavour_spam_preserves_critical_inventory_and_state
```

Expected: PASS.

- [ ] **Step 6: Commit Task 4**

```bash
git add game/flavour_cellar.py game/interactions.py tests/test_interactions.py
git commit -m "Add second-wave cellar interactions"
```

---

### Task 5: Forest and raider second-wave pack

**Files:**
- Create: `game/flavour_forest.py`
- Modify: `game/interactions.py`
- Modify: `tests/test_interactions.py`

**Interfaces:**
- Consumes: existing static tuple-key registry.
- Produces: `FOREST_STATIC_INTERACTIONS` with at least 10 new non-duplicating rule keys.

- [ ] **Step 1: Write failing forest pack tests**

Add:

```python
from game.flavour_forest import FOREST_STATIC_INTERACTIONS


def test_forest_second_wave_has_10_new_rules():
    assert len(FOREST_STATIC_INTERACTIONS) >= 10


def test_impossible_drink_on_raiders_is_bespoke_and_preserved(capsys):
    game = Game()
    game.current_room = "forest_path"
    game.player.add_item(Item("Impossible Drink", "Reality gave up."))

    game.handle_command("use impossible drink on raiders")
    output = capsys.readouterr().out.lower()

    assert "raider" in output or "drink" in output or "impossible" in output
    assert game._has_inventory_item("impossible drink")
    assert game.running is True
```

- [ ] **Step 2: Run forest tests and confirm RED**

Run:

```bash
pytest -q tests/test_interactions.py::test_forest_second_wave_has_10_new_rules tests/test_interactions.py::test_impossible_drink_on_raiders_is_bespoke_and_preserved
```

Expected: import failure.

- [ ] **Step 3: Create 10 or more forest rules**

Use:

```python
FOREST_STATIC_INTERACTIONS = {
    # At least 10 unique keys not already present in STATIC_INTERACTIONS.
}
```

Prioritize:

- Impossible Drink on raiders / tree / treasure
- map on raiders / tree
- beast drink on raiders
- treasure on spoon / fork / tree
- boot on mud / raiders
- key on tree or bush

Do not create new combat or treasure state transitions.

- [ ] **Step 4: Merge forest pack into `STATIC_INTERACTIONS`**

In `game/interactions.py`:

```python
from .flavour_forest import FOREST_STATIC_INTERACTIONS

STATIC_INTERACTIONS.update(FOREST_STATIC_INTERACTIONS)
```

- [ ] **Step 5: Run forest and normal-win regression tests**

Run:

```bash
pytest -q tests/test_interactions.py::test_forest_second_wave_has_10_new_rules tests/test_interactions.py::test_impossible_drink_on_raiders_is_bespoke_and_preserved tests/test_interactions.py::test_normal_win_route_survives_optional_interaction_spam
```

Expected: PASS.

- [ ] **Step 6: Commit Task 5**

```bash
git add game/flavour_forest.py game/interactions.py tests/test_interactions.py
git commit -m "Add second-wave forest interactions"
```

---

### Task 6: Prove the new 100-rule floor and reject duplicate static keys

**Files:**
- Modify: `game/interactions.py`
- Modify: `tests/test_interactions.py`

**Interfaces:**
- Consumes all four second-wave packs.
- Produces:
  - `SECOND_WAVE_STATIC_INTERACTIONS`
  - `SECOND_WAVE_RULE_COUNT: int`
  - `LEGACY_INTERACTION_KEYS: frozenset[tuple]`

- [ ] **Step 1: Write failing structural tests**

Add to `tests/test_interactions.py`:

```python
from game.interactions import (
    LEGACY_INTERACTION_KEYS,
    SECOND_WAVE_RULE_COUNT,
    SECOND_WAVE_STATIC_INTERACTIONS,
)


def test_second_wave_contains_at_least_100_new_rule_keys():
    assert SECOND_WAVE_RULE_COUNT >= 100


def test_second_wave_static_keys_do_not_replace_legacy_jokes():
    assert LEGACY_INTERACTION_KEYS.isdisjoint(SECOND_WAVE_STATIC_INTERACTIONS)


def test_second_wave_static_packs_do_not_duplicate_each_other():
    expected = (
        len(TAVERN_STATIC_INTERACTIONS)
        + len(BEAST_STATIC_INTERACTIONS)
        + len(CELLAR_STATIC_INTERACTIONS)
        + len(FOREST_STATIC_INTERACTIONS)
    )
    assert len(SECOND_WAVE_STATIC_INTERACTIONS) == expected
```

- [ ] **Step 2: Run structural tests and confirm RED**

Run:

```bash
pytest -q tests/test_interactions.py::test_second_wave_contains_at_least_100_new_rule_keys tests/test_interactions.py::test_second_wave_static_keys_do_not_replace_legacy_jokes tests/test_interactions.py::test_second_wave_static_packs_do_not_duplicate_each_other
```

Expected: import failures because the structural constants do not exist.

- [ ] **Step 3: Capture legacy keys before second-wave merge**

Immediately after the existing `STATIC_INTERACTIONS.update(EXTRA_INTERACTIONS)` call:

```python
LEGACY_INTERACTION_KEYS = frozenset(STATIC_INTERACTIONS)
```

- [ ] **Step 4: Build the combined second-wave registry and count**

After importing the four packs:

```python
SECOND_WAVE_STATIC_INTERACTIONS = {
    **TAVERN_STATIC_INTERACTIONS,
    **BEAST_STATIC_INTERACTIONS,
    **CELLAR_STATIC_INTERACTIONS,
    **FOREST_STATIC_INTERACTIONS,
}

SECOND_WAVE_RULE_COUNT = (
    len(TAVERN_STATIC_INTERACTIONS)
    + len(TAVERN_STATE_INTERACTIONS)
    + len(BEAST_STATIC_INTERACTIONS)
    + len(BEAST_STATE_INTERACTIONS)
    + len(CELLAR_STATIC_INTERACTIONS)
    + len(FOREST_STATIC_INTERACTIONS)
)

STATIC_INTERACTIONS.update(SECOND_WAVE_STATIC_INTERACTIONS)
```

Remove the four individual `STATIC_INTERACTIONS.update(...)` calls added in Tasks 2 through 5 so the merge happens exactly once.

- [ ] **Step 5: Run structural tests**

Run:

```bash
pytest -q tests/test_interactions.py::test_second_wave_contains_at_least_100_new_rule_keys tests/test_interactions.py::test_second_wave_static_keys_do_not_replace_legacy_jokes tests/test_interactions.py::test_second_wave_static_packs_do_not_duplicate_each_other
```

Expected: PASS. If the count is below 100, add unique content keys to the relevant domain pack instead of weakening the threshold.

- [ ] **Step 6: Run all interaction and economy tests**

Run:

```bash
pytest -q tests/test_interactions.py tests/test_economy.py tests/test_lick_states_and_beasts.py
```

Expected: PASS.

- [ ] **Step 7: Commit Task 6**

```bash
git add game/interactions.py game/flavour_tavern.py game/flavour_beasts.py game/flavour_cellar.py game/flavour_forest.py tests/test_interactions.py
git commit -m "Enforce second-wave interaction rule floor"
```

---

### Task 7: Quest-integrity regression and final verification

**Files:**
- Modify: `tests/test_interactions.py`
- Modify: `tests/test_economy.py` only if an uncovered Impossible Drink invariant belongs there

**Interfaces:**
- Consumes all finished feature behavior.
- Produces no new runtime API. Produces regression proof for quest and item integrity.

- [ ] **Step 1: Add a regression proving flavour cannot consume the Impossible Drink**

Add to `tests/test_interactions.py`:

```python
def test_impossible_drink_survives_non_drinking_flavour_spam(capsys):
    game = Game()
    game.player.add_item(Item("Impossible Drink", "Reality gave up."))

    for room, command in [
        ("tavern", "use impossible drink on bartender"),
        ("root_cellar", "use impossible drink on cask"),
        ("cave_chamber", "use impossible drink on beast"),
        ("forest_path", "use impossible drink on raiders"),
    ]:
        game.current_room = room
        if room == "cave_chamber":
            game.beasts_thirsty = True
            game.beast_pet_count = 2
        game.handle_command(command)
        capsys.readouterr()
        assert game._has_inventory_item("impossible drink")

    game.handle_command("drink impossible drink")
    capsys.readouterr()

    assert game.victory is True
    assert game.running is False
```

- [ ] **Step 2: Add a normal-treasure-route regression with second-wave interactions**

Add:

```python
def test_normal_treasure_route_survives_second_wave_interactions(capsys):
    game = Game()
    game.player.coins = 5

    for command in [
        "inspect sign",
        "pet bartender",
        "use coin on wall",
    ]:
        game.handle_command(command)
        capsys.readouterr()

    game.drink_from_bar()
    capsys.readouterr()

    game.move("north")
    capsys.readouterr()
    game.take_item("torch")
    capsys.readouterr()
    game.use_item("key")
    capsys.readouterr()
    game.move("north")
    capsys.readouterr()

    game.resolve_cave_fight(use_torch=False)
    capsys.readouterr()
    game.move("east")
    capsys.readouterr()
    game.handle_command("fight raiders")
    capsys.readouterr()
    game.take_item("hidden treasure")
    capsys.readouterr()

    assert game.victory is True
    assert game.state == "victory"
```

- [ ] **Step 3: Run the two new regression tests**

Run:

```bash
pytest -q tests/test_interactions.py::test_impossible_drink_survives_non_drinking_flavour_spam tests/test_interactions.py::test_normal_treasure_route_survives_second_wave_interactions
```

Expected: PASS.

- [ ] **Step 4: Run Python compilation**

Run:

```bash
python -m py_compile adventure_game.py game/*.py
```

Expected: exit code 0.

- [ ] **Step 5: Run the complete test suite**

Run:

```bash
pytest -q
```

Expected: all tests pass with zero failures.

- [ ] **Step 6: Run whitespace verification**

Run:

```bash
git diff --check
```

Expected: no output and exit code 0.

- [ ] **Step 7: Inspect final diff for temporary scaffolding**

Run:

```bash
git status --short
git diff --stat main...HEAD
git diff --name-only main...HEAD
```

Expected: only intended source, test, spec/plan, and content-pack files. No temporary patchers, transient workflows, generated logs, or scratch files.

- [ ] **Step 8: Commit final regression tests**

```bash
git add tests/test_interactions.py tests/test_economy.py
git commit -m "Protect second-wave quest integrity"
```

- [ ] **Step 9: Re-run full verification after the final commit**

Run:

```bash
python -m py_compile adventure_game.py game/*.py
pytest -q
git diff --check
```

Expected: compilation succeeds, all tests pass, and diff check is clean.
