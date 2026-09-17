from game.game import Game
from game.items import Item
from game.interactions import normalize_item


def give_map(game):
    game.player.add_item(Item("crumpled map", "A suspicious map."))


def test_map_alias_resolves_to_carried_crumpled_map(capsys):
    game = Game()
    give_map(game)

    assert normalize_item("map") == "crumpled map"

    game.handle_command("use map on bartender")
    use_output = capsys.readouterr().out.lower()
    game.handle_command("rub map on bartender")
    rub_output = capsys.readouterr().out.lower()

    assert "not carrying map" not in use_output
    assert "not carrying map" not in rub_output
    assert "map" in use_output
    assert "map" in rub_output


def test_rubbing_drink_on_flaming_bartender_puts_him_out_and_makes_him_sad(capsys):
    game = Game()
    game.drinks_bought = 1
    game.bartender_on_fire = True
    game.bartender_hostile = True

    game.handle_command("rub drink on bartender")
    output = capsys.readouterr().out.lower()

    assert game.bartender_on_fire is False
    assert game.bartender_extinguished is True
    assert "hiss" in output or "steam" in output
    assert "warm" in output

    game.speak_to_bartender()
    sad_output = capsys.readouterr().out.lower()
    assert "warm" in sad_output or "summer" in sad_output


def test_irrelevant_directions_have_room_flavour(capsys):
    game = Game()
    game.current_room = "tavern"

    game.move("west")
    output = capsys.readouterr().out.lower()

    assert game.current_room == "tavern"
    assert "that way is closed to you" not in output
    assert "wall" in output or "trophy" in output or "door" in output


def test_cellar_to_cave_route_turns_east_instead_of_continuing_north(capsys):
    game = Game()

    assert game.rooms["root_cellar"].exits.get("east") == "cave_entrance"
    assert "north" not in game.rooms["root_cellar"].exits
    assert game.rooms["cave_entrance"].exits.get("west") == "root_cellar"

    game.current_room = "root_cellar"
    game.move("east")
    locked_output = capsys.readouterr().out.lower()
    assert game.current_room == "root_cellar"
    assert "iron door" in locked_output

    game.lock_open = True
    game.move("east")
    capsys.readouterr()
    assert game.current_room == "cave_entrance"

    game.move("west")
    capsys.readouterr()
    assert game.current_room == "root_cellar"


def test_map_renders_zig_zag_route(capsys):
    game = Game()
    give_map(game)
    game.visited_rooms = {"tavern", "root_cellar", "cave_entrance", "cave_chamber"}

    game.show_map()
    output = capsys.readouterr().out

    assert "[Root Cellar] -- [Cave Entrance]" in output
    assert "[Cave Chamber]" in output
