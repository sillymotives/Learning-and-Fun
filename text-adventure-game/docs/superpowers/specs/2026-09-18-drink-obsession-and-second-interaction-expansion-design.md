# Drink Obsession and Second Interaction Expansion Design

## Goal

Extend *The Secret That Wasn't* with two related pieces of optional comedy content:

1. A revised drink-obsession arc with milestones at **5, 10, 20, 50, and 100** failed attempts to drink somewhere without a real drink.
2. At least **100 new bespoke interactions**, biased toward the bartender and cave beasts, while preserving the existing data-driven interaction architecture.

The expansion should reward players who keep trying strange commands without making the main treasure route harder to understand or complete.

## Relationship to the Existing Interaction System

This design extends the existing interaction and flavour system rather than replacing it.

The existing rules remain authoritative:

- static flavour belongs in declarative interaction registries
- state-changing behaviour belongs in small named handlers
- the parser must not become a second interaction engine
- quest-critical items and exits remain protected
- exact bespoke interactions beat generic fallbacks
- optional comedy must not become mandatory progression

The existing `game/flavour_expansion.py` remains intact. New content will be added in focused domain packs rather than growing that file indefinitely.

## Scope

This implementation includes:

- drink-obsession milestones at 5 / 10 / 20 / 50 / 100
- an inventory reward at 20: the **Impossible Drink**
- an alternate victory triggered only by drinking the Impossible Drink
- a cosmetic obsession achievement at 100
- special 50 and 100 milestone text that notices if the player still carries the unused winning drink
- at least 100 new bespoke optional interactions
- deeper bartender state combinations
- deeper hostile / thirsty / sleeping beast interactions
- additional tavern, cellar, cave, forest, and raider flavour
- representative regression tests and quest-integrity tests

This implementation does not add a new combat system, new mandatory quest flags, a generic rule language, or new mandatory areas.

## Architecture

### Interaction registry hub

`game/interactions.py` remains the normalization and lookup hub.

It continues to own:

- item aliases
- target aliases
- verb aliases
- room target sets
- static interaction lookup
- generic and room-specific fallbacks

The new flavour packs export dictionaries using the existing key shape:

```python
(verb, item_or_none, target, room_id)
```

`interactions.py` imports those dictionaries and merges them into `STATIC_INTERACTIONS`.

### New domain packs

New content will be divided by domain:

- `game/flavour_tavern.py`
- `game/flavour_beasts.py`
- `game/flavour_cellar.py`
- `game/flavour_forest.py`

The existing `game/flavour_expansion.py` stays unchanged unless a tiny compatibility edit is required.

This is a content organization boundary, not a new runtime subsystem.

### Stateful handlers

State-dependent behaviour remains in small named helpers called by `Game`.

Examples:

- bartender state specificity
- hostile versus thirsty versus sleeping beast reactions
- drink-obsession milestone handling
- awarding the Impossible Drink
- drinking the Impossible Drink
- the alternate victory transition

Static flavour should not mutate game state.

## Drink Obsession Arc

### Counter

The existing `failed_drink_attempts` counter remains the source of truth.

It increases only when the player uses the plain `drink` command somewhere that does not provide a drink.

The tavern's normal drink progression remains unchanged.

### Milestones

The milestone thresholds become:

- **5**: early concern
- **10**: confirmed habit
- **20**: reward, the Impossible Drink
- **50**: absurd dedication
- **100**: capstone milestone plus cosmetic achievement

Each milestone fires exactly once because each attempt number can only be reached once per run.

### Milestone 5

The game acknowledges that the repeated behaviour is becoming a pattern.

Representative tone:

> This is becoming a pattern.

No item or achievement is awarded.

### Milestone 10

The game acknowledges a confirmed habit.

Representative tone:

> This has officially become a habit.

No item or achievement is awarded.

### Milestone 20: the Impossible Drink

At attempt 20, reality capitulates.

The player receives one inventory item named:

`Impossible Drink`

Representative scene:

> [Drink obsession milestone] Twenty attempts. Reality has filed a complaint.
>
> There is a small pop.
>
> A sealed drink appears in your hand.
>
> You stare at it.
>
> It is cold.
> It is real.
>
> The universe has capitulated.

The reward is granted exactly once.

The Impossible Drink is not the bartender's second drink and does not trigger the tavern's lethal second-drink logic.

### Impossible Drink properties

The Impossible Drink:

