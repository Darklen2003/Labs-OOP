import math
from typing import Any

from core.config import MonsterConfig
from core.game_object import GameObject
from core.mixins import LoggingMixin


class Monster(LoggingMixin, GameObject):

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        config: MonsterConfig | None = None,
    ) -> None:
        self._cfg = config if config is not None else MonsterConfig()
        super().__init__(name=self._cfg.name)

        self.x: float = x
        self.y: float = y
        self.hp: int = self._cfg.max_hp

        self.log(
            f"Появился монстр {self.name} (id={self.id}) "
            f"на ({self.x}, {self.y})"
        )

    def update(self, dt: float) -> None:
        if not self.active:
            return

    def draw(self) -> str:
        return "M"

    def move(self, dx: float, dy: float) -> None:
        if not self.active:
            return
        self.x += dx
        self.y += dy
        self.log(f"{self.name} сместился на ({self.x}, {self.y})")

    @property
    def collision_radius(self) -> float:
        return self._cfg.collision_radius

    def collides_with(self, other: Any) -> bool:
        has_pos = hasattr(other, "x") and hasattr(other, "y")
        if not (has_pos and hasattr(other, "collision_radius")):
            return False
        dist = math.hypot(self.x - other.x, self.y - other.y)
        return dist <= (self.collision_radius + other.collision_radius)

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)
        self.log(f"{self.name} получил {amount} урона (HP: {self.hp})")
        if self.hp <= 0:
            self.deactivate()
            self.log(f"{self.name} повержен!")
