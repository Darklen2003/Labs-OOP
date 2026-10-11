import pytest
from core.game_object import GameObject


class IncompleteObject(GameObject):
    pass


class ConcreteObject(GameObject):

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> str:
        return "C"


def test_cannot_instantiate_abstract():
    with pytest.raises(TypeError):
        GameObject("test")


def test_subclass_must_implement_methods():
    with pytest.raises(TypeError):
        IncompleteObject("incomplete")


def test_concrete_subclass_works():
    obj = ConcreteObject("concrete")
    assert obj.name == "concrete"
    assert obj.active is True
    assert isinstance(obj.id, int)
    expected_repr = (
        f"<ConcreteObject(id={obj.id}, name='concrete', active=True)>"
    )
    assert repr(obj) == expected_repr


def test_unique_ids():
    obj1 = ConcreteObject("item_1")
    obj2 = ConcreteObject("item_2")
    assert obj1.id != obj2.id
    assert obj2.id > obj1.id


def test_deactivate():
    obj = ConcreteObject("target")
    assert obj.active is True
    obj.deactivate()
    assert obj.active is False
