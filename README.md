this team project was made a part of the 42 curriculum.

# <u>DESCRIPTION: </u>


A-Maze-Ing is an interactive terminal-based maze generator and solver built in Python. The goal of the project is to procedurally generate mazes of configurable size, solve them automatically, and let players navigate them manually, all rendered directly in the terminal using the curses library!

The project is structured around a reusable mazegen package that encapsulates:

- Maze generation using two distinct algorithms: Depth-First Search (DFS).
- Maze solving using Breadth-First Search (BFS), which guarantees the shortest path.
- Real-time visualization of both generation and solving steps, rendered cell-by-cell in the terminal.
- Theming system with multiple visual styles switchable at runtime.
- Config-driven setup: maze dimensions, entry/exit points, algorithm, seed, and output file are all defined in a plain-text config file.
- Mazes can be saved to a text file in a compact hexadecimal grid format, along with the seed, entry/exit coordinates, and solution string!

---
# <u> INSTRUCTIONS: </u>

## Running the Project

The project is meant to be used through a **Makefile**. Instead of running several commands manually, everything you'll need is wrapped into simple make targets. This keeps the workflow clean and avoids remembering long commands every time you want to run the maze.

### Tools

- The following tools are required to run and manage A-Maze-Ing:

-Python 3.10+ – The core language used for the project.

- Make – Used to run commands like make run, make install, and make clean.

- mypy – Checks type annotations to ensure code correctness.

- flake8 – Ensures consistent Python code style and formatting.

- All Python dependencies and linting tools can be installed automatically with:

```bash
    make install
```
This installs everything needed for the program to run correctly, like the libraries used for terminal rendering and the tools used for linting and type checking.

### Run the program

Once everything is installed, you can start the maze with:

```bash
    make run
```
When you run the maze, you have several interactive options available directly in the terminal. These make exploring and customizing your experience quick and intuitive:

**Regenerate Maze (1):**

- Press 1 to regenerate the maze.

- This will create a brand new layout, overriding the current seed if one is set. Perfect for exploring different maze structures quickly.

**Show / Hide Solution (2):**

- Press 2 to toggle the solution path.

- You can hide the solution for a challenge or reveal it to check the shortest path through the maze.

**Change Colors (3):**

- Press 3 to switch between different color themes.

- Each theme changes how walls, paths, and the solution are displayed in the terminal, giving the maze a fresh look.

**Exit (4):**

- Press 4 to exit the program at any time.

- Cleanly closes the terminal interface without leaving artifacts behind.

- These options make A-Maze-Ing highly interactive, allowing you to experiment, customize, and replay the maze in multiple ways without restarting the program.

- This launches the program and renders the maze directly inside the terminal!

### Check code quality

The **Makefile** also includes linting tools to keep the codebase clean and consistent. To run them:

```bash
    make lint
```

This runs tools such as **mypy** and **flake8**, which check type annotations, formatting issues, and other common problems in Python code.

### Clean the repository

During development Python may generate cache files or temporary artifacts. These can be removed with:

```bash
    make clean
```

This clears Python cache folders and other unnecessary files so the repository stays nice and tidy.

Using the Makefile makes the project much easier to manage. Instead of dealing with multiple setup commands, everything is handled through a few clear targets!

---

# <u> Maze Generation and Solving: </u>

At its core, **A-Maze-Ing** generates a random maze and renders it visually in the terminal using **ASCII characters**. The maze exists internally as a grid structure, which is then translated into a visual format so it can be displayed and explored.

Every run creates a new maze unless a specific seed is provided. The structure of the maze, the entry and exit points, and other settings can all be configured through a configuration file.

The ASCII display was a deliberate choice. It keeps the program lightweight, portable, and perfectly suited for a terminal environment. Initially we thought it would limit creativity when it came to maze customization, as we were only limited to ASCII characters. But despite being text-based, we found so much can be done to give it personality!

---

# <u> Generation Algorithm: </u>

The maze is generated using **Depth-First Search (DFS)**.

DFS works by exploring as far as possible down one path before backtracking and trying another direction, usually using recursion. When used for maze generation, this produces long winding corridors with fewer short branches, which in turn tends to create mazes that feel natural and interesting to navigate.

The algorithm works roughly this way:

- Start from an initial cell
- Randomly select an unvisited neighboring cell
- Carve a path between the current cell and the chosen neighbor
- Continue recursively until no unvisited neighbors remain
- Backtrack when necessary until the entire grid has been visited

### Why DFS

