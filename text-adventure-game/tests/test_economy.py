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
