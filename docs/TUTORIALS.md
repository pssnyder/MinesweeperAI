# Minesweeper AI Tutorials

This file contains step-by-step tutorials to help you understand and improve the Minesweeper AI. Each tutorial builds on the previous ones, so start from the beginning!

## 📚 Tutorial Structure

Each tutorial includes:
- **Learning Goals**: What you'll understand after completing it
- **Prerequisites**: What you should know before starting
- **Step-by-Step Instructions**: Detailed walkthrough
- **Code Examples**: Working code you can try
- **Exercises**: Practice problems to reinforce learning
- **Solutions**: Complete solutions for reference

---

## 🎯 Tutorial 1: Understanding the Game

**Learning Goals:**
- Understand how Minesweeper works internally
- Learn about the game state and data structures
- Practice reading and modifying existing code

**Prerequisites:**
- Basic Python knowledge (variables, functions, lists)
- Have completed the "Getting Started" guide

### Step 1: Explore the Game Class

Open `src/minesweeper_game.py` and find the `Minesweeper` class.

**Questions to explore:**
1. How is the game board represented?
2. Where are the mines stored?
3. What's the difference between `game_board` and `player_board`?

**Exercise 1.1: Add Debug Output**
Add a method to print the hidden board (with mines visible):

```python
def print_debug_board(self):
    """Print the board with mines visible for debugging."""
    print("Hidden board (for debugging):")
    print("   " + " ".join(f"{i:2}" for i in range(self.cols)))
    print("  " + "---" * self.cols)
    
    for i, row in enumerate(self.game_board):
        print(f"{i:2}| " + " ".join(f"{cell:2}" for cell in row))
```

Try adding this method and calling it in your test games.

### Step 2: Understand Mine Placement

Look at the `_place_mines()` method.

**Questions:**
1. Why use a `set` instead of a `list` for mine positions?
2. How does the random placement work?
3. What prevents two mines from being placed in the same location?

**Exercise 1.2: Custom Mine Placement**
Create a method to place mines in specific positions (useful for testing):

```python
def place_mines_at_positions(self, positions):
    """
    Place mines at specific positions (for testing).
    
    Args:
        positions: List of (row, col) tuples where mines should be placed
    """
    self.mine_positions.clear()
    
    for row in range(self.rows):
        for col in range(self.cols):
            self.game_board[row][col] = '-'
    
    for row, col in positions:
        if self.is_valid_position(row, col):
            self.mine_positions.add((row, col))
            self.game_board[row][col] = '*'
    
    self._fill_numbers()
```

### Step 3: Number Calculation

Study the `_fill_numbers()` method.

**Exercise 1.3: Verify Number Calculation**
Create a test to verify that numbers are calculated correctly:

```python
def test_number_calculation():
    """Test that numbers are calculated correctly."""
    game = Minesweeper(3, 3, 0)  # No mines initially
    
    # Place a mine in the center
    game.place_mines_at_positions([(1, 1)])
    
    # Check that all edge cells show '1'
    expected_ones = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)]
    
    for row, col in expected_ones:
        assert game.game_board[row][col] == '1', f"Cell ({row}, {col}) should be '1'"
    
    print("✅ Number calculation test passed!")
```

---

## 🤖 Tutorial 2: Basic AI Logic

**Learning Goals:**
- Understand how the AI tracks game state
- Implement simple safe move detection
- Learn about constraint satisfaction basics

**Prerequisites:**
- Completed Tutorial 1
- Understanding of sets and basic logic

### Step 1: AI State Management

Look at the `MinesweeperAI` class constructor.

**Key data structures:**
- `uncovered`: Cells the AI has revealed
- `flags`: Cells the AI thinks are mines
- `safe_cells`: Cells the AI knows are safe
- `mine_cells`: Cells the AI knows are mines

**Exercise 2.1: Add State Visualization**
Create a method to visualize what the AI knows:

