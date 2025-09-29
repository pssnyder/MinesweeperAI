"""
Improved Minesweeper Game Implementation

This module contains the core game logic for Minesweeper, designed to be
educational and easy to understand for new programmers.
"""

import random
from typing import List, Set, Tuple, Optional


class Minesweeper:
    """
    A Minesweeper game implementation with improved error handling and documentation.
    
    This class represents the complete state of a Minesweeper game, including
    the hidden board with mines and numbers, and the player's visible board.
    """
    
    def __init__(self, rows: int, cols: int, mines: int):
        """
        Initialize the Minesweeper game board.

        Args:
            rows (int): Number of rows in the game board (must be > 0)
            cols (int): Number of columns in the game board (must be > 0)
            mines (int): Number of mines to be placed on the board (must be < rows * cols)
            
        Raises:
            ValueError: If parameters are invalid
        """
        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and columns must be positive integers")
        if mines < 0 or mines >= rows * cols:
            raise ValueError(f"Number of mines must be between 0 and {rows * cols - 1}")
            
        self.rows = rows
        self.cols = cols
        self.mines = mines
        
        # Initialize boards
        self.game_board: List[List[str]] = [['-' for _ in range(cols)] for _ in range(rows)]
        self.player_board: List[List[str]] = [['-' for _ in range(cols)] for _ in range(rows)]
        
        # Game state
        self.mine_positions: Set[Tuple[int, int]] = set()
        self.game_over = False
        self.game_won = False
        
        # Initialize the game
        self._place_mines()
        self._fill_numbers()

    def _place_mines(self) -> None:
        """
        Randomly place mines on the board.
        Uses a set to ensure unique positions.
        """
        positions = set()
        while len(positions) < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            positions.add((row, col))
        
        # Place mines on the board
        for row, col in positions:
            self.game_board[row][col] = '*'
        
        self.mine_positions = positions

    def _fill_numbers(self) -> None:
        """
        Fill the board with numbers indicating the count of adjacent mines for each cell.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.game_board[row][col] == '*':
                    continue
                    
                # Count adjacent mines
                count = 0
                for r in range(max(0, row - 1), min(self.rows, row + 2)):
                    for c in range(max(0, col - 1), min(self.cols, col + 2)):
                        if (r, c) in self.mine_positions:
                            count += 1
                
                self.game_board[row][col] = str(count)

    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Check if the given position is within the board boundaries.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            bool: True if position is valid, False otherwise
        """
        return 0 <= row < self.rows and 0 <= col < self.cols

    def uncover(self, row: int, col: int) -> bool:
        """
        Uncover a cell at the specified row and column.

        Args:
            row (int): The row index of the cell to uncover
            col (int): The column index of the cell to uncover

        Returns:
            bool: False if a mine is uncovered (game over), True otherwise
            
        Raises:
            ValueError: If position is invalid
        """
        if not self.is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
            
        if self.game_over:
            return False
            
        if self.player_board[row][col] != '-':
            return True  # Already uncovered or flagged
            
        # Uncover the cell
        self.player_board[row][col] = self.game_board[row][col]
        
        # Check if it's a mine
        if (row, col) in self.mine_positions:
            self.game_over = True
            return False
            
        # If it's a zero, auto-reveal adjacent cells
        if self.game_board[row][col] == '0':
            self._reveal_adjacent_zeros(row, col)
            
        # Check win condition
        self._check_win_condition()
        
        return True

    def _reveal_adjacent_zeros(self, start_row: int, start_col: int) -> None:
        """
        Recursively reveal adjacent cells when a zero is uncovered.
        Uses flood fill algorithm to reveal connected empty areas.
        
        Args:
            start_row (int): Starting row position
            start_col (int): Starting column position
        """
        stack = [(start_row, start_col)]
        visited = set()
        
        while stack:
            row, col = stack.pop()
            
            if (row, col) in visited:
                continue
                
            visited.add((row, col))
            
            # Reveal all adjacent cells
            for r in range(max(0, row - 1), min(self.rows, row + 2)):
                for c in range(max(0, col - 1), min(self.cols, col + 2)):
                    if self.player_board[r][c] == '-':
                        self.player_board[r][c] = self.game_board[r][c]
                        
                        # If adjacent cell is also zero, add to stack for processing
                        if self.game_board[r][c] == '0' and (r, c) not in visited:
                            stack.append((r, c))

    def flag(self, row: int, col: int) -> bool:
        """
        Flag a cell at the specified row and column as a mine.

        Args:
            row (int): The row index of the cell to flag
            col (int): The column index of the cell to flag
            
        Returns:
            bool: True if flag was placed/removed successfully, False otherwise
            
        Raises:
            ValueError: If position is invalid
        """
        if not self.is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
            
        if self.game_over:
            return False
            
        # Can't flag an already uncovered cell
        if self.player_board[row][col] not in ['-', 'F']:
            return False
            
        # Toggle flag
        if self.player_board[row][col] == 'F':
            self.player_board[row][col] = '-'
        else:
            self.player_board[row][col] = 'F'
            
        return True

    def _check_win_condition(self) -> None:
        """
        Check if the player has won the game.
        Win condition: All non-mine cells are uncovered.
        """
        uncovered_count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if (self.player_board[row][col] != '-' and 
                    self.player_board[row][col] != 'F'):
                    uncovered_count += 1
        
        total_safe_cells = (self.rows * self.cols) - self.mines
        if uncovered_count == total_safe_cells:
            self.game_won = True
            self.game_over = True

    def get_adjacent_cells(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get all valid adjacent cell positions for a given cell.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            List[Tuple[int, int]]: List of (row, col) tuples for adjacent cells
        """
        adjacent = []
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if r != row or c != col:  # Don't include the cell itself
                    adjacent.append((r, c))
        return adjacent

    def get_cell_value(self, row: int, col: int) -> Optional[str]:
        """
        Get the value of a cell on the player board.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            Optional[str]: Cell value if position is valid, None otherwise
        """
        if not self.is_valid_position(row, col):
            return None
        return self.player_board[row][col]

    def get_hidden_value(self, row: int, col: int) -> Optional[str]:
        """
        Get the actual value of a cell (for AI or debugging).
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            Optional[str]: Actual cell value if position is valid, None otherwise
        """
        if not self.is_valid_position(row, col):
            return None
        return self.game_board[row][col]

    def print_board(self, show_hidden: bool = False) -> None:
        """
        Print the current state of the board to the console.
        
        Args:
            show_hidden (bool): If True, shows the actual board with mines visible
        """
        board_to_show = self.game_board if show_hidden else self.player_board
        
        print("   " + " ".join(f"{i:2}" for i in range(self.cols)))
        print("  " + "---" * self.cols)
        
        for i, row in enumerate(board_to_show):
            print(f"{i:2}| " + " ".join(f"{cell:2}" for cell in row))
            
        if self.game_over:
            if self.game_won:
                print("\n🎉 Congratulations! You won! 🎉")
            else:
                print("\n💥 Game Over! You hit a mine! 💥")

    def get_game_state(self) -> dict:
        """
        Get the current game state as a dictionary.
        
        Returns:
            dict: Dictionary containing game state information
        """
        return {
            'rows': self.rows,
            'cols': self.cols,
            'mines': self.mines,
            'game_over': self.game_over,
            'game_won': self.game_won,
            'player_board': [row[:] for row in self.player_board],  # Deep copy
        }


def create_game_from_difficulty(difficulty: str) -> Minesweeper:
    """
    Create a Minesweeper game with predefined difficulty settings.
    
    Args:
        difficulty (str): One of 'beginner', 'intermediate', 'expert', 'custom'
        
    Returns:
        Minesweeper: A new game instance
        
    Raises:
        ValueError: If difficulty is not recognized
    """
    difficulty_settings = {
        'beginner': (9, 9, 10),
        'intermediate': (16, 16, 40),
        'expert': (16, 30, 99),
        'ai_test': (24, 30, 180),  # For AI testing
    }
    
    if difficulty.lower() not in difficulty_settings:
        raise ValueError(f"Unknown difficulty: {difficulty}. "
                        f"Available: {list(difficulty_settings.keys())}")
    
    rows, cols, mines = difficulty_settings[difficulty.lower()]
    return Minesweeper(rows, cols, mines)


def start_interactive_game() -> None:
    """
    Start an interactive command-line Minesweeper game.
    This is the main game loop for human players.
    """
    print("🎮 Welcome to Minesweeper! 🎮")
    print("\nDifficulty levels:")
    print("1. Beginner (9x9, 10 mines)")
    print("2. Intermediate (16x16, 40 mines)")
    print("3. Expert (16x30, 99 mines)")
    print("4. AI Test (24x30, 180 mines)")
    print("5. Custom")
    
    try:
        choice = input("\nSelect difficulty (1-5): ").strip()
        
        if choice == '1':
            game = create_game_from_difficulty('beginner')
        elif choice == '2':
            game = create_game_from_difficulty('intermediate')
        elif choice == '3':
            game = create_game_from_difficulty('expert')
        elif choice == '4':
            game = create_game_from_difficulty('ai_test')
        elif choice == '5':
            rows = int(input("Enter number of rows: "))
            cols = int(input("Enter number of columns: "))
            mines = int(input("Enter number of mines: "))
            game = Minesweeper(rows, cols, mines)
        else:
            print("Invalid choice. Starting beginner game.")
            game = create_game_from_difficulty('beginner')
            
    except ValueError as e:
        print(f"Error: {e}")
        print("Starting beginner game.")
        game = create_game_from_difficulty('beginner')
    
    print("\n📝 Instructions:")
    print("- Enter 'u row col' to uncover a cell (e.g., 'u 3 4')")
    print("- Enter 'f row col' to flag/unflag a cell")
    print("- Enter 'q' to quit")
    print("- Enter 'h' to show the hidden board (cheating!)")
    
    game.print_board()
    
    while not game.game_over:
        try:
            move = input("\nEnter your move: ").strip().split()
            
            if not move:
                continue
                
            if move[0].lower() == 'q':
                print("Thanks for playing!")
                break
            elif move[0].lower() == 'h':
                print("\n🔍 Hidden board (cheating!):")
                game.print_board(show_hidden=True)
                continue
            elif len(move) != 3:
                print("Invalid input! Use format: 'u row col' or 'f row col'")
                continue
                
            action, row_str, col_str = move
            row, col = int(row_str), int(col_str)
            
            if action.lower() == 'u':
                result = game.uncover(row, col)
                if not result:
                    print("💥 BOOM! You hit a mine!")
            elif action.lower() == 'f':
                game.flag(row, col)
            else:
                print("Invalid action! Use 'u' to uncover or 'f' to flag.")
                continue
                
            game.print_board()
            
        except (ValueError, IndexError) as e:
            print(f"Invalid input: {e}")
        except KeyboardInterrupt:
            print("\nGame interrupted. Thanks for playing!")
            break


if __name__ == "__main__":
    start_interactive_game()