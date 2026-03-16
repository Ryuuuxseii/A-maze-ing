import random
from typing import Optional, Any


class MazeGenerator:
    """
    A class that handles the generation, validation, and visual conversion
    of a randomized DFS maze.
    """

    # Wall bit masks--------------
    N, E, S, W = 1, 2, 4, 8

    DX = {E: 1, W: -1, N: 0, S: 0}
    DY = {E: 0, W: 0, N: -1, S: 1}

    OPP = {E: W, W: E, N: S, S: N}
    # ---------------------------

    def __init__(self, config: dict[str, Any]):
        """
        Initializes the generator with a given configuration dictionary.
        """
        self.config = config

    def validate(self) -> None:
        """
        Validates the maze configuration settings.
        Checks for logical errors in dimensions, entry/exit bounds,
        and overlaps
        with the '42' center pattern.
        """
        try:
            m_width = int(self.config['WIDTH'])
            m_height = int(self.config['HEIGHT'])
            if m_width < 0 or m_height < 0:
                raise ValueError("HEIGHT and WIDTH can't be negative >:()")
        except (ValueError, KeyError):
            raise ValueError("Configuration must be a valid value!!")

        try:
            entry = self.config['ENTRY']
            if isinstance(entry, str):
                x_entry, y_entry = map(int, entry.split(","))
            else:
                x_entry, y_entry = entry

            ex = self.config['EXIT']
            if isinstance(ex, str):
                x_exit, y_exit = map(int, ex.split(","))
            else:
                x_exit, y_exit = ex
        except (ValueError, KeyError):
            raise ValueError("ENTRY/EXIT are absurd!")

        # Coordinates validation
        if not (0 <= x_entry < m_width) or not (0 <= y_entry < m_height):
            raise ValueError("The entry is out of bounds!")
        if not (0 <= x_exit < m_width) or not (0 <= y_exit < m_height):
            raise ValueError("The exit is out of bounds!")
        elif (x_entry, y_entry) == (x_exit, y_exit):
            raise ValueError(
                "x and y entry cannot be the same as x_exit and y_exit."
                )

        # Check if entry or exit overlaps with the 42 pattern
        if m_width >= 12 and m_height >= 8:
            cx, cy = m_width // 2, m_height // 2
            forty_two = [
                # The '4'
                (cx-3, cy-2), (cx-1, cy-2),
                (cx-3, cy-1), (cx-1, cy-1),
                (cx-3, cy),   (cx-2, cy),   (cx-1, cy),
                                            (cx-1, cy+1),
                                            (cx-1, cy+2),
                # The '2'
                (cx+1, cy-2), (cx+2, cy-2), (cx+3, cy-2),
                                            (cx+3, cy-1),
                (cx+1, cy),   (cx+2, cy),   (cx+3, cy),
                (cx+1, cy+1),
                (cx+1, cy+2), (cx+2, cy+2), (cx+3, cy+2)
            ]
            if (x_entry, y_entry) in forty_two:
                raise ValueError(
                    "Entry position cannot overlap with the center pattern 42."
                    )
            if (x_exit, y_exit) in forty_two:
                raise ValueError(
                    "Exit position cannot overlap with the center pattern 42."
                    )

    def _dfs(
        self,
        blocked: Optional[list[tuple[int, int]]] = None
    ) -> list[list[int]]:
        """
        Internal method: Generates the logical maze using Depth First Search.
        """
        w, h = self.config['WIDTH'], self.config['HEIGHT']
        maze = [[15 for _ in range(w)] for _ in range(h)]
        visited = [[False for _ in range(w)] for _ in range(h)]

        if blocked:  # another layer of protection of the 42
            for bx, by in blocked:
                maze[by][bx] = 15
                visited[by][bx] = True

        sx, sy = 0, 0
        stack = [(sx, sy)]
        visited[sy][sx] = True

        while stack:
            x, y = stack[-1]
            dirs = [self.E, self.N, self.W, self.S]
            random.shuffle(dirs)

            moved = False
            for d in dirs:
                nx = x + self.DX[d]
                ny = y + self.DY[d]

                if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                    maze[y][x] ^= d
                    maze[ny][nx] ^= self.OPP[d]
                    visited[ny][nx] = True
                    stack.append((nx, ny))
                    moved = True
                    break

            if not moved:
                stack.pop()

        return maze

    def _convert(self, maze: list[list[int]]) -> list[list[int]]:
        """
        Internal method: Converts the logical maze into a visual grid map.
        """
        w, h = self.config['WIDTH'], self.config['HEIGHT']
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

                if not (cell & self.E):
                    maze_conv[gy][gx + 1] = 0
                if not (cell & self.W):
                    maze_conv[gy][gx - 1] = 0
                if not (cell & self.N):
                    maze_conv[gy - 1][gx] = 0
                if not (cell & self.S):
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

        return maze_conv

    def generate(self) -> tuple[list[list[int]], list[list[int]]]:
        """
        Main controller for generating and returning the maze.
        Handles seed initialization, blocking the '42', DFS, and conversion.
        """
        width = self.config['WIDTH']
        height = self.config['HEIGHT']

        seed = self.config.get("SEED")
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()

        entry = self.config['ENTRY']
        if isinstance(entry, str):
            start_pos = tuple(map(int, entry.split(",")))
        else:
            start_pos = entry

        ex = self.config['EXIT']
        if isinstance(ex, str):
            end_pos = tuple(map(int, ex.split(",")))
        else:
            end_pos = ex

        if start_pos == end_pos:
            end_pos = (width - 1, height - 1)

        blocked = []
        if width >= 12 and height >= 8:
            cx, cy = width // 2, height // 2
            blocked = [
                (cx-3, cy-2), (cx-1, cy-2),
                (cx-3, cy-1), (cx-1, cy-1),
                (cx-3, cy),   (cx-2, cy),   (cx-1, cy),
                                            (cx-1, cy+1),
                                            (cx-1, cy+2),
                (cx+1, cy-2), (cx+2, cy-2), (cx+3, cy-2),
                                            (cx+3, cy-1),
                (cx+1, cy),   (cx+2, cy),   (cx+3, cy),
                (cx+1, cy+1),
                (cx+1, cy+2), (cx+2, cy+2), (cx+3, cy+2)
            ]

        maze = self._dfs(blocked)
        cnv_maze = self._convert(maze)

        sx = (start_pos[0] * 2) + 1
        sy = (start_pos[1] * 2) + 1
        ex = (end_pos[0] * 2) + 1
        ey = (end_pos[1] * 2) + 1

        if 0 <= sy < len(cnv_maze) and 0 <= sx < len(cnv_maze[0]):
            cnv_maze[sy][sx] = 2

        if 0 <= ey < len(cnv_maze) and 0 <= ex < len(cnv_maze[0]):
            cnv_maze[ey][ex] = 3

        return cnv_maze, maze
