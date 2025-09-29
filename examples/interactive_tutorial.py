#!/usr/bin/env python3
"""
Interactive Minesweeper AI Tutorial

A guided, interactive tutorial that walks new programmers through
understanding and improving the Minesweeper AI step by step.
"""

import sys
import os
import time
import random

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from minesweeper_game import Minesweeper, create_game_from_difficulty
    from minesweeper_ai import MinesweeperAI
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running this from the project root directory.")
    sys.exit(1)


class InteractiveTutorial:
    """
    An interactive tutorial system that guides users through learning
    Minesweeper AI concepts step by step.
    """
    
    def __init__(self):
        self.current_lesson = 0
        self.user_progress = {}
        
    def start(self):
        """Start the interactive tutorial."""
        self.print_welcome()
        
        lessons = [
            self.lesson_1_game_basics,
            self.lesson_2_ai_introduction,
            self.lesson_3_safe_moves,
            self.lesson_4_probability,
            self.lesson_5_advanced_ai
        ]
        
        while self.current_lesson < len(lessons):
            lesson_func = lessons[self.current_lesson]
            
            print(f"\n{'='*60}")
            print(f"LESSON {self.current_lesson + 1}")
            print(f"{'='*60}")
            
            try:
                lesson_func()
                self.current_lesson += 1
            except KeyboardInterrupt:
                print("\n\nTutorial interrupted. Your progress has been saved!")
                break
            except Exception as e:
                print(f"\nError in lesson: {e}")
                choice = input("Continue anyway? (y/n): ").lower()
                if choice == 'y':
                    self.current_lesson += 1
                else:
                    break
        
        self.print_conclusion()
    
    def print_welcome(self):
        """Print welcome message and introduction."""
        print("🎮 Welcome to the Interactive Minesweeper AI Tutorial! 🤖")
        print("\nThis tutorial will teach you:")
        print("• How Minesweeper works internally")
        print("• Basic AI concepts and logical reasoning")
        print("• Probability and decision making under uncertainty")
        print("• Advanced AI techniques")
        print("\nYou'll learn by:")
        print("• Playing interactive examples")
        print("• Watching the AI make decisions")
        print("• Completing hands-on coding exercises")
        print("• Building your own AI improvements")
        
        input("\nPress Enter to begin your journey...")
    
    def lesson_1_game_basics(self):
        """Lesson 1: Understanding Minesweeper game mechanics."""
        print("🎯 LESSON 1: Understanding Minesweeper")
        print("\nFirst, let's make sure you understand how Minesweeper works.")
        
        # Create a simple game for demonstration
        print("\nCreating a small 5x5 game with 3 mines for demonstration...")
        game = Minesweeper(5, 5, 3)
        
        print("\nThis is what the player sees initially:")
        game.print_board()
        
        print("\nAnd this is what's actually hidden underneath:")
        game.print_board(show_hidden=True)
        
        print("\nNotice:")
        print("• Mines are marked with '*'")
        print("• Numbers show how many mines are adjacent to that cell")
        print("• The player only sees '-' (unknown cells) initially")
        
        self.interactive_game_demo(game)
        
        print("\n✅ Lesson 1 Complete! You understand the basic game mechanics.")
        input("Press Enter to continue to Lesson 2...")
    
    def interactive_game_demo(self, game):
        """Let the user try a few moves to understand the game."""
        print("\n🎮 Try making a few moves to see how the game works!")
        print("Commands:")
        print("• 'u row col' to uncover a cell (e.g., 'u 2 2')")
        print("• 'f row col' to flag a cell")
        print("• 'show' to see the hidden board (cheating!)")
        print("• 'done' to finish this demo")
        
        moves_made = 0
        while moves_made < 5 and not game.game_over:
            print(f"\nCurrent board (Move {moves_made + 1}):")
            game.print_board()
            
            try:
                command = input("Enter command: ").strip().split()
                
                if not command:
                    continue
                elif command[0] == 'done':
                    break
                elif command[0] == 'show':
                    print("Hidden board:")
                    game.print_board(show_hidden=True)
                    continue
                elif len(command) == 3:
                    action, row_str, col_str = command
                    row, col = int(row_str), int(col_str)
                    
                    if action == 'u':
                        result = game.uncover(row, col)
                        moves_made += 1
                        if not result:
                            print("💥 You hit a mine! Don't worry, this is just practice.")
                            game.print_board(show_hidden=True)
                            break
                        else:
                            cell_value = game.get_cell_value(row, col)
                            if cell_value.isdigit():
                                print(f"Good! Cell ({row}, {col}) has {cell_value} adjacent mines.")
                            elif cell_value == '0':
                                print(f"Great! Cell ({row}, {col}) has no adjacent mines, so nearby cells are auto-revealed.")
                    elif action == 'f':
                        game.flag(row, col)
                        print(f"Flagged cell ({row}, {col}) as a potential mine.")
                else:
                    print("Invalid command. Try 'u 2 2' or 'f 1 3'")
                    
            except (ValueError, IndexError):
                print("Invalid input. Use format like 'u 2 2' or 'f 1 3'")
            except Exception as e:
                print(f"Error: {e}")
        
        print("\nGood job exploring the game mechanics!")
    
    def lesson_2_ai_introduction(self):
        """Lesson 2: Introduction to AI decision making."""
        print("🤖 LESSON 2: Introduction to AI Decision Making")
        print("\nNow let's see how an AI can play Minesweeper!")
        
        print("\nCreating a new game and AI...")
        game = create_game_from_difficulty('beginner')
        ai = MinesweeperAI(game)
        
        print("Initial board:")
        game.print_board()
        
        print("\nLet's watch the AI make its first few moves...")
        
        for move_num in range(5):
            if game.game_over:
                break
                
            print(f"\n--- AI Move {move_num + 1} ---")
            
            # Show what the AI is thinking
            print("AI is analyzing the board...")
            time.sleep(1)  # Dramatic pause
            
            if ai.make_move():
                print("AI made a move!")
                game.print_board()
                
                # Explain the move
                if hasattr(ai, 'explain_last_move'):
                    print(f"AI reasoning: {ai.explain_last_move()}")
                
                # Show AI's internal state
                print(f"AI has uncovered {len(ai.uncovered)} cells")
                print(f"AI has flagged {len(ai.flags)} cells")
                
            else:
                print("AI couldn't find a good move.")
                break
            
            input("Press Enter to see the next move...")
        
        print("\n🧠 What did you notice about the AI's decision making?")
        observations = input("What patterns did you see? (Press Enter to continue): ")
        
        if observations.strip():
            print(f"Great observation: {observations}")
        
        print("\n✅ Lesson 2 Complete! You've seen basic AI decision making.")
        input("Press Enter to continue to Lesson 3...")
    
    def lesson_3_safe_moves(self):
        """Lesson 3: Understanding safe move detection."""
        print("🎯 LESSON 3: Safe Move Detection")
        print("\nLet's learn how the AI determines which moves are 100% safe!")
        
        print("\nI'll create a specific scenario to demonstrate logical reasoning...")
        
        # Create a custom scenario for teaching
        game = Minesweeper(5, 5, 3)
        
        # Manually set up a teaching scenario
        game.mine_positions = {(0, 0), (2, 2), (4, 4)}
        game._place_mines = lambda: None  # Don't place random mines
        
        # Rebuild the board with our custom mine placement
        for row in range(5):
            for col in range(5):
                if (row, col) in game.mine_positions:
                    game.game_board[row][col] = '*'
                else:
                    game.game_board[row][col] = '-'
        game._fill_numbers()
        
        # Simulate some moves to create an interesting scenario
        game.uncover(1, 1)  # Should be safe and reveal a number
        game.uncover(3, 3)  # Another safe cell
        
        print("Here's a scenario where the AI can use logic:")
        game.print_board()
        
        print("\nLet's analyze what the AI can deduce...")
        
        # Show the logical reasoning process
        for row in range(game.rows):
            for col in range(game.cols):
                cell_value = game.get_cell_value(row, col)
                if cell_value and cell_value.isdigit():
                    number = int(cell_value)
                    adjacent = game.get_adjacent_cells(row, col)
                    
                    print(f"\nCell ({row}, {col}) shows '{number}'")
                    print(f"This means {number} of its {len(adjacent)} neighbors contain mines")
                    
                    # Count what we know
                    unknown_neighbors = []
                    for adj_row, adj_col in adjacent:
                        if game.get_cell_value(adj_row, adj_col) == '-':
                            unknown_neighbors.append((adj_row, adj_col))
                    
                    print(f"Unknown neighbors: {unknown_neighbors}")
                    
                    if number == 0:
                        print("→ Since the number is 0, ALL unknown neighbors are safe!")
                    elif number == len(unknown_neighbors):
                        print("→ Since we need all remaining cells to be mines, they're all dangerous!")
        
        print("\n🧪 YOUR TURN: Let's implement safe move detection together!")
        print("\nI'll show you a simple version of the logic:")
        
        self.coding_exercise_safe_moves(game)
        
        print("\n✅ Lesson 3 Complete! You understand logical deduction.")
        input("Press Enter to continue to Lesson 4...")
    
    def coding_exercise_safe_moves(self, game):
        """Interactive coding exercise for safe move detection."""
        print("\n" + "="*50)
        print("CODING EXERCISE: Safe Move Detection")
        print("="*50)
        
        print("\nHere's a simple function to find safe moves:")
        print("""
def find_safe_moves(game):
    safe_moves = []
    
    # Look at each uncovered numbered cell
    for row in range(game.rows):
        for col in range(game.cols):
            cell_value = game.get_cell_value(row, col)
            
            if cell_value and cell_value.isdigit():
                number = int(cell_value)
                adjacent = game.get_adjacent_cells(row, col)
                
                # Count flagged neighbors (mines we've already found)
                flagged_count = 0
                unknown_neighbors = []
                
                for adj_row, adj_col in adjacent:
                    neighbor_value = game.get_cell_value(adj_row, adj_col)
                    if neighbor_value == 'F':  # Flagged
                        flagged_count += 1
                    elif neighbor_value == '-':  # Unknown
                        unknown_neighbors.append((adj_row, adj_col))
                
                # If we've found all the mines for this number,
                # the rest are safe!
                if flagged_count == number:
                    safe_moves.extend(unknown_neighbors)
    
    return safe_moves
""")
        
        print("\n🤔 Can you trace through this logic?")
        print("Think about what happens when:")
        print("1. A cell shows '1' and has 1 flagged neighbor")
        print("2. A cell shows '2' and has 2 flagged neighbors")
        
        understanding = input("\nDo you understand how this works? (y/n): ").lower()
        
        if understanding == 'y':
            print("Excellent! This is the foundation of AI logical reasoning.")
        else:
            print("No worries! Let's break it down step by step...")
            print("\nThe key insight: If a numbered cell has already found all its mines,")
            print("then any remaining unknown neighbors must be safe to uncover.")
            
        print("\nTry to think of other logical rules we could implement...")
        user_ideas = input("Any ideas? (Press Enter to continue): ")
        
        if user_ideas.strip():
            print(f"Great thinking: {user_ideas}")
            print("These kinds of insights are how we build better AI!")
    
    def lesson_4_probability(self):
        """Lesson 4: Probability and uncertainty."""
        print("🎲 LESSON 4: Dealing with Uncertainty")
        print("\nSometimes logic alone isn't enough. We need probability!")
        
        print("\nImagine this scenario:")
        self.demonstrate_probability_scenario()
        
        print("\n🧮 Let's learn about probability calculation...")
        self.probability_exercise()
        
        print("\n✅ Lesson 4 Complete! You understand probabilistic reasoning.")
        input("Press Enter to continue to Lesson 5...")
    
    def demonstrate_probability_scenario(self):
        """Show a scenario where probability is needed."""
        print("""
        ? ? ?
        ? 2 ?
        ? ? ?
        
        Here, we know exactly 2 of the 8 unknown cells contain mines.
        But which 2? Logic alone can't tell us!
        
        This is where probability comes in:
        • Each cell has a 2/8 = 25% chance of being a mine
        • We should choose cells with the LOWEST probability
        • Sometimes we have to make educated guesses
        """)
        
        print("\nReal scenarios are more complex:")
        print("• Multiple numbered cells create overlapping constraints")
        print("• Some cells might be constrained by multiple numbers")
        print("• We need to consider global mine density")
        
    def probability_exercise(self):
        """Interactive probability calculation exercise."""
        print("\n" + "="*50)
        print("PROBABILITY EXERCISE")
        print("="*50)
        
        scenarios = [
            {
                'description': "A cell shows '1' with 3 unknown neighbors and 0 flagged",
                'answer': 1/3,
                'explanation': "1 mine among 3 cells = 1/3 ≈ 33.3%"
            },
            {
                'description': "A cell shows '2' with 5 unknown neighbors and 1 flagged",
                'answer': 1/5,
                'explanation': "Need 1 more mine among 5 cells = 1/5 = 20%"
            },
            {
                'description': "Global: 10 mines total, 50 cells left, 3 mines flagged",
                'answer': 7/50,
                'explanation': "7 remaining mines among 50 cells = 7/50 = 14%"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\nScenario {i}: {scenario['description']}")
            print("What's the probability that any given unknown cell is a mine?")
            
            try:
                user_answer = input("Enter probability as decimal (e.g., 0.25): ")
                user_prob = float(user_answer)
                
                correct_prob = scenario['answer']
                
                if abs(user_prob - correct_prob) < 0.01:
                    print("🎉 Correct!")
                else:
                    print(f"Not quite. The answer is {correct_prob:.3f}")
                
                print(f"Explanation: {scenario['explanation']}")
                
            except ValueError:
                print(f"The answer is {scenario['answer']:.3f}")
                print(f"Explanation: {scenario['explanation']}")
    
    def lesson_5_advanced_ai(self):
        """Lesson 5: Advanced AI techniques."""
        print("🚀 LESSON 5: Advanced AI Techniques")
        print("\nLet's explore cutting-edge AI concepts!")
        
        print("\nAdvanced techniques include:")
        print("• Constraint Satisfaction Problems (CSP)")
        print("• Pattern recognition")
        print("• Monte Carlo simulation")
        print("• Machine learning approaches")
        
        self.demonstrate_constraint_satisfaction()
        self.discuss_future_improvements()
        
        print("\n🎓 Congratulations! You've completed the tutorial!")
    
    def demonstrate_constraint_satisfaction(self):
        """Show how constraint satisfaction works."""
        print("\n🧩 Constraint Satisfaction Problems (CSP)")
        print("\nCSP is about finding solutions that satisfy multiple constraints.")
        
        print("\nExample scenario:")
        print("""
        A B C
        1 2 1
        D E F
        
        Constraints:
        • Left '1': exactly 1 mine among {A, B, D, E}
        • Center '2': exactly 2 mines among {A, B, C, E, F}
        • Right '1': exactly 1 mine among {B, C, E, F}
        
        By combining these constraints, we can deduce:
        • If {A, B, D, E} has 1 mine and {A, B, C, E, F} has 2 mines,
          then {C, F} must have exactly 1 mine
        • If {B, C, E, F} has 1 mine and we know {C, F} has 1 mine,
          then {B, E} must have 0 mines (they're safe!)
        """)
        
        print("\nThis is much more powerful than analyzing each constraint separately!")
    
    def discuss_future_improvements(self):
        """Discuss potential AI improvements."""
        print("\n🔮 Future AI Improvements")
        print("\nHere are some advanced ideas you could implement:")
        
        improvements = [
            ("Pattern Recognition", "Recognize common patterns and their solutions"),
            ("Monte Carlo Methods", "Use random simulation when exact calculation is too hard"),
            ("Neural Networks", "Train AI to recognize good moves from examples"),
            ("Genetic Algorithms", "Evolve AI strategies through natural selection"),
            ("Reinforcement Learning", "Let AI learn by playing many games"),
            ("Multi-step Planning", "Think several moves ahead"),
            ("Uncertainty Reasoning", "Handle incomplete information better")
        ]
        
        for technique, description in improvements:
            print(f"• {technique}: {description}")
        
        print("\n💡 Your Challenge:")
        print("Pick one of these techniques and try to implement it!")
        print("Start small, test thoroughly, and have fun learning!")
        
        choice = input("\nWhich technique interests you most? ").strip()
        if choice:
            print(f"Great choice! {choice} is a fascinating area to explore.")
            print("Check the documentation for implementation ideas.")
    
    def print_conclusion(self):
        """Print tutorial conclusion and next steps."""
        print("\n" + "="*60)
        print("🎉 TUTORIAL COMPLETE! 🎉")
        print("="*60)
        
        print("\nWhat you've learned:")
        print("✅ How Minesweeper works internally")
        print("✅ Basic AI decision making")
        print("✅ Logical deduction and safe move detection")
        print("✅ Probability and uncertainty handling")
        print("✅ Advanced AI concepts")
        
        print("\nNext Steps:")
        print("🔬 Experiment with the code in src/")
        print("📚 Read the detailed tutorials in docs/TUTORIALS.md")
        print("🛠️ Try the coding exercises")
        print("🚀 Implement your own AI improvements")
        print("🤝 Contribute to the project!")
        
        print("\nRemember:")
        print("• Learning AI is a journey, not a destination")
        print("• Start simple and gradually add complexity")
        print("• Test your ideas thoroughly")
        print("• Don't be afraid to experiment!")
        
        print("\n🎓 Happy coding, and welcome to the world of AI! 🤖")


def main():
    """Main function to start the interactive tutorial."""
    try:
        tutorial = InteractiveTutorial()
        tutorial.start()
    except KeyboardInterrupt:
        print("\n\nTutorial interrupted. Come back anytime to continue learning!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please check that all required files are present and try again.")


if __name__ == "__main__":
    main()