```python
def print_ai_knowledge(self):
    """Print what the AI knows about each cell."""
    print("AI Knowledge (S=Safe, M=Mine, ?=Unknown):")
    
    for row in range(self.game.rows):
        for col in range(self.game.cols):
            if (row, col) in self.uncovered:
                # Show the actual value
                value = self.game.get_cell_value(row, col)
                print(f"{value:2}", end=" ")
            elif (row, col) in self.safe_cells:
                print(" S", end=" ")
            elif (row, col) in self.mine_cells:
                print(" M", end=" ")
            elif (row, col) in self.flags:
                print(" F", end=" ")
            else:
                print(" ?", end=" ")
        print()  # New line after each row
```

### Step 2: Simple Safe Move Detection

Let's implement basic logic for finding safe moves.

**Exercise 2.2: Complete the Safe Move Function**
Improve the `is_safe_move` method:

```python
def is_safe_move(self, row, col):
    """
    Determine if uncovering a cell is definitely safe.
    
    Args:
        row, col: Position to check
        
    Returns:
        bool: True if definitely safe, False if unknown/unsafe
    """
    # Can't uncover already uncovered or flagged cells
    if (row, col) in self.uncovered or (row, col) in self.flags:
        return False
    
    # If we've identified this cell as safe, it's safe
    if (row, col) in self.safe_cells:
        return True
    
    # If we've identified this cell as a mine, it's not safe
    if (row, col) in self.mine_cells:
        return False
    
    # Check if we can deduce safety from numbered neighbors
    return self._can_deduce_safety(row, col)

def _can_deduce_safety(self, row, col):
    """Check if we can deduce that a cell is safe from its neighbors."""
    for adj_row, adj_col in self.game.get_adjacent_cells(row, col):
        if (adj_row, adj_col) in self.uncovered:
            cell_value = self.game.get_cell_value(adj_row, adj_col)
            
            if cell_value and cell_value.isdigit():
                number = int(cell_value)
                
                # Count flagged mines around this numbered cell
                adjacent_to_numbered = self.game.get_adjacent_cells(adj_row, adj_col)
                flagged_count = sum(1 for r, c in adjacent_to_numbered 
                                  if (r, c) in self.flags)
                
                # If all mines are found, remaining cells are safe
                if flagged_count == number:
                    return True
    
    return False
```

### Step 3: Mine Detection

**Exercise 2.3: Implement Mine Detection**
Add logic to identify definite mines:

```python
def find_definite_mines(self):
    """Find cells that must be mines based on current knowledge."""
    new_mines = set()
    
    for row, col in self.uncovered:
        cell_value = self.game.get_cell_value(row, col)
        
        if cell_value and cell_value.isdigit():
            number = int(cell_value)
            adjacent_cells = self.game.get_adjacent_cells(row, col)
            
            # Count current state around this cell
            covered_cells = []
            flagged_count = 0
            
            for adj_row, adj_col in adjacent_cells:
                if (adj_row, adj_col) in self.flags:
                    flagged_count += 1
                elif self.game.get_cell_value(adj_row, adj_col) == '-':
                    covered_cells.append((adj_row, adj_col))
            
            remaining_mines = number - flagged_count
            
            # If remaining mines equals remaining covered cells,
            # all covered cells must be mines
            if remaining_mines == len(covered_cells) and remaining_mines > 0:
                new_mines.update(covered_cells)
    
    return new_mines
```

---

## 🎲 Tutorial 3: Probability and Uncertainty

**Learning Goals:**
- Understand when logic isn't enough
- Implement basic probability calculation
- Learn to make decisions under uncertainty

**Prerequisites:**
- Completed Tutorials 1 and 2
- Basic understanding of probability

### Step 1: When Logic Fails

Sometimes the AI can't determine with certainty whether a cell is safe. In these cases, we need probability.

**Example scenario:**
```
? ? ?
? 2 ?
? ? ?
```

