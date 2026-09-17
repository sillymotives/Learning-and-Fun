# Interaction and Flavour System Design

## Goal

Expand *The Secret That Wasn't* so non-critical experimentation is consistently rewarded with funny, state-aware responses without turning `game/game.py` into a large chain of special-case conditionals.

The main quest must remain unchanged: optional interactions may create comedy state, achievements, and flavour consequences, but they must not consume required quest items, remove mandatory exits, or introduce new victory requirements.

## Scope

This design covers:

- scalable item-on-target interactions such as `use torch on bartender` and `rub boot on wall`
- standalone flavour verbs such as `inspect`, `poke`, `kick`, `lick`, `pet`, and `sit`
- room-aware and state-aware flavour text
- contextual objects that are not permanent inventory items, such as a tavern drink or mug
- hidden joke-only achievements
- rotating fallback responses for combinations without bespoke text
- tests that protect the critical treasure route from optional comedy features

The first implementation batch should target roughly **80-120 bespoke interactions** plus reusable fallbacks. The architecture must make adding hundreds of future flavour entries mostly a content task rather than a parser rewrite.

## Architecture

### `game/interactions.py`

A new module will own interaction content and normalization metadata.

It will contain:

- verb aliases and supported flavour verbs
- item aliases such as `boot`, `left boot`, and `bartender's boot`
- target aliases such as `barkeep`, `innkeeper`, and `bartender`
- room/context target definitions
- exact interaction rules for static flavour
- room-aware fallback lines
- generic rotating fallback lines

Most rules should be declarative Python data rather than functions. A representative key may conceptually look like:

`("rub", "drink", "bartender face")`

The value is one or more flavour lines or an interaction identifier.

### Stateful interaction handlers

Interactions that change game state or depend heavily on existing state remain small methods on `Game` or focused helper functions called by `Game`.

Examples:

- setting the bartender on fire
- reacting differently if the bartender is already on fire
- bartender dialogue after his boot is stolen
- fighting the bartender while he is burning
- unlocking achievements

The interaction table should point to named stateful handlers rather than embedding state mutation inside data.

### `game/achievements.py`

A small module will define hidden joke achievements and their descriptions. `Game` will maintain an unlocked-achievement set plus lightweight counters used by achievements.

Achievements are cosmetic only. Unlocking or missing one must never affect the main quest.

Initial examples:

- **Bartender Moisturized** - rub a drink on the bartender's face
- **Wall Licked** - lick a wall
- **Applied Science** - use or rub the stolen boot on several distinct targets
- **Attempted Capitalism On Stone** - use a coin on a wall
- **Training Arc** - perform 100 optional non-critical interactions; flavour may reference the sacred regimen of 100 pushups, 100 situps, and a 10 km run, but no real-world exercise tracking is required

Achievement announcements should be brief and not interrupt command processing.

## Command Model

### Item-on-target commands

Supported forms:

- `use <item> on <target>`
- `rub <item> on <target>`

The existing plain `use <item>` behaviour remains intact for quest actions such as using the key or torch normally.

### Standalone flavour verbs

Supported forms:

- `inspect <target>`
- `poke <target>`
- `kick <target>`
- `lick <target>`
- `pet <target>`
- `sit`
- `sit on <target>`

These verbs are optional flavour actions. Unknown but syntactically valid targets receive a safe fallback response rather than an error whenever reasonable.

## Resolution Order

Each interaction follows this order:

1. Normalize verb, item, and target aliases.
2. Resolve whether the item is available from inventory, game state, or room context.
3. Check for a stateful exact interaction.
4. Check for a static exact interaction.
5. Check for a room-specific interaction or fallback.
6. Use a rotating generic fallback.
7. Record optional interaction statistics and evaluate hidden achievements.

Exact rules always beat generic rules.

## Contextual Objects

Some interactable things should exist without being permanent inventory items.

Examples:

- tavern drink / ale / mug
- bar
- chair
- wall
- cellar door
- forest trees
- cave stone
- raiders
- bartender's face

A contextual object can be available only in appropriate rooms or states.

For example, `drink` becomes usable as a contextual object after the player has bought the first drink. This enables:

`rub drink on bartender face`

without adding a permanent `drink` inventory item or changing the existing drink progression.

## Bespoke Interaction Families

The first content batch should include 80-120 interactions distributed across all major locations and quest objects. The goal is not even distribution for its own sake; high-value objects such as the bartender, boot, drink, torch, sword, wall, and suspicious scenery should receive deeper coverage because players are more likely to experiment with them.

### Bartender

Examples:

- drink on bartender face
- drink on bartender face while he is burning
- drink on bartender face while his boot is stolen
- drink on bartender face while he is burning and bootless
- stolen boot on bartender
- key on bartender
- coin on bartender
- torch on bartender
- treasure on bartender
- sword on bartender
- pet bartender
- poke bartender
- inspect bartender
- kick bartender only as flavour or a route into the existing fight system
- lick bartender only if a deliberately absurd response is appropriate
- sit on bar while bartender watches
- rub mug on bartender
- rub treasure on bartender after victory

