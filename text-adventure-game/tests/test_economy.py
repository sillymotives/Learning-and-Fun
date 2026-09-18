import pytest

from game.game import Game
from game.items import Item
from game.player import Player


def test_second_drink_spends_a_second_coin(capsys):
    game = Game()
    game.player.coins = 2

    game.drink_from_bar()
    capsys.readouterr()
    assert game.player.coins == 1

    game.drink_from_bar()
    output = capsys.readouterr().out.lower()

    assert "ah. a second drink" in output
    assert game.player.coins == 0


def test_inventory_shows_coin_balance_even_without_items(capsys):
    player = Player(coins=1)

    player.show_inventory()
    output = capsys.readouterr().out.lower()

    assert "you are carrying nothing" in output
    assert "coins: 1" in output


def test_no_coin_drink_refusal_does_not_end_game(capsys):
    game = Game()
    game.state = "in progress"
    game.player.coins = 0

    game.drink_from_bar()
    output = capsys.readouterr().out.lower()

    assert "no coin" in output
    assert game.running is True
    assert game.state == "in progress"


def test_wrong_place_drinking_escalates_without_ending_game(capsys):
    game = Game()
    game.state = "in progress"
    game.current_room = "root_cellar"
    game.drinks_bought = 1

    game.drink_from_bar()
    first = capsys.readouterr().out.lower()
    game.drink_from_bar()
    second = capsys.readouterr().out.lower()

    assert "am i an alcoholic" in first
    assert "cellar" in first
    assert "was there something else in that first drink" in second
    assert game.failed_drink_attempts == 2
    assert game.running is True
    assert game.state == "in progress"


def test_wrong_place_drink_milestones_stop_at_100(capsys):
    game = Game()
    game.current_room = "forest_path"
    game.failed_drink_attempts = 99

    game.drink_from_bar()
    hundred = capsys.readouterr().out.lower()

    assert "attempt 100" in hundred
    assert game.failed_drink_attempts == 100

    game.drink_from_bar()
    one_hundred_one = capsys.readouterr().out.lower()

    assert "milestone" not in one_hundred_one
    assert game.failed_drink_attempts == 101


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
    assert not any(item.name.lower() == "impossible drink" for item in game.player.inventory)


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
    assert not any(item.name.lower() == "impossible drink" for item in game.player.inventory)


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