If no adjacent cells are flagged, we know 2 out of 8 cells are mines, but we don't know which ones.

### Step 2: Basic Probability Calculation

**Exercise 3.1: Simple Probability**
Implement basic probability estimation:

```python
def calculate_basic_probability(self, row, col):
    """
    Calculate basic mine probability for a frontier cell.
    
    Returns:
        float: Probability between 0.0 and 1.0
    """
    if (row, col) in self.safe_cells:
        return 0.0
    if (row, col) in self.mine_cells:
        return 1.0
    
    # Look at numbered neighbors
    probabilities = []
    
    for adj_row, adj_col in self.game.get_adjacent_cells(row, col):
        if (adj_row, adj_col) in self.uncovered:
            cell_value = self.game.get_cell_value(adj_row, adj_col)
            
            if cell_value and cell_value.isdigit():
                prob = self._probability_from_numbered_cell(
                    row, col, adj_row, adj_col, int(cell_value)
                )
                if prob is not None:
                    probabilities.append(prob)
    
    if probabilities:
        return sum(probabilities) / len(probabilities)
    else:
        # Global probability
        return self._global_mine_probability()

def _probability_from_numbered_cell(self, target_row, target_col, 
                                   num_row, num_col, number):
    """Calculate probability based on a single numbered cell."""
    adjacent_cells = self.game.get_adjacent_cells(num_row, num_col)
    
    # Count current state
    unknown_cells = []
    flagged_count = 0
    
    for adj_row, adj_col in adjacent_cells:
        if (adj_row, adj_col) in self.flags:
            flagged_count += 1
        elif self.game.get_cell_value(adj_row, adj_col) == '-':
            unknown_cells.append((adj_row, adj_col))
    
    if (target_row, target_col) not in unknown_cells:
        return None
    
    remaining_mines = number - flagged_count
    
    if len(unknown_cells) == 0:
        return 0.0
    
    return remaining_mines / len(unknown_cells)

def _global_mine_probability(self):
    """Calculate probability based on global mine density."""
    total_cells = self.game.rows * self.game.cols
    uncovered_count = len(self.uncovered)
    flagged_count = len(self.flags)
    
    remaining_cells = total_cells - uncovered_count - flagged_count
    remaining_mines = self.game.mines - flagged_count
    
    if remaining_cells <= 0:
        return 0.0
    
    return max(0.0, remaining_mines / remaining_cells)
```

### Step 3: Making Probabilistic Decisions

**Exercise 3.2: Choose Best Probabilistic Move**
Implement move selection based on probability:

```python
def choose_probabilistic_move(self):
    """
    Choose the cell with the lowest mine probability.
    
    Returns:
        tuple: (row, col) of best move, or None if no moves available
    """
    frontier = self.get_frontier_cells()
    
    if not frontier:
        # No frontier, pick any uncovered cell
        all_cells = [(r, c) for r in range(self.game.rows) 
                     for c in range(self.game.cols)]
        available = [(r, c) for r, c in all_cells 
                    if self.game.get_cell_value(r, c) == '-']
        
        if available:
            return random.choice(available)
        return None
    
    # Calculate probabilities for all frontier cells
    cell_probabilities = []
    
    for row, col in frontier:
        prob = self.calculate_basic_probability(row, col)
        cell_probabilities.append(((row, col), prob))
    
    # Sort by probability (lowest first)
    cell_probabilities.sort(key=lambda x: x[1])
    
    # Return the safest cell
    return cell_probabilities[0][0]
```

---

## 🧩 Tutorial 4: Constraint Satisfaction

**Learning Goals:**
- Understand constraint satisfaction problems
- Implement advanced logical reasoning
- Handle multiple overlapping constraints

**Prerequisites:**
- Completed Tutorials 1-3
- Understanding of logical reasoning

### Step 1: What are Constraints?

