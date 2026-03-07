import random

# Wall bit masks -------------
E, N, W, S = 1, 2, 4, 8

DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}

OPP = {E: W, W: E, N: S, S: N}
# ----------------------------


def generate_maze(w, h):
    maze = [[15 for _ in range(w)] for _ in range(h)]
    visited = [[False for _ in range(w)] for _ in range(h)]

    stack = [(0, 0)]
    visited[0][0] = True

    while stack:
        x, y = stack[-1]  # starting point
        dirs = [E, N, W, S]
        random.shuffle(dirs)

        moved = False
        for d in dirs:
            nx = x + DX[d]
            ny = y + DY[d]

            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                maze[y][x] ^= d
                maze[ny][nx] ^= OPP[d]
                visited[ny][nx] = True
                stack.append((nx, ny))
                moved = True
                break  # we move to the first unvisited neighbor

        if not moved:
            stack.pop()  # its a dead end, so we gots to backtrack :p

    return maze


def converter(maze, width, height):

    grid_w = 2 * width + 1   # we basically are putting a wall in
    grid_h = 2 * height + 1  # a [WALL] [CELL] [WALL] pattern, + 1 for outters

    # beginning: we assume all is wall
    maze_conv = [[1 for _ in range(grid_w)] for _ in range(grid_h)]

    for y in range(height):
        for x in range(width):

            cell = maze[y][x]

            gx = 2 * x + 1
            gy = 2 * y + 1

            # cell center is always a path
            maze_conv[gy][gx] = 0

            # if there is no wall, open the space
            if not (cell & E):
                maze_conv[gy][gx + 1] = 0

            if not (cell & W):
                maze_conv[gy][gx - 1] = 0

            if not (cell & N):
                maze_conv[gy - 1][gx] = 0

            if not (cell & S):
                maze_conv[gy + 1][gx] = 0

    return maze_conv


def maze_gen_main():

    maze = generate_maze(15, 15)


maze_gen_main()
