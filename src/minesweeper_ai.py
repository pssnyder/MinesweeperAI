"""
Minesweeper AI Implementation

This module contains an AI that can play Minesweeper using logical reasoning
and probability estimation. Designed for educational purposes to teach AI concepts.
"""

import random
from typing import Set, Tuple, List, Dict, Optional, Any
from collections import defaultdict


class MinesweeperAI:
    """
    An AI player for Minesweeper that uses constraint satisfaction and probability estimation.
    
    This AI demonstrates several important concepts:
    1. Constraint Satisfaction Problems (CSP)
    2. Logical deduction
    3. Probability estimation
    4. Game tree search strategies
    """
    
    def __init__(self, game):
        """
        Initialize the Minesweeper AI with the game instance.

        Args:
            game (Minesweeper): The Minesweeper game instance
        """
        self.game = game
        self.uncovered: Set[Tuple[int, int]] = set()  # Cells we've uncovered
        self.flags: Set[Tuple[int, int]] = set()      # Cells we've flagged as mines
        self.safe_cells: Set[Tuple[int, int]] = set()  # Cells we know are safe
        self.mine_cells: Set[Tuple[int, int]] = set()  # Cells we know are mines
        
        # For advanced reasoning
        self.constraints: List[Dict] = []  # CSP constraints
        self.move_history: List[Tuple[str, int, int]] = []  # Track moves for learning

    def reset(self) -> None:
        """Reset the AI state for a new game."""
        self.uncovered.clear()
        self.flags.clear()
        self.safe_cells.clear()
        self.mine_cells.clear()
        self.constraints.clear()
        self.move_history.clear()

    def get_frontier_cells(self) -> Set[Tuple[int, int]]:
        """
        Get all frontier cells (covered cells adjacent to uncovered numbered cells).
        These are the most interesting cells for analysis.
        
        Returns:
            Set[Tuple[int, int]]: Set of frontier cell positions
        """
        frontier = set()
        
        for row, col in self.uncovered:
            cell_value = self.game.get_cell_value(row, col)
            
            # Only numbered cells provide information
            if cell_value and cell_value.isdigit():
                for adj_row, adj_col in self.game.get_adjacent_cells(row, col):
                    # Add covered cells to frontier
                    if self.game.get_cell_value(adj_row, adj_col) == '-':
                        frontier.add((adj_row, adj_col))
        
        return frontier

    def update_knowledge(self, row: int, col: int) -> None:
        """
        Update AI knowledge after uncovering a cell.
        
        Args:
            row (int): Row of the uncovered cell
            col (int): Column of the uncovered cell
        """
        self.uncovered.add((row, col))
        cell_value = self.game.get_cell_value(row, col)
        
        if cell_value and cell_value.isdigit():
            self._analyze_numbered_cell(row, col, int(cell_value))

    def _analyze_numbered_cell(self, row: int, col: int, number: int) -> None:
        """
        Analyze a numbered cell to deduce safe cells and mines.
        
        Args:
            row (int): Row of the numbered cell
            col (int): Column of the numbered cell  
            number (int): The number in the cell
        """
        adjacent_cells = self.game.get_adjacent_cells(row, col)
        
        # Categorize adjacent cells
        covered_cells = []
        flagged_count = 0
        
        for adj_row, adj_col in adjacent_cells:
            cell_value = self.game.get_cell_value(adj_row, adj_col)
            if cell_value == '-':
                covered_cells.append((adj_row, adj_col))
            elif cell_value == 'F' or (adj_row, adj_col) in self.flags:
                flagged_count += 1
        
        remaining_mines = number - flagged_count
        
        # Apply logical deductions
        if remaining_mines == 0:
            # All remaining covered cells are safe
            for cell in covered_cells:
                self.safe_cells.add(cell)
        elif remaining_mines == len(covered_cells):
            # All remaining covered cells are mines
            for cell in covered_cells:
                self.mine_cells.add(cell)
        else:
            # Create constraint for CSP solving
            constraint = {
                'cells': covered_cells,
                'mines': remaining_mines,
                'source': (row, col)
            }
            self.constraints.append(constraint)

    def solve_constraints(self) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]]]:
        """
        Use constraint satisfaction to find definite safe cells and mines.
        
        Returns:
            Tuple[Set, Set]: (new_safe_cells, new_mine_cells)
        """
        new_safe = set()
        new_mines = set()
        
        # Simple constraint propagation
        for constraint in self.constraints:
            cells = [c for c in constraint['cells'] 
                    if c not in self.safe_cells and c not in self.mine_cells]
            mines_needed = constraint['mines']
            
            # Remove already identified mines from count
            for cell in constraint['cells']:
                if cell in self.mine_cells:
                    mines_needed -= 1
            
            if mines_needed == 0:
                new_safe.update(cells)
            elif mines_needed == len(cells):
                new_mines.update(cells)
        
        # Advanced: Check for subset constraints
        # If one constraint is a subset of another, we can deduce more
        for i, c1 in enumerate(self.constraints):
            for j, c2 in enumerate(self.constraints):
                if i != j:
                    cells1 = set(c1['cells']) - self.safe_cells - self.mine_cells
                    cells2 = set(c2['cells']) - self.safe_cells - self.mine_cells
                    
                    if cells1.issubset(cells2) and cells1:
                        # c1 is subset of c2
                        remaining_cells = cells2 - cells1
                        remaining_mines = c2['mines'] - c1['mines']
                        
                        if remaining_mines == 0:
                            new_safe.update(remaining_cells)
                        elif remaining_mines == len(remaining_cells):
                            new_mines.update(remaining_cells)
        
        return new_safe, new_mines

    def calculate_mine_probabilities(self) -> Dict[Tuple[int, int], float]:
        """
        Calculate the probability that each frontier cell contains a mine.
        
        Returns:
            Dict[Tuple[int, int], float]: Mapping of cell positions to mine probabilities
        """
        probabilities = {}
        frontier = self.get_frontier_cells()
        
        if not frontier:
            return probabilities
        
        # Simple probability estimation based on constraints
        for cell in frontier:
            if cell in self.safe_cells:
                probabilities[cell] = 0.0
            elif cell in self.mine_cells:
                probabilities[cell] = 1.0
            else:
                # Calculate based on relevant constraints
                relevant_constraints = [c for c in self.constraints if cell in c['cells']]
                
                if relevant_constraints:
                    # Simple average of constraint-based probabilities
                    total_prob = 0.0
                    count = 0
                    
                    for constraint in relevant_constraints:
                        active_cells = [c for c in constraint['cells'] 
                                      if c not in self.safe_cells and c not in self.mine_cells]
                        if active_cells:
                            prob = constraint['mines'] / len(active_cells)
                            total_prob += prob
                            count += 1
                    
                    probabilities[cell] = total_prob / count if count > 0 else 0.5
                else:
                    # Default probability based on global mine density
                    total_cells = self.game.rows * self.game.cols
                    uncovered_count = len(self.uncovered)
                    flagged_count = len(self.flags)
                    remaining_cells = total_cells - uncovered_count - flagged_count
                    remaining_mines = self.game.mines - flagged_count
                    
                    if remaining_cells > 0:
                        probabilities[cell] = remaining_mines / remaining_cells
                    else:
                        probabilities[cell] = 0.0
        
        return probabilities

    def find_safe_move(self) -> Optional[Tuple[int, int]]:
        """
        Find a guaranteed safe move using logical deduction.
        
        Returns:
            Optional[Tuple[int, int]]: Safe cell position or None if none found
        """
        # Update knowledge from current board state
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                cell_value = self.game.get_cell_value(row, col)
                if (cell_value and cell_value.isdigit() and 
                    (row, col) not in self.uncovered):
                    self.update_knowledge(row, col)
        
        # Use constraint satisfaction
        new_safe, new_mines = self.solve_constraints()
        self.safe_cells.update(new_safe)
        self.mine_cells.update(new_mines)
        
        # Flag newly identified mines
        for mine_cell in new_mines:
            if mine_cell not in self.flags:
                self.flags.add(mine_cell)
                # Note: In a real implementation, you'd call game.flag() here
        
        # Return a safe cell to uncover
        for safe_cell in self.safe_cells:
            if self.game.get_cell_value(safe_cell[0], safe_cell[1]) == '-':
                return safe_cell
        
        return None

    def find_probable_move(self) -> Optional[Tuple[int, int]]:
        """
        Find the best probabilistic move when no safe moves are available.
        
        Returns:
            Optional[Tuple[int, int]]: Best cell position based on probabilities
        """
        probabilities = self.calculate_mine_probabilities()
        
        if not probabilities:
            # No frontier cells, pick a random uncovered cell
            all_cells = [(r, c) for r in range(self.game.rows) 
                        for c in range(self.game.cols)]
            available_cells = [(r, c) for r, c in all_cells 
                             if self.game.get_cell_value(r, c) == '-']
            
            if available_cells:
                return random.choice(available_cells)
            return None
        
        # Choose cell with lowest mine probability
        best_cell = min(probabilities.keys(), key=lambda x: probabilities[x])
        return best_cell

    def make_move(self) -> bool:
        """
        Decide and make the next move based on the current state of the game.
        
        Returns:
            bool: True if a move was made, False if no moves available
        """
        if self.game.game_over:
            return False
        
        # First try to find a safe move
        safe_move = self.find_safe_move()
        if safe_move:
            row, col = safe_move
            result = self.uncover(row, col)
            self.move_history.append(('uncover', row, col))
            return result
        
        # Flag any known mines
        for mine_row, mine_col in self.mine_cells:
            if (mine_row, mine_col) not in self.flags:
                self.flag(mine_row, mine_col)
                self.move_history.append(('flag', mine_row, mine_col))
                return True
        
        # If no safe moves, make a probabilistic move
        probable_move = self.find_probable_move()
        if probable_move:
            row, col = probable_move
            result = self.uncover(row, col)
            self.move_history.append(('uncover', row, col))
            return result
        
        return False

    def uncover(self, row: int, col: int) -> bool:
        """
        Uncover a cell and update AI knowledge.

        Args:
            row (int): The row index of the cell to uncover
            col (int): The column index of the cell to uncover
            
        Returns:
            bool: True if successful, False if hit a mine
        """
        if (row, col) in self.uncovered or (row, col) in self.flags:
            return True
            
        result = self.game.uncover(row, col)
        if result:
            self.update_knowledge(row, col)
        
        return result

    def flag(self, row: int, col: int) -> bool:
        """
        Flag a cell as a mine.

        Args:
            row (int): The row index of the cell to flag
            col (int): The column index of the cell to flag
            
        Returns:
            bool: True if successful
        """
        if (row, col) in self.uncovered:
            return False
            
        result = self.game.flag(row, col)
        if result:
            self.flags.add((row, col))
        
        return result

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get AI performance statistics.
        
        Returns:
            Dict[str, any]: Statistics about the AI's performance
        """
        return {
            'moves_made': len(self.move_history),
            'cells_uncovered': len(self.uncovered),
            'mines_flagged': len(self.flags),
            'safe_cells_identified': len(self.safe_cells),
            'mine_cells_identified': len(self.mine_cells),
            'constraints_active': len(self.constraints),
            'game_won': self.game.game_won,
            'game_over': self.game.game_over
        }

    def explain_last_move(self) -> str:
        """
        Explain the reasoning behind the last move.
        
        Returns:
            str: Explanation of the last move
        """
        if not self.move_history:
            return "No moves made yet."
        
        action, row, col = self.move_history[-1]
        
        if action == 'uncover':
            if (row, col) in self.safe_cells:
                return f"Uncovered ({row}, {col}) - logically deduced to be safe"
            else:
                probs = self.calculate_mine_probabilities()
                if (row, col) in probs:
                    prob = probs[(row, col)]
                    return f"Uncovered ({row}, {col}) - probability of mine: {prob:.2%}"
                else:
                    return f"Uncovered ({row}, {col}) - random choice (no information available)"
        elif action == 'flag':
            return f"Flagged ({row}, {col}) - logically deduced to be a mine"
        
        return f"Unknown action: {action}"


def create_ai_demo() -> None:
    """
    Create a demonstration of the AI playing Minesweeper.
    """
    from .minesweeper_game import create_game_from_difficulty
    
    print("🤖 Minesweeper AI Demo 🤖")
    print("\nStarting a beginner game...")
    
    game = create_game_from_difficulty('beginner')
    ai = MinesweeperAI(game)
    
    move_count = 0
    max_moves = 200  # Prevent infinite loops
    
    print("Initial board:")
    game.print_board()
    
    while not game.game_over and move_count < max_moves:
        print(f"\n--- Move {move_count + 1} ---")
        
        if ai.make_move():
            move_count += 1
            game.print_board()
            print(f"AI reasoning: {ai.explain_last_move()}")
            
            # Show statistics periodically
            if move_count % 10 == 0:
                stats = ai.get_statistics()
                print(f"Statistics: {stats}")
        else:
            print("AI couldn't make a move!")
            break
    
    print(f"\nGame finished after {move_count} moves!")
    stats = ai.get_statistics()
    print(f"Final statistics: {stats}")
    
    if game.game_won:
        print("🎉 AI won the game! 🎉")
    else:
        print("💥 AI hit a mine! 💥")


if __name__ == "__main__":
    create_ai_demo()