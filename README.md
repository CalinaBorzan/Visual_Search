# Visual Search Pathfinding Project

## Overview
The **Visual Search Pathfinding Project** is a Python-based application that implements various pathfinding algorithms using **Pygame** for visualization. Users can interactively select start and end points, place obstacles, and choose from multiple algorithms to visualize how different search strategies traverse the grid. The grid updates dynamically to reflect the search process, providing a clear representation of each algorithm's behavior.

## Features
- **Pathfinding Algorithms**:
  - **Breadth-First Search (BFS)**
  - **Depth-First Search (DFS)**
  - **Uniform Cost Search (UCS)**
  - **Dijkstra's Algorithm**
  - **A* Search Algorithm (A*)**
- **Interactive Grid**:
  - Click to place start, end, and barrier nodes.
  - Right-click to remove placed nodes.
  - Grid size can be increased or decreased dynamically.
- **Real-Time Visualization**:
  - Shows visited nodes and final path in an animated fashion.
  - Highlights open and closed nodes in different colors.
- **User Controls**:
  - `R` key to reset the grid.
  - Mouse click interactions for setting points and barriers.
  - Buttons for selecting algorithms.

## Technologies Used
- **Programming Language**: Python
- **Visualization Library**: Pygame
- **Algorithms**: BFS, DFS, UCS, Dijkstra, A*
- **Data Structures**: Priority Queue, Queue, Stack

## Installation & Setup
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/CalinaBorzan/Visual_Search.git
   ```
2. **Install Dependencies**:
   ```sh
   pip install pygame
   ```
3. **Run the Application**:
   ```sh
   python main.py
   ```

## How to Use
1. **Select Start and End Points**:
   - Left-click on the grid to set the **start node** (blue) and **end node** (purple).
2. **Place Barriers**:
   - Left-click additional grid cells to place barriers (black).
3. **Select an Algorithm**:
   - Click on one of the buttons (**BFS, DFS, UCS, Dijkstra, A* Search**) to start pathfinding.
4. **Reset the Grid**:
   - Press `R` to reset the grid and start a new search.
5. **Increase or Decrease Grid Size**:
   - Click **Increase Size** or **Decrease Size** buttons to adjust the grid resolution.

## Future Enhancements
- **Weighted Graph Support**: Implement weight variations for paths.
- **More Heuristic Functions**: Enhance A* search with multiple heuristic options.
- **Obstacle Generation**: Auto-generate random mazes and obstacles.
- **Performance Optimization**: Improve efficiency for larger grid sizes.
- **GUI Improvements**: Introduce a cleaner UI with additional user options.

---
This project highlights my expertise in **algorithm implementation, data structures, and interactive visualization**, making it a valuable addition to my portfolio for software development and AI-related roles.

