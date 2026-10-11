import math
from core.config import GameConfig, MonsterConfig, PlayerConfig
from entities.environment import Chest, Trap
from entities.monsters import Monster
from entities.player import Player


def choose_difficulty() -> tuple[GameConfig, PlayerConfig, MonsterConfig]:
    print("=" * 44)
    print("        Dungeon Rogue: Depths of OOP")
    print("=" * 44)
    print("Выберите уровень сложности:")
    print("1 — Легкий   (много энергии и HP, слабые враги)")
    print("2 — Обычный  (сбалансированные параметры)")
    print("3 — Хардкор  (жесткий таймер, опасные ловушки)")

    choice = input("Ваш выбор (1-3, Enter для 2): ").strip()

    if choice == "1":
        game_cfg = GameConfig(
            field_width=20,
            field_height=8,
            max_turns=150,
            step_energy_cost=1,
            trap_damage=5,
        )
        player_cfg = PlayerConfig(
            name="Паладин",
            max_hp=150,
            max_energy=40,
            base_attack=18,
        )
        monster_cfg = MonsterConfig(
            name="Слабый гоблин",
            max_hp=25,
            attack_power=5,
            aggro_radius=3.0,
        )
    elif choice == "3":
        game_cfg = GameConfig(
            field_width=20,
            field_height=8,
            max_turns=40,
            step_energy_cost=2,
            trap_damage=25,
        )
        player_cfg = PlayerConfig(
            name="Бродяга",
            max_hp=60,
            max_energy=15,
            base_attack=10,
        )
        monster_cfg = MonsterConfig(
            name="Орк-берсерк",
            max_hp=50,
            attack_power=14,
            aggro_radius=5.0,
        )
    else:
        game_cfg = GameConfig(field_width=20, field_height=8)
        player_cfg = PlayerConfig()
        monster_cfg = MonsterConfig()

    return game_cfg, player_cfg, monster_cfg


def render_map(
    player: Player,
    monsters: list[Monster],
    chests: list[Chest],
    traps: list[Trap],
    width: int,
    height: int,
) -> None:
    grid = [["." for _ in range(width)] for _ in range(height)]

    for trap in traps:
        tx, ty = int(trap.x), int(trap.y)
        if 0 <= tx < width and 0 <= ty < height:
            grid[ty][tx] = trap.draw()

    for chest in chests:
        cx, cy = int(chest.x), int(chest.y)
        if 0 <= cx < width and 0 <= cy < height:
            grid[cy][cx] = "C" if not chest.is_opened else "_"

    for mon in monsters:
        if mon.active:
            mx, my = int(mon.x), int(mon.y)
            if 0 <= mx < width and 0 <= my < height:
                grid[my][mx] = mon.draw()

    px, py = int(player.x), int(player.y)
    if 0 <= px < width and 0 <= py < height:
        grid[py][px] = player.draw()

    print("+" + "-" * width + "+")
    for row in grid:
        print("|" + "".join(row) + "|")
    print("+" + "-" * width + "+")

    print("Легенда: [@] Игрок  [M] Монстр  [C] Сундук  [^] Ловушка  [.] Пол")


def run_game() -> None:
    game_cfg, player_cfg, monster_cfg = choose_difficulty()

    player = Player(
        x=1.0,
        y=1.0,
        config=player_cfg,
        game_config=game_cfg,
    )

    monsters = [
        Monster(x=12.0, y=4.0, config=monster_cfg),
        Monster(x=16.0, y=6.0, config=monster_cfg),
    ]

    chests = [
        Chest(x=6.0, y=2.0),
        Chest(x=17.0, y=2.0),
    ]

    traps = [
        Trap(x=4.0, y=1.0, game_config=game_cfg),
        Trap(x=9.0, y=4.0, game_config=game_cfg),
    ]

    turn = 1
    move_map = {
        "w": (0, -1),
        "s": (0, 1),
        "a": (-1, 0),
        "d": (1, 0),
    }

    print("\nУправление: w/a/s/d — шаг, r — отдых (+энергия), q — выход")

    while turn <= game_cfg.max_turns and player.active:
        print(f"\n--- Ход {turn}/{game_cfg.max_turns} ---")
        print(
            f"Герой: {player.name} | HP: {player.hp}/{player_cfg.max_hp} | "
            f"Энергия: {player.energy}/{player_cfg.max_energy}"
        )

        render_map(
            player,
            monsters,
            chests,
            traps,
            game_cfg.field_width,
            game_cfg.field_height,
        )

        cmd = input("Действие (w/a/s/d/r/q): ").strip().lower()

        if cmd == "q":
            print("Вы завершили игру.")
            break

        if cmd in move_map:
            dx, dy = move_map[cmd]
            nx, ny = player.x + dx, player.y + dy
            if 0 <= nx < game_cfg.field_width and (
                0 <= ny < game_cfg.field_height
            ):
                player.move(dx, dy)
            else:
                player.log_warning("Путь прегражден стеной комнаты!")
        elif cmd == "r":
            player.rest()
        else:
            print("Неверный ввод! Используйте w, a, s, d, r или q.")
            continue

        for trap in traps:
            if not trap.is_triggered and player.collides_with(trap):
                trap.trigger(player)

        for chest in chests:
            if not chest.is_opened and player.collides_with(chest):
                chest.open()

        for mon in monsters:
            if not mon.active:
                continue

            dist = math.hypot(player.x - mon.x, player.y - mon.y)

            if player.collides_with(mon):
                mon.log(
                    f"{mon.name} наносит {monster_cfg.attack_power} урона!"
                )
                player.take_damage(monster_cfg.attack_power)
            elif dist <= monster_cfg.aggro_radius:
                step_x = 1 if player.x > mon.x else (
                    -1 if player.x < mon.x else 0
                )
                step_y = 1 if player.y > mon.y else (
                    -1 if player.y < mon.y else 0
                )
                mon.move(step_x, step_y)

        turn += 1

    if not player.active:
        print("\n=== ВЫ ПОГИБЛИ! Игра окончена. ===")
    elif turn > game_cfg.max_turns:
        print("\n=== ВРЕМЯ ИСТЕКЛО! Подземелье обрушилось. ===")


if __name__ == "__main__":
    run_game()
