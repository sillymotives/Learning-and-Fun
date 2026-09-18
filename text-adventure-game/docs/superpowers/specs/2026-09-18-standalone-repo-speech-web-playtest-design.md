# Standalone Repository, Contextual Speech, and Web Playtest Design

## Status

Approved in conversation on 2026-09-18. This document records the design before implementation.

## Goal

Graduate *The Secret That Wasn't* from the `text-adventure-game/` subproject in `sillymotives/Learning-and-Fun` into its own history-preserving repository at `sillymotives/The-Secret-That-Wasn-t`, deepen the safe `speak` command for the bartender, raiders, and cave beasts, and add a password-gated browser playtest interface that runs the same Python game engine as the CLI.

The result should make the game easier to maintain, easier to share with playtesters, and harder for the CLI and browser versions to drift apart.

## Project Split

This work is deliberately separated into three linked implementation stages:

1. **History-preserving repository migration**
2. **Contextual speech expansion**
3. **Browser playtest interface**

They share one design because later stages depend on the standalone repository and on the canonical game engine, but each stage must remain independently testable.

## Non-Goals

This project does not:

- rewrite the game in JavaScript
- create a second browser-specific game engine
- remove or deprecate the CLI
- add a database
- add permanent player accounts
- add public registration
- build production-grade identity/authentication
- persist games across server restarts
- redesign the core treasure quest
- make speaking dangerous or progression-critical
- move unrelated `Learning-and-Fun` projects into the new repository

---

# 1. History-Preserving Standalone Repository

## Source and Destination

Source:

`sillymotives/Learning-and-Fun`

Source subtree:

`text-adventure-game/`

Destination:

`sillymotives/The-Secret-That-Wasn-t`

The destination repository is currently private and empty.

## Preservation Requirement

The migration must preserve the Git history of the game, not merely copy the latest files.

The new repository should contain the commits that affected `text-adventure-game/`, preserving their author identity, author/commit dates, and commit messages wherever Git history filtering permits.

Paths are rewritten so:

`text-adventure-game/game/game.py`

becomes:

`game/game.py`

and similarly for all other files under the game subtree.

Commits that never touched `text-adventure-game/` are intentionally absent from the standalone history.

## Migration Method

The canonical history transformation is equivalent to:

```bash
git filter-repo \
  --path text-adventure-game/ \
  --path-rename text-adventure-game/:
```

The migration must operate from a full clone of `Learning-and-Fun`, not from a shallow snapshot.

Because the current execution environment may not permit direct Git network transport, the implementation may use a temporary GitHub Actions bootstrap workflow in the empty destination repository:

1. bootstrap the empty destination with a temporary migration workflow
2. clone the public `Learning-and-Fun` repository inside GitHub Actions
3. install/run `git-filter-repo`
4. filter to `text-adventure-game/` and rewrite that directory to repository root
5. force-push the filtered `main` history into the destination repository using that destination repository's scoped `GITHUB_TOKEN`
6. allow the bootstrap commit/workflow to disappear when the filtered history replaces it
7. verify the destination history and tree before adding new feature work

The temporary bootstrap workflow is migration machinery only and must not remain in the final repository unless independently useful.

## Migration Verification

The migration is accepted only when all of the following are true:

- destination `main` contains the current game tree at repository root
- destination has non-trivial historical depth, not one import commit
- known historical game commit messages are present
- game-relevant author/date metadata is preserved
- no unrelated top-level `Learning-and-Fun` projects appear
- `README.md`, `game/`, `data/`, `tests/`, `docs/`, `adventure_game.py`, and dependency files are present where applicable
- the existing full game test suite passes in the destination repository
- source `Learning-and-Fun` remains intact

After migration verification, all new speech and web implementation work happens only in `The-Secret-That-Wasn-t`.

---

# 2. Canonical Game Engine and Front Ends

## One Game, Two Front Ends

The Python engine remains canonical.

The project exposes two front ends:

1. the existing CLI through `adventure_game.py`
2. the new browser interface through Flask

Both invoke the same `Game` implementation and state model.

No game rules, room logic, inventory rules, achievement rules, dialogue state, or victory conditions may be duplicated in browser JavaScript.

## CLI Compatibility

The existing terminal game remains a first-class interface.

All current CLI commands and tests continue to work.

The web project may add adapter modules around `Game`, but it should avoid invasive engine rewrites solely for Flask.

---

# 3. Contextual Speech System

## User-Facing Commands

The command parser supports:

- `speak`
- `talk`
- `chat`
- `speak bartender`
- `speak raiders`
- `speak beast`
- `speak beasts`

