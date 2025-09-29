"""
Basic tests for the Minesweeper AI project.

These tests verify that the core functionality works correctly.
"""

import sys
import os
import unittest

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from minesweeper_game import Minesweeper, create_game_from_difficulty
    from minesweeper_ai import MinesweeperAI
except ImportError as e:
    print(f"Could not import modules: {e}")
    print("Make sure you're running tests from the project root directory.")
    sys.exit(1)


class TestMinesweeper(unittest.TestCase):
    """Test cases for the Minesweeper game class."""
    
    def test_game_creation(self):
        """Test that games are created correctly."""
        game = Minesweeper(5, 5, 3)
        
        self.assertEqual(game.rows, 5)
        self.assertEqual(game.cols, 5)
        self.assertEqual(game.mines, 3)
        self.assertFalse(game.game_over)
        self.assertFalse(game.game_won)
        self.assertEqual(len(game.mine_positions), 3)
    
    def test_invalid_parameters(self):
        """Test that invalid parameters raise ValueError."""
        with self.assertRaises(ValueError):
            Minesweeper(0, 5, 3)  # Invalid rows
        
        with self.assertRaises(ValueError):
            Minesweeper(5, 0, 3)  # Invalid cols
        
        with self.assertRaises(ValueError):
            Minesweeper(5, 5, 25)  # Too many mines
        
        with self.assertRaises(ValueError):
            Minesweeper(5, 5, -1)  # Negative mines
    
    def test_position_validation(self):
        """Test position validation."""
        game = Minesweeper(3, 3, 1)
        
        self.assertTrue(game.is_valid_position(0, 0))
        self.assertTrue(game.is_valid_position(2, 2))
        self.assertFalse(game.is_valid_position(-1, 0))
        self.assertFalse(game.is_valid_position(0, -1))
        self.assertFalse(game.is_valid_position(3, 0))
        self.assertFalse(game.is_valid_position(0, 3))
    
    def test_adjacent_cells(self):
        """Test adjacent cell calculation."""
        game = Minesweeper(3, 3, 1)
        
        # Center cell should have 8 neighbors
        adjacent = game.get_adjacent_cells(1, 1)
        self.assertEqual(len(adjacent), 8)
        
        # Corner cell should have 3 neighbors
        adjacent = game.get_adjacent_cells(0, 0)
        self.assertEqual(len(adjacent), 3)
        
        # Edge cell should have 5 neighbors
        adjacent = game.get_adjacent_cells(0, 1)
        self.assertEqual(len(adjacent), 5)
    
    def test_uncover_safe_cell(self):
        """Test uncovering a safe cell."""
        game = Minesweeper(5, 5, 0)  # No mines for predictable testing
        
        # Should succeed
        result = game.uncover(2, 2)
        self.assertTrue(result)
        self.assertFalse(game.game_over)
        
        # Cell should now be uncovered
        cell_value = game.get_cell_value(2, 2)
        self.assertNotEqual(cell_value, '-')
    
    def test_flagging(self):
        """Test cell flagging functionality."""
        game = Minesweeper(3, 3, 1)
        
        # Should be able to flag
        result = game.flag(0, 0)
        self.assertTrue(result)
        self.assertEqual(game.get_cell_value(0, 0), 'F')
        
        # Should be able to unflag
        result = game.flag(0, 0)
        self.assertTrue(result)
        self.assertEqual(game.get_cell_value(0, 0), '-')
    
    def test_difficulty_creation(self):
        """Test difficulty-based game creation."""
        beginner = create_game_from_difficulty('beginner')
        self.assertEqual(beginner.rows, 9)
        self.assertEqual(beginner.cols, 9)
        self.assertEqual(beginner.mines, 10)
        
        intermediate = create_game_from_difficulty('intermediate')
        self.assertEqual(intermediate.rows, 16)
        self.assertEqual(intermediate.cols, 16)
        self.assertEqual(intermediate.mines, 40)
        
        with self.assertRaises(ValueError):
            create_game_from_difficulty('invalid')


