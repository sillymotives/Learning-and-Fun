# Standalone Repo, Contextual Speech, and Web Playtest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Preserve the game's Git history in sillymotives/The-Secret-That-Wasn-t, add safe contextual speech for bartender/raiders/beasts, and ship a password-gated Flask playtest site powered by the same Python Game engine as the CLI.

**Architecture:** First migrate the text-adventure-game subtree into the empty standalone repository with git-filter-repo and verify the filtered history before any new feature work. Then add a focused speech data/router layer, followed by a Flask application factory and an in-memory per-browser GameSessionStore that serializes stdout capture through one process-wide lock. The CLI remains canonical and unchanged in behavior; the browser is a thin adapter around Game.handle_command().

**Tech Stack:** Python 3.12, pytest, Flask 3.x, Gunicorn 23.x, vanilla HTML/CSS/JavaScript, GitHub Actions, git-filter-repo, Docker.

**Spec:** docs/superpowers/specs/2026-09-18-standalone-repo-speech-web-playtest-design.md

## Global Constraints

- Destination repository is sillymotives/The-Secret-That-Wasn-t.
- Preserve game Git history rather than flattening to a single import commit.
- Rewrite text-adventure-game/ to the destination repository root.
- Source Learning-and-Fun remains intact.
- After migration, all new game feature work happens only in The-Secret-That-Wasn-t.
- The existing CLI remains a first-class supported interface.
- Browser and CLI use the same Game implementation.
- Speaking is mechanically safe: no deaths, item consumption, combat completion, mandatory progression, or victory transitions.
- Existing speak_to_bartender() remains authoritative for bartender dialogue.
- Raider and beast speech rotates and is state-aware.
- PLAYTEST_PASSWORD and FLASK_SECRET_KEY are required at application startup outside explicitly injected test configuration.
- Secrets and the actual playtest password are never committed.
- Browser game sessions are isolated from one another.
- Browser game state is intentionally in-memory and ephemeral.
- Initial hosted deployment uses exactly one application worker.
- Every print-producing Game operation used by the browser runs under the same process-wide re-entrant output lock.
- No JavaScript game-rule implementation and no front-end framework.
- No database or permanent user accounts in this phase.
- Production feature changes follow TDD: failing test first, observed RED, minimal GREEN, then refactor.

---

## File Structure After Migration

The standalone repository should converge on:

~~~text
The-Secret-That-Wasn-t/
├── adventure_game.py
├── game/
│   ├── __init__.py
│   ├── __main__.py
│   ├── achievements.py
│   ├── bartender_dialogue.py
│   ├── flavour_beasts.py
│   ├── flavour_cellar.py
│   ├── flavour_expansion.py
│   ├── flavour_forest.py
│   ├── flavour_tavern.py
│   ├── game.py
│   ├── interactions.py
│   ├── items.py
│   ├── player.py
│   ├── speech.py
│   └── world.py
├── data/
├── tests/
│   ├── test_speech.py
│   ├── test_web_app.py
│   └── existing test files...
├── web/
│   ├── __init__.py
│   ├── app.py
│   ├── game_bridge.py
│   ├── templates/
│   │   ├── game.html
│   │   └── login.html
│   └── static/
│       ├── game.js
│       └── style.css
├── docs/
├── .env.example
├── Dockerfile
├── Procfile
├── requirements.txt
└── README.md
~~~

---

### Task 1: Preserve the game history in the standalone repository

**Repositories:**
- Source: sillymotives/Learning-and-Fun
- Destination: sillymotives/The-Secret-That-Wasn-t

**Files:**
- Temporary create in destination: .github/workflows/migrate-game-history.yml
- No persistent production file is introduced by this task beyond the filtered source tree.

**Interfaces:**
- Consumes: source branch design/standalone-repo-speech-web-playtest, which contains the approved design and this plan on top of the verified game main history.
- Produces: destination main whose root is the filtered former text-adventure-game/ subtree, with historical commits preserved.

- [ ] **Step 1: Confirm the destination is still safe to replace**

Use the GitHub repository metadata and tree APIs to verify:

- repository_full_name is sillymotives/The-Secret-That-Wasn-t
- default branch is main
- repository size is 0 or the only content is migration bootstrap machinery created by this task
- there is no user-authored game content to preserve

If unexpected content exists, STOP before creating or force-pushing anything.

- [ ] **Step 2: Record the source branch head**

Fetch design/standalone-repo-speech-web-playtest and record its exact SHA as SOURCE_SHA.

The migration workflow must checkout this named branch, because it contains the approved spec and implementation plan while retaining all game history reachable from main.

- [ ] **Step 3: Create the temporary migration workflow in the destination**

Create .github/workflows/migrate-game-history.yml as the destination's bootstrap commit. If the empty repository has no resolvable main ref yet, create the file without an explicit branch argument so GitHub creates the default main branch; otherwise target main normally.

Use exactly this workflow shape:

~~~yaml
name: Migrate game history

on:
  workflow_dispatch:
  push:
    branches:
      - main
    paths:
      - ".github/workflows/migrate-game-history.yml"

