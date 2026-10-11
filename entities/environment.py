import math
from typing import Any

from core.config import GameConfig, ItemData
from core.game_object import GameObject
from core.mixins import LoggingMixin


class Chest(LoggingMixin, GameObject):

    def __init__(
        self,
        x: float,
        y: float,
        item: ItemData | None = None,
        radius: float = 0.5,
    ) -> None:
        super().__init__(name="Сундук")
        self.x: float = x
        self.y: float = y
        self._radius: float = radius
        default_item = ItemData(name="Золото", value=50)
        self.item: ItemData = item if item is not None else default_item
        self.is_opened: bool = False

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> str:
        return "[_]" if self.is_opened else "[C]"

    @property
    def collision_radius(self) -> float:
        return self._radius

    def collides_with(self, other: Any) -> bool:
        has_pos = hasattr(other, "x") and hasattr(other, "y")
        if not (has_pos and hasattr(other, "collision_radius")):
            return False
        dist = math.hypot(self.x - other.x, self.y - other.y)
        return dist <= (self.collision_radius + other.collision_radius)

    def open(self) -> ItemData | None:
        if self.is_opened:
            self.log_warning("Сундук уже открыт")
            return None
        self.is_opened = True
        self.log(
            f"Сундук открыт! Получено: {self.item.name} (+{self.item.value})"
        )
        return self.item


class Trap(LoggingMixin, GameObject):

    def __init__(
        self,
        x: float,
        y: float,
        game_config: GameConfig | None = None,
        radius: float = 0.4,
    ) -> None:
        super().__init__(name="Ловушка")
        self.x: float = x
        self.y: float = y
        self._radius: float = radius
        self._game_cfg = game_config or GameConfig()
        self.is_triggered: bool = False

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> str:
        return "_" if self.is_triggered else "^"

    @property
    def collision_radius(self) -> float:
        return self._radius

    def collides_with(self, other: Any) -> bool:
        has_pos = hasattr(other, "x") and hasattr(other, "y")
        if not (has_pos and hasattr(other, "collision_radius")):
            return False
        dist = math.hypot(self.x - other.x, self.y - other.y)
        return dist <= (self.collision_radius + other.collision_radius)

    def trigger(self, target: Any) -> None:
        if self.is_triggered:
            return
        self.is_triggered = True
        dmg = self._game_cfg.trap_damage
        name = getattr(target, 'name', 'объект')
        self.log_warning(f"Ловушка сработала на {name}! Урон: {dmg}")
        if hasattr(target, "take_damage"):
            target.take_damage(dmg)