DFS was chosen because it produces **clean, connected mazes** while staying simple to implement. It also performs well even on larger grids and naturally produces structures that feel like classic labyrinths.

Another advantage is that DFS produces **perfect mazes**, meaning every cell is reachable and there is exactly one path between any two cells.

---

# <u> Solving Algorithm: </u>

To solve the maze automatically, the project uses **Breadth-First Search (BFS)**.

Unlike DFS, BFS explores the maze layer by layer outward from the starting position. Because of this, the first time it reaches the exit it is guaranteed to have found the **shortest possible path**.

This makes BFS a natural choice for maze solving where the goal is not just finding a path but finding the optimal one.

---

# <u> Maze Configuration: </u>

The maze behavior is controlled through a simple text configuration file. This allows the maze to be modified without touching the source code.

Example structure of the config file:

width=20  
height=10  
seed=42  
entry=0,0 
exit=19,19
OUTPUT_FILE=maze.txt
perfect=True  

### <u> What each setting does: </u>

- **width / height**

    -Defines the size of the maze grid.

- **seed**

    -The seed allows a maze to be reproduced exactly. If the same seed and dimensions are used, the generated maze will always be identical.

- **entry and exit coordinates**

    -These determine where the maze begins and where the goal is located.

- **perfect flag**

    -When enabled, the maze will contain _only one possible solution_. This removes loops and ensures the maze behaves like a classic perfect maze.

---

# <u> Reusable Maze Generator: </u>

A key design goal of the project was making the **maze generator reusable**. The generation logic lives in its own module inside the `mazegen` package.

This module handles:

- grid creation
- path carving
- algorithm execution
- exporting final maze data

Because the generator is separated from rendering/visual and solution logic, it can easily be reused in other projects that require procedural maze generation.

This means future projects could reuse the generator without needing the terminal interface or solving logic included in A-Maze-Ing.

---

# <u> Planning and Development: </u>

At the beginning the idea was fairly simple: generate a maze, display it, and solve it. As development progressed the structure evolved quite a bit. The project eventually split into multiple modules so that generation, solving, rendering, and configuration handling were clearly separated.

This ended up making the code easier to maintain and helped turn the generator into a reusable component in the end.

### What worked well:

Separating the maze generator from the rest of the program worked really well. It made the algorithm easier to test and made the code more prone to being modular overall.

The ASCII rendering also turned out to be a good choice. Even though it is very simple, it still provides a clear and readable maze inside the terminal.

### What could have been improved:

One thing that would have helped a lot is having a better overview of the tasks earlier in the project. Many parts were approached without fully planning the structure first, which led to extra time spent figuring out how different components should interact together.

With more micro planning at the start, a lot of that trial and error could probably have been avoided.

On the other hand, it really pushed us to think outside the box and find solutions that worked well with everything else that had already been implemented. In the end it turned into a great exercise in problem solving and learning to adapt to its state as the project evolved.


### How to use The MazeGenerator
The `mazegen` package is designed to be standalone. Once installed via pip (using the `.whl` or `.tar.gz` file in the root), you can use it in any Python 3.10+ project:

```python
import mazegen

config = {
    "WIDTH": 30, "HEIGHT": 20, "ENTRY": (0, 0), "EXIT": (29, 19), "PERFECT": True
}
generator = mazegen.MazeGenerator(config)
cnv_maze, logic_maze = generator.generate()
solution = generator.solve()
```

### Specific Tools Used
- **Language:** Python 3.10+
- **Linting:** `flake8` and `mypy`
- **Automation:** `GNU Make`
- **Packaging:** `setuptools` and `build`

### Resources

- [BFS Algorithm Explained](https://www.youtube.com/watch?v=HZ5YTanv5QE) - Used for implementing the shortest path solver.
- [DFS Maze Generation](https://www.youtube.com/watch?v=0O2sq9HlU9c) - Foundation for the procedural generation logic.
- [Python Curses Documentation](https://docs.python.org/3/howto/curses.html) - For the terminal UI rendering.

***
<div style="display: flex; justify-content: center; gap: 20px;">
  <img src="https://www.gifcen.com/wp-content/uploads/2021/07/-66.gif" alt="miku_typing" style="height:150px;">
  <img src="https://media.tenor.com/yRSnf6wABQ4AAAAj/pato-duck.gif" alt="duck" style="height:150px;">
</div>

<div style="text-align: center; margin-top: 10px;">
  <span style="font-weight: bold; text-decoration: underline;">Ryuuuxseii   and   SolarianDev</span>
</div>
