from game.game import Game
from game.items import Item


def give_map(game):
    game.player.add_item(Item("crumpled map", "Suspicious cartography."))


def speak(game, capsys):
    game.speak_to_bartender()
    return capsys.readouterr().out.lower()


def test_bartender_has_exactly_fifty_curated_dialogue_combinations():
    game = Game()
    rules = getattr(game, "bartender_dialogue_rules", ())

    assert len(rules) == 50
    assert len({rule.key for rule in rules}) == 50
    assert all(len(rule.required) >= 2 for rule in rules)


def test_damp_bootless_map_owner_gets_specific_combination(capsys):
    game = Game()
    game.bartender_extinguished = True
    game.bartender_boot_stolen = True
    give_map(game)

    output = speak(game, capsys)

    assert "specific my hatred" in output
    assert "cold" in output or "wet" in output or "damp" in output


def test_fire_bootless_map_owner_uses_more_specific_state(capsys):
    game = Game()
    game.bartender_on_fire = True
    game.bartender_boot_stolen = True
    give_map(game)

    output = speak(game, capsys)

    assert "map" in output
    assert "fire" in output or "burn" in output
    assert "boot" in output


def test_curated_combination_rotates_its_own_lines(capsys):
    game = Game()
    game.bartender_extinguished = True
    game.bartender_boot_stolen = True
    give_map(game)

    first = speak(game, capsys)
    second = speak(game, capsys)

    assert first != second
    assert "specific my hatred" in first + second


def test_extinguishing_is_remembered_after_reignition(capsys):
    game = Game()
    game.drinks_bought = 1
    game.torch_taken = True

    game.handle_command("use torch on bartender")
    capsys.readouterr()
    game.handle_command("rub drink on bartender")
    capsys.readouterr()
    game.handle_command("use torch on bartender")
    capsys.readouterr()

    output = speak(game, capsys)

    assert "last time" in output or "remember" in output or "summer" in output
    assert "put me out" in output or "extinguish" in output or "warm" in output


def test_unmatched_extra_state_can_contribute_modifier(capsys):
    game = Game()
    game.bartender_extinguished = True
    game.bartender_boot_stolen = True
    give_map(game)
    game.treasure_found = True

    output = speak(game, capsys)

    assert "treasure" in output


def test_damp_map_interaction_inherits_bartender_state(capsys):
    game = Game()
    game.bartender_extinguished = True
    give_map(game)

    game.handle_command("rub map on bartender")
    output = capsys.readouterr().out.lower()

    assert "wet" in output or "damp" in output
    assert "map" in output


def test_damp_boot_return_attempt_is_state_aware(capsys):
    game = Game()
    game.bartender_extinguished = True
    game.bartender_boot_stolen = True
    game.player.add_item(Item("bartender's left boot", "His stolen boot."))

    game.handle_command("use boot on bartender")
    output = capsys.readouterr().out.lower()

    assert "now" in output
    assert "boot" in output
    assert "wet" in output or "sock" in output or "damp" in output
