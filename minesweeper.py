import random

class Minesweeper:
    def __init__(self, rows, cols, mines):
        """
        Initialize the Minesweeper game board.

        Args:
            rows (int): Number of rows in the game board.
            cols (int): Number of columns in the game board.
            mines (int): Number of mines to be placed on the board.
        """
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.game_board = [['-' for _ in range(cols)] for _ in range(rows)]  # Initialize the board with empty cells
        self.player_board = [['-' for _ in range(cols)] for _ in range(rows)]  # Initialize the player board with empty cells
        self.mine_positions = self.place_mines()  # Randomly place mines on the board
        self.fill_numbers()  # Fill the board with numbers indicating adjacent mines

    def place_mines(self):
        """
        Randomly place mines on the board.

        Returns:
            set: A set of tuples representing the positions of the mines.
        """
        positions = set()
        while len(positions) < self.mines:
            pos = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
            positions.add(pos)
        for r, c in positions:
            self.game_board[r][c] = '*'  # Place a mine at the specified position
        return positions

    def fill_numbers(self):
        """
        Fill the board with numbers indicating the count of adjacent mines for each cell.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.game_board[r][c] == '*':
                    continue
                count = sum((nr, nc) in self.mine_positions for nr in range(r-1, r+2) for nc in range(c-1, c+2) if 0 <= nr < self.rows and 0 <= nc < self.cols)
                self.game_board[r][c] = str(count)  # Set the cell to the count of adjacent mines

    def print_board(self):
        """
        Print the current state of the board to the console.
        """
        for row in self.player_board:
            print(' '.join(row))

    def uncover(self, row, col):
        """
        Uncover a cell at the specified row and column.

        Args:
            row (int): The row index of the cell to uncover.
            col (int): The column index of the cell to uncover.

        Returns:
            bool: False if a mine is uncovered (game over), True otherwise.
        """
        if (row, col) in self.mine_positions:
            return False  # Hit a mine
        return True  # Safe move

    def check_for_zeros(self):
        """
        Check to ensure there are no zeros without their adjacent cells exposed.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.player_board[r][c] == '0':
                    self.player_board[r-1][c-1] = self.game_board[r-1][c-1]
                    self.player_board[r-1][c] = self.game_board[r-1][c]
                    self.player_board[r-1][c+1] = self.game_board[r-1][c+1]
                    self.player_board[r][c-1] = self.game_board[r][c-1]
                    self.player_board[r][c+1] = self.game_board[r][c+1]
                    self.player_board[r+1][c-1] = self.game_board[r+1][c-1]
                    self.player_board[r+1][c] = self.game_board[r+1][c]
                    self.player_board[r+1][c+1] = self.game_board[r+1][c+1]
                    for r in range(self.rows):
                        for c in range(self.cols):
                            if self.player_board[r][c] == '0':
                                self.check_for_zeros()
                    
    def flag(self, row, col):
        """
        Flag a cell at the specified row and column as a mine.

        Args:
            row (int): The row index of the cell to flag.
            col (int): The column index of the cell to flag.
        """
        self.player_board[row][col] = 'F'  # Mark the cell as flagged

def start_game():
    """
    Initialize and start a new game of Minesweeper.
    """
    # Prompt the user for the number of rows, columns, and mines
    difficulty = int(input("Select Difficulty (1-5): "))
    
    if difficulty == 1:
        rows = 9
        cols = 9
        mines = 10
        print("Beginner Selected: 10 mines 9x9 grid")
    elif difficulty == 2:
        rows = 16
        cols = 16
        mines = 40
        print("Intermediate Selected: 40 mines 16x16 grid")
    elif difficulty == 3:
        rows = 30
        cols = 16
        mines = 99
        print("Advanced Selected: 99 mines 30x16 grid")
    elif difficulty == 4:
        rows = 24
        cols = 30
        mines = 180
        print("Expert Selected: 180 mines 24x30 grid")
    elif difficulty == 5:
        rows = 240
        cols = 300
        mines = 1800
        print("AI Selected: 1800 mines 240x300 grid")
    

    # Create a new Minesweeper game with the specified parameters
    game = Minesweeper(rows, cols, mines)

    # Print the initial state of the board
    game.print_board()
    
    # Start the game loop
    while True:
        # Prompt the player for their next move
        move = input("Enter 'u' to uncover or 'f' to flag, followed by row and column (e.g., 'u 3 4'): ").split()
        action, row, col = move[0], int(move[1]), int(move[2])

        # Update the game state based on the player's input
        if action == 'u':
            if not game.uncover(row, col):
                # If the player uncovered a mine they lose
                print("Game Over! You hit a mine.")
                game.print_board()
                break
            elif game.uncover(row,col):
                # If the player didn't uncover a mine, update their player board
                game.player_board[row][col] = game.game_board[row][col]
        elif action == 'f':
            game.flag(row, col)
        else:
            print("Invalid action! Please enter 'u' to uncover or 'f' to flag.")

        # Print the updated board state
        game.print_board()

        # Check if the game is won
        grid_count = len(game.rows) * len(game.cols)
        current_grid = 0
        for r in range(game.rows):
            for c in range(game.cols):
                if game.player_board[r][c] != '-':
                    current_grid
                    print("Congratulations You've won the game.")
                    break

# Main function
if __name__ == "__main__":
    start_game()