The bartender's responses should reflect state such as boot stolen, on fire, defeated, key given, sword obtained, or combinations of those states.

A core flavour example:

When the player rubs a drink on the bartender's face, he remains motionless, asks why, and points out that he watched the player do it. If he is burning, the ale hisses and he describes it as refreshing. If his boot was also stolen, his line should acknowledge the escalating sequence of indignities.

### Tavern

Examples should cover the mug, bar, chair, wall, floor, sign, door, trophies, lanterns, drink, bartender, and stolen boot. Candidate actions include sword-on-mug, coin-on-wall, boot-on-wall, torch-on-chair, kick-bar, inspect-chair, sit-on-floor, sit-on-chair, lick-wall, pet-chair, poke-trophy, rub-drink-on-sign, and attempting commerce with structural masonry.

### Cellar

Examples should cover the cellar wall, torch bracket, torch, coin, casks, iron door, stairs, damp stone, and floor. Candidate actions include key-on-torch, boot-on-cellar-door, coin-on-cask, lick-wall, kick-iron-door, pet-torch, sit-on-cask, inspect-damp-stone, rub-boot-on-cask, and poke-door.

### Cave

Examples should cover cave wall, glowing eyes, beast den, bones, sword, stone, darkness, torch, and floor. Candidate actions include coin-on-cave-wall, boot-on-beast-scenery, sword-on-stone, lick-cave-wall, sit-in-beast-den, poke-glowing-eyes when context allows, pet-darkness, inspect-bones, rub-boot-on-sword, and kick-stone.

### Forest and Raiders

Examples should cover trees, path, grass, treasure, raiders, spoons, forks, suspicious sword, mud, and bushes. Candidate actions include torch-on-forest with narrator intervention and no wildfire state, coin-on-tree, boot-on-tree, pet-tree, kick-tree, rub-treasure-on-raiders after defeat, sword-on-suspicious-cutlery, lick-tree, sit-in-bush, poke-raider, and inspect-spoon.

## Safety and Quest Integrity Rules

Optional interactions must obey the following invariants:

- quest-critical inventory items are not consumed by flavour interactions
- `use <item> on <target>` cannot silently replace the existing critical-path `use <item>` behaviour
- optional interactions cannot permanently remove the bartender, raiders, exits, key, torch, sword, or treasure unless an already-designed quest outcome does so
- optional comedy state cannot block access to the key, cave, sword, forest, or treasure
- generic fallbacks never mutate quest state
- achievements never mutate quest state
- potentially destructive jokes, such as using a torch on the forest, resolve as flavour only unless explicitly designed otherwise
- content authors may add harmless counters, seen-flags, or cosmetic state, but must not add new progression requirements without a separate design decision

## Flavour Rotation

Repeated experimentation should not immediately repeat the same line.

The system will keep lightweight counters keyed by normalized interaction family. Exact interactions may provide several alternate lines. Fallback pools rotate deterministically, avoiding randomness in tests while still producing variety during play.

## Error Handling

Malformed commands should produce concise guidance:

- `rub boot` -> `Rub it on what?`
- `use on wall` -> `Use what on the wall?`
- unavailable item -> `You are not carrying <item>.`

Contextual items should produce specific availability messages where useful, for example attempting to rub a drink on something before buying a drink.

Unknown targets should usually be treated as opportunities for flavour rather than hard parser failures, provided doing so does not falsely imply the target exists in a quest-critical way.

## Testing Strategy

Tests will be split into focused groups.

### Parser tests

Verify:

- item-on-target parsing
- standalone flavour verbs
- alias normalization
- malformed-command guidance

### Exact interaction tests

Verify representative bespoke interactions such as:

- drink on bartender face
- burning bartender plus drink
- bootless bartender plus drink
- coin on wall
- torch on forest
- sword on mug
- boot on wall

### State-aware tests

Verify bartender reactions across combinations such as:

- normal
- boot stolen
- on fire
- defeated
- on fire plus boot stolen
- post-victory where appropriate

### Achievement tests

Verify unlock conditions, one-time announcements, and that achievements remain cosmetic.

### Quest-integrity regression tests

Run the complete existing suite plus explicit tests proving that optional interactions do not consume critical items or prevent the normal win route.

## Initial Implementation Boundaries

The first implementation will add the engine, achievements, and approximately **80-120 curated interactions**. It will not attempt to manually enumerate every possible noun combination.

Future flavour growth should mainly require adding entries to `game/interactions.py` and, only when state mutation is genuinely necessary, a small named handler.

This keeps the system expandable enough for hundreds of interactions without allowing the command parser or `Game` class to become an unmaintainable wall of special cases.
