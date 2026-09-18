import pytest

from game import bartender_dialogue
from game import interactions as interaction_module
from game.game import Game
from game.items import Item


EXPECTED_LICK_STATES = {
    "normal",
    "bootless",
    "hostile",
    "defeated",
    "damp",
    "fire",
    "was_extinguished",
    "flaming_boot",
    "map_owned",
    "cave_done",
    "treasure_found",
    "beasts_thirsty",
    "beast_drink_given",
    "beasts_asleep",
}


def give_boot(game):
    game.player.add_item(Item("bartender's left boot", "A stolen tavern boot."))
    game.bartender_boot_stolen = True


def give_map(game):
    game.player.add_item(Item("crumpled map", "Suspicious cartography."))


def put_in_live_beast_cave(game):
    game.current_room = "cave_chamber"
    game.torch_taken = True


def test_every_major_bartender_lick_state_has_at_least_two_responses():
    pools = getattr(bartender_dialogue, "BARTENDER_LICK_POOLS", {})

    assert EXPECTED_LICK_STATES <= set(pools)
    for state in EXPECTED_LICK_STATES:
        assert len(pools[state]) >= 2
        assert all(len(response) >= 2 for response in pools[state])


def test_bootless_bartender_lick_rotates(capsys):
    game = Game()
    give_boot(game)

    game.handle_command("lick bartender")
    first = capsys.readouterr().out.lower()
    game.handle_command("lick bartender")
    second = capsys.readouterr().out.lower()

    assert first != second
    assert "boot" in first or "sock" in first
    assert "boot" in second or "sock" in second


def test_damp_bootless_flaming_boot_lick_uses_specific_combination(capsys):
    game = Game()
    give_boot(game)
    game.bartender_extinguished = True
    game.bartender_was_extinguished = True
    game.boot_on_fire = True

    game.handle_command("lick bartender")
    output = capsys.readouterr().out.lower()

    assert "boot" in output or "shoe" in output
    assert "fire" in output or "burn" in output or "flaming" in output
    assert "lick" in output or "taste" in output


def test_burning_bartender_lick_is_heat_aware(capsys):
    game = Game()
    game.bartender_on_fire = True

    game.handle_command("lick bartender")
    output = capsys.readouterr().out.lower()

    assert "hot" in output or "fire" in output or "burn" in output
    assert game.running is True


def test_first_pet_is_safe_second_pet_reveals_thirst(capsys):
    game = Game()
    put_in_live_beast_cave(game)

    game.handle_command("pet beast")
    first = capsys.readouterr().out.lower()

    assert game.running is True
    assert getattr(game, "beast_pet_count", 0) == 1
    assert getattr(game, "beasts_thirsty", False) is False
    assert "lean" in first or "pet" in first

    game.handle_command("pet beast")
    second = capsys.readouterr().out.lower()

    assert game.running is True
    assert getattr(game, "beast_pet_count", 0) == 2
    assert getattr(game, "beasts_thirsty", False) is True
    assert "thirst" in second


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("poke beast", "experiment"),
        ("lick beast", "offend"),
        ("kick beast", "kick"),
        ("sit on beast", "sit"),
    ],
)
def test_reckless_direct_beast_interactions_are_distinctive_deaths(capsys, command, expected):
    game = Game()
    put_in_live_beast_cave(game)

    game.handle_command(command)
    output = capsys.readouterr().out.lower()

    assert expected in output
    assert "maul" in output or "eat" in output or "death" in output or "lose" in output
    assert game.running is False
    assert game.state == "game over"


def test_inspecting_live_beasts_is_safe_but_unsettling(capsys):
    game = Game()
    put_in_live_beast_cave(game)

    game.handle_command("inspect beast")
    output = capsys.readouterr().out.lower()

    assert "teeth" in output or "eyes" in output
    assert "beast" in output
    assert game.running is True


def test_map_on_beast_is_safe_and_loses_bad_geography(capsys):
    game = Game()
    put_in_live_beast_cave(game)
    give_map(game)

    game.handle_command("use map on beast")
    output = capsys.readouterr().out.lower()

    assert "map" in output
    assert "chew" in output or "corner" in output
    assert "accurate" in output or "geography" in output or "scale" in output
    assert game.running is True


