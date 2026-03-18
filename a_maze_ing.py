import mazegen.generator as gen
import mazeparse.parser as parse
import random
from typing import Iterator, Any
import os
import time
import sys

# Wall bit masks -------------
N, E, S, W = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPP = {E: W, W: E, N: S, S: N}
# ----------------------------


def imperfect_maze(
                cnv_maze: list[list[int]],
                logic_maze: list[list[int]]
                ) -> None:
    """
    Randomly breaks walls to turn the maze into an imperfect one.

    The function scans the canvas maze for walls separating two cells that are
    not part of the solution path. A percentage of those walls are randomly
    removed to create alternative routes while preserving the original
    shortest solution.
    """
    chance = 0.3
    h = len(cnv_maze)
    w = len(cnv_maze[0])

    breakable = []

    for y in range(1, h - 1):
        for x in range(1, w - 1):

            if cnv_maze[y][x] != 1:
                continue

            if y % 2 == 1 and x % 2 == 0:  # vertical wall

                cx = (x // 2) - 1
                cy = (y - 1) // 2

                cell1 = (cx, cy)
                cell2 = (cx + 1, cy)
                wall_type = "vertical"

            elif y % 2 == 0 and x % 2 == 1:  # horizontal wall

                cx = (x - 1) // 2
                cy = (y // 2) - 1

                cell1 = (cx, cy)
                cell2 = (cx, cy + 1)
                wall_type = "horizontal"

            else:
                continue

            breakable.append((x, y, wall_type, cell1, cell2))

    walls_to_break = int(len(breakable) * chance)

    for x, y, wall_type, cell1, cell2 in random.sample(
            breakable, walls_to_break):
        cnv_maze[y][x] = 0
        if wall_type == "vertical":
            logic_maze[cell1[1]][cell1[0]] &= ~E
            logic_maze[cell2[1]][cell2[0]] &= ~W
        elif wall_type == "horizontal":
            logic_maze[cell1[1]][cell1[0]] &= ~S
            logic_maze[cell2[1]][cell2[0]] &= ~N


def solution_marker(
                maze: list[list[int]],
                path: list[tuple[int, int]]
            ) -> Iterator[list[list[int]]]:
    """
    Animates and marks the solution path on the canvas maze.

    Each step of the path is temporarily marked and yielded to allow animated
    visualization of the solving process. After the animation, the path is
    permanently marked except for entry and exit cells.
    """
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
    """
    Converts the path into movement directions and writes them to a file.

    Each consecutive pair of coordinates is translated into one of the
    four cardinal directions (N, S, E, W).
    """

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
        file.write("\n")


def convert(
            config: dict[str, Any],
            maze: list[list[int]]
            ) -> tuple[list[list[int]], list[list[int]]]:
    """
    Internal method: Converts the logical maze into a visual grid map.
    """
    w, h = config['WIDTH'], config['HEIGHT']
    grid_w = 2 * w + 1
    grid_h = 2 * h + 1

    maze_conv = [[1 for _ in range(grid_w)] for _ in range(grid_h)]

    for y in range(h):
        for x in range(w):
            cell = maze[y][x]
            gx = 2 * x + 1
            gy = 2 * y + 1

            # cell center is always a path
            maze_conv[gy][gx] = 0

            if not (cell & E):
                maze_conv[gy][gx + 1] = 0
            if not (cell & W):
                maze_conv[gy][gx - 1] = 0
            if not (cell & N):
                maze_conv[gy - 1][gx] = 0
            if not (cell & S):
                maze_conv[gy + 1][gx] = 0

    for y in range(h):
        for x in range(w):
            if maze[y][x] == 15:
                gx = 2 * x + 1
                gy = 2 * y + 1

                # Fill the entire 3x3 expanded block with '4'
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        maze_conv[gy + dy][gx + dx] = 4

                maze_conv[gy][gx] = 5

    entry = config['ENTRY']
    exit_ = config['EXIT']

    # MARKING ENTRY
    ex, ey = entry
    gx, gy = 2 * ex + 1, 2 * ey + 1
    maze_conv[gy][gx] = 2

    # MARKING EXIT
    ex, ey = exit_
    gx, gy = 2 * ex + 1, 2 * ey + 1
    maze_conv[gy][gx] = 3

    return maze_conv, maze


def dmaze_display(maze: list[list[int]], r: int) -> None:
    """
    Displays the maze in the terminal using ASCII graphics.

    Different cell values correspond to walls, paths, entry, exit, and
    other visual elements. The color/theme of the maze depends on the
    randomly selected index.
    """

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
        maze_gen = gen.MazeGenerator(config)
        maze_gen.validate()
    except (ValueError, FileNotFoundError, KeyError, Exception) as e:
        print("Error: ", e)
        return

    os.system("clear")

    maze = maze_gen.generate()
    cnv_maze, maze = convert(config, maze)

    r = random.randint(0, 3)
    path = maze_gen.bfs(maze, config)

    if config['PERFECT'] is False:
        imperfect_maze(cnv_maze, maze)
        path = maze_gen.bfs(maze, config)

    copy = [row[:] for row in cnv_maze]

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

            width = int(config["WIDTH"])
            height = int(config["HEIGHT"])

            if (height < 8 or width < 10):
                print("\033[1m\nERROR: maze dimensions too small to fit"
                      " 42 pattern!\n")

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

                maze = maze_gen.generate()
                cnv_maze, maze = convert(config, maze)
                path = maze_gen.bfs(maze, config)

                if config['PERFECT'] is False:
                    imperfect_maze(cnv_maze, maze)
                    path = maze_gen.bfs(maze, config)

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