class TestMinesweeperAI(unittest.TestCase):
    """Test cases for the Minesweeper AI class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = Minesweeper(5, 5, 3)
        self.ai = MinesweeperAI(self.game)
    
    def test_ai_creation(self):
        """Test AI initialization."""
        self.assertEqual(len(self.ai.uncovered), 0)
        self.assertEqual(len(self.ai.flags), 0)
        self.assertEqual(len(self.ai.safe_cells), 0)
        self.assertEqual(len(self.ai.mine_cells), 0)
    
    def test_ai_reset(self):
        """Test AI state reset."""
        # Make some moves to change AI state
        self.ai.safe_cells.add((1, 1))
        self.ai.flags.add((2, 2))
        
        # Reset should clear everything
        self.ai.reset()
        
        self.assertEqual(len(self.ai.uncovered), 0)
        self.assertEqual(len(self.ai.flags), 0)
        self.assertEqual(len(self.ai.safe_cells), 0)
        self.assertEqual(len(self.ai.mine_cells), 0)
    
    def test_frontier_cells(self):
        """Test frontier cell detection."""
        # Initially no frontier (no uncovered cells)
        frontier = self.ai.get_frontier_cells()
        self.assertEqual(len(frontier), 0)
        
        # Uncover a cell to create frontier
        self.game.uncover(2, 2)
        self.ai.uncovered.add((2, 2))
        
        frontier = self.ai.get_frontier_cells()
        self.assertGreater(len(frontier), 0)
    
    def test_make_move(self):
        """Test that AI can make moves without crashing."""
        moves_made = 0
        max_moves = 10
        
        while not self.game.game_over and moves_made < max_moves:
            if self.ai.make_move():
                moves_made += 1
            else:
                break
        
        # AI should have made at least one move
        self.assertGreater(moves_made, 0)
    
    def test_statistics(self):
        """Test AI statistics collection."""
        stats = self.ai.get_statistics()
        
        # Should return a dictionary with expected keys
        expected_keys = [
            'moves_made', 'cells_uncovered', 'mines_flagged',
            'safe_cells_identified', 'mine_cells_identified',
            'constraints_active', 'game_won', 'game_over'
        ]
        
        for key in expected_keys:
            self.assertIn(key, stats)


class TestGameIntegration(unittest.TestCase):
    """Integration tests for game and AI working together."""
    
    def test_complete_game_simulation(self):
        """Test a complete game simulation."""
        game = Minesweeper(5, 5, 2)  # Small game for faster testing
        ai = MinesweeperAI(game)
        
        moves_made = 0
        max_moves = 50  # Prevent infinite loops
        
        while not game.game_over and moves_made < max_moves:
            if ai.make_move():
                moves_made += 1
            else:
                # AI couldn't make a move, game might be stuck
                break
        
        # Game should have ended in some way
        self.assertTrue(game.game_over or moves_made >= max_moves)
        
        # AI should have made some moves
        self.assertGreater(moves_made, 0)
        
        # Statistics should be reasonable
        stats = ai.get_statistics()
        self.assertEqual(stats['moves_made'], moves_made)
        self.assertGreaterEqual(stats['cells_uncovered'], 0)
        self.assertGreaterEqual(stats['mines_flagged'], 0)
    
    def test_no_mine_game(self):
        """Test game with no mines (should always win)."""
        game = Minesweeper(3, 3, 0)  # No mines
        ai = MinesweeperAI(game)
        
        moves_made = 0
        max_moves = 20
        
        while not game.game_over and moves_made < max_moves:
            if ai.make_move():
                moves_made += 1
            else:
                break
        
        # Should win a game with no mines
        self.assertTrue(game.game_won)
    
    def test_probability_calculation(self):
        """Test that probability calculation doesn't crash."""
        game = Minesweeper(5, 5, 3)
        ai = MinesweeperAI(game)
        
        # Make a move to create some state
        ai.make_move()
        
        # Calculate probabilities
        try:
            probs = ai.calculate_mine_probabilities()
            
            # Should return a dictionary
            self.assertIsInstance(probs, dict)
            
            # All probabilities should be between 0 and 1
            for prob in probs.values():
                self.assertGreaterEqual(prob, 0.0)
                self.assertLessEqual(prob, 1.0)
                
        except Exception as e:
            self.fail(f"Probability calculation failed: {e}")


def run_basic_smoke_test():
    """Run a quick smoke test to verify basic functionality."""
    print("Running basic smoke test...")
    
    try:
        # Test game creation
        game = Minesweeper(5, 5, 3)
        print("✓ Game creation works")
        
        # Test AI creation
        ai = MinesweeperAI(game)
        print("✓ AI creation works")
        
        # Test making moves
        move_count = 0
        while move_count < 5 and not game.game_over:
            if ai.make_move():
                move_count += 1
            else:
                break
        
        print(f"✓ AI made {move_count} moves successfully")
        
        # Test statistics
        stats = ai.get_statistics()
        print(f"✓ Statistics: {stats}")
        
        print("🎉 Basic smoke test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")
        return False


if __name__ == '__main__':
    print("Minesweeper AI Test Suite")
    print("=" * 40)
    
    # Run smoke test first
    if not run_basic_smoke_test():
        print("\nBasic functionality failed. Skipping unit tests.")
        sys.exit(1)
    
    print("\nRunning unit tests...")
    print("=" * 40)
    
    # Run unit tests
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 40)
    print("Test suite completed!")