Existing aliases such as `barkeep`, `innkeeper`, `raider`, `creature`, `creatures`, `monster`, and `monsters` may normalize to those canonical speech targets.

## Bare Speak Resolution

Bare `speak`, `talk`, or `chat` chooses the obvious local character:

- tavern → bartender
- cave chamber with live or sleeping beasts → beasts
- forest path with raiders present or defeated → raiders

If no supported conversational target is present, the game reports that there is nobody obvious to speak to.

Bare speech does not silently address a character in another room.

## Explicit Target Resolution

Explicit speech only addresses the named target.

Examples:

- `speak bartender` outside the tavern reports that the bartender is not there.
- `speak raiders` outside the forest reports that the raiders are not there.
- `speak beasts` outside the cave reports that the beasts are not there.

Unknown targets receive concise guidance rather than being routed to the bartender.

## Safety Rule

Speaking is mechanically safe.

Speech may:

- reveal hints
- acknowledge current state
- rotate comedy lines
- reinforce personality
- hint at the beast hydration route
- react to victory/progression states

Speech may not:

- kill the player
- consume items
- remove exits
- award or remove mandatory quest items
- complete combat
- substitute for the beast drink
- unlock the treasure route directly

## Bartender

Existing `speak_to_bartender()` remains authoritative for bartender conversation.

The new target-aware command routing calls that existing behavior rather than creating a duplicate bartender dialogue system.

## Raiders

Raider speech is state-aware.

At minimum it distinguishes:

- active raiders before defeat
- defeated/surrendered raiders
- treasure found, if the player can still address them after victory-state setup

Dialogue should rotate across repeated conversations.

Tone: overconfident, bureaucratically incompetent banditry, with the raider captain trying to claim credit and the second raider undermining him.

Speaking to undefeated raiders remains safe even when fighting them would be dangerous.

## Beasts

Beast speech is nonverbal but treated as conversation.

At minimum it distinguishes:

- hostile live beasts
- petted but not yet thirsty beasts
- thirsty beasts
- sleeping beasts after peaceful resolution
- absent/gone beasts after a non-sleeping cave resolution

Repeated conversations rotate lines.

Thirsty-beast speech can make hydration clues clearer, but it does not itself set `beasts_thirsty`; the established petting route remains the state transition.

Sleeping-beast speech should be aggressively wholesome.

## Dialogue Data

New raider and beast speech pools live in a focused module such as:

`game/speech.py`

The module owns dialogue data and simple state-key selection.

`Game` owns actual state and command routing.

This avoids growing another large block of prose inside `game.py`.

---

# 4. Browser Playtest Architecture

## Framework

Use Flask as a thin Python web layer.

Use server-rendered HTML plus small vanilla JavaScript for command submission and transcript updates.

Do not add React, Vue, a Node build pipeline, or another front-end framework.

## Proposed Repository Layout

```text
The-Secret-That-Wasn-t/
├── adventure_game.py
├── game/
├── data/
├── tests/
├── docs/
├── web/
│   ├── __init__.py
│   ├── app.py
│   ├── game_bridge.py
│   ├── templates/
│   │   ├── login.html
│   │   └── game.html
│   └── static/
│       ├── game.js
│       └── style.css
├── requirements.txt
├── .env.example
├── Dockerfile
├── README.md
└── deployment metadata as needed
```

The exact deployment metadata may include a `Procfile` or equivalent generic WSGI command if useful.

## Game Bridge

The browser must not call CLI stdin/stdout directly.

A focused `web/game_bridge.py` adapter owns browser-session game instances.

Each browser game session contains:

- one `Game` instance
- its transcript
- minimal session metadata such as last access time if needed

The bridge exposes operations conceptually equivalent to:

- `new_game() -> session state`
- `run_command(command: str) -> output lines + game status`
- `reset_game() -> fresh session state`
- `get_transcript() -> output lines`

## Capturing Existing Printed Output

The existing game prints extensively.

For this playtest phase, avoid a project-wide print-to-emitter rewrite unless tests prove it necessary.

The web bridge may capture the engine's existing stdout with `contextlib.redirect_stdout()`, protected by a process-wide lock so concurrent requests cannot mix output.

This deliberately trades command-level parallelism for a small, low-risk adapter. Text-adventure commands are extremely short, so serializing command execution is acceptable for the intended private playtest audience.

A future output-emitter refactor may replace this bridge if the game later needs high concurrency or richer structured events.

## Web Session Isolation

Each authenticated browser receives a random session identifier stored in Flask's signed session cookie.

