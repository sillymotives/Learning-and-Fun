from game.game import Game
from game.items import Item


def give_boot(game):
    game.player.add_item(Item("bartender's left boot", "A stolen tavern boot."))
    game.bartender_boot_stolen = True


def enter_cave_fight(game):
    game.current_room = "cave_chamber"
    game.cave_fight()


def test_cave_prompt_does_not_advertise_boot(capsys):
    game = Game()

    enter_cave_fight(game)
    output = capsys.readouterr().out.lower()

    assert "use torch" in output
    assert "pound chest" in output
    assert "use boot" not in output
    assert "flaming boot" not in output


def test_plain_boot_is_a_secret_hilarious_death(capsys):
    game = Game()
    give_boot(game)
    game.current_room = "cave_chamber"

    game.handle_command("use boot")
    output = capsys.readouterr().out.lower()

    assert "grimace" in output
    assert "maul" in output
    assert "boot" in output
    assert game.running is False
    assert game.state == "game over"
    assert game.cave_battle_done is False


def test_torch_on_boot_creates_persistent_flaming_boot(capsys):
    game = Game()
    give_boot(game)
    game.torch_taken = True

    game.handle_command("use torch on boot")
    output = capsys.readouterr().out.lower()

    assert "boot" in output
    assert "fire" in output or "flame" in output or "burn" in output
    assert game.boot_on_fire is True
    assert any(item.name.lower() == "bartender's left boot" for item in game.player.inventory)


def test_flaming_boot_makes_cave_beasts_feel_unwell_and_leave(capsys):
    game = Game()
    give_boot(game)
    game.boot_on_fire = True
    game.current_room = "cave_chamber"

    game.handle_command("use boot")
    output = capsys.readouterr().out.lower()

    assert "unwell" in output
    assert "leave" in output
    assert "not frightened" in output
    assert game.cave_battle_done is True
    assert game.sword_taken is True
    assert game.running is True
    assert game.state != "game over"
    assert game.boot_on_fire is True
    assert any(item.name.lower() == "bartender's left boot" for item in game.player.inventory)
