import unittest
from game.game import Game


def test_game_starts_in_tavern():
    game = Game()
    assert game.current_room == "tavern"


def test_room_exists():
    game = Game()
    assert "tavern" in game.rooms
    assert "root_cellar" in game.rooms


def test_take_torch_adds_to_inventory():
    game = Game()
    game.current_room = "root_cellar"
    game.take_item("torch")
    assert any(item.name == "torch" for item in game.player.inventory)


def test_turn_back_retreats_from_raiders_to_tavern():
    game = Game()
    game.trigger_forest_raid()

    game.handle_command("turn back")

    assert game.current_room == "tavern"
    assert game.running is True


def test_old_prototype_rooms_are_not_loaded():
    game = Game()
    assert "start" not in game.rooms
    assert "glade" not in game.rooms


def test_start_screen_has_elaborate_tavern(capsys):
    game = Game()
    game.start("Aster")
    output = capsys.readouterr().out

    assert "T H E   S E C R E T   T H A T   W A S N ' T" in output
    assert "NO REFUNDS" in output
    assert "SECOND DRINK" in output
    assert "THE END" in output


def test_stealing_bartenders_left_boot(capsys):
    game = Game()

    game.handle_command("steal from bartender")
    output = capsys.readouterr().out.lower()

    assert game.bartender_boot_stolen is True
    assert game.bartender_hostile is True
    assert any(
        item.name.lower() == "bartender's left boot"
        for item in game.player.inventory
    )
    assert "boot" in output

    # Apparently business outranks footwear.
    game.drink_from_bar()
    assert any(
        item.name.lower() == "old key"
        for item in game.player.inventory
    )


def test_fighting_bartender_without_sword_is_a_terrible_idea(capsys):
    game = Game()

    game.handle_command("fight bartender")
    output = capsys.readouterr().out.lower()

    assert game.state == "game over"
    assert game.running is False
    assert "towel" in output


def test_fighting_bartender_with_sword_defeats_him(capsys):
    game = Game()
    game.sword_taken = True

    game.handle_command("fight bartender")
    output = capsys.readouterr().out.lower()

    assert game.bartender_defeated is True
    assert game.running is True
    assert "chair" in output
    assert any(
        item.name.lower() == "old key"
        for item in game.player.inventory
    )


def test_help_uses_generic_item_and_target_commands(capsys):
    game = Game()

    game.print_help()
    output = capsys.readouterr().out.lower()

    assert "use <item>" in output
    assert "fight <target>" in output
    assert "steal" in output
    assert "use key" not in output
    assert "use torch" not in output


def test_bartender_does_not_dump_the_walkthrough(capsys):
    game = Game()

    game.speak_to_bartender()
    output = capsys.readouterr().out.lower()

    assert "torch" not in output
    assert "unlock" not in output
    assert "cave" not in output


def test_bartender_dialogue_rotates(capsys):
    game = Game()

    game.speak_to_bartender()
    first = capsys.readouterr().out

    game.speak_to_bartender()
    second = capsys.readouterr().out

    assert first != second


def test_bartender_is_very_upset_about_his_boot(capsys):
    game = Game()

    game.handle_command("steal from bartender")
    capsys.readouterr()

    game.speak_to_bartender()
    output = capsys.readouterr().out.lower()

    assert "boot" in output or "sock" in output


def test_use_torch_on_bartender_sets_him_on_fire(capsys):
    game = Game()
    game.torch_taken = True

    game.handle_command("use torch on bartender")
    output = capsys.readouterr().out.lower()

    assert game.bartender_on_fire is True
    assert game.bartender_hostile is True
    assert game.running is True
    assert "freezing for twenty years" in output


def test_rub_alias_can_polish_wall_with_stolen_boot(capsys):
    game = Game()

    game.handle_command("steal from bartender")
    capsys.readouterr()

    game.handle_command("rub boot on wall")
    output = capsys.readouterr().out.lower()

    assert "boot" in output
    assert "wall" in output
    assert "polish" in output


def test_generic_item_on_target_interaction_is_funny(capsys):
    game = Game()
    game.torch_taken = True

    game.handle_command("use torch on ceiling")
    output = capsys.readouterr().out.lower()

    assert "torch" in output
    assert "ceiling" in output


def test_item_interaction_requires_possession(capsys):
    game = Game()

    game.handle_command("use sword on chandelier")
    output = capsys.readouterr().out.lower()

    assert "not carrying" in output
    assert game.running is True


def test_flaming_bartender_fights_with_flaming_chair(capsys):
    game = Game()
    game.torch_taken = True
    game.sword_taken = True

    game.handle_command("use torch on bartender")
    capsys.readouterr()

    game.handle_command("fight bartender")
    output = capsys.readouterr().out.lower()

    assert game.bartender_defeated is True
    assert game.bartender_on_fire is True
    assert "chair catches fire" in output
    assert "hospitality" in output


def test_help_advertises_item_on_target_and_rubbing(capsys):
    game = Game()

    game.print_help()
    output = capsys.readouterr().out.lower()

    assert "use <item> on <target>" in output
    assert "rub <item> on <target>" in output


def test_burning_bartender_does_not_imagine_his_boot_was_stolen(capsys):
    game = Game()
    game.torch_taken = True

    game.handle_command("use torch on bartender")
    capsys.readouterr()

    game.drink_from_bar()
    output = capsys.readouterr().out.lower()

    assert "boot back" not in output
    assert "fire" in output


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_initial_state(self):
        self.assertEqual(self.game.state, "not started")

    def test_start_game(self):
        self.game.start("Aster")
        self.assertEqual(self.game.state, "in progress")

    def test_game_over(self):
        self.game.start("Aster")
        self.game.end()
        self.assertEqual(self.game.state, "game over")

    def test_player_starts_with_one_coin(self):
        self.assertEqual(self.game.player.coins, 1)

    def test_first_drink_gives_key(self):
        self.game.start("Aster")
        self.game.drink_from_bar()
        self.assertTrue(any(item.name.lower() == "old key" for item in self.game.player.inventory))

    def test_second_drink_kills_you(self):
        self.game.start("Aster")
        self.game.drink_from_bar()
        self.game.drink_from_bar()
        self.assertEqual(self.game.state, "game over")

    def test_coin_in_cellar_is_pickupable(self):
        self.game.current_room = "root_cellar"
        self.game.take_item("coin")
        self.assertTrue(any(item.name.lower() == "coin" for item in self.game.player.inventory))

    def test_use_key_unlocks_cave(self):
        self.game.current_room = "root_cellar"
        self.game.player.add_item(type("Item", (), {"name": "old key", "description": "A key"})())
        self.game.use_item("key")
        self.assertTrue(self.game.lock_open)
        self.assertEqual(self.game.current_room, "cave_entrance")

    def test_treasure_requires_defeating_raiders(self):
        self.game.current_room = "forest_path"
        self.game.take_item("hidden treasure")
        self.assertFalse(self.game.treasure_found)

    def test_sword_defeats_raiders_before_treasure(self):
        self.game.sword_taken = True
        self.game.move("east")
        self.game.handle_command("fight raiders")
        self.game.take_item("hidden treasure")
        self.assertTrue(self.game.raiders_defeated)
        self.assertTrue(self.game.victory)

    def test_turn_back_returns_from_forest(self):
        self.game.current_room = "forest_path"
        self.game.handle_command("turn back")
        self.assertEqual(self.game.current_room, "tavern")


if __name__ == "__main__":
    unittest.main()