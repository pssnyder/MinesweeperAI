# API Reference Documentation

This document provides detailed API documentation for the Minesweeper AI project. It's intended for developers who want to understand the codebase or extend functionality.

## Table of Contents

- [Core Classes](#core-classes)
  - [Minesweeper](#minesweeper)
  - [MinesweeperAI](#minesweeperai)
- [Utility Functions](#utility-functions)
- [Constants and Configuration](#constants-and-configuration)
- [Error Handling](#error-handling)
- [Examples](#examples)

---

## Core Classes

### Minesweeper

The core game engine that manages the Minesweeper game state.

#### Constructor

```python
Minesweeper(rows: int, cols: int, mines: int)
```

**Parameters:**
- `rows` (int): Number of rows in the game board (must be > 0)
- `cols` (int): Number of columns in the game board (must be > 0)  
- `mines` (int): Number of mines to place (must be < rows * cols)

**Raises:**
- `ValueError`: If parameters are invalid

**Example:**
```python
game = Minesweeper(9, 9, 10)  # Beginner difficulty
```

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `rows` | `int` | Number of rows in the board |
| `cols` | `int` | Number of columns in the board |
| `mines` | `int` | Total number of mines |
| `game_board` | `List[List[str]]` | Hidden board with mines and numbers |
| `player_board` | `List[List[str]]` | Visible board (what player sees) |
| `mine_positions` | `Set[Tuple[int, int]]` | Set of mine coordinates |
| `game_over` | `bool` | True if game has ended |
| `game_won` | `bool` | True if player won |

#### Methods

##### `uncover(row: int, col: int) -> bool`

Uncover a cell at the specified position.

**Parameters:**
- `row` (int): Row index (0-based)
- `col` (int): Column index (0-based)

**Returns:**
- `bool`: False if mine was hit (game over), True otherwise

**Raises:**
- `ValueError`: If position is invalid

**Example:**
```python
result = game.uncover(4, 4)
if not result:
    print("Hit a mine!")
```

##### `flag(row: int, col: int) -> bool`

Flag or unflag a cell as a potential mine.

**Parameters:**
- `row` (int): Row index
- `col` (int): Column index

**Returns:**
- `bool`: True if flag was toggled successfully

**Example:**
```python
game.flag(0, 0)  # Flag cell as mine
game.flag(0, 0)  # Unflag cell
```

##### `is_valid_position(row: int, col: int) -> bool`

Check if coordinates are within board boundaries.

**Parameters:**
- `row` (int): Row index
- `col` (int): Column index

**Returns:**
- `bool`: True if position is valid

##### `get_adjacent_cells(row: int, col: int) -> List[Tuple[int, int]]`

Get all valid adjacent cell positions.

**Parameters:**
- `row` (int): Row index
- `col` (int): Column index

**Returns:**
- `List[Tuple[int, int]]`: List of adjacent cell coordinates

**Example:**
```python
neighbors = game.get_adjacent_cells(1, 1)
# Returns [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]
```

##### `get_cell_value(row: int, col: int) -> Optional[str]`

Get the value of a cell on the player board.

**Parameters:**
- `row` (int): Row index
- `col` (int): Column index

**Returns:**
- `Optional[str]`: Cell value or None if invalid position

**Possible return values:**
- `'-'`: Unknown cell
- `'F'`: Flagged cell
- `'0'-'8'`: Number of adjacent mines
- `None`: Invalid position

##### `get_hidden_value(row: int, col: int) -> Optional[str]`

Get the actual value of a cell (for AI or debugging).

**Parameters:**
- `row` (int): Row index
- `col` (int): Column index

**Returns:**
- `Optional[str]`: Actual cell value

**Possible return values:**
- `'*'`: Mine
- `'0'-'8'`: Number of adjacent mines
- `None`: Invalid position

##### `print_board(show_hidden: bool = False) -> None`

Print the current board state to console.

**Parameters:**
- `show_hidden` (bool): If True, shows actual board with mines visible

**Example:**
```python
game.print_board()              # Show player view
game.print_board(show_hidden=True)  # Show actual board
```

##### `get_game_state() -> dict`

Get comprehensive game state information.

**Returns:**
- `dict`: Game state with keys: 'rows', 'cols', 'mines', 'game_over', 'game_won', 'player_board'

**Example:**
```python
state = game.get_game_state()
print(f"Game over: {state['game_over']}")
```

---

### MinesweeperAI

AI player that can analyze and play Minesweeper games.

#### Constructor

```python
MinesweeperAI(game: Minesweeper)
```

**Parameters:**
- `game` (Minesweeper): The game instance to play

**Example:**
```python
game = Minesweeper(9, 9, 10)
ai = MinesweeperAI(game)
```

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `game` | `Minesweeper` | Reference to game instance |
| `uncovered` | `Set[Tuple[int, int]]` | Cells AI has uncovered |
| `flags` | `Set[Tuple[int, int]]` | Cells AI has flagged |
| `safe_cells` | `Set[Tuple[int, int]]` | Cells AI knows are safe |
| `mine_cells` | `Set[Tuple[int, int]]` | Cells AI knows are mines |
| `constraints` | `List[Dict]` | Active CSP constraints |
| `move_history` | `List[Tuple]` | History of moves made |

#### Methods

##### `make_move() -> bool`

Make the next best move based on current knowledge.

**Returns:**
- `bool`: True if move was made, False if no moves available

**Example:**
```python
while not game.game_over:
    if not ai.make_move():
        break
    game.print_board()
```

##### `reset() -> None`

Reset AI state for a new game.

**Example:**
```python
ai.reset()  # Clear all knowledge for new game
```

##### `uncover(row: int, col: int) -> bool`

AI version of uncovering a cell (updates AI knowledge).

**Parameters:**
- `row` (int): Row index
- `col` (int): Column index

**Returns:**
- `bool`: True if successful, False if hit mine

##### `flag(row: int, col: int) -> bool`

AI version of flagging a cell.

**Parameters:**
- `row` (int): Row index
- `col` (int): Column index

**Returns:**
- `bool`: True if successful

##### `get_frontier_cells() -> Set[Tuple[int, int]]`

Get all frontier cells (unknown cells adjacent to revealed numbers).

**Returns:**
- `Set[Tuple[int, int]]`: Set of frontier cell positions

**Example:**
```python
frontier = ai.get_frontier_cells()
print(f"AI is considering {len(frontier)} frontier cells")
```

##### `find_safe_move() -> Optional[Tuple[int, int]]`

Find a guaranteed safe move using logical deduction.

**Returns:**
- `Optional[Tuple[int, int]]`: Safe cell position or None

##### `find_probable_move() -> Optional[Tuple[int, int]]`

Find best probabilistic move when no safe moves available.

**Returns:**
- `Optional[Tuple[int, int]]`: Best cell based on probabilities

##### `calculate_mine_probabilities() -> Dict[Tuple[int, int], float]`

Calculate mine probability for each frontier cell.

**Returns:**
- `Dict[Tuple[int, int], float]`: Mapping of positions to probabilities

**Example:**
```python
probs = ai.calculate_mine_probabilities()
for (row, col), prob in probs.items():
    print(f"Cell ({row}, {col}): {prob:.1%} chance of mine")
```

##### `solve_constraints() -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]]]`

Use constraint satisfaction to find definite safe cells and mines.

**Returns:**
- `Tuple[Set, Set]`: (new_safe_cells, new_mine_cells)

##### `get_statistics() -> Dict[str, Any]`

Get AI performance statistics.

**Returns:**
- `Dict[str, Any]`: Statistics dictionary

**Example:**
```python
stats = ai.get_statistics()
print(f"Moves made: {stats['moves_made']}")
print(f"Win rate: {stats['game_won']}")
```

##### `explain_last_move() -> str`

Get explanation of the reasoning behind the last move.

**Returns:**
- `str`: Human-readable explanation

**Example:**
```python
ai.make_move()
print(ai.explain_last_move())
# Output: "Uncovered (3, 4) - logically deduced to be safe"
```

---

## Utility Functions

### `create_game_from_difficulty(difficulty: str) -> Minesweeper`

Create a game with predefined difficulty settings.

**Parameters:**
- `difficulty` (str): One of 'beginner', 'intermediate', 'expert', 'ai_test'

**Returns:**
- `Minesweeper`: New game instance

**Raises:**
- `ValueError`: If difficulty is not recognized

**Example:**
```python
game = create_game_from_difficulty('beginner')  # 9x9 with 10 mines
```

**Difficulty Settings:**
| Difficulty | Rows | Cols | Mines |
|------------|------|------|-------|
| beginner | 9 | 9 | 10 |
| intermediate | 16 | 16 | 40 |
| expert | 16 | 30 | 99 |
| ai_test | 24 | 30 | 180 |

### `start_interactive_game() -> None`

Start an interactive command-line game for human players.

**Example:**
```python
from minesweeper_game import start_interactive_game
start_interactive_game()
```

---

## Constants and Configuration

### Cell Values

| Constant | Value | Description |
|----------|-------|-------------|
| Unknown Cell | `'-'` | Cell not yet uncovered |
| Flagged Cell | `'F'` | Cell flagged as potential mine |
| Mine | `'*'` | Cell contains a mine |
| Numbers | `'0'-'8'` | Count of adjacent mines |

### Game States

| State | Description |
|-------|-------------|
| `game_over=False, game_won=False` | Game in progress |
| `game_over=True, game_won=False` | Game lost (hit mine) |
| `game_over=True, game_won=True` | Game won |

---

## Error Handling

### Common Exceptions

#### `ValueError`
Raised when invalid parameters are provided:
- Invalid board dimensions (rows/cols ≤ 0)
- Too many mines (mines ≥ rows * cols)
- Invalid cell coordinates

**Example:**
```python
try:
    game = Minesweeper(-1, 5, 10)  # Invalid rows
except ValueError as e:
    print(f"Error: {e}")
```

#### `IndexError`
May be raised when accessing invalid board positions:
```python
try:
    value = game.game_board[100][100]  # Out of bounds
except IndexError:
    print("Position out of bounds")
```

### Best Practices

1. **Always validate inputs:**
   ```python
   if game.is_valid_position(row, col):
       game.uncover(row, col)
   ```

2. **Check game state before moves:**
   ```python
   if not game.game_over:
       ai.make_move()
   ```

3. **Handle AI limitations:**
   ```python
   if not ai.make_move():
       print("AI couldn't find a good move")
   ```

---

## Examples

### Basic Game Usage

```python
from minesweeper_game import Minesweeper

# Create a beginner game
game = Minesweeper(9, 9, 10)

# Make some moves
result = game.uncover(4, 4)  # Uncover center
if result:
    game.flag(0, 0)  # Flag a suspicious cell
    game.print_board()
else:
    print("Hit a mine!")
```

### AI Usage

```python
from minesweeper_game import create_game_from_difficulty
from minesweeper_ai import MinesweeperAI

# Create game and AI
game = create_game_from_difficulty('beginner')
ai = MinesweeperAI(game)

# Let AI play automatically
move_count = 0
while not game.game_over and move_count < 100:
    if ai.make_move():
        move_count += 1
        print(f"Move {move_count}: {ai.explain_last_move()}")
    else:
        break

# Show results
if game.game_won:
    print(f"AI won in {move_count} moves!")
else:
    print("AI hit a mine!")

print(f"Statistics: {ai.get_statistics()}")
```

### Advanced AI Analysis

```python
# Create custom game for testing
game = Minesweeper(5, 5, 3)
ai = MinesweeperAI(game)

# Make initial move
ai.make_move()

# Analyze AI's reasoning
frontier = ai.get_frontier_cells()
probabilities = ai.calculate_mine_probabilities()

print(f"Frontier cells: {len(frontier)}")
for (row, col), prob in sorted(probabilities.items(), key=lambda x: x[1]):
    print(f"Cell ({row}, {col}): {prob:.1%} mine probability")

# Check constraint satisfaction
safe_cells, mine_cells = ai.solve_constraints()
print(f"Found {len(safe_cells)} safe cells and {len(mine_cells)} mines")
```

### Performance Testing

```python
import time

def benchmark_ai(difficulty='beginner', games=10):
    """Benchmark AI performance."""
    wins = 0
    total_moves = 0
    total_time = 0
    
    for i in range(games):
        game = create_game_from_difficulty(difficulty)
        ai = MinesweeperAI(game)
        
        start_time = time.time()
        moves = 0
        
        while not game.game_over and moves < 1000:
            if ai.make_move():
                moves += 1
            else:
                break
        
        end_time = time.time()
        
        if game.game_won:
            wins += 1
        
        total_moves += moves
        total_time += (end_time - start_time)
        
        print(f"Game {i+1}: {'WIN' if game.game_won else 'LOSE'} in {moves} moves")
    
    print(f"\nResults for {games} {difficulty} games:")
    print(f"Win rate: {wins/games:.1%}")
    print(f"Average moves: {total_moves/games:.1f}")
    print(f"Average time: {total_time/games:.2f}s")

# Run benchmark
benchmark_ai('beginner', 10)
```

### Custom Difficulty

```python
def create_custom_game(rows, cols, mine_percentage=0.15):
    """Create a game with custom mine density."""
    total_cells = rows * cols
    mines = int(total_cells * mine_percentage)
    mines = max(1, min(mines, total_cells - 1))  # Ensure valid range
    
    return Minesweeper(rows, cols, mines)

# Create a custom 12x12 board with 15% mines
custom_game = create_custom_game(12, 12, 0.15)
print(f"Created {custom_game.rows}x{custom_game.cols} game with {custom_game.mines} mines")
```

---

## Type Hints

The codebase uses Python type hints for better code documentation and IDE support:

```python
from typing import List, Set, Tuple, Optional, Dict, Any

def example_function(
    board: List[List[str]], 
    position: Tuple[int, int]
) -> Optional[str]:
    """Example of type-hinted function."""
    row, col = position
    if 0 <= row < len(board) and 0 <= col < len(board[0]):
        return board[row][col]
    return None
```

---

## Testing

### Unit Testing

```python
import unittest
from minesweeper_game import Minesweeper

class TestMinesweeper(unittest.TestCase):
    def test_board_creation(self):
        game = Minesweeper(5, 5, 3)
        self.assertEqual(game.rows, 5)
        self.assertEqual(game.cols, 5)
        self.assertEqual(game.mines, 3)
    
    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            Minesweeper(0, 5, 3)  # Invalid rows
        
        with self.assertRaises(ValueError):
            Minesweeper(5, 5, 25)  # Too many mines

if __name__ == '__main__':
    unittest.main()
```

---

This API reference provides comprehensive documentation for using and extending the Minesweeper AI project. For more examples and tutorials, see the other documentation files in the `docs/` directory.