In Minesweeper, numbered cells create constraints:
- A cell showing "2" means exactly 2 of its neighbors are mines
- These constraints can interact and help us deduce more information

### Step 2: Representing Constraints

**Exercise 4.1: Constraint Data Structure**
Create a constraint representation:

```python
class Constraint:
    """Represents a constraint from a numbered cell."""
    
    def __init__(self, cells, mine_count, source_cell):
        """
        Args:
            cells: Set of (row, col) tuples that this constraint applies to
            mine_count: Number of mines that must be in these cells
            source_cell: (row, col) of the numbered cell that created this constraint
        """
        self.cells = set(cells)
        self.mine_count = mine_count
        self.source_cell = source_cell
    
    def is_satisfied(self, mine_assignments):
        """
        Check if a mine assignment satisfies this constraint.
        
        Args:
            mine_assignments: Set of (row, col) positions that are mines
            
        Returns:
            bool: True if constraint is satisfied
        """
        mines_in_constraint = len(self.cells.intersection(mine_assignments))
        return mines_in_constraint == self.mine_count
    
    def remove_known_cells(self, known_mines, known_safe):
        """
        Update constraint by removing cells we already know about.
        
        Args:
            known_mines: Set of known mine positions
            known_safe: Set of known safe positions
        """
        # Remove known mines and reduce mine count
        mines_found = self.cells.intersection(known_mines)
        self.mine_count -= len(mines_found)
        self.cells -= mines_found
        
        # Remove known safe cells
        self.cells -= known_safe
    
    def __str__(self):
        return f"Constraint: {self.mine_count} mines in {len(self.cells)} cells from {self.source_cell}"
```

### Step 3: Constraint Solving

**Exercise 4.2: Basic Constraint Solver**
Implement constraint satisfaction logic:

```python
def solve_constraints(self):
    """
    Use constraint satisfaction to find definite safe cells and mines.
    
    Returns:
        tuple: (new_safe_cells, new_mine_cells)
    """
    constraints = self._build_constraints()
    new_safe = set()
    new_mines = set()
    
    # Clean up constraints with known information
    for constraint in constraints:
        constraint.remove_known_cells(self.mine_cells, self.safe_cells)
    
    # Remove empty constraints
    constraints = [c for c in constraints if c.cells]
    
    # Apply simple constraint rules
    for constraint in constraints:
        if constraint.mine_count == 0:
            # All remaining cells are safe
            new_safe.update(constraint.cells)
        elif constraint.mine_count == len(constraint.cells):
            # All remaining cells are mines
            new_mines.update(constraint.cells)
    
    # Apply subset reasoning
    subset_safe, subset_mines = self._apply_subset_reasoning(constraints)
    new_safe.update(subset_safe)
    new_mines.update(subset_mines)
    
    return new_safe, new_mines

def _build_constraints(self):
    """Build constraint objects from current game state."""
    constraints = []
    
    for row, col in self.uncovered:
        cell_value = self.game.get_cell_value(row, col)
        
        if cell_value and cell_value.isdigit():
            number = int(cell_value)
            adjacent_cells = self.game.get_adjacent_cells(row, col)
            
            # Find unknown adjacent cells
            unknown_cells = []
            for adj_row, adj_col in adjacent_cells:
                if self.game.get_cell_value(adj_row, adj_col) == '-':
                    unknown_cells.append((adj_row, adj_col))
            
            if unknown_cells:
                constraint = Constraint(unknown_cells, number, (row, col))
                constraints.append(constraint)
    
    return constraints

def _apply_subset_reasoning(self, constraints):
    """
    Apply subset reasoning to constraints.
    If one constraint is a subset of another, we can deduce more.
    """
    new_safe = set()
    new_mines = set()
    
    for i, c1 in enumerate(constraints):
        for j, c2 in enumerate(constraints):
            if i != j and c1.cells.issubset(c2.cells):
                # c1 is a subset of c2
                remaining_cells = c2.cells - c1.cells
                remaining_mines = c2.mine_count - c1.mine_count
                
                if remaining_mines == 0:
                    new_safe.update(remaining_cells)
                elif remaining_mines == len(remaining_cells):
                    new_mines.update(remaining_cells)
    
    return new_safe, new_mines
```

