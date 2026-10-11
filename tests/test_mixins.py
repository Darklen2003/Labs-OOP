from core.mixins import LoggingMixin


class StandaloneClass(LoggingMixin):
    pass


def test_mixin_log_without_explicit_init():
    obj = StandaloneClass()
    obj.log("Информационное сообщение")


def test_mixin_warning_and_error():
    obj = StandaloneClass()
    obj.log_warning("Предупреждающее сообщение")
    obj.log_error("Сообщение об ошибке")


def test_mixin_slots_empty():
    """Миксин не создает __dict__ и имеет пустой __slots__."""
    assert LoggingMixin.__slots__ == ()
