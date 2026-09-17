from game.interactions import (
    STATIC_INTERACTIONS,
    normalize_item,
    normalize_target,
    normalize_verb,
)


def test_interaction_alias_normalization():
    assert normalize_item("left boot") == "bartender's left boot"
    assert normalize_item("blade") == "sword"
    assert normalize_target("the barkeep") == "bartender"
    assert normalize_target("stone walls") == "wall"
    assert normalize_verb("examine") == "inspect"
    assert normalize_verb("stroke") == "pet"


def test_static_interaction_pack_is_large_enough():
    assert 160 <= len(STATIC_INTERACTIONS) <= 190

from game.game import Game


def test_standalone_flavour_verbs_are_routed(capsys):
    game = Game()
    game.handle_command("inspect chair")
    first = capsys.readouterr().out.lower()
    game.handle_command("pet chair")
    second = capsys.readouterr().out.lower()
    game.handle_command("sit on chair")
    third = capsys.readouterr().out.lower()
    assert "combat experience" in first
    assert "gentlest interaction" in second
    assert "manufacturer intent" in third


def test_malformed_standalone_flavour_command_is_helpful(capsys):
    game = Game()
    game.handle_command("poke")
    assert "poke what" in capsys.readouterr().out.lower()


def test_unknown_flavour_target_uses_rotating_fallback(capsys):
    game = Game()
    game.handle_command("inspect chandelier")
    first = capsys.readouterr().out
    game.handle_command("inspect chandelier")
    second = capsys.readouterr().out
    assert first != second


def test_drink_becomes_contextual_after_first_purchase(capsys):
    game = Game()
    game.drink_from_bar()
    capsys.readouterr()
    game.handle_command("rub drink on bartender face")
    assert "watched you do it" in capsys.readouterr().out.lower()


def test_drink_is_unavailable_before_purchase(capsys):
    game = Game()
    game.handle_command("rub drink on bartender face")
    assert "not available" in capsys.readouterr().out.lower()


def test_tavern_mug_is_contextual(capsys):
    game = Game()
    game.handle_command("rub mug on bartender")
    assert "cloths" in capsys.readouterr().out.lower()


def test_static_item_interaction_does_not_consume_quest_item(capsys):
    game = Game()
    game.torch_taken = True
    game.handle_command("use torch on wall")
    capsys.readouterr()
    assert game.torch_taken is True


def test_bartender_moisturized_unlocks_once(capsys):
    game = Game()
    game.drink_from_bar()
    capsys.readouterr()
    game.handle_command("rub drink on bartender face")
    first = capsys.readouterr().out.lower()
    game.handle_command("rub drink on bartender face")
    second = capsys.readouterr().out.lower()
    assert "achievement unlocked" in first
    assert "bartender moisturized" in first
    assert "achievement unlocked" not in second


def test_wall_licked_is_cosmetic(capsys):
    game = Game()
    before = (game.current_room, game.lock_open, game.victory, game.running)
    game.handle_command("lick wall")
    output = capsys.readouterr().out.lower()
    after = (game.current_room, game.lock_open, game.victory, game.running)
    assert "wall licked" in output
    assert before == after


def test_attempted_capitalism_on_stone(capsys):
    game = Game()
    game.handle_command("use coin on wall")
    assert "attempted capitalism on stone" in capsys.readouterr().out.lower()


def test_training_arc_unlocks_at_100_optional_interactions(capsys):
    game = Game()
    for _ in range(100):
        game.handle_command("inspect chandelier")
    output = capsys.readouterr().out.lower()
    assert "training arc" in output
    assert "100 pushups" in output
    assert "100 situps" in output
    assert "10 km run" in output


def _buy_drink(game, capsys):
    game.drink_from_bar()
    capsys.readouterr()


def test_burning_bartender_calls_face_ale_refreshing(capsys):
    game = Game()
    _buy_drink(game, capsys)
    game.torch_taken = True
    game.handle_command("use torch on bartender")
    capsys.readouterr()
    game.handle_command("rub drink on bartender face")
    output = capsys.readouterr().out.lower()
    assert "hisses" in output
    assert "refreshing" in output


def test_bootless_bartender_objects_to_lager_moisturizer(capsys):
    game = Game()
    _buy_drink(game, capsys)
    game.handle_command("steal from bartender")
    capsys.readouterr()
    game.handle_command("rub drink on bartender face")
    output = capsys.readouterr().out.lower()
    assert "stole my boot" in output
    assert "moistur" in output


