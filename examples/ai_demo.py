#!/usr/bin/env python3
"""
AI Demo - Watch the AI Play Minesweeper

This script demonstrates the AI playing Minesweeper automatically.
Watch how it makes decisions and learn from its reasoning.
"""

import sys
import os
import time

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from minesweeper_game import Minesweeper, create_game_from_difficulty
from minesweeper_ai import MinesweeperAI


def ai_demo_interactive():
    """
    Interactive AI demo where you can watch each move.
    """
    print("🤖 Minesweeper AI Demo 🤖")
    print("\nChoose difficulty:")
    print("1. Beginner (9x9, 10 mines)")
    print("2. Intermediate (16x16, 40 mines)")
    print("3. Expert (16x30, 99 mines)")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        if choice == '1':
            game = create_game_from_difficulty('beginner')
        elif choice == '2':
            game = create_game_from_difficulty('intermediate')
        elif choice == '3':
            game = create_game_from_difficulty('expert')
        else:
            print("Invalid choice, using beginner.")
            game = create_game_from_difficulty('beginner')
    except ValueError:
        print("Invalid input, using beginner.")
        game = create_game_from_difficulty('beginner')
    
    ai = MinesweeperAI(game)
    move_count = 0
    max_moves = 1000
    
    print("\nInitial board:")
    game.print_board()
    
    print("\nPress Enter after each move to continue, or 'q' to quit...")
    
    while not game.game_over and move_count < max_moves:
        move_count += 1
        print(f"\n{'='*50}")
        print(f"Move {move_count}")
        print(f"{'='*50}")
        
        # Show current AI state
        stats = ai.get_statistics()
        print(f"AI Stats: {stats['cells_uncovered']} uncovered, "
              f"{stats['mines_flagged']} flagged, "
              f"{stats['safe_cells_identified']} safe identified")
        
        if ai.make_move():
            game.print_board()
            print(f"\nAI reasoning: {ai.explain_last_move()}")
            
            # Show frontier and probabilities
            frontier = ai.get_frontier_cells()
            if frontier:
                print(f"Frontier cells: {len(frontier)}")
                probs = ai.calculate_mine_probabilities()
                if probs:
                    sorted_probs = sorted(probs.items(), key=lambda x: x[1])
                    print("Top 5 safest cells:")
                    for (r, c), prob in sorted_probs[:5]:
                        print(f"  ({r}, {c}): {prob:.1%} mine probability")
        else:
            print("AI couldn't make a move!")
            break
        
        # Wait for user input
        user_input = input("\nPress Enter to continue (or 'q' to quit): ").strip().lower()
        if user_input == 'q':
            break
    
    print(f"\nGame finished after {move_count} moves!")
    final_stats = ai.get_statistics()
    print(f"Final statistics: {final_stats}")
    
    if game.game_won:
        print("🎉 AI won the game! 🎉")
    elif game.game_over:
        print("💥 AI hit a mine! 💥")
        print("\nRevealing the complete board:")
        game.print_board(show_hidden=True)
    else:
        print("Game was interrupted.")


def ai_demo_auto():
    """
    Automatic AI demo that runs without user interaction.
    """
    print("🚀 Automatic AI Demo 🚀")
    
    difficulties = ['beginner', 'intermediate']
    results = {}
    
    for difficulty in difficulties:
        print(f"\nTesting {difficulty} difficulty...")
        wins = 0
        total_games = 5
        total_moves = 0
        
        for game_num in range(total_games):
            game = create_game_from_difficulty(difficulty)
            ai = MinesweeperAI(game)
            moves = 0
            max_moves = 500
            
            while not game.game_over and moves < max_moves:
                if ai.make_move():
                    moves += 1
                else:
                    break
            
            if game.game_won:
                wins += 1
                print(f"  Game {game_num + 1}: WON in {moves} moves")
            else:
                print(f"  Game {game_num + 1}: LOST after {moves} moves")
            
            total_moves += moves
        
        win_rate = wins / total_games
        avg_moves = total_moves / total_games
        results[difficulty] = {
            'win_rate': win_rate,
            'avg_moves': avg_moves,
            'wins': wins,
            'total': total_games
        }
        
        print(f"Results for {difficulty}:")
        print(f"  Win rate: {win_rate:.1%}")
        print(f"  Average moves: {avg_moves:.1f}")
    
    print("\n📊 Summary Results:")
    for difficulty, result in results.items():
        print(f"{difficulty.title()}: {result['wins']}/{result['total']} wins "
              f"({result['win_rate']:.1%}), avg {result['avg_moves']:.1f} moves")


def main():
    """
    Main demo function - choose between interactive and automatic mode.
    """
    print("Choose demo mode:")
    print("1. Interactive (watch each move)")
    print("2. Automatic (run multiple games)")
    
    try:
        choice = input("\nEnter choice (1-2): ").strip()
        if choice == '1':
            ai_demo_interactive()
        elif choice == '2':
            ai_demo_auto()
        else:
            print("Invalid choice, running interactive demo.")
            ai_demo_interactive()
    except KeyboardInterrupt:
        print("\nDemo interrupted. Thanks for watching!")
    except Exception as e:
        print(f"Error: {e}")
        print("Please check that all required files are present.")


if __name__ == "__main__":
    main()