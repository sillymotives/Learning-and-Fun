# Text Adventure Game

## Overview

This is a small command-line text adventure about suspicious drinks, questionable maps, cave beasties, stolen footwear, and the consequences of typing strange things just to see whether the game understands you.

The game runs entirely in a terminal. There are no third-party runtime dependencies, so if you have a reasonably modern Python 3 installation, you can play it.

The main entry point is:

```text
adventure_game.py
```

## Quick Start

Clone the repository, enter the game directory, and run the adventure:

```bash
git clone https://github.com/sillymotives/Learning-and-Fun.git
cd Learning-and-Fun/text-adventure-game
python3 adventure_game.py
```

On systems where the Python command is `python` rather than `python3`, use:

```bash
python adventure_game.py
```

You can also run the package directly:

```bash
python3 -m game
```

## Linux

Linux is the simplest way to run the game.

### 1. Install Python and Git

On Debian, Ubuntu, Linux Mint, and related distributions:

```bash
sudo apt update
sudo apt install python3 git
```

On Fedora:

```bash
sudo dnf install python3 git
```

On Arch Linux:

```bash
sudo pacman -S python git
```

### 2. Clone and run

```bash
git clone https://github.com/sillymotives/Learning-and-Fun.git
cd Learning-and-Fun/text-adventure-game
python3 adventure_game.py
```

That is enough to play.

## Windows

The game works in PowerShell, Windows Terminal, Command Prompt, or another normal Windows terminal.

### 1. Install Python

Install Python 3 and make sure either the `py` launcher or the `python` command works.

You can check with:

```powershell
py --version
```

or:

```powershell
python --version
```

You will also need Git if you want to clone the repository rather than download it as a ZIP.

### 2. Clone the repository

In PowerShell:

```powershell
git clone https://github.com/sillymotives/Learning-and-Fun.git
cd .\Learning-and-Fun\text-adventure-game
```

### 3. Run the game

Using the Windows Python launcher:

```powershell
py adventure_game.py
```

If your installation uses `python` instead:

```powershell
python adventure_game.py
```

## Phone and Tablet

Because this is a terminal game rather than a graphical application, it can also run on a phone. The main requirement is simply somewhere that can run Python and accept keyboard input.

### Android: run locally with Termux

A terminal environment such as Termux can run the game directly on Android.

Inside Termux:

```bash
pkg update
pkg install python git
git clone https://github.com/sillymotives/Learning-and-Fun.git
cd Learning-and-Fun/text-adventure-game
python adventure_game.py
```

A physical keyboard is not required, although command-heavy adventuring is considerably less thumb-hostile with one.

### Any phone or tablet: run in a browser

If your GitHub account has access to a browser-based development environment such as GitHub Codespaces, you can run the repository without installing Python locally.

Open the repository in the browser, create/open the development environment, then use its terminal:

```bash
cd text-adventure-game
python adventure_game.py
```

This is also the easiest option on iPhone and iPad.

### iPhone and iPad: local Python apps

iOS and iPadOS do not include a general-purpose system Python interpreter. You can still run the game in a Python-capable app that supports local files or Git repositories.

The exact import/clone steps depend on the app, but once the `text-adventure-game` folder is available, run:

```text
adventure_game.py
```

If the app provides a terminal, the equivalent command is usually:

```bash
python adventure_game.py
```

## How to Play

The game accepts typed commands at the prompt. Explore, inspect things, talk to characters, use items, and try suspiciously specific ideas.

Useful examples include:

```text
look
inventory
speak
go north
inspect wall
take torch
use torch on boot
pet beast
```

The obvious choices are not always the only choices. The game deliberately contains hidden interactions and state-dependent dialogue, so experimentation is encouraged.

Some experiments are healthier than others.

## Running the Tests

The game itself has no third-party runtime dependencies.

The development requirements currently contain `pytest`, which is only needed for the automated test suite.

Install it with:

```bash
python3 -m pip install -r requirements.txt
```

On Windows:

```powershell
py -m pip install -r requirements.txt
```

Then run:

```bash
python3 -m pytest -q
```

or on Windows:

```powershell
py -m pytest -q
```

## Project Structure

```text
text-adventure-game/
├── adventure_game.py        # Main entry point
├── README.md
├── requirements.txt         # Development/test dependency list
├── data/
│   └── story.json           # Rooms and story data
├── game/
│   ├── __init__.py
│   ├── __main__.py
│   ├── achievements.py
│   ├── bartender_dialogue.py
│   ├── flavour_expansion.py
│   ├── game.py
│   ├── interactions.py
│   ├── items.py
│   ├── player.py
│   └── world.py
└── tests/                   # Automated game and regression tests
```

## Contributing

If you would like to add another interaction, joke, state combination, puzzle, or deeply inadvisable use for a bartender's boot, contributions are welcome.

Feel free to open an issue or submit a pull request.
