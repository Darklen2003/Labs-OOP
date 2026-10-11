from core.protocols import Collidable, Drawable, Movable


class MockDrawable:
    def draw(self) -> str:
        return "D"


class MockMovable:
    def move(self, dx: float, dy: float) -> None:
        pass


class MockCollidable:
    @property
    def collision_radius(self) -> float:
        return 1.0

    def collides_with(self, other) -> bool:
        return True


class MockEmpty:
    pass


def test_drawable_runtime_check():
    obj = MockDrawable()
    assert isinstance(obj, Drawable)


def test_not_drawable_runtime_check():
    obj = MockEmpty()
    assert not isinstance(obj, Drawable)


def test_movable_runtime_check():
    obj = MockMovable()
    assert isinstance(obj, Movable)


def test_collidable_runtime_check():
    obj = MockCollidable()
    assert isinstance(obj, Collidable)


def test_primitive_types_not_implementing_protocol():
    assert not isinstance(42, Drawable)
    assert not isinstance("raw_string", Movable)
