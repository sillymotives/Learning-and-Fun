# Fox Handoff: Interaction and Flavour Expansion

## Mission

Take *The Secret That Wasn't* from a funny text adventure with a handful of bespoke object interactions into a world where curious players can prod, rub, lick, kick, inspect, pet, sit on, and otherwise bother nearly everything without breaking the actual treasure quest.

The design branch is:

`design/interaction-flavour-system`

The authoritative design spec is:

`text-adventure-game/docs/superpowers/specs/2026-09-17-interaction-flavour-system-design.md`

The first implementation target has been doubled to **80-120 bespoke interactions** plus reusable fallbacks.

## Important Rule

You are being asked to write jokes into a framework, not to build a second parser.

The interaction engine should be data-driven. New static flavour should mostly be added to `game/interactions.py`. Stateful behaviour should use small named handlers only when necessary.

Do not solve individual jokes by adding dozens of new branches to `Game.handle_command()`.

## Existing Energy

The game already supports absurdity such as:

- stealing the bartender's left boot while he is still wearing it
- fighting the bartender
- setting the bartender on fire
- the bartender enjoying being on fire
- using and rubbing inventory items on arbitrary targets
- rotating generic fallback responses

The expansion should preserve that tone: dry absurdity, escalating consequences, and the narrator treating ridiculous player behaviour with increasing concern.

## Core Command Families

Item-on-target:

- `use <item> on <target>`
- `rub <item> on <target>`

Standalone flavour verbs to add:

- `inspect <target>`
- `poke <target>`
- `kick <target>`
- `lick <target>`
- `pet <target>`
- `sit`
- `sit on <target>`

## Contextual Objects

Not everything needs to live in inventory. Contextual targets/items can exist by room and state:

- drink / ale / mug
- bartender / bartender face
- bar / chair / wall / floor / sign / trophies / lanterns
- cellar casks / cellar wall / iron door / torch bracket
- cave wall / darkness / glowing eyes / beast den / bones
- forest trees / bushes / grass / mud / raiders / spoons / forks

The first drink should become a contextual object after purchase so this works:

`rub drink on bartender face`

## Required Bartender Joke

Normal:

The player rubs ale on the bartender's face. He stands still, asks why, and points out that he watched the player do it.

Burning:

The ale hisses on his face. He calls it refreshing.

Boot stolen:

He explicitly acknowledges that the player stole his boot and is now moisturizing him with lager.

Burning + boot stolen:

Escalate accordingly. He should miss normal customers.

## Interaction Families To Fill Out

Aim for depth around things players will naturally experiment with rather than artificially equal counts.

### Bartender

Drink, mug, boot, key, coin, torch, sword, treasure, pet, poke, inspect, kick, lick, sit/bar interactions. Include state-aware variants where worthwhile.

### Tavern

Mug, bar, chair, wall, floor, sign, door, trophies, lanterns, drink, bartender, boot.

### Cellar

Wall, torch, torch bracket, coin, casks, iron door, stairs, damp stone, floor.

### Cave

Wall, glowing eyes, beast den, bones, sword, stone, darkness, torch, floor.

### Forest and Raiders

Trees, path, grass, treasure, raiders, spoons, forks, suspicious sword, mud, bushes.

## Joke-Only Achievements

These are cosmetic and must never affect progression:

- **Bartender Moisturized** - rub a drink on the bartender's face
- **Wall Licked** - lick a wall
- **Attempted Capitalism On Stone** - use a coin on a wall
- **Applied Science** - apply the stolen boot to several distinct surfaces
- **Training Arc** - perform 100 optional interactions

For Training Arc, flavour may invoke the sacred regimen: 100 pushups, 100 situps, and a 10 km run. No actual exercise tracking is needed.

## Quest Integrity

This is non-negotiable:

- do not consume key, torch, sword, treasure, or other quest-critical items through flavour interactions
- do not remove required exits
- do not create new mandatory progression flags
- generic fallbacks never mutate quest state
- achievements never mutate quest state
- destructive jokes such as torch-on-forest are flavour only unless separately designed
- the normal treasure route must remain completable after arbitrary optional interactions

## Testing Expectations

Test representative examples, not every joke individually.

Cover:

- parser forms and aliases
- contextual object availability
- exact bespoke interactions
- bartender state combinations
- achievement unlocks
- rotating fallbacks
- quest-critical inventory preservation
- one complete normal win route after optional interaction spam

## Creative North Star

Reward curiosity.

If a player thinks, "Surely the game will not let me rub this on that," the ideal response is that the game absolutely notices and has an opinion.

The world should feel surprisingly reactive without the code becoming surprisingly unmaintainable.
