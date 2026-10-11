cat << 'EOF' > docs/uml_module2.md
# UML-диаграмма архитектуры (Модуль 2)

```mermaid
classDiagram
    class GameObject {
        <<abstract>>
        -_next_id: int$
        -_id: int
        -_name: str
        -_active: bool
        +id: int
        +name: str
        +active: bool
        +deactivate() void
        +update(dt: float)* void
        +draw()* str
        +__repr__() str
    }

    class Movable {
        <<protocol>>
        +move(dx: float, dy: float) void
    }

    class Drawable {
        <<protocol>>
        +draw() str
    }

    class Collidable {
        <<protocol>>
        +collision_radius: float
        +collides_with(other: Any) bool
    }

    class LoggingMixin {
        +log(message: str) void
        +log_warning(message: str) void
        +log_error(message: str) void
    }

    class Player {
        +x: float
        +y: float
        +hp: int
        +energy: int
        +move(dx: float, dy: float) void
        +draw() str
        +collision_radius: float
        +collides_with(other: Any) bool
        +update(dt: float) void
        +rest() void
        +take_damage(amount: int) void
    }

    class Monster {
        +x: float
        +y: float
        +hp: int
        +move(dx: float, dy: float) void
        +draw() str
        +collision_radius: float
        +collides_with(other: Any) bool
        +update(dt: float) void
        +take_damage(amount: int) void
    }

    class Chest {
        +x: float
        +y: float
        +is_opened: bool
        +draw() str
        +collision_radius: float
        +collides_with(other: Any) bool
        +update(dt: float) void
        +open() ItemData
    }

    class Trap {
        +x: float
        +y: float
        +is_triggered: bool
        +draw() str
        +collision_radius: float
        +collides_with(other: Any) bool
        +update(dt: float) void
        +trigger(target: Any) void
    }

    GameObject <|-- Player
    GameObject <|-- Monster
    GameObject <|-- Chest
    GameObject <|-- Trap

    LoggingMixin <|-- Player
    LoggingMixin <|-- Monster
    LoggingMixin <|-- Chest
    LoggingMixin <|-- Trap

    Player ..|> Movable
    Player ..|> Drawable
    Player ..|> Collidable

    Monster ..|> Movable
    Monster ..|> Drawable
    Monster ..|> Collidable

    Chest ..|> Drawable
    Chest ..|> Collidable

    Trap ..|> Drawable
    Trap ..|> Collidable