- is a real inventory item
- may be inspected and used in optional flavour interactions
- is never consumed by `use`, `rub`, `inspect`, or other flavour actions
- may have bespoke interactions with the bartender, beasts, walls, raiders, and other high-value targets
- is consumed only by explicitly drinking it
- is not required for the normal treasure route

Aliases may include concise forms such as `impossible drink` and `impossible`, provided they do not interfere with normal `drink`.

### Alternate victory

The command:

`drink impossible drink`

consumes the Impossible Drink and triggers an alternate victory.

Representative ending:

> You break the seal.
>
> It tastes like every drink you tried to summon and none of them.
> Rain. Smoke. Ale. Cold stone. Something faintly impossible.
>
> The tavern, the cave, the forest, the treasure... all of it seems suddenly very far away.
>
> You were never looking for the secret.
>
> You were thirsty.
>
> And now you are not.
>
> You win.

Mechanically:

- remove the Impossible Drink from inventory
- set `victory = True`
- set `state = "victory"`
- set `running = False`

This is a real alternate ending, not flavour text that leaves the game loop active.

### Command handling

The existing plain `drink` command continues to mean “attempt to drink from the current environment.”

A small explicit path is added so `drink impossible drink` resolves the inventory item before the existing generic drink handling.

This must remain a narrow extension, not a second parser.

### Milestone 50

The 50-attempt milestone is intentionally available only to a player who has ignored the alternate ending.

If the player still carries the Impossible Drink, the milestone explicitly notices this.

Representative tone:

> Fifty attempts.
>
> You are carrying a perfectly valid ending.
>
> You have chosen instead to keep trying to drink the atmosphere.

No additional progression reward is required.

### Milestone 100

Attempt 100 is the obsession capstone.

If the Impossible Drink is still carried, the text again notices that the player rejected an available ending in favor of continued research.

The player unlocks one cosmetic achievement:

**Longitudinal Study**

The achievement is joke-only and has no progression effect.

Representative tone:

> Attempt 100.
>
> This is no longer thirst.
>
> This is a completed research programme.

## Interaction Content Expansion

### Quantity

The implementation adds **at least 100 new bespoke interactions** beyond the current interaction registries.

This minimum is tested structurally at the content-pack level rather than by asserting every joke's exact wording.

### Distribution

The target distribution is intentionally biased toward characters and stateful targets:

- approximately 30 bartender and bartender-state interactions
- approximately 25 beast interactions across hostile, thirsty, and sleeping states
- approximately 15 tavern scenery interactions
- approximately 10 cellar interactions
- approximately 10 cave / cave-entrance interactions
- approximately 10 forest / raider interactions

These are guidance targets, not rigid quotas. The total must remain at least 100.

## Bartender Expansion

Bartender content should favor combinations that recognize accumulated player behaviour.

High-value states include:

- normal
- hostile
- bootless
- defeated
- burning
- damp / extinguished
- previously extinguished
- flaming boot owned
- map owned
- cave completed
- beasts thirsty
- beast drink given
- beasts asleep
- treasure found

Examples of worthwhile combinations include:

- rub map on damp bartender
- pet burning bartender
- use beast drink on bootless bartender
- use Impossible Drink on bartender
- rub Impossible Drink on bartender face
- sit on bar while bartender is defeated
- present treasure while still holding the stolen boot
- bother the bartender after peacefully solving the beast encounter

Exact multi-state reactions should outrank generic single-state reactions.

Most bartender combinations are harmless flavour. Existing state-changing exceptions remain explicit handlers.

## Beast Expansion

The beasts have three meaningful modes.

### Hostile

Hostile beasts are dangerous and easily offended.

Some direct actions remain lethal when already designed that way. New static flavour must not accidentally make lethal actions safe unless explicitly specified.

### Thirsty

After the existing pet-twice discovery, thirsty beasts behave less like monsters and more like enormous dehydrated idiots.

Their interactions should increasingly hint at:

- dry tongues
- staring at hands or containers
- interest in drinks
- competing for attention
- confusion rather than pure aggression

The beast drink route remains the designed peaceful cave solution.

### Sleeping

After the peaceful hydration victory, sleeping beasts become aggressively wholesome.

Interactions may include:

- gentle petting
- inspecting paws, tails, breathing, or sleeping positions
- safe pokes that become cuddling reactions
- sitting nearby
- presenting harmless items without waking them
- the narrator blocking unusually cruel or absurd actions when appropriate

The sleeping state should feel different enough that revisiting the cave rewards curiosity.

## Impossible Drink Interaction Family

The Impossible Drink receives a compact bespoke family, roughly 8 to 12 of the new interactions.

