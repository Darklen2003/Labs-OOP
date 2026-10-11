from dataclasses import dataclass, field


@dataclass(frozen=True)
class GameConfig:
    field_width: int = 20
    field_height: int = 10
    max_turns: int = 100
    step_energy_cost: int = 1
    rest_energy_restore: int = 5
    trap_damage: int = 15


@dataclass(frozen=True)
class PlayerConfig:
    name: str = "Герой"
    max_hp: int = 100
    max_energy: int = 25
    base_attack: int = 12
    collision_radius: float = 0.5


@dataclass(frozen=True)
class MonsterConfig:
    name: str = "Гоблин"
    max_hp: int = 40
    attack_power: int = 8
    aggro_radius: float = 4.0
    collision_radius: float = 0.5


@dataclass
class ItemData:
    name: str
    item_type: str = "treasure"
    value: int = 50


@dataclass
class RoomConfig:
    name: str = "Подземелье"
    trap_count: int = 2
    monsters: list[MonsterConfig] = field(default_factory=list)
    items: list[ItemData] = field(default_factory=list)