def test_burning_bootless_bartender_misses_normal_customers(capsys):
    game = Game()
    _buy_drink(game, capsys)
    game.handle_command("steal from bartender")
    capsys.readouterr()
    game.torch_taken = True
    game.handle_command("use torch on bartender")
    capsys.readouterr()
    game.handle_command("rub drink on bartender face")
    output = capsys.readouterr().out.lower()
    assert "stole my boot" in output
    assert "set me on fire" in output
    assert "normal customers" in output


def test_flavour_spam_preserves_critical_inventory_and_state(capsys):
    game = Game()
    game.player.coins = 5
    game.drink_from_bar()
    capsys.readouterr()
    game.current_room = "root_cellar"
    game.take_item("torch")
    capsys.readouterr()
    for command in ["use coin on wall", "rub key on torch", "lick wall", "kick cask", "pet torch", "sit on cask"]:
        game.handle_command(command)
        capsys.readouterr()
    assert game.running is True
    assert game.torch_taken is True
    assert any(item.name.lower() == "old key" for item in game.player.inventory)


def test_normal_win_route_survives_optional_interaction_spam(capsys):
    game = Game()
    game.player.coins = 5
    for command in ["inspect chair", "lick wall", "pet bartender", "kick bar"]:
        game.handle_command(command)
        capsys.readouterr()
    game.drink_from_bar(); capsys.readouterr()
    game.move("north"); capsys.readouterr()
    game.handle_command("use coin on wall"); capsys.readouterr()
    game.take_item("torch"); capsys.readouterr()
    game.use_item("key"); capsys.readouterr()
    game.move("north"); capsys.readouterr()
    game.resolve_cave_fight(use_torch=False); capsys.readouterr()
    game.move("east"); capsys.readouterr()
    game.handle_command("fight raiders"); capsys.readouterr()
    game.take_item("hidden treasure"); capsys.readouterr()
    assert game.victory is True
    assert game.state == "victory"


def test_help_lists_flavour_commands(capsys):
    game = Game()
    game.print_help()
    output = capsys.readouterr().out.lower()
    assert "inspect <target>" in output
    assert "poke/kick/lick <target>" in output
    assert "pet <target>" in output
    assert "sit [on <target>]" in output


def test_bartender_standard_flavour_verbs_are_bespoke(capsys):
    expectations = {
        "inspect bartender": "apron",
        "poke bartender": "finger",
        "kick bartender": "kick",
        "lick bartender": "tongue",
        "pet bartender": "hand",
        "sit on bartender": "lap",
    }
    for command, phrase in expectations.items():
        game = Game()
        game.handle_command(command)
        output = capsys.readouterr().out.lower()
        assert phrase in output, command
        assert "the bartender notices" not in output, command


def test_bartender_item_interactions_cover_common_inventory(capsys):
    game = Game()
    game.player.coins = 5
    game.drink_from_bar()
    capsys.readouterr()
    game.torch_taken = True
    game.sword_taken = True
    game.player.add_item(type("Item", (), {"name": "sword", "description": ""})())
    game.handle_command("steal from bartender")
    capsys.readouterr()

    for command in [
        "rub coin on bartender",
        "use key on bartender",
        "rub mug on bartender",
        "use drink on bartender",
        "rub boot on bartender",
        "use treasure on bartender",
    ]:
        if command == "use treasure on bartender":
            game.player.add_item(type("Item", (), {"name": "hidden treasure", "description": ""})())
        game.handle_command(command)
        output = capsys.readouterr().out.lower()
        assert "the bartender notices" not in output, command
        assert "nothing improves" not in output, command


def test_expanded_interaction_pack_has_real_density():
    assert 160 <= len(STATIC_INTERACTIONS) <= 190


def test_common_room_targets_have_multiple_bespoke_verbs():
    required = {
        "tavern": ["bartender", "bar", "chair", "wall", "sign"],
        "root_cellar": ["cask", "wall", "cellar door", "stairs"],
        "cave_entrance": ["wall", "darkness", "glowing eyes"],
        "cave_chamber": ["bones", "beast den", "stone", "wall"],
        "forest_path": ["tree", "bush", "mud", "raiders", "grass"],
    }
    for room, targets in required.items():
        for target in targets:
            count = sum(
                1
                for verb in ("inspect", "poke", "kick", "lick", "pet", "sit")
                if (verb, None, target, room) in STATIC_INTERACTIONS
            )
            assert count >= 3, (room, target, count)
