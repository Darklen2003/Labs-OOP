import math
from typing import Any

from core.config import GameConfig, PlayerConfig
from core.game_object import GameObject
from core.mixins import LoggingMixin


class Player(LoggingMixin, GameObject):

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        config: PlayerConfig | None = None,
        game_config: GameConfig | None = None,
    ) -> None:
        self._cfg = config if config is not None else PlayerConfig()
        self._game_cfg = (
            game_config if game_config is not None else GameConfig()
        )

        super().__init__(name=self._cfg.name)

        self.x: float = x
        self.y: float = y
        self.hp: int = self._cfg.max_hp
        self.energy: int = self._cfg.max_energy

        self.log(
            f"Создан {self.name} на ({self.x}, {self.y}) с {self.hp} HP"
        )

    def update(self, dt: float) -> None:
        if not self.active:
            return

    def draw(self) -> str:
        return "@"

    def move(self, dx: float, dy: float) -> None:
        if not self.active:
            self.log_warning(
                f"{self.name} не может двигаться: объект неактивен"
            )
            return

        cost = self._game_cfg.step_energy_cost
        if self.energy < cost:
            self.log_warning(
                f"Недостаточно энергии! Надо {cost}, есть {self.energy}"
            )
            return

        self.energy -= cost
        self.x += dx
        self.y += dy
        self.log(
            f"{self.name} переместился на ({self.x}, {self.y}). "
            f"Энергия: {self.energy}"
        )

    @property
    def collision_radius(self) -> float:
        return self._cfg.collision_radius

    def collides_with(self, other: Any) -> bool:
        has_pos = hasattr(other, "x") and hasattr(other, "y")
        if not (has_pos and hasattr(other, "collision_radius")):
            return False
        dist = math.hypot(self.x - other.x, self.y - other.y)
        return dist <= (self.collision_radius + other.collision_radius)

    def rest(self) -> None:
        restore = self._game_cfg.rest_energy_restore
        self.energy = min(self._cfg.max_energy, self.energy + restore)
        self.log(
            f"{self.name} отдыхает. Энергия восстановлена: {self.energy}"
        )

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)
        self.log(f"{self.name} получил {amount} урона! Остаток HP: {self.hp}")
        if self.hp <= 0:
            self.deactivate()
            self.log_error(f"{self.name} погиб!")
