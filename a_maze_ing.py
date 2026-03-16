import mazegen.generator as gen
import mazeparse.parser as parse
import random
from typing import Iterator, Any
import os
import time
import collections as col
import sys

# Wall bit masks -------------
N, E, S, W = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPP = {E: W, W: E, N: S, S: N}
# ----------------------------


def imperfect_maze(
                maze: list[list[int]],
                path: list[tuple[int, int]],
                ) -> None:

    chance = 0.3
    h = len(maze)
    w = len(maze[0])

    path_set = set(path)
    breakable = []

    for y in range(1, h - 1):
        for x in range(1, w - 1):

            if maze[y][x] != 1:
                continue

            if y % 2 == 1 and x % 2 == 0:  # vertical wall

                cx = (x // 2) - 1
                cy = (y - 1) // 2

                cell1 = (cx, cy)
                cell2 = (cx + 1, cy)

            elif y % 2 == 0 and x % 2 == 1:  # horizontal wall

                cx = (x - 1) // 2
                cy = (y // 2) - 1

                cell1 = (cx, cy)
                cell2 = (cx, cy + 1)

            else:
                continue

            if cell1 in path_set or cell2 in path_set:
                continue

            breakable.append((x, y))

    walls_to_break = int(len(breakable) * chance)

    for x, y in random.sample(breakable, walls_to_break):
        maze[y][x] = 0


def bfs(maze: list[list[int]], s: dict[str, Any]) -> list[tuple[int, int]]:

    entry = s['ENTRY']
    if isinstance(entry, str):
        x, y = map(int, entry.split(','))
        start: tuple[int, int] = (x, y)
    else:
        start = entry

    ex = s['EXIT']
    if isinstance(ex, str):
        x, y = map(int, ex.split(','))
        goal: tuple[int, int] = (x, y)
    else:
        goal = ex

    width = int(s['WIDTH'])
    height = int(s['HEIGHT'])

    queue = col.deque([(start[0], start[1], [start])])
    visited = {start}

    while queue:
        x, y, path = queue.popleft()

        if (x, y) == goal:
            return path

        for direction in [S, W, N, E]:

            # if there is no wall
            if (maze[y][x] & direction) == 0:

                nx = x + DX[direction]
                ny = y + DY[direction]

                if (0 <= nx < width and 0 <= ny < height and (nx, ny)
                   not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(nx, ny)]))

    return []


def solution_marker(
                maze: list[list[int]],
                path: list[tuple[int, int]]
            ) -> Iterator[list[list[int]]]:

    for x, y in path:
        gx = 2 * x + 1
        gy = 2 * y + 1
        temp = maze[gy][gx]

        maze[gy][gx] = 6
        yield maze
        maze[gy][gx] = temp

    # permanent path
    for x, y in path:
        gx = 2 * x + 1
        gy = 2 * y + 1
        if maze[gy][gx] != 2 and maze[gy][gx] != 3:
            maze[gy][gx] = 6


def get_directions(
                path: list[tuple[int, int]],
                config: dict[str, Any]
            ) -> None:

    index = 0
    path_len = len(path)
    with open(config['OUTPUT_FILE'], "a") as file:
        while (index < path_len - 1):
            x, y = path[index]
            nx, ny = path[index + 1]

            dx = nx - x
            dy = ny - y
            # translator
            if dx == 1:
                file.write("E")
            elif dx == -1:
                file.write("W")
            elif dy == 1:
                file.write("S")
            elif dy == -1:
                file.write("N")
            index += 1


def dmaze_display(maze: list[list[int]], r: int) -> None:

    WALL = ["🟥", "🟦", "🟩", "🟪"]
    ENTRIES = ["🚑", "🐱", "🦋", "🐒"]
    EXISTS = ["𐀪 ", "🐭", "🌷", "🍌"]
    PATH = "  "
    THUMBNAIL = "⬜"

    for row in maze:
        for cell in row:
            if cell == 0:
                print(PATH, end="")
            elif cell == 1:
                print(WALL[r], end="")
            elif cell == 2:
                print(ENTRIES[r], end="")  # start
            elif cell == 3:
                print(EXISTS[r], end="")  # exit
            elif cell == 4:
                print(THUMBNAIL, end="")
            elif cell == 5:
                print(WALL[r], end="")
            elif cell == 6:
                print(ENTRIES[r], end="")
        print()


def main() -> None:
    try:
        filename = sys.argv[1]
        config = parse.config_parser(filename)
        # Initialize the generator object and validate
        maze_gen = gen.MazeGenerator(config)
        maze_gen.validate()
    except (ValueError, FileNotFoundError, KeyError, Exception) as e:
        print("Error: ", e)
        return
    os.system("clear")
    # Generate the maze using the object
    cnv_maze, maze = maze_gen.generate()
    copy = [row[:] for row in cnv_maze]
    r = random.randint(0, 3)
    path = bfs(maze, config)

    if config['PERFECT'] is False:
        imperfect_maze(cnv_maze, path)

    solution_marker(cnv_maze, path)

    running = True
    sol_shown = False
    dmaze_display(cnv_maze, r)

    while running:

        try:
            output_file = config['OUTPUT_FILE']
            with open(output_file, "w") as file:
                for row in maze:
                    for numbers in row:
                        file.write(hex(numbers)[2:].upper())
                    file.write('\n')
                entry = config['ENTRY']
                ex = config['EXIT']
                file.write(f"\n{entry[0]},{entry[1]}\n")
                file.write(f"{ex[0]},{ex[1]}\n")
            get_directions(path, config)
            print("\033[1m\n── ⋆⋅𖤓⋅⋆ ── A-Maze-Ing ── ⋆⋅𖤓⋅⋆ ──")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                if "SEED" in config:
                    del config["SEED"]
                sol_shown = False
                os.system("clear")
                # Re-generate the maze when user presses "1"
                cnv_maze, maze = maze_gen.generate()
                path = bfs(maze, config)
                if config['PERFECT'] is False:
                    imperfect_maze(cnv_maze, path)
                copy = [row[:] for row in cnv_maze]

                dmaze_display(cnv_maze, r)
                with open(output_file, "w") as file:
                    for row in maze:
                        for numbers in row:
                            file.write(hex(numbers)[2:].upper())
                        file.write('\n')
                    entry = config['ENTRY']
                    ex = config['EXIT']
                    file.write(f"\n{entry[0]},{entry[1]}\n")
                    file.write(f"{ex[0]},{ex[1]}\n")
                get_directions(path, config)
            elif choice == "2":
                if not sol_shown:
                    for m in solution_marker(cnv_maze, path):
                        os.system("clear")
                        dmaze_display(m, r)
                        time.sleep(0.09)

                    os.system("clear")
                    dmaze_display(cnv_maze, r)

                else:
                    dmaze_display(cnv_maze, r)
                    cnv_maze = [row[:] for row in copy]
                    os.system("clear")
                    dmaze_display(cnv_maze, r)

                sol_shown = not sol_shown

            elif choice == "3":
                os.system("clear")
                choices = [0, 1, 2, 3]
                choices.remove(r)
                r = random.choice(choices)
                dmaze_display(cnv_maze, r)

            elif choice == "4":
                running = False

            else:
                os.system("clear")
                print("Invalid choice. Please try again.")

        except (KeyboardInterrupt, EOFError):
            running = False


if __name__ == "__main__":
    main()