Candidate targets include:

- bartender
- bartender face
- bar
- wall
- sign
- cave beasts
- sleeping beasts
- raiders
- tree
- treasure

These interactions never consume the item.

Only `drink impossible drink` consumes it and wins.

## Scenery Expansion

Scenery interactions should prefer memorable item-target combinations over exhaustive coverage.

Priority items:

- bartender's boot
- crumpled map
- torch
- sword
- hidden treasure
- beast drink
- Impossible Drink
- coin
- old key

Priority targets are the existing high-value room nouns rather than generic stone variants.

The design favors one strong response such as `rub treasure on sign` over several weak variants of interacting with indistinguishable masonry.

## Resolution and Specificity

The existing resolution principle remains:

1. normalize aliases
2. confirm item/context availability
3. stateful exact handler
4. static exact interaction
5. state-aware overlay where appropriate
6. room fallback
7. generic fallback
8. record optional-interaction statistics

Specific state combinations beat generic states.

Static content packs must not bypass stateful handlers that already own gameplay consequences.

## Quest Integrity

The following remain non-negotiable:

- key, torch, sword, treasure, map, boot, beast drink, and Impossible Drink are not consumed by flavour interactions unless explicitly designed
- the Impossible Drink is consumed only by its alternate-victory command
- optional interactions cannot block the key, cave, sword, forest, raiders, or treasure
- the normal treasure ending remains completable
- the beast drink route remains completable
- the flaming boot cave route remains completable
- generic fallbacks never mutate quest state
- joke achievements never alter progression
- no new interaction pack adds mandatory progression flags

## Error Handling

Malformed item-on-target commands keep the existing concise guidance.

For the Impossible Drink:

- attempting to drink it before owning it should not fabricate the item
- `drink impossible drink` should clearly report that the player does not have it when absent
- aliases should normalize predictably
- flavour interactions with unavailable inventory items use the normal unavailable-item behaviour

No failure path should silently award the alternate victory.

## Testing Strategy

### TDD sequence

Implementation begins with failing tests for the new behavior.

The minimum red-green coverage includes:

- thresholds at 5, 10, 20, 50, and 100
- no obsolete milestone at 25
- Impossible Drink awarded exactly once at 20
- Impossible Drink appears in inventory
- `drink impossible drink` fails safely when not owned
- `drink impossible drink` consumes the item and sets a real victory state
- 50 and 100 text notices the still-carried Impossible Drink
- Longitudinal Study unlocks at 100
- at least 100 new bespoke content entries exist
- representative interactions from every content pack
- bartender specific-state rules beat generic rules
- hostile / thirsty / sleeping beast behavior remains distinct
- Impossible Drink survives non-drinking flavour interactions
- quest-critical items remain intact after optional interaction spam
- the normal treasure route still wins after representative optional interactions

### Content tests

Do not assert every joke word-for-word.

Tests should verify:

- registry structure
- content-count floor
- representative lookup keys
- important semantic phrases only where player feedback matters
- state precedence
- non-consumption and state mutation rules

This keeps joke writing editable without making the test suite brittle.

### Full regression

After focused tests pass:

- run Python compilation
- run the complete pytest suite
- run whitespace / diff checks
- verify the feature branch contains no temporary test scaffolding before integration

## Files Expected to Change

Primary implementation files:

- `game/game.py`
- `game/interactions.py`
- `game/achievements.py`
- `game/flavour_tavern.py`
- `game/flavour_beasts.py`
- `game/flavour_cellar.py`
- `game/flavour_forest.py`
- focused tests under `tests/`

The existing `game/flavour_expansion.py` should remain intact unless a small compatibility change is unavoidable.

## Non-Goals

This change does not:

- enumerate every possible verb-item-target combination
- create a generic rules DSL
- replace the current parser
- redesign combat
- redesign the main quest
- add persistence across separate game runs
- make achievements mandatory
- turn the Impossible Drink into a general-purpose quest item

## Success Criteria

The feature is complete when:

- failed-drink milestones occur at exactly 5 / 10 / 20 / 50 / 100
- attempt 20 awards one Impossible Drink
- drinking the Impossible Drink triggers a real alternate victory
- attempts 50 and 100 acknowledge an unused winning drink when carried
- attempt 100 unlocks Longitudinal Study
- at least 100 new bespoke interactions are present
- bartender and beast states feel materially deeper
- static content lives in focused packs rather than bloating `game.py`
- all focused and regression tests pass
- the normal treasure route remains intact
