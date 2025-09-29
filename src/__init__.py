"""
Minesweeper AI Learning Project

A comprehensive implementation of Minesweeper with AI capabilities,
designed for educational purposes.
"""

__version__ = "1.0.0"
__author__ = "Minesweeper AI Learning Project"

from .minesweeper_game import Minesweeper
from .minesweeper_ai import MinesweeperAI

__all__ = ["Minesweeper", "MinesweeperAI"]