Server memory maps that identifier to its own game session.

One playtester cannot alter another playtester's:

- inventory
- bartender state
- beast state
- transcript
- victory state
- achievements

Game sessions are intentionally ephemeral.

They may disappear when the server restarts.

No database is introduced in this phase.

## Single-Process Hosting Constraint

Because game state is in process memory, the initial deployment must use one application worker.

Multiple threads are acceptable because command capture is lock-protected.

The deployment command must therefore explicitly use one worker, for example a single Gunicorn worker.

If persistent or multi-worker sessions become necessary later, session storage becomes a separate design project.

---

# 5. Web Routes and Data Flow

## Authentication Routes

### `GET /login`

Shows the playtest password form.

### `POST /login`

Compares the submitted password to `PLAYTEST_PASSWORD`.

On success:

- marks the Flask session authenticated
- redirects to the game

On failure:

- does not reveal configuration details
- returns the login page with a concise error

### `POST /logout`

Clears authentication and game-session association.

## Game Routes

### `GET /`

Requires authentication.

Returns the game interface and current transcript for the browser's game session.

If the browser has no game session yet, creates one.

### `POST /api/command`

Requires authentication.

Accepts JSON:

```json
{"command": "inspect bartender"}
```

Returns JSON conceptually shaped as:

```json
{
  "lines": ["..."],
  "transcript": ["..."],
  "running": true,
  "state": "in progress",
  "victory": false
}
```

Blank commands are rejected without changing game state.

### `POST /api/reset`

Requires authentication.

Replaces only the current browser's game with a fresh `Game` instance and returns the fresh opening transcript.

## Request Flow

```text
browser command
    ↓
authenticated Flask route
    ↓
browser session id
    ↓
GameSession bridge
    ↓
canonical Game.handle_command()
    ↓
captured output lines
    ↓
session transcript
    ↓
JSON response
    ↓
browser transcript
```

---

# 6. Password Gate and Configuration

## Environment Variables

The app requires:

- `PLAYTEST_PASSWORD`
- `FLASK_SECRET_KEY`

The application fails closed if either required value is missing.

The shared playtest password itself is never committed to Git.

The user's proposed initial deployment password, `kaiithegreat`, may be configured in the hosting environment, but the repository contains only a placeholder in `.env.example`.

## Password Comparison

Use a constant-time comparison such as `hmac.compare_digest()`.

This is a private playtest gate, not a substitute for account-level authentication.

## Cookies

Authentication state is stored in Flask's signed session cookie.

Cookies should be:

- HttpOnly
- SameSite=Lax
- Secure when deployed behind HTTPS

Local development may disable the Secure cookie requirement so `http://localhost` remains usable.

## Secrets

No:

- passwords
- Flask secret keys
- hosting credentials
- GitHub tokens

may appear in committed source, tests, examples, or deployment metadata.

---

# 7. Browser Experience

## Visual Direction

The web interface is a dark, atmospheric terminal-like play surface rather than a generic admin panel.

Primary elements:

- game title
- compact status/header area
- scrolling transcript
- command input
- submit button
- convenience controls for Help, Look, Inventory, and Reset
- clear victory/game-over state without disabling transcript review

It should feel like the same strange tavern game, not a web form wrapped around Python.

## Mobile Support

The page is mobile-first enough for comfortable phone playtesting.

Requirements:

- no horizontal scrolling at normal phone widths
- command input remains reachable above the mobile keyboard
- transcript text remains readable
- buttons wrap sensibly
- Enter submits on desktop
- tap submits on mobile
- transcript auto-scrolls after a command but remains manually scrollable

## Client JavaScript

Vanilla JavaScript handles:

- command POSTs
- response rendering
- convenience buttons
- reset confirmation/action
- disabled/busy state while a command is in flight
- graceful network/server errors

JavaScript does not implement game rules.

---

# 8. Local and Hosted Deployment

## Local

The site can be launched locally with documented environment variables and a simple command.

Development mode may use Flask's development server.

## Hosted

The production entry point uses a WSGI server such as Gunicorn.

The repository includes:

- all Python dependencies
- a production launch command
- a `Dockerfile` for portable self-hosting/cloud use
- environment-variable documentation
- one-worker configuration because sessions are in memory

The design must remain provider-neutral enough to run on common container/web-service hosts.

Provider-specific one-click metadata may be added later if it materially helps deployment, but the application must not depend on one vendor.

## Public URL

Building and verifying the deployable application is part of this project.

Actually publishing a public URL requires either:

- a connected hosting provider available to the assistant, or
- the user deploying the prepared repository through their chosen host

The repository should make that final deployment step small and mechanical.

---

# 9. Error Handling

## Web

The API returns useful errors without exposing tracebacks or secrets.

Expected cases include:

- unauthenticated request → authentication response
- blank command → 400-style client error with message
- malformed JSON → client error
- unknown game command → normal game output, not HTTP failure
- missing required server environment variable → startup failure
- internal game exception → logged server-side and generic failure response to browser

A single failed request must not silently replace another browser's game.

## Game

Contextual speech follows existing command error style.

Absent/unknown speakers return concise in-world guidance and do not mutate state.

---

# 10. Testing Strategy

## Migration Tests and Checks

Verify:

- source repository remains unchanged except deliberate design/plan documentation
- destination contains filtered history
- destination tree matches source `text-adventure-game/` content at migration point
- destination does not contain unrelated source projects
- existing tests pass after migration

## Speech Tests

Add focused tests covering:

- bare `speak` in tavern routes to bartender
- bare `speak` in cave routes to beasts
- bare `speak` in forest routes to raiders
- explicit target aliases
- absent-target responses
- raider pre-defeat rotation
- raider defeated rotation
- hostile beast speech is safe
- petted/thirsty beast speech differs
- thirsty speech does not itself set thirst
- sleeping beast speech is distinct and safe
- repeated lines rotate
- existing bartender dialogue tests remain green
- normal treasure and alternate victory routes remain intact

## Web Authentication Tests

Using Flask's test client:

- missing config fails startup
- unauthenticated `GET /` redirects/rejects
- wrong password is rejected
- correct password establishes authenticated session
- logout clears authentication
- protected API endpoints reject unauthenticated requests
- password value never appears in rendered HTML or responses

## Web Game Tests

Cover:

- first authenticated visit creates a game
- command round-trip returns captured game output
- `help`, `look`, and `inventory` work through HTTP
- unknown game command returns normal game text
- blank command is rejected without state change
- reset creates a fresh game
- transcript survives page refresh within the same server process
- victory/game-over status is returned correctly
- Impossible Drink alternate ending works through the browser

## Session Isolation Tests

Create two Flask test clients.

Prove:

- each receives a different game session
- inventory/state changes in client A do not appear in client B
- reset for A does not reset B
- transcripts remain separate

## Full Regression

Before integration:

```bash
python -m py_compile adventure_game.py game/*.py web/*.py
pytest -q
git diff --check
```

Run the existing CLI smoke path as well as Flask tests.

---

# 11. Documentation

The standalone `README.md` becomes game-specific and documents:

- what the game is
- CLI setup and play
- web setup and play
- Linux/Windows/phone-friendly browser access
- environment variables
- local Flask launch
- production/Gunicorn launch
- Docker build/run
- test commands
- password-gate limitations
- ephemeral session limitation
- contribution/development notes

The old `Learning-and-Fun` repository may later replace its embedded game copy with a short archival pointer to the standalone repository, but deleting the old subtree is not part of this migration project.

Keeping the old subtree initially gives us a safe historical/reference copy and avoids making migration destructive.

---

# 12. Implementation Order

Implementation follows this order:

1. finalize and commit this design and its implementation plan in `Learning-and-Fun/text-adventure-game/docs/`
2. execute the history-preserving extraction into `The-Secret-That-Wasn-t`
3. verify the destination history and run the existing suite there
4. create a feature branch in the standalone repository
5. implement contextual speech with TDD
6. implement the Flask bridge and password gate with TDD
7. build the browser UI
8. add portable deployment configuration
9. update standalone documentation
10. run complete CLI + web verification
11. integrate the standalone feature branch after user choice

After step 2, no new game feature code is added to the embedded `Learning-and-Fun/text-adventure-game/` copy during this project.

---

# Success Criteria

The project is complete when:

- `sillymotives/The-Secret-That-Wasn-t` contains history-preserved game commits rooted at the game directory
- unrelated `Learning-and-Fun` projects are absent from the standalone repo
- the current CLI works from the standalone repo
- `speak` supports contextual bartender, raider, and beast conversations
- speaking is safe and state-aware
- the same `Game` engine powers CLI and browser
- the browser requires the environment-configured playtest password
- no password or secret is committed
- separate browser sessions have isolated games
- reset affects only the current browser session
- the web interface works comfortably on desktop and phone-sized screens
- local and containerized/hosted launch paths are documented
- all existing and new tests pass
- the normal treasure ending and Impossible Drink ending both remain playable through the browser