### Step 4: Integration

**Exercise 4.3: Integrate Constraint Solving**
Update the main AI logic to use constraints:

```python
def make_smart_move(self):
    """
    Enhanced move making with constraint satisfaction.
    """
    if self.game.game_over:
        return False
    
    # Update knowledge from current board
    self._update_knowledge_from_board()
    
    # Use constraint satisfaction
    new_safe, new_mines = self.solve_constraints()
    self.safe_cells.update(new_safe)
    self.mine_cells.update(new_mines)
    
    # Flag newly discovered mines
    for mine_row, mine_col in new_mines:
        if (mine_row, mine_col) not in self.flags:
            self.flag(mine_row, mine_col)
            return True
    
    # Uncover newly discovered safe cells
    for safe_row, safe_col in new_safe:
        if self.game.get_cell_value(safe_row, safe_col) == '-':
            self.uncover(safe_row, safe_col)
            return True
    
    # Fall back to probability
    prob_move = self.choose_probabilistic_move()
    if prob_move:
        self.uncover(*prob_move)
        return True
    
    return False

def _update_knowledge_from_board(self):
    """Update AI knowledge based on current board state."""
    for row in range(self.game.rows):
        for col in range(self.game.cols):
            cell_value = self.game.get_cell_value(row, col)
            
            if (cell_value and cell_value.isdigit() and 
                (row, col) not in self.uncovered):
                self.uncovered.add((row, col))
```

---

## 🏆 Tutorial 5: Advanced Techniques

**Learning Goals:**
- Implement pattern recognition
- Add performance optimization
- Create learning and adaptation

**Prerequisites:**
- Completed Tutorials 1-4
- Strong understanding of algorithms

### Step 1: Pattern Recognition

Some Minesweeper patterns have known solutions.

**Exercise 5.1: Implement 1-2-1 Pattern**
This is a common pattern where the middle cell is always safe:

```python
def detect_121_pattern(self):
    """
    Detect and solve 1-2-1 patterns.
    
    Pattern:
    ? ? ?
    1 2 1
    
    Solution: Middle top cell is always safe
    """
    new_safe = set()
    
    # Check horizontal 1-2-1 patterns
    for row in range(self.game.rows):
        for col in range(self.game.cols - 2):
            if self._is_121_horizontal(row, col):
                # Add safe cells above the pattern
                if row > 0:
                    new_safe.add((row - 1, col + 1))
    
    # Check vertical 1-2-1 patterns  
    for row in range(self.game.rows - 2):
        for col in range(self.game.cols):
            if self._is_121_vertical(row, col):
                # Add safe cells to the right of the pattern
                if col < self.game.cols - 1:
                    new_safe.add((row + 1, col + 1))
    
    return new_safe

def _is_121_horizontal(self, row, col):
    """Check if there's a horizontal 1-2-1 pattern starting at (row, col)."""
    try:
        values = [
            self.game.get_cell_value(row, col),
            self.game.get_cell_value(row, col + 1),
            self.game.get_cell_value(row, col + 2)
        ]
        return values == ['1', '2', '1']
    except:
        return False

def _is_121_vertical(self, row, col):
    """Check if there's a vertical 1-2-1 pattern starting at (row, col)."""
    try:
        values = [
            self.game.get_cell_value(row, col),
            self.game.get_cell_value(row + 1, col),
            self.game.get_cell_value(row + 2, col)
        ]
        return values == ['1', '2', '1']
    except:
        return False
```

### Step 2: Performance Optimization

**Exercise 5.2: Caching and Memoization**
Cache expensive calculations:

