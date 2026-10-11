from abc import ABC, abstractmethod


class GameObject(ABC):

    _next_id: int = 1

    def __init__(self, name: str) -> None:
        self._id: int = GameObject._next_id
        GameObject._next_id += 1
        self._name: str = name
        self._active: bool = True

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def active(self) -> bool:
        return self._active

    def deactivate(self) -> None:
        self._active = False

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self) -> str:
        pass

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return (
            f"<{cls_name}(id={self._id}, "
            f"name='{self._name}', active={self._active})>"
        )
