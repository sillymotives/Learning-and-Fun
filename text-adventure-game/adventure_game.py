# Entry point for the text-based adventure game.

from game.__main__ import main
from game.game import Game


def start_game(player_name=None):
    """Start the adventure using the course-facing function name."""
    game = Game()
    game.start_game(player_name)
    return game


def forest_path(game):
    """Run the existing forest scenario."""
    game.trigger_forest_raid()
    return game


def cave_path(game):
    """Run the existing cave decision scenario."""
    game.current_room = "cave_chamber"
    game.show_current_room()
    game.cave_fight()
    return game


if __name__ == "__main__":
    print("Starting The Secret That Wasn't...\n")
    main()