permissions:
  contents: write

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - name: Install tools
        run: |
          python -m pip install --upgrade pip
          python -m pip install git-filter-repo pytest

      - name: Clone source history
        env:
          SOURCE_REPO: https://github.com/sillymotives/Learning-and-Fun.git
        run: |
          git clone --branch design/standalone-repo-speech-web-playtest --single-branch "$SOURCE_REPO" source

      - name: Filter to game subtree
        working-directory: source
        run: |
          git filter-repo --force \
            --path text-adventure-game/ \
            --path-rename text-adventure-game/:

      - name: Verify filtered tree before push
        working-directory: source
        run: |
          test -f adventure_game.py
          test -f README.md
          test -d game
          test -d tests
          test -d data
          test -d docs
          test ! -d text-adventure-game
          test "$(git rev-list --count HEAD)" -gt 10
          git log --format='%s' | grep -F "Document Linux Windows and phone setup"
          python -m py_compile adventure_game.py game/*.py
          pytest -q
          git diff --check

      - name: Replace empty destination main with filtered history
        working-directory: source
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          git remote add destination "https://x-access-token:${GH_TOKEN}@github.com/sillymotives/The-Secret-That-Wasn-t.git"
          git push destination HEAD:refs/heads/main --force
~~~

The workflow intentionally disappears when the force-pushed filtered source history replaces the bootstrap commit.

- [ ] **Step 4: Allow the workflow to execute and inspect the destination head**

Wait by condition, not an arbitrary sleep: repeatedly fetch destination main until its head is no longer the bootstrap commit.

Expected destination root includes:

- adventure_game.py
- README.md
- game/
- tests/
- data/
- docs/
- requirements.txt

Expected root does not include text-adventure-game/.

- [ ] **Step 5: Verify preserved history**

Using GitHub commit/history APIs, confirm:

- more than 10 commits are reachable from destination main
- the commit message Document Linux Windows and phone setup is present
- the recent drink-obsession/interaction work is present in history
- commit author/date metadata on at least two known historical commits matches the source commit metadata
- no unrelated source project directories are at destination root

- [ ] **Step 6: Verify source remains intact**

Fetch sillymotives/Learning-and-Fun main and confirm:

- text-adventure-game/ still exists
- main has not been force-moved or rewritten as part of migration
- unrelated source projects remain present

- [ ] **Step 7: Verify baseline tests in the standalone repository**

If the migration workflow log already proves the exact filtered commit passed the full suite, record that output.

Also verify on destination main:

~~~bash
python -m py_compile adventure_game.py game/*.py
pytest -q
git diff --check
~~~

Expected: current baseline remains green.

- [ ] **Step 8: Create the implementation branch in the standalone repository**

Create:

~~~text
feature/contextual-speech-and-web-playtest
~~~

from destination main.

All following tasks execute only on that branch in sillymotives/The-Secret-That-Wasn-t.

---

### Task 2: Add contextual, rotating, mechanically safe speech

**Files:**
- Create: game/speech.py
- Modify: game/game.py
- Create: tests/test_speech.py
- Existing regression: tests/test_bartender_dialogue.py
- Existing regression: tests/test_lick_states_and_beasts.py

**Interfaces:**
- Produces: normalize_speaker(name: str) -> str
- Produces: choose_rotating_line(lines: tuple[str, ...], counts: dict, key: str) -> str
- Produces: Game.speak_to(target_name: str | None = None) -> None
- Produces: Game.speech_counts: dict[str, int]
- Consumes: existing Game.speak_to_bartender() unchanged for bartender speech.

- [ ] **Step 1: Write failing routing and alias tests**

Create tests/test_speech.py:

~~~python
from game.game import Game
from game.speech import normalize_speaker


def test_speaker_aliases_normalize():
    assert normalize_speaker("barkeep") == "bartender"
    assert normalize_speaker("the innkeeper") == "bartender"
    assert normalize_speaker("raider") == "raiders"
    assert normalize_speaker("bandits") == "raiders"
    assert normalize_speaker("beast") == "beasts"
    assert normalize_speaker("monsters") == "beasts"


def test_bare_speak_routes_to_obvious_local_character(capsys):
    game = Game()

    game.current_room = "tavern"
    game.handle_command("speak")
    tavern = capsys.readouterr().out.lower()
    assert "bartender:" in tavern

    game.current_room = "cave_chamber"
    game.handle_command("speak")
    cave = capsys.readouterr().out.lower()
    assert "beast" in cave

    game.current_room = "forest_path"
    game.raiders_seen = True
    game.handle_command("speak")
    forest = capsys.readouterr().out.lower()
    assert "raider" in forest


def test_explicit_speaker_must_be_present(capsys):
    game = Game()

    game.current_room = "forest_path"
    game.handle_command("speak bartender")
    assert "not here" in capsys.readouterr().out.lower()

    game.current_room = "tavern"
    game.handle_command("speak beasts")
    assert "not here" in capsys.readouterr().out.lower()

    game.current_room = "forest_path"
    game.raiders_seen = False
    game.raiders_defeated = False
    game.handle_command("speak raiders")
    assert "not here" in capsys.readouterr().out.lower()


def test_unknown_speaker_gets_guidance(capsys):
    game = Game()
    game.handle_command("speak chandelier")
    output = capsys.readouterr().out.lower()
    assert "speak to" in output
    assert "bartender" in output
    assert "raiders" in output
    assert "beasts" in output
~~~

- [ ] **Step 2: Run routing tests and confirm RED**

Run:

~~~bash
pytest -q tests/test_speech.py
~~~

Expected: import failure for game.speech or assertions showing current speak still always calls the bartender.

- [ ] **Step 3: Implement speaker aliases, selector, and dialogue pools**

Create game/speech.py:

~~~python
SPEAKER_ALIASES = {
    "bartender": "bartender",
    "the bartender": "bartender",
    "barkeep": "bartender",
    "the barkeep": "bartender",
    "innkeeper": "bartender",
    "the innkeeper": "bartender",
    "raider": "raiders",
    "raiders": "raiders",
    "the raiders": "raiders",
    "bandit": "raiders",
    "bandits": "raiders",
    "beast": "beasts",
    "beasts": "beasts",
    "the beast": "beasts",
    "the beasts": "beasts",
    "creature": "beasts",
    "creatures": "beasts",
    "monster": "beasts",
    "monsters": "beasts",
}


def normalize_speaker(name):
    cleaned = " ".join(name.lower().strip().split())
    return SPEAKER_ALIASES.get(cleaned, cleaned)


def choose_rotating_line(lines, counts, key):
    index = counts.get(key, 0)
    counts[key] = index + 1
    return lines[index % len(lines)]


RAIDER_SPEECH = {
    "active": (
        'Raider captain: "We discovered this path first."',
        'Second raider: "It is a public path."',
        'Raider captain: "Quiet. Discovery is mostly confidence."',
    ),
    "defeated": (
        'Raider captain: "We are conducting a tactical surrender."',
        'Second raider: "He means we lost."',
        'Raider captain: "The spoons were experimental."',
    ),
    "treasure_found": (
        'Raider captain: "For the record, we still found it first."',
        'Second raider: "For the record, no."',
        'Raider captain: "History is written by whoever keeps talking."',
    ),
}


BEAST_SPEECH = {
    "hostile": (
        "The beasts answer with a low chittering growl.",
        "One beast shows you several opinions, all of them teeth.",
        "The second beast snorts. Diplomacy remains provisional.",
    ),
    "petted": (
        "The nearer beast makes a confused rumbling noise and leans closer.",
        "The second beast watches your hands as if conversation might involve snacks.",
        "Both beasts chitter at once. You choose to interpret this as progress.",
    ),
    "thirsty": (
        "One beast opens its mouth, displays a very dry tongue, and stares at your hands.",
        "The other makes a plaintive rumble and noses around for something drink-shaped.",
        "Both beasts stare at you with the unmistakable intensity of customers awaiting water.",
    ),
    "sleeping": (
        "One sleeping beast makes a tiny dream-chuff.",
        "The other answers without waking and tucks its nose under a paw.",
        "The conversation is mostly breathing and is somehow the most successful one today.",
    ),
    "gone": (
        "The cave answers for the absent beasts with one distant drip.",
        "Whatever the beasts would say, they are no longer here to say it.",
        "You address the empty den. The empty den maintains professional silence.",
    ),
}
~~~

- [ ] **Step 4: Add failing state and safety tests**

Append to tests/test_speech.py:

~~~python
def test_raider_dialogue_rotates_and_changes_after_defeat(capsys):
    game = Game()
    game.current_room = "forest_path"
    game.raiders_seen = True

    game.handle_command("speak raiders")
    first = capsys.readouterr().out
    game.handle_command("speak raiders")
    second = capsys.readouterr().out

    assert first != second
    assert game.running is True

    game.raiders_defeated = True
    game.handle_command("speak raiders")
    defeated = capsys.readouterr().out.lower()
    assert "surrender" in defeated or "lost" in defeated


def test_beast_speech_states_are_distinct_and_safe(capsys):
    game = Game()
    game.current_room = "cave_chamber"

    before = (game.running, game.beasts_thirsty, game.cave_battle_done)
    game.handle_command("speak beasts")
    hostile = capsys.readouterr().out.lower()
    assert "teeth" in hostile or "growl" in hostile
    assert (game.running, game.beasts_thirsty, game.cave_battle_done) == before

    game.beast_pet_count = 1
    game.handle_command("speak beasts")
    petted = capsys.readouterr().out.lower()
    assert "hands" in petted or "progress" in petted
    assert game.beasts_thirsty is False

    game.beasts_thirsty = True
    game.beast_pet_count = 2
    game.handle_command("speak beasts")
    thirsty = capsys.readouterr().out.lower()
    assert "dry" in thirsty or "water" in thirsty

    game.beasts_thirsty = False
    game.beasts_asleep = True
    game.cave_battle_done = True
    game.handle_command("speak beasts")
    sleeping = capsys.readouterr().out.lower()
    assert "sleep" in sleeping or "dream" in sleeping or "breathing" in sleeping
    assert game.running is True


def test_absent_beasts_after_non_sleeping_resolution_have_gone_dialogue(capsys):
    game = Game()
    game.current_room = "cave_chamber"
    game.cave_battle_done = True
    game.beasts_asleep = False

    game.handle_command("speak beasts")
    output = capsys.readouterr().out.lower()

    assert "absent" in output or "no longer here" in output or "empty den" in output
~~~

- [ ] **Step 5: Run state tests and confirm RED**

Run:

~~~bash
pytest -q tests/test_speech.py
~~~

Expected: failures because Game has no target-aware speech router yet.

- [ ] **Step 6: Implement Game speech routing**

In Game.__init__ add:

~~~python
        self.speech_counts = {}
~~~

Import from game.speech:

~~~python
from .speech import (
    BEAST_SPEECH,
    RAIDER_SPEECH,
    choose_rotating_line,
    normalize_speaker,
)
~~~

Add methods:

~~~python
    def _obvious_speaker(self):
        if self.current_room == "tavern":
            return "bartender"
        if self.current_room == "cave_chamber":
            return "beasts"
        if self.current_room == "forest_path" and (self.raiders_seen or self.raiders_defeated):
            return "raiders"
        return None

    def _raider_speech_state(self):
        if self.treasure_found:
            return "treasure_found"
        if self.raiders_defeated:
            return "defeated"
        return "active"

    def _beast_speech_state(self):
        if self.beasts_asleep:
            return "sleeping"
        if self.cave_battle_done:
            return "gone"
        if self.beasts_thirsty:
            return "thirsty"
        if self.beast_pet_count > 0:
            return "petted"
        return "hostile"

    def speak_to(self, target_name=None):
        speaker = normalize_speaker(target_name) if target_name else self._obvious_speaker()

        if speaker is None:
            print("There is nobody obvious here to speak to.")
            return

        if speaker == "bartender":
            if self.current_room != "tavern":
                print("The bartender is not here.")
                return
            self.speak_to_bartender()
            return

        if speaker == "raiders":
            raiders_present = self.raiders_seen or self.raiders_defeated or self.treasure_found
            if self.current_room != "forest_path" or not raiders_present:
                print("The raiders are not here.")
                return
            state = self._raider_speech_state()
            line = choose_rotating_line(
                RAIDER_SPEECH[state],
                self.speech_counts,
                f"raiders:{state}",
            )
            print(line)
            return

        if speaker == "beasts":
            if self.current_room != "cave_chamber":
                print("The beasts are not here.")
                return
            state = self._beast_speech_state()
            line = choose_rotating_line(
                BEAST_SPEECH[state],
                self.speech_counts,
                f"beasts:{state}",
            )
            print(line)
            return

        print("You can speak to the bartender, the raiders, or the beasts when they are present.")
~~~

- [ ] **Step 7: Route speak/talk/chat through the new method**

Replace:

~~~python
        if verb in {"speak", "talk", "chat"}:
            self.speak_to_bartender(); return
~~~

with:

~~~python
        if verb in {"speak", "talk", "chat"}:
            target = " ".join(parts[1:]).strip()
            self.speak_to(target or None)
            return
~~~

- [ ] **Step 8: Run speech and existing dialogue regression suites**

Run:

~~~bash
pytest -q   tests/test_speech.py   tests/test_bartender_dialogue.py   tests/test_lick_states_and_beasts.py   tests/test_game.py
~~~

Expected: PASS.

- [ ] **Step 9: Run full suite and commit**

Run:

~~~bash
python -m py_compile adventure_game.py game/*.py
pytest -q
git diff --check
~~~

Commit:

~~~bash
git add game/speech.py game/game.py tests/test_speech.py
git commit -m "Add contextual character speech"
~~~

---

### Task 3: Add a lock-safe in-memory browser game bridge

**Files:**
- Create: web/__init__.py
- Create: web/game_bridge.py
- Create: tests/test_web_app.py
- Modify: requirements.txt

**Interfaces:**
- Produces: BrowserGameSession dataclass with game: Game and transcript: list[str]
- Produces: GameSessionStore.get_or_create(session_id: str) -> BrowserGameSession
- Produces: GameSessionStore.run_command(session_id: str, command: str) -> dict
- Produces: GameSessionStore.reset(session_id: str) -> dict
- Produces: GameSessionStore.drop(session_id: str) -> None
- Uses one module-level OUTPUT_LOCK = threading.RLock() for all stdout capture.
- No Flask request/session imports belong in game_bridge.py.

- [ ] **Step 1: Add runtime dependencies**

Replace requirements.txt with:

~~~text
Flask>=3.1,<4
gunicorn>=23,<24
pytest
~~~

- [ ] **Step 2: Write failing bridge creation and command tests**

Create tests/test_web_app.py:

~~~python
from web.game_bridge import GameSessionStore


def test_store_creates_game_with_opening_transcript():
    store = GameSessionStore()

    result = store.get_or_create("alpha")

    assert result.game.player.name == "Traveller"
    assert result.game.state == "in progress"
    transcript = "\n".join(result.transcript).lower()
    assert "the secret that wasn't" in transcript
    assert "the end" in transcript


def test_run_command_appends_only_new_output():
    store = GameSessionStore()
    session = store.get_or_create("alpha")
    original_length = len(session.transcript)

    result = store.run_command("alpha", "inventory")

    assert result["lines"][0] == "> inventory"
    assert any("coins:" in line.lower() for line in result["lines"])
    assert len(result["transcript"]) > original_length
    assert result["transcript"][-len(result["lines"]):] == result["lines"]
    assert result["running"] is True
~~~

- [ ] **Step 3: Run bridge tests and confirm RED**

Run:

~~~bash
pytest -q tests/test_web_app.py
~~~

Expected: import failure because web.game_bridge does not exist.

- [ ] **Step 4: Create the web package and bridge**

Create web/__init__.py as an empty package initializer for this task.

Create web/game_bridge.py:

~~~python
from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
import threading

from game.game import Game


OUTPUT_LOCK = threading.RLock()


@dataclass
class BrowserGameSession:
    game: Game
    transcript: list[str]


def _captured_lines(callback):
    with OUTPUT_LOCK:
        buffer = StringIO()
        with redirect_stdout(buffer):
            callback()
    return buffer.getvalue().splitlines()


class GameSessionStore:
    def __init__(self):
        self._sessions = {}

    def _new_session(self):
        game = Game()
        lines = _captured_lines(lambda: game.start_game(player_name="Traveller"))
        return BrowserGameSession(game=game, transcript=list(lines))

    def get_or_create(self, session_id):
        with OUTPUT_LOCK:
            if session_id not in self._sessions:
                self._sessions[session_id] = self._new_session()
            return self._sessions[session_id]

    def run_command(self, session_id, command):
        with OUTPUT_LOCK:
            browser_session = self.get_or_create(session_id)
            output_lines = _captured_lines(lambda: browser_session.game.handle_command(command))
            lines = [f"> {command}", *output_lines]
            browser_session.transcript.extend(lines)
            return {
                "lines": lines,
                "transcript": list(browser_session.transcript),
                "running": browser_session.game.running,
                "state": browser_session.game.state,
                "victory": browser_session.game.victory,
            }

    def reset(self, session_id):
        with OUTPUT_LOCK:
            browser_session = self._new_session()
            self._sessions[session_id] = browser_session
            return {
                "lines": list(browser_session.transcript),
                "transcript": list(browser_session.transcript),
                "running": browser_session.game.running,
                "state": browser_session.game.state,
                "victory": browser_session.game.victory,
            }

    def drop(self, session_id):
        with OUTPUT_LOCK:
            self._sessions.pop(session_id, None)
~~~

- [ ] **Step 5: Add failing isolation/reset tests**

Append:

~~~python
def test_store_isolates_game_state_between_session_ids():
    store = GameSessionStore()
    alpha = store.get_or_create("alpha")
    beta = store.get_or_create("beta")

    alpha.game.player.coins = 9

    assert beta.game.player.coins != 9
    assert alpha is not beta
    assert alpha.game is not beta.game


def test_reset_replaces_only_requested_game():
    store = GameSessionStore()
    alpha = store.get_or_create("alpha")
    beta = store.get_or_create("beta")
    alpha.game.player.coins = 9
    beta.game.player.coins = 7

    store.reset("alpha")

    assert store.get_or_create("alpha").game.player.coins == 1
    assert store.get_or_create("beta").game.player.coins == 7
~~~

- [ ] **Step 6: Run bridge tests and confirm GREEN**

Run:

~~~bash
pytest -q tests/test_web_app.py
~~~

Expected: PASS.

- [ ] **Step 7: Run existing CLI tests and commit**

Run:

~~~bash
pytest -q
python -m py_compile adventure_game.py game/*.py web/*.py
git diff --check
~~~

Commit:

~~~bash
git add requirements.txt web/__init__.py web/game_bridge.py tests/test_web_app.py
git commit -m "Add browser game session bridge"
~~~

---

### Task 4: Build the Flask application factory and password gate

**Files:**
- Create: web/app.py
- Modify: web/__init__.py
- Create: web/templates/login.html
- Create: web/templates/game.html
- Modify: tests/test_web_app.py

**Interfaces:**
- Produces: create_app(config: dict | None = None) -> Flask
- App extension: app.extensions["game_store"] -> GameSessionStore
- Session keys: authenticated: bool, game_session_id: str
- Required config keys: PLAYTEST_PASSWORD, SECRET_KEY
- Optional env/config: SESSION_COOKIE_SECURE, default false for local development.

- [ ] **Step 1: Write failing startup and authentication tests**

Append:

~~~python
import pytest

from web import create_app


def test_create_app_fails_closed_without_required_secrets(monkeypatch):
    monkeypatch.delenv("PLAYTEST_PASSWORD", raising=False)
    monkeypatch.delenv("FLASK_SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError, match="PLAYTEST_PASSWORD"):
        create_app()


def make_test_app():
    return create_app({
        "TESTING": True,
        "PLAYTEST_PASSWORD": "test-pass",
        "SECRET_KEY": "test-secret",
        "SESSION_COOKIE_SECURE": False,
    })


def test_game_page_requires_authentication():
    client = make_test_app().test_client()

    response = client.get("/")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_wrong_password_is_rejected():
    client = make_test_app().test_client()

    response = client.post("/login", data={"password": "wrong"})

    assert response.status_code == 401
    assert b"incorrect" in response.data.lower()


def test_correct_password_establishes_session():
    client = make_test_app().test_client()

    response = client.post("/login", data={"password": "test-pass"})

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_logout_clears_authentication():
    client = make_test_app().test_client()
    client.post("/login", data={"password": "test-pass"})

    response = client.post("/logout", follow_redirects=False)

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
    assert client.get("/").status_code == 302
~~~

- [ ] **Step 2: Run auth tests and confirm RED**

Run:

~~~bash
pytest -q tests/test_web_app.py
~~~

Expected: import failure for create_app or missing routes.

- [ ] **Step 3: Implement application factory**

Create web/app.py:

~~~python
import hmac
import os
import secrets
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from .game_bridge import GameSessionStore


def _env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        playtest_password = os.environ.get("PLAYTEST_PASSWORD")
        secret_key = os.environ.get("FLASK_SECRET_KEY")
        if not playtest_password:
            raise RuntimeError("PLAYTEST_PASSWORD is required")
        if not secret_key:
            raise RuntimeError("FLASK_SECRET_KEY is required")
        app.config.update(
            PLAYTEST_PASSWORD=playtest_password,
            SECRET_KEY=secret_key,
            SESSION_COOKIE_SECURE=_env_bool("SESSION_COOKIE_SECURE", False),
        )
    else:
        app.config.update(config)
        if not app.config.get("PLAYTEST_PASSWORD"):
            raise RuntimeError("PLAYTEST_PASSWORD is required")
        if not app.config.get("SECRET_KEY"):
            raise RuntimeError("SECRET_KEY is required")

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    app.extensions["game_store"] = GameSessionStore()

    def require_auth(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not session.get("authenticated"):
                if request.path.startswith("/api/"):
                    return jsonify({"error": "authentication required"}), 401
                return redirect(url_for("login"))
            return view(*args, **kwargs)
        return wrapped

    @app.get("/login")
    def login():
        return render_template("login.html", error=None)

    @app.post("/login")
    def login_post():
        submitted = request.form.get("password", "")
        expected = app.config["PLAYTEST_PASSWORD"]
        if not hmac.compare_digest(submitted, expected):
            return render_template("login.html", error="Incorrect password."), 401
        session.clear()
        session["authenticated"] = True
        return redirect(url_for("game_page"))

    @app.post("/logout")
    def logout():
        session_id = session.get("game_session_id")
        if session_id:
            app.extensions["game_store"].drop(session_id)
        session.clear()
        return redirect(url_for("login"))

    @app.get("/")
    @require_auth
    def game_page():
        session_id = session.get("game_session_id")
        if not session_id:
            session_id = secrets.token_urlsafe(24)
            session["game_session_id"] = session_id
        browser_game = app.extensions["game_store"].get_or_create(session_id)
        return render_template("game.html", transcript=browser_game.transcript)

    return app
~~~

- [ ] **Step 4: Create the login and temporary game templates**

Create web/templates/login.html:

~~~html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>The Secret That Wasn't - Playtest</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body class="login-page">
  <main class="login-card">
    <p class="eyebrow">Private playtest</p>
    <h1>The Secret That Wasn't</h1>
    <p>Enter the tavern password to continue.</p>
    {% if error %}
      <p class="login-error" role="alert">{{ error }}</p>
    {% endif %}
    <form method="post" action="{{ url_for('login_post') }}">
      <label for="password">Playtest password</label>
      <input id="password" name="password" type="password" required autocomplete="current-password">
      <button type="submit">Enter The End</button>
    </form>
  </main>
</body>
</html>
~~~

Create web/templates/game.html:

~~~html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>The Secret That Wasn't</title>
</head>
<body>
  <main id="transcript">
    {% for line in transcript %}
      <div>{{ line }}</div>
    {% endfor %}
  </main>
</body>
</html>
~~~

Task 6 replaces game.html with the finished interface.

- [ ] **Step 5: Export create_app**

Replace web/__init__.py with:

~~~python
from .app import create_app

__all__ = ["create_app"]
~~~

- [ ] **Step 6: Run auth tests and confirm GREEN**

Run:

~~~bash
pytest -q tests/test_web_app.py
~~~

Expected: PASS.

- [ ] **Step 7: Verify password is not rendered**

Append:

~~~python
def test_password_value_is_not_rendered_after_login():
    client = make_test_app().test_client()
    client.post("/login", data={"password": "test-pass"})

    response = client.get("/")

    assert b"test-pass" not in response.data
~~~

Run:

~~~bash
pytest -q tests/test_web_app.py
~~~

Expected: PASS.

- [ ] **Step 8: Commit Task 4**

~~~bash
git add web/app.py web/__init__.py web/templates/login.html web/templates/game.html tests/test_web_app.py
git commit -m "Add password gated Flask app"
~~~

---

### Task 5: Add command/reset APIs and prove browser session isolation

**Files:**
- Modify: web/app.py
- Modify: tests/test_web_app.py

**Interfaces:**
- Produces: POST /api/command
- Produces: POST /api/reset
- JSON response keys: lines, transcript, running, state, victory

- [ ] **Step 1: Write failing protected API and round-trip tests**

Append:

~~~python
def login(client):
    response = client.post("/login", data={"password": "test-pass"})
    assert response.status_code == 302


def test_api_requires_authentication():
    client = make_test_app().test_client()

    response = client.post("/api/command", json={"command": "look"})

    assert response.status_code == 401
    assert response.get_json()["error"] == "authentication required"


def test_command_round_trip_returns_game_output_and_status():
    client = make_test_app().test_client()
    login(client)

    response = client.post("/api/command", json={"command": "inventory"})
    payload = response.get_json()

    assert response.status_code == 200
    assert any("coins:" in line.lower() for line in payload["lines"])
    assert payload["running"] is True
    assert payload["state"] == "in progress"
    assert payload["victory"] is False


def test_blank_command_is_rejected_without_growing_transcript():
    app = make_test_app()
    client = app.test_client()
    login(client)
    before = client.get("/").data

    response = client.post("/api/command", json={"command": "   "})

    assert response.status_code == 400
    assert response.get_json()["error"] == "command is required"
    after = client.get("/").data
    assert after == before


def test_malformed_json_is_rejected():
    client = make_test_app().test_client()
    login(client)

    response = client.post(
        "/api/command",
        data="{not-json",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "JSON body required"


def test_unknown_game_command_is_normal_game_output():
    client = make_test_app().test_client()
    login(client)

    response = client.post("/api/command", json={"command": "xyzzy"})

    assert response.status_code == 200
    assert any("unknown command" in line.lower() for line in response.get_json()["lines"])


@pytest.mark.parametrize("command", ["help", "look", "inventory"])
def test_standard_commands_work_through_http(command):
    client = make_test_app().test_client()
    login(client)

    response = client.post("/api/command", json={"command": command})

    assert response.status_code == 200
    assert len(response.get_json()["lines"]) >= 2


def test_game_over_status_is_returned_through_http():
    client = make_test_app().test_client()
    login(client)

    response = client.post("/api/command", json={"command": "quit"})
    payload = response.get_json()

    assert payload["running"] is False
    assert payload["state"] == "game over"
~~~

- [ ] **Step 2: Run API tests and confirm RED**

Run:

~~~bash
pytest -q tests/test_web_app.py
~~~

Expected: 404 for missing API routes.

- [ ] **Step 3: Add current session helper and API routes**

Inside create_app():

~~~python
    def current_game_session_id():
        session_id = session.get("game_session_id")
        if not session_id:
            session_id = secrets.token_urlsafe(24)
            session["game_session_id"] = session_id
        return session_id

    @app.post("/api/command")
    @require_auth
    def api_command():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "JSON body required"}), 400
        command = str(payload.get("command", "")).strip()
        if not command:
            return jsonify({"error": "command is required"}), 400

        try:
            result = app.extensions["game_store"].run_command(
                current_game_session_id(),
                command,
            )
        except Exception:
            app.logger.exception("Game command failed")
            return jsonify({"error": "The tavern connection failed."}), 500
        return jsonify(result)

    @app.post("/api/reset")
    @require_auth
    def api_reset():
        try:
            result = app.extensions["game_store"].reset(current_game_session_id())
        except Exception:
            app.logger.exception("Game reset failed")
            return jsonify({"error": "The tavern connection failed."}), 500
        return jsonify(result)
~~~

Refactor game_page() to call current_game_session_id() rather than repeating session-id creation.

- [ ] **Step 4: Add failing session-isolation tests**

Append:

~~~python
def test_two_browser_clients_have_isolated_game_state():
    app = make_test_app()
    alpha = app.test_client()
    beta = app.test_client()
    login(alpha)
    login(beta)

    alpha.post("/api/command", json={"command": "drink"})
    alpha_inventory = alpha.post("/api/command", json={"command": "inventory"}).get_json()
    beta_inventory = beta.post("/api/command", json={"command": "inventory"}).get_json()

    assert any("old key" in line.lower() for line in alpha_inventory["lines"])
    assert all("old key" not in line.lower() for line in beta_inventory["lines"])


def test_reset_affects_only_current_browser_session():
    app = make_test_app()
    alpha = app.test_client()
    beta = app.test_client()
    login(alpha)
    login(beta)

    alpha.post("/api/command", json={"command": "drink"})
    beta.post("/api/command", json={"command": "drink"})

    alpha.post("/api/reset")

    alpha_inventory = alpha.post("/api/command", json={"command": "inventory"}).get_json()
    beta_inventory = beta.post("/api/command", json={"command": "inventory"}).get_json()

    assert all("old key" not in line.lower() for line in alpha_inventory["lines"])
    assert any("old key" in line.lower() for line in beta_inventory["lines"])


def test_transcript_survives_page_refresh_in_same_process():
    client = make_test_app().test_client()
    login(client)
    client.post("/api/command", json={"command": "inventory"})

    page = client.get("/")

    assert b"&gt; inventory" in page.data
    assert b"Coins:" in page.data


def test_internal_game_error_is_logged_but_redacted(monkeypatch):
    app = make_test_app()
    client = app.test_client()
    login(client)

    def explode(*args, **kwargs):
        raise RuntimeError("private stack detail")

    monkeypatch.setattr(app.extensions["game_store"], "run_command", explode)
    response = client.post("/api/command", json={"command": "look"})

    assert response.status_code == 500
    assert response.get_json() == {"error": "The tavern connection failed."}
    assert b"private stack detail" not in response.data
~~~

- [ ] **Step 5: Run API/isolation tests and confirm GREEN**

Run:

~~~bash
pytest -q tests/test_web_app.py
~~~

Expected: PASS.

- [ ] **Step 6: Add browser Impossible Drink ending regression**

Append:

~~~python
def test_impossible_drink_ending_works_through_http():
    app = make_test_app()
    client = app.test_client()
    login(client)
    client.get("/")

    with client.session_transaction() as flask_session:
        session_id = flask_session["game_session_id"]

    browser_game = app.extensions["game_store"].get_or_create(session_id)
    browser_game.game.failed_drink_attempts = 19
    browser_game.game.current_room = "forest_path"

    client.post("/api/command", json={"command": "drink"})
    response = client.post("/api/command", json={"command": "drink impossible"})
    payload = response.get_json()

    assert payload["victory"] is True
    assert payload["running"] is False
    assert any("you win" in line.lower() for line in payload["lines"])
~~~

- [ ] **Step 7: Run complete web and game regressions**

Run:

~~~bash
pytest -q tests/test_web_app.py tests/test_economy.py tests/test_speech.py
pytest -q
git diff --check
~~~

Expected: PASS.

- [ ] **Step 8: Commit Task 5**

~~~bash
git add web/app.py tests/test_web_app.py
git commit -m "Add isolated browser command sessions"
~~~

---

### Task 6: Build the mobile-friendly playtest interface

**Files:**
- Replace: web/templates/game.html
- Create: web/static/game.js
- Create: web/static/style.css
- Modify: tests/test_web_app.py

**Interfaces:**
- DOM IDs: transcript, command-form, command-input, send-button, reset-button, status
- Convenience button selector: [data-command]
- API contracts remain those from Task 5.

- [ ] **Step 1: Write failing page-structure test**

Append:

~~~python
def test_game_page_contains_playtest_controls():
    client = make_test_app().test_client()
    login(client)

    response = client.get("/")
    html = response.data.lower()

    assert b'id="transcript"' in html
    assert b'id="command-form"' in html
    assert b'id="command-input"' in html
    assert b'data-command="help"' in html
    assert b'data-command="look"' in html
    assert b'data-command="inventory"' in html
    assert b'id="reset-button"' in html
    assert b"game.js" in html
    assert b"style.css" in html
~~~

- [ ] **Step 2: Run page test and confirm RED**

Run:

~~~bash
pytest -q tests/test_web_app.py::test_game_page_contains_playtest_controls
~~~

Expected: failure against temporary template.

- [ ] **Step 3: Replace game.html**

~~~html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#090b10">
  <title>The Secret That Wasn't</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
  <div class="page-shell">
    <header class="game-header">
      <div>
        <p class="eyebrow">Private playtest</p>
        <h1>The Secret That Wasn't</h1>
      </div>
      <form method="post" action="{{ url_for('logout') }}">
        <button class="ghost-button" type="submit">Leave tavern</button>
      </form>
    </header>

    <main class="game-panel">
      <section id="transcript" class="transcript" aria-live="polite" aria-label="Game transcript">
        {% for line in transcript %}
          <div class="transcript-line">{{ line }}</div>
        {% endfor %}
      </section>

      <div id="status" class="status" aria-live="polite"></div>

      <div class="quick-actions" aria-label="Quick commands">
        <button type="button" data-command="help">Help</button>
        <button type="button" data-command="look">Look</button>
        <button type="button" data-command="inventory">Inventory</button>
        <button type="button" id="reset-button" class="danger-ghost">Reset</button>
      </div>

      <form id="command-form" class="command-form" autocomplete="off">
        <label class="sr-only" for="command-input">Command</label>
        <span class="prompt" aria-hidden="true">&gt;</span>
        <input
          id="command-input"
          name="command"
          type="text"
          enterkeyhint="send"
          autocapitalize="none"
          spellcheck="false"
          placeholder="Try: speak bartender"
          autofocus
        >
        <button id="send-button" type="submit">Send</button>
      </form>
    </main>
  </div>
  <script src="{{ url_for('static', filename='game.js') }}" defer></script>
</body>
</html>
~~~

- [ ] **Step 4: Create game.js**

Create web/static/game.js:

~~~javascript
const transcript = document.getElementById("transcript");
const form = document.getElementById("command-form");
const input = document.getElementById("command-input");
const sendButton = document.getElementById("send-button");
const resetButton = document.getElementById("reset-button");
const statusBox = document.getElementById("status");

function setBusy(busy) {
  input.disabled = busy;
  sendButton.disabled = busy;
  resetButton.disabled = busy;
  document.querySelectorAll("[data-command]").forEach((button) => {
    button.disabled = busy;
  });
}

function appendLines(lines) {
  lines.forEach((line) => {
    const row = document.createElement("div");
    row.className = line.startsWith("> ")
      ? "transcript-line command-echo"
      : "transcript-line";
    row.textContent = line;
    transcript.appendChild(row);
  });
  transcript.scrollTop = transcript.scrollHeight;
}

async function sendCommand(command) {
  const cleaned = command.trim();
  if (!cleaned) return;

  setBusy(true);
  statusBox.textContent = "";

  try {
    const response = await fetch("/api/command", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({command: cleaned}),
    });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error || "Command failed.");
    }

    appendLines(payload.lines);

    if (payload.victory) {
      statusBox.textContent = "Victory.";
    } else if (!payload.running) {
      statusBox.textContent = "The run has ended. Reset when you are ready.";
    }
  } catch (error) {
    statusBox.textContent = error.message || "The tavern connection failed.";
  } finally {
    setBusy(false);
    input.value = "";
    input.focus();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendCommand(input.value);
});

document.querySelectorAll("[data-command]").forEach((button) => {
  button.addEventListener("click", () => sendCommand(button.dataset.command));
});

resetButton.addEventListener("click", async () => {
  if (!window.confirm("Reset this playthrough?")) return;

  setBusy(true);
  statusBox.textContent = "";

  try {
    const response = await fetch("/api/reset", {method: "POST"});
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "Reset failed.");
    }

    transcript.replaceChildren();
    appendLines(payload.transcript);
    statusBox.textContent = "Fresh playthrough started.";
  } catch (error) {
    statusBox.textContent = error.message || "The tavern refused to reset.";
  } finally {
    setBusy(false);
    input.focus();
  }
});

window.addEventListener("load", () => {
  transcript.scrollTop = transcript.scrollHeight;
  input.focus();
});
~~~

- [ ] **Step 5: Create responsive CSS**

Create web/static/style.css:

~~~css
:root {
  color-scheme: dark;
  --bg: #090b10;
  --panel: rgba(16, 19, 27, 0.94);
  --panel-soft: rgba(25, 29, 39, 0.8);
  --text: #e9e6dd;
  --muted: #9e9a91;
  --accent: #d8b36b;
  --accent-soft: rgba(216, 179, 107, 0.15);
  --danger: #dc8c8c;
  --border: rgba(216, 179, 107, 0.24);
  --shadow: 0 24px 70px rgba(0, 0, 0, 0.45);
  font-family: ui-monospace, "Cascadia Code", "SFMono-Regular", Consolas, monospace;
}

* { box-sizing: border-box; }

html,
body {
  margin: 0;
  min-height: 100%;
  background:
    radial-gradient(circle at top, rgba(72, 55, 37, 0.25), transparent 38rem),
    linear-gradient(180deg, #0c0e14 0%, var(--bg) 70%);
  color: var(--text);
}

body {
  min-height: 100vh;
  padding: max(16px, env(safe-area-inset-top)) 16px max(16px, env(safe-area-inset-bottom));
}

button,
input { font: inherit; }

button {
  color: var(--text);
  background: var(--panel-soft);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 14px;
  cursor: pointer;
}

button:hover,
button:focus-visible {
  border-color: var(--accent);
  background: var(--accent-soft);
  outline: none;
}

button:disabled,
input:disabled {
  opacity: 0.55;
  cursor: wait;
}

.page-shell {
  width: min(980px, 100%);
  margin: 0 auto;
}

.game-header {
  display: flex;
  gap: 20px;
  justify-content: space-between;
  align-items: end;
  margin-bottom: 14px;
}

.game-header h1,
.login-card h1 {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.eyebrow {
  margin: 0 0 6px;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.72rem;
}

.game-panel,
.login-card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
}

.game-panel { padding: 14px; }

.transcript {
  min-height: 54vh;
  max-height: 66vh;
  overflow-y: auto;
  padding: 18px;
  border-radius: 12px;
  background: rgba(2, 4, 8, 0.72);
  border: 1px solid rgba(255, 255, 255, 0.05);
  line-height: 1.55;
  scrollbar-color: var(--accent) transparent;
}

.transcript-line {
  min-height: 1.45em;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.command-echo {
  color: var(--accent);
  margin-top: 0.7rem;
}

.status {
  min-height: 1.5rem;
  padding: 8px 4px 0;
  color: var(--accent);
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 10px 0;
}

.danger-ghost { color: var(--danger); }

.command-form {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 8px;
  background: rgba(2, 4, 8, 0.78);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 8px;
}

.prompt {
  color: var(--accent);
  padding-left: 8px;
}

.command-form input {
  width: 100%;
  min-height: 44px;
  color: var(--text);
  background: transparent;
  border: 0;
  outline: 0;
}

.command-form input::placeholder { color: #6f716f; }
.ghost-button { white-space: nowrap; }

.login-page {
  display: grid;
  place-items: center;
}

.login-card {
  width: min(460px, 100%);
  padding: 28px;
}

.login-card form {
  display: grid;
  gap: 10px;
  margin-top: 24px;
}

.login-card input {
  width: 100%;
  min-height: 46px;
  padding: 10px 12px;
  color: var(--text);
  background: rgba(2, 4, 8, 0.75);
  border: 1px solid var(--border);
  border-radius: 10px;
}

.login-error { color: var(--danger); }

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
}

@media (max-width: 640px) {
  body {
    padding-left: 10px;
    padding-right: 10px;
  }

  .game-header { align-items: center; }
  .game-header h1 { font-size: 1.35rem; }

  .game-panel {
    padding: 8px;
    border-radius: 14px;
  }

  .transcript {
    min-height: 58vh;
    max-height: 62vh;
    padding: 12px;
    font-size: 0.9rem;
  }

  .quick-actions button { flex: 1 1 auto; }

  .command-form {
    position: sticky;
    bottom: max(6px, env(safe-area-inset-bottom));
  }

  .command-form button {
    padding-left: 12px;
    padding-right: 12px;
  }
}
~~~

- [ ] **Step 6: Run page and static-file checks**

Run:

~~~bash
pytest -q tests/test_web_app.py
test -s web/static/game.js
test -s web/static/style.css
grep -F 'viewport-fit=cover' web/templates/game.html
grep -F 'enterkeyhint="send"' web/templates/game.html
git diff --check
~~~

Expected: PASS.

- [ ] **Step 7: Commit Task 6**

~~~bash
git add web/templates/game.html web/static/game.js web/static/style.css tests/test_web_app.py
git commit -m "Build browser playtest interface"
~~~

---

### Task 7: Add portable deployment and standalone documentation

**Files:**
- Create: .env.example
- Create: Dockerfile
- Create: Procfile
- Modify: README.md
- Modify: tests/test_web_app.py

**Interfaces:**
- Factory entry point: web:create_app
- Production server: one Gunicorn worker, four threads
- Required env: PLAYTEST_PASSWORD, FLASK_SECRET_KEY
- HTTPS recommendation: SESSION_COOKIE_SECURE=1

- [ ] **Step 1: Create .env.example without real secrets**

~~~text
PLAYTEST_PASSWORD=replace-me
FLASK_SECRET_KEY=replace-with-a-long-random-value
SESSION_COOKIE_SECURE=0
PORT=8000
~~~

- [ ] **Step 2: Create Dockerfile**

~~~dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "exec gunicorn --workers 1 --threads 4 --bind 0.0.0.0:${PORT:-8000} 'web:create_app()'"]
~~~

- [ ] **Step 3: Create Procfile**

~~~text
web: gunicorn --workers 1 --threads 4 --bind 0.0.0.0:$PORT 'web:create_app()'
~~~

- [ ] **Step 4: Rewrite README as standalone documentation**

README must document these exact commands:

~~~bash
git clone https://github.com/sillymotives/The-Secret-That-Wasn-t.git
cd The-Secret-That-Wasn-t
python -m pip install -r requirements.txt
python adventure_game.py
~~~

Local web launch:

~~~bash
export PLAYTEST_PASSWORD='choose-a-password'
export FLASK_SECRET_KEY='choose-a-long-random-secret'
flask --app 'web:create_app()' run
~~~

PowerShell:

~~~powershell
$env:PLAYTEST_PASSWORD = "choose-a-password"
$env:FLASK_SECRET_KEY = "choose-a-long-random-secret"
flask --app "web:create_app()" run
~~~

Production:

~~~bash
gunicorn --workers 1 --threads 4 --bind 0.0.0.0:${PORT:-8000} 'web:create_app()'
~~~

Docker:

~~~bash
docker build -t secret-that-wasnt .
docker run --rm -p 8000:8000   -e PLAYTEST_PASSWORD='choose-a-password'   -e FLASK_SECRET_KEY='choose-a-long-random-secret'   secret-that-wasnt
~~~

README must also state:

- set SESSION_COOKIE_SECURE=1 behind HTTPS
- the password gate is shared access, not user accounts
- browser game sessions are in memory
- server restarts erase browser runs
- production currently requires one Gunicorn worker
- browser sessions remain isolated inside that process
- hosted browser play is the easiest phone/tablet option
- Android/Termux CLI remains supported
- tests run with python compilation plus pytest

- [ ] **Step 5: Add deployment invariant test**

Append:

~~~python
from pathlib import Path


def test_deployment_files_keep_single_worker_and_no_real_password():
    dockerfile = Path("Dockerfile").read_text(encoding="utf-8")
    procfile = Path("Procfile").read_text(encoding="utf-8")
    env_example = Path(".env.example").read_text(encoding="utf-8").lower()

    assert "--workers 1" in dockerfile
    assert "--workers 1" in procfile
    assert "playtest_password=replace-me" in env_example
    assert "kaiithegreat" not in env_example
~~~

- [ ] **Step 6: Run deployment and full regressions**

Run:

~~~bash
pytest -q tests/test_web_app.py
python -m py_compile adventure_game.py game/*.py web/*.py
pytest -q
git diff --check
git grep -n "kaiithegreat" -- . ':!docs/superpowers/specs/*' ':!docs/superpowers/plans/*' || true
~~~

Expected: tests pass; grep shows no application/config occurrence of the proposed real password.

- [ ] **Step 7: Commit Task 7**

~~~bash
git add .env.example Dockerfile Procfile README.md tests/test_web_app.py
git commit -m "Package and document web playtest"
~~~

---

### Task 8: Final end-to-end verification and branch completion

**Files:**
- Modify tests only if verification uncovers a reproducible bug; any bug fix requires a failing regression test first.
- No temporary workflow, report, or scratch files may remain.

**Interfaces:**
- Produces a verified feature branch ready for superpowers:finishing-a-development-branch.

- [ ] **Step 1: Check every design success criterion**

Re-read:

~~~text
docs/superpowers/specs/2026-09-18-standalone-repo-speech-web-playtest-design.md
~~~

Map each success criterion to implementation and test evidence. If any gap exists, return to TDD before continuing.

- [ ] **Step 2: Verify preserved history**

Run:

~~~bash
git rev-list --count HEAD
git log --oneline --all | head -30
git log --format='%s' | grep -F "Document Linux Windows and phone setup"
~~~

Expected: non-trivial filtered game history with known historical commit.

- [ ] **Step 3: Run compilation**

~~~bash
python -m py_compile adventure_game.py game/*.py web/*.py
~~~

Expected: exit 0.

- [ ] **Step 4: Run complete tests**

~~~bash
pytest -q
~~~

Expected: zero failures.

- [ ] **Step 5: Run CLI smoke**

~~~bash
printf 'look\nquit\n' | python adventure_game.py
~~~

Expected: game starts and accepts normal Game commands without traceback.

- [ ] **Step 6: Re-run focused speech/web/endings tests**

~~~bash
pytest -q   tests/test_speech.py   tests/test_web_app.py   tests/test_economy.py   tests/test_interactions.py   tests/test_lick_states_and_beasts.py
~~~

Expected: PASS.

- [ ] **Step 7: Verify secrets and diff hygiene**

~~~bash
git diff --check
git status --short
git grep -n "kaiithegreat" -- . ':!docs/superpowers/specs/*' ':!docs/superpowers/plans/*' || true
~~~

Expected: clean diff/status and no real password in application/config files.

- [ ] **Step 8: Verify repository shape**

~~~bash
test -f adventure_game.py
test -d game
test -d web
test -d tests
test -d data
test -f Dockerfile
test -f Procfile
test -f .env.example
test ! -d text-adventure-game
~~~

Expected: all checks pass.

- [ ] **Step 9: Inspect final feature diff**

~~~bash
git diff --stat main...HEAD
git diff --name-only main...HEAD
~~~

Expected feature changes are limited to:

- game/speech.py
- game/game.py
- tests/test_speech.py
- requirements.txt
- web/
- tests/test_web_app.py
- .env.example
- Dockerfile
- Procfile
- README.md

No temporary migration verifier or generated report remains.

- [ ] **Step 10: Invoke verification-before-completion**

Use superpowers:verification-before-completion and base every completion claim on fresh outputs from this task.

- [ ] **Step 11: Invoke finishing-a-development-branch**

Use superpowers:finishing-a-development-branch.

Base branch:

~~~text
main
~~~

Feature branch:

~~~text
feature/contextual-speech-and-web-playtest
~~~

Present the standard integration choices and wait for the user's decision.
