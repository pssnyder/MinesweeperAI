# Minesweeper Game with AI

## Overview

This repository contains a Python implementation of the classic Minesweeper game, offering both a command-line interface for human players and a basic AI player that can make moves. The project demonstrates fundamental game logic, board generation, and an introduction to AI decision-making in a strategic puzzle game.

## Features

* **Human Playable:** Interact with the game directly through the console to uncover cells or flag potential mines.

* **Difficulty Levels:** Choose from predefined board sizes and mine counts (Beginner, Intermediate, Advanced, Expert, AI).

* **AI Player (Work in Progress):** An `MinesweeperAI` class is included with initial logic for making safe moves and probabilistic guesses.

* **Board Generation:** Dynamically creates game boards with randomly placed mines and calculated adjacent mine counts.

* **Clear Console Output:** The game board is printed to the console for easy visualization.

## Getting Started

### Prerequisites

* Python 3.x installed on your system.

### Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/your-username/minesweeper-ai.git
   cd minesweeper-ai
   
   ```

### How to Play (Human Player)

1. **Run the game:**

   ```
   python minesweeper.py
   
   ```

2. **Select Difficulty:** The game will prompt you to select a difficulty level (1-5).

3. **Make your move:**

   * To **uncover** a cell, type `u <row> <col>` (e.g., `u 3 4`).

   * To **flag** a cell as a mine, type `f <row> <col>` (e.g., `f 1 2`).

### How to Run the AI (Example)

The `ai_player.py` file contains an example of how to initialize and use the `MinesweeperAI` class.

1. **Run the AI example:**

   ```
   python ai_player.py
   
   ```

   *Note: The AI's move logic is currently basic and under development. You'll see one move made and the updated board.*

## Project Structure

* `minesweeper.py`: Contains the core `Minesweeper` game logic, including board initialization, mine placement, number filling, and game interaction.

* `ai_player.py`: Implements the `MinesweeperAI` class, designed to play the game autonomously.

## Future Enhancements (Roadmap)

* **Improved AI Logic:** Enhance `MinesweeperAI` with advanced constraint satisfaction (CSP) and probability estimation techniques for more intelligent gameplay.

* **Graphical User Interface (GUI):** Develop a visual interface using libraries like Tkinter, Pygame, or PyQt for a richer user experience.

* **Game State Management:** More robust handling of game states (win/loss conditions, restarts).

* **Refined Zero Propagation:** Ensure all adjacent zero cells are automatically uncovered.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

\[Choose and add your preferred license here, e.g., MIT, Apache 2.0, etc.\]

*Remember to save and backup your work after any changes!*