```python
from functools import lru_cache

class OptimizedMinesweeperAI(MinesweeperAI):
    """AI with performance optimizations."""
    
    def __init__(self, game):
        super().__init__(game)
        self._probability_cache = {}
        self._constraint_cache = {}
    
    def clear_caches(self):
        """Clear all caches when game state changes significantly."""
        self._probability_cache.clear()
        self._constraint_cache.clear()
    
    @lru_cache(maxsize=128)
    def _cached_adjacency(self, row, col):
        """Cache adjacent cell calculations."""
        return tuple(self.game.get_adjacent_cells(row, col))
    
    def calculate_probability_cached(self, row, col):
        """Calculate probability with caching."""
        cache_key = (row, col, len(self.uncovered), len(self.flags))
        
        if cache_key in self._probability_cache:
            return self._probability_cache[cache_key]
        
        prob = self.calculate_basic_probability(row, col)
        self._probability_cache[cache_key] = prob
        return prob
```

### Step 3: Learning and Adaptation

**Exercise 5.3: Move Quality Assessment**
Learn from successful and unsuccessful moves:

```python
class LearningMinesweeperAI(OptimizedMinesweeperAI):
    """AI that learns from its moves."""
    
    def __init__(self, game):
        super().__init__(game)
        self.move_quality_history = []
        self.pattern_success_rates = {}
    
    def assess_move_quality(self, row, col, was_successful):
        """
        Assess the quality of a move after seeing the result.
        
        Args:
            row, col: Position of the move
            was_successful: True if move was safe, False if hit mine
        """
        move_info = {
            'position': (row, col),
            'successful': was_successful,
            'probability_estimate': self.calculate_probability_cached(row, col),
            'move_type': self._classify_move_type(row, col),
            'game_state': self._get_game_state_signature()
        }
        
        self.move_quality_history.append(move_info)
        
        # Update pattern success rates
        pattern = self._identify_local_pattern(row, col)
        if pattern:
            if pattern not in self.pattern_success_rates:
                self.pattern_success_rates[pattern] = {'successes': 0, 'attempts': 0}
            
            self.pattern_success_rates[pattern]['attempts'] += 1
            if was_successful:
                self.pattern_success_rates[pattern]['successes'] += 1
    
    def _classify_move_type(self, row, col):
        """Classify what type of move this was."""
        if (row, col) in self.safe_cells:
            return 'logical_safe'
        elif (row, col) in self.get_frontier_cells():
            return 'probabilistic_frontier'
        else:
            return 'random_guess'
    
    def _get_game_state_signature(self):
        """Create a signature of the current game state."""
        return (
            len(self.uncovered),
            len(self.flags),
            len(self.get_frontier_cells())
        )
    
    def _identify_local_pattern(self, row, col):
        """Identify the local pattern around a cell."""
        pattern = []
        for r in range(max(0, row-1), min(self.game.rows, row+2)):
            pattern_row = []
            for c in range(max(0, col-1), min(self.game.cols, col+2)):
                value = self.game.get_cell_value(r, c)
                pattern_row.append(value if value else '?')
            pattern.append(''.join(pattern_row))
        return tuple(pattern)
    
    def get_learning_stats(self):
        """Get statistics about learning progress."""
        if not self.move_quality_history:
            return {}
        
        total_moves = len(self.move_quality_history)
        successful_moves = sum(1 for move in self.move_quality_history if move['successful'])
        
        move_types = {}
        for move in self.move_quality_history:
            move_type = move['move_type']
            if move_type not in move_types:
                move_types[move_type] = {'successes': 0, 'attempts': 0}
            move_types[move_type]['attempts'] += 1
            if move['successful']:
                move_types[move_type]['successes'] += 1
        
        return {
            'total_moves': total_moves,
            'success_rate': successful_moves / total_moves,
            'move_type_stats': move_types,
            'pattern_stats': self.pattern_success_rates
        }
```

