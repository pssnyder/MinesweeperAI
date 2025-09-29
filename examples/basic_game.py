#!/usr/bin/env python3
"""
Basic Minesweeper Game

A simple implementation that lets you play Minesweeper manually.
Great for understanding the game mechanics before diving into AI.
"""

import sys
import os

# Add the src directory to the Python path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from minesweeper_game import start_interactive_game
except ImportError:
    print("Could not import the game module.")
    print("Please make sure you're running this from the project root directory.")
    sys.exit(1)

if __name__ == "__main__":
    start_interactive_game()