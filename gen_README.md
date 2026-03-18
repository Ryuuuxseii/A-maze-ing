# Maze Generator & Solver

A Python-based maze generator built using classic graph traversal algorithms.  
This project focuses on generating clean, fully connected mazes and solving them efficiently.

---

## Overview

This package provides:

- **Maze Generation** using Depth-First Search (DFS)
- **Maze Solving** using Breadth-First Search (BFS)
- Configuration validation
- Optional deterministic generation via seeding
- Custom entry/exit handling
- A protected center pattern ("42")

---

## Maze Representation

The maze is stored as a 2D grid of integers using **bitmasking** to represent walls.

Each cell contains up to four walls:

| Direction | Bit |
|----------|-----|
| North    | 1   |
| East     | 2   |
| South    | 4   |
| West     | 8   |

### Example

A cell value of `15` means all walls are present:

```
1 (N) + 2 (E) + 4 (S) + 8 (W) = 15
```

Walls are removed using XOR operations during generation.

---

## Maze Generation Algorithm

### Depth-First Search (DFS)

Maze generation is implemented using a randomized DFS (recursive backtracking via a stack).

### Steps

1. Start from an initial cell (default: `(0, 0)`)
2. Mark it as visited
3. Randomly shuffle directions
4. For each direction:
   - If the neighbor is unvisited:
     - Remove the wall between current and neighbor
     - Move to neighbor
5. If no moves are possible:
   - Backtrack using the stack
6. Repeat until all cells are visited

### Properties

- **Perfect Maze**
  - Every cell is reachable
  - Exactly one path between any two cells

- **Organic Structure**
  - Long corridors
  - Fewer dead-end clusters

- **Efficient**
  - Time complexity: `O(width × height)`

---

## Maze Solving Algorithm

### Breadth-First Search (BFS)

The solver uses BFS to guarantee the **shortest path** from entry to exit.

### Steps

1. Start from the entry point
2. Explore neighbors layer by layer
3. Track visited cells
4. Store the path taken
5. Stop when exit is reached
6. Return the reconstructed shortest path

### Properties

- Always finds the **optimal path**
- Works perfectly on unweighted grids
- Deterministic and reliable

---

## Configuration

The generator is controlled via a configuration dictionary:

```python
config = {
    "WIDTH": int,
    "HEIGHT": int,
    "ENTRY": (x, y) or "x,y",
    "EXIT": (x, y) or "x,y",
    "SEED": optional int
}
```

### Validation

The generator ensures:

- Width and height are valid
- Entry and exit are within bounds
- Entry and exit are not the same
- Entry/exit do not overlap restricted areas

---

## Special Feature: "42" Pattern

For sufficiently large mazes, a **blocked center pattern shaped like "42"** is embedded.

### Characteristics

- Cells forming "42" are marked as **visited and inaccessible**
- The maze generates around this structure
- Entry and exit cannot overlap this region

This adds a unique visual and structural element to the maze.

---

## Key Methods

### `validate()`
Validates configuration and constraints.

### `_dfs(blocked=None)`
Internal method that generates the maze using DFS.

### `bfs(maze, config)`
Finds the shortest path from entry to exit.

### `generate()`
Main method:
- Applies seed
- Builds blocked pattern
- Runs DFS
- Returns the maze grid

---

## Example Usage

```python
from maze_generator import MazeGenerator

config = {
    "WIDTH": 20,
    "HEIGHT": 10,
    "ENTRY": (0, 0),
    "EXIT": (19, 9),
    "SEED": 42
}

gen = MazeGenerator(config)
gen.validate()

maze = gen.generate()

path = gen.bfs(maze, config)
```
## Summary

- DFS creates the maze → **structure**
- BFS solves the maze → **optimal path**

---