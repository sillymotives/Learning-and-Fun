from game.game import Game
from game.items import Item


def give_map(game):
    game.player.add_item(
        Item(
            "crumpled map",
            "A cheaply drawn map. Someone has aggressively erased a section marked 'TREASURE'.",
        )
    )


def test_map_command_requires_map(capsys):
    game = Game()

    game.show_map()
    output = capsys.readouterr().out.lower()

    assert "do not have a map" in output
    assert "hidden treasure" not in output


def test_buy_map_spends_extra_coin_and_adds_real_item(capsys):
    game = Game()
    game.drinks_bought = 1
    game.player.coins = 1

    game.buy_map()
    output = capsys.readouterr().out.lower()

    assert game.player.coins == 0
    assert any(item.name.lower() == "crumpled map" for item in game.player.inventory)
    assert "map" in output


def test_buy_map_before_first_drink_is_refused(capsys):
    game = Game()
    game.player.coins = 1

    game.buy_map()
    output = capsys.readouterr().out.lower()

    assert game.player.coins == 1
    assert not any(item.name.lower() == "crumpled map" for item in game.player.inventory)
    assert "drink" in output


def test_map_offer_appears_when_returning_with_spare_coin(capsys):
    game = Game()
    game.state = "in progress"
    game.drinks_bought = 1
    game.player.coins = 1
    game.current_room = "root_cellar"

    game.move("south")
    output = capsys.readouterr().out.lower()

    assert "another drink" in output
    assert "or a map" in output
    assert game.map_offer_made is True


def test_map_expands_with_exploration_without_spoiling_treasure(capsys):
    game = Game()
    give_map(game)
    game.visited_rooms = {"tavern", "root_cellar"}

    game.show_map()
    early = capsys.readouterr().out.lower()

    assert "[tavern]" in early
    assert "[root cellar]" in early
    assert "[?]" in early
    assert "cave entrance" not in early
    assert "forest path" not in early
    assert "treasure" not in early

    game.visited_rooms.add("cave_entrance")
    game.show_map()
    deeper = capsys.readouterr().out.lower()

    assert "[cave entrance]" in deeper
    assert "cave chamber" not in deeper
    assert "[?]" in deeper
    assert "treasure" not in deeper

    game.visited_rooms.add("forest_path")
    game.treasure_found = True
    game.show_map()
    discovered = capsys.readouterr().out.lower()

    assert "[forest path]" in discovered
    assert "treasure discovered" in discovered


def test_room_display_records_exploration(capsys):
    game = Game()
    game.current_room = "root_cellar"

    game.show_current_room()
    capsys.readouterr()

    assert "root_cellar" in game.visited_rooms


def test_cellar_coin_is_currency_not_inventory_object(capsys):
    game = Game()
    game.current_room = "root_cellar"
    starting_coins = game.player.coins

    game.take_item("coin")
    capsys.readouterr()

    assert game.player.coins == starting_coins + 1
    assert not any(item.name.lower() == "coin" for item in game.player.inventory)
    assert "coin" not in [item.lower() for item in game.rooms["root_cellar"].items]


def test_owned_map_has_bespoke_inspect_and_lick_text(capsys):
    game = Game()
    give_map(game)

    game.flavour_action("inspect", "map")
    inspect_output = capsys.readouterr().out.lower()
    game.flavour_action("lick", "map")
    lick_output = capsys.readouterr().out.lower()

    assert "cartography" in inspect_output
    assert "administrative negligence" in lick_output