def test_pet_twice_then_bartender_gives_free_beast_drink(capsys):
    game = Game()
    put_in_live_beast_cave(game)

    game.handle_command("pet beast")
    capsys.readouterr()
    game.handle_command("pet beast")
    capsys.readouterr()

    game.current_room = "tavern"
    coins_before = game.player.coins
    game.handle_command("speak")
    output = capsys.readouterr().out.lower()

    assert "cave" in output
    assert "drink" in output
    assert "customer" in output or "tip" in output
    assert getattr(game, "beast_drink_given", False) is True
    assert any(item.name.lower() == "beast drink" for item in game.player.inventory)
    assert game.player.coins == coins_before


def test_beast_drink_makes_beasts_happy_sleepy_and_adorable(capsys):
    game = Game()
    put_in_live_beast_cave(game)
    game.beasts_thirsty = True
    game.beast_drink_given = True
    game.player.add_item(Item("beast drink", "A suspiciously generous mug for cave wildlife."))

    game.handle_command("use beast drink on beast")
    output = capsys.readouterr().out.lower()

    assert "slurp" in output
    assert "sleep" in output or "curl" in output
    assert "adorable" in output or "sweet" in output
    assert getattr(game, "beasts_asleep", False) is True
    assert game.cave_battle_done is True
    assert game.sword_taken is True
    assert game.running is True
    assert game.state != "game over"
    assert game.current_room == "tavern"
    assert not any(item.name.lower() == "beast drink" for item in game.player.inventory)


def test_sleeping_beasts_have_gentle_post_victory_flavour(capsys):
    game = Game()
    put_in_live_beast_cave(game)
    game.cave_battle_done = True
    game.beasts_asleep = True

    game.handle_command("inspect beasts")
    output = capsys.readouterr().out.lower()

    assert "sleep" in output or "curled" in output
    assert "adorable" in output or "sweet" in output or "paw" in output
    assert game.running is True


def test_plain_boot_on_beast_uses_existing_grimacing_death(capsys):
    game = Game()
    put_in_live_beast_cave(game)
    give_boot(game)

    game.handle_command("use boot on beast")
    output = capsys.readouterr().out.lower()

    assert "grimace" in output
    assert "maul" in output
    assert game.state == "game over"


def test_flaming_boot_on_beast_uses_existing_unwell_victory(capsys):
    game = Game()
    put_in_live_beast_cave(game)
    give_boot(game)
    game.boot_on_fire = True

    game.handle_command("use boot on beast")
    output = capsys.readouterr().out.lower()

    assert "unwell" in output
    assert game.cave_battle_done is True
    assert game.running is True


def test_secret_beast_routes_stay_hidden_from_cave_prompt(capsys):
    game = Game()
    put_in_live_beast_cave(game)

    game.cave_fight()
    output = capsys.readouterr().out.lower()

    assert "use torch" in output
    assert "pound chest" in output
    assert "pet beast" not in output
    assert "beast drink" not in output


def test_beast_second_wave_has_35_new_rules():
    assert hasattr(interaction_module, "BEAST_STATIC_INTERACTIONS")
    assert hasattr(interaction_module, "BEAST_STATE_INTERACTIONS")
    assert (
        len(interaction_module.BEAST_STATIC_INTERACTIONS)
        + len(interaction_module.BEAST_STATE_INTERACTIONS)
        >= 35
    )


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

    assert "reality" in output
    assert "dry" in output or "thirst" in output
    assert game.cave_battle_done is False
    assert game._has_inventory_item("impossible drink")


def test_thirsty_beast_inspection_uses_state_pack(capsys):
    game = Game()
    put_in_live_beast_cave(game)
    game.beasts_thirsty = True
    game.beast_pet_count = 2

    game.handle_command("inspect beast")
    output = capsys.readouterr().out.lower()

    assert "customer" in output
    assert game.running is True
