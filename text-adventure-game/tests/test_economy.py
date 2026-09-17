from game.game import Game
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
