from dataclasses import FrozenInstanceError
import pytest

from core.config import GameConfig, ItemData, MonsterConfig, RoomConfig


def test_game_config_frozen():
    cfg = GameConfig()
    with pytest.raises(FrozenInstanceError):
        cfg.max_turns = 200


def test_game_config_defaults():
    cfg = GameConfig()
    assert cfg.field_width == 20
    assert cfg.field_height == 10
    assert cfg.step_energy_cost == 1
    assert cfg.trap_damage == 15


def test_game_config_equality():
    cfg1 = GameConfig()
    cfg2 = GameConfig()
    assert cfg1 == cfg2
    assert cfg1 is not cfg2


def test_room_config_independent_lists():
    room1 = RoomConfig(name="Room 1")
    room2 = RoomConfig(name="Room 2")

    room1.monsters.append(MonsterConfig(name="Орк"))
    room1.items.append(ItemData(name="Ключ"))

    assert len(room1.monsters) == 1
    assert len(room1.items) == 1
    assert len(room2.monsters) == 0
    assert len(room2.items) == 0
    assert room1.monsters is not room2.monsters