---

## 🎓 Final Project: Complete AI Integration

**Goal**: Combine all techniques into a comprehensive AI.

**Exercise: Build the Ultimate AI**
Create a final AI class that uses all the techniques you've learned:

```python
class UltimateMinesweeperAI(LearningMinesweeperAI):
    """
    The complete AI implementation using all learned techniques.
    """
    
    def make_ultimate_move(self):
        """
        Make the best possible move using all available techniques.
        """
        if self.game.game_over:
            return False
        
        # 1. Pattern recognition
        pattern_safe = self.detect_121_pattern()
        if pattern_safe:
            self.safe_cells.update(pattern_safe)
            for row, col in pattern_safe:
                if self.game.get_cell_value(row, col) == '-':
                    result = self.uncover(row, col)
                    self.assess_move_quality(row, col, result)
                    return result
        
        # 2. Constraint satisfaction
        new_safe, new_mines = self.solve_constraints()
        self.safe_cells.update(new_safe)
        self.mine_cells.update(new_mines)
        
        # 3. Flag mines
        for mine_row, mine_col in new_mines:
            if (mine_row, mine_col) not in self.flags:
                self.flag(mine_row, mine_col)
                return True
        
        # 4. Uncover safe cells
        for safe_row, safe_col in new_safe:
            if self.game.get_cell_value(safe_row, safe_col) == '-':
                result = self.uncover(safe_row, safe_col)
                self.assess_move_quality(safe_row, safe_col, result)
                return result
        
        # 5. Probabilistic reasoning with learning
        prob_move = self._choose_learned_probabilistic_move()
        if prob_move:
            result = self.uncover(*prob_move)
            self.assess_move_quality(prob_move[0], prob_move[1], result)
            return result
        
        return False
    
    def _choose_learned_probabilistic_move(self):
        """Choose probabilistic move enhanced with learning."""
        frontier = self.get_frontier_cells()
        
        if not frontier:
            return None
        
        # Calculate probabilities with pattern learning adjustment
        best_cell = None
        best_score = float('inf')
        
        for row, col in frontier:
            base_prob = self.calculate_probability_cached(row, col)
            
            # Adjust based on learned patterns
            pattern = self._identify_local_pattern(row, col)
            if pattern in self.pattern_success_rates:
                stats = self.pattern_success_rates[pattern]
                if stats['attempts'] > 5:  # Only use if we have enough data
                    learned_success_rate = stats['successes'] / stats['attempts']
                    # Combine base probability with learned success rate
                    adjusted_prob = base_prob * (2 - learned_success_rate)
                else:
                    adjusted_prob = base_prob
            else:
                adjusted_prob = base_prob
            
            if adjusted_prob < best_score:
                best_score = adjusted_prob
                best_cell = (row, col)
        
        return best_cell
```

---

## 🎯 Practice Challenges

### Challenge 1: Custom Patterns
Implement detection for these patterns:
- 1-1 adjacent pattern
- Corner patterns
- Edge patterns

### Challenge 2: Advanced Constraints
- Implement overlapping constraint resolution
- Add constraint simplification
- Handle contradiction detection

### Challenge 3: Performance
- Benchmark your AI against different board sizes
- Optimize for speed vs. accuracy trade-offs
- Implement multi-threading for constraint solving

### Challenge 4: Machine Learning
- Collect training data from many games
- Train a neural network to predict mine probabilities
- Compare ML approach with logical reasoning

---

## ✅ Solutions and Testing

Each tutorial includes complete working solutions in the `solutions/` directory. Test your implementations against these to verify correctness.

**Running Tests:**
```bash
python -m pytest tests/tutorial_tests.py -v
```

**Benchmarking:**
```bash
python examples/benchmark_ai.py
```

Remember: The goal is learning, not just completing the exercises. Take time to understand each concept before moving on!

---

**Happy Learning! 🎉**