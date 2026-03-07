import random

# wall bit masks
E, N, W, S = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPP = {E: W, W: E, N: S, S: N}


# ======================
# DFS MAZE GENERATOR
# ======================

def generate_maze(w, h):

    # 15 is the default for all cells.
    maze = [[15 for _ in range(w)] for _ in range(h)]
    visited = [[False for _ in range(w)] for _ in range(h)]

    def dfs(x, y):

        visited[y][x] = True

        # randomize directions so maze is random
        dirs = [E, N, W, S]
        random.shuffle(dirs)

        for d in dirs:

            nx = x + DX[d]
            ny = y + DY[d]

            # visit unvisited neighbor
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:

                # remove wall between cells
                maze[y][x] ^= d
                maze[ny][nx] ^= OPP[d]

                dfs(nx, ny)

    dfs(0, 0)

    return maze


# ======================
# CONVERT CELL MAZE
# INTO ASCII GRID
# ======================

def convert(maze, w, h):

    grid_w = 2 * w + 1
    grid_h = 2 * h + 1

    # start with everything as walls
    maze_conv = [[1 for _ in range(grid_w)] for _ in range(grid_h)]

    for y in range(h):
        for x in range(w):

            cell = maze[y][x]

            gx = 2 * x + 1
            gy = 2 * y + 1

            # cell center is always a path
            maze_conv[gy][gx] = 0

            # if wall is removed, open the tile between cells
            if not (cell & E):
                maze_conv[gy][gx + 1] = 0

            if not (cell & W):
                maze_conv[gy][gx - 1] = 0

            if not (cell & N):
                maze_conv[gy - 1][gx] = 0

            if not (cell & S):
                maze_conv[gy + 1][gx] = 0

    return maze_conv


# ======================
# DISPLAY MAZE
# ======================

def display_maze(maze):

    WALL = f"\033[38;5;{random.randint(1,256)};48;5;16m██\033[0m"
    PATH = "  "

    for row in maze:
        for cell in row:

            if cell == 0:
                print(PATH, end="")

            elif cell == 1:
                print(WALL, end="")

            elif cell == 2:
                print("██", end="")  # start

            elif cell == 3:
                print("\033[36m██\033[0m", end="")  # exit

        print()


# ======================
# CONFIG READER
# ======================              

def load_config():

    width = 10
    height = 10
    start_pos = [0, 0]
    end_pos = [0, 0]

    with open("config.txt", "r") as file:

        lines = file.read().splitlines()

        for line in lines:

            if "=" not in line:
                continue

            key, value = line.split("=")
            key = key.strip()
            value = value.strip()

            if key == "WIDTH":
                width = int(value)

            elif key == "HEIGHT":
                height = int(value)

            elif key == "ENTRY":
                x, y = value.split(",")
                start_pos = [int(x), int(y)]

            elif key == "EXIT":
                x, y = value.split(",")
                end_pos = [int(x), int(y)]

    return width, height, start_pos, end_pos


# ======================
# MAIN
# ======================
def main():

    width, height, start_pos, end_pos = load_config()

    # prevent start and exit being identical
    if start_pos == end_pos:
        end_pos = [width - 1, height - 1]

    maze = generate_maze(width, height)

    new_maze = convert(maze, width, height)

    # convert cell coordinates → ascii grid coordinates
    sx = (start_pos[0] * 2) + 1
    sy = (start_pos[1] * 2) + 1

    ex = (end_pos[0] * 2) + 1
    ey = (end_pos[1] * 2) + 1

    # mark start
    if 0 <= sy < len(new_maze) and 0 <= sx < len(new_maze[0]):
        new_maze[sy][sx] = 2

    # mark exit
    if 0 <= ey < len(new_maze) and 0 <= ex < len(new_maze[0]):
        new_maze[ey][ex] = 3

    display_maze(new_maze)

    print()
    print("=" * width * 2 * 2, end="")
    print("==")
    print(f"width: {width}")
    print(f"height: {height}")
    print(f"start: {start_pos}")
    print(f"exit: {end_pos}")


if __name__ == "__main__":
    main()
