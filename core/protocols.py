from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Movable(Protocol):
    """Способность объекта изменять свои координаты."""

    def move(self, dx: float, dy: float) -> None:
        ...


@runtime_checkable
class Drawable(Protocol):
    """Способность возвращать символ для отрисовки."""

    def draw() -> str:
        ...


@runtime_checkable
class Collidable(Protocol):
    """Способность участвовать в расчете пространственных коллизий."""

    @property
    def collision_radius(self) -> float:
        ...

    def collides_with(self, other: Any) -> bool:
        ...
