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


if __name__ == "__main__":
    unittest.main()