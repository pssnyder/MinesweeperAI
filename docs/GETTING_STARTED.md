# Getting Started with Minesweeper AI

Welcome to the Minesweeper AI learning project! This guide will help you get started and understand the codebase step by step.

## 🎯 Prerequisites

Before diving in, make sure you have:

- **Python 3.7+** installed on your computer
- Basic understanding of Python concepts:
  - Variables and data types
  - Functions and classes
  - Lists and dictionaries
  - Basic control flow (if/else, loops)

Don't worry if you're not an expert - this project is designed to help you learn!

## 📚 Understanding Minesweeper

If you've never played Minesweeper, here's how it works:

1. **Goal**: Uncover all cells that don't contain mines
2. **Rules**:
   - Click a cell to uncover it
   - Numbers show how many mines are adjacent to that cell
   - If you uncover a mine, you lose
   - Flag cells you think contain mines
3. **Strategy**: Use the numbers to deduce where mines must be

## 🗂️ Project Structure Overview

```
src/
├── minesweeper_game.py    # Core game logic
├── minesweeper_ai.py      # AI implementation
└── __init__.py           # Package initialization

examples/
├── basic_game.py         # Simple game to try
├── ai_demo.py           # Watch the AI play
└── interactive_tutorial.py  # Guided learning

docs/
├── GETTING_STARTED.md   # This file
├── AI_CONCEPTS.md       # AI theory explained
├── API_REFERENCE.md     # Code documentation
└── TUTORIALS.md         # Step-by-step exercises
```

## 🚀 Your First Steps

### Step 1: Run the Basic Game

Start by understanding how Minesweeper works:

```bash
cd examples
python basic_game.py
```

This will start an interactive game where you can play manually.

### Step 2: Watch the AI Play

See the AI in action:

```bash
python ai_demo.py
```

Watch how the AI makes decisions and try to understand its reasoning.

### Step 3: Explore the Code

Open `src/minesweeper_game.py` and read through the `Minesweeper` class:

1. **`__init__`**: How the game board is created
2. **`_place_mines`**: How mines are randomly placed
3. **`_fill_numbers`**: How numbers are calculated
4. **`uncover`**: What happens when you click a cell
5. **`print_board`**: How the board is displayed

### Step 4: Understand the AI Basics

Open `src/minesweeper_ai.py` and look at the `MinesweeperAI` class:

1. **`__init__`**: What the AI tracks
2. **`make_move`**: How the AI decides what to do
3. **`find_safe_move`**: How it finds guaranteed safe moves
4. **`find_probable_move`**: How it makes educated guesses

## 🧠 Key Concepts to Learn

### 1. Object-Oriented Programming
- Classes represent things (Game, AI)
- Methods are actions those things can do
- Attributes store information about the object

### 2. Data Structures
- **Sets**: Store unique items (uncovered cells, flags)
- **Lists**: Store ordered items (game board rows)
- **Dictionaries**: Store key-value pairs (cell probabilities)

### 3. Game State Management
- The game tracks what's happened so far
- The AI builds knowledge from observations
- State changes affect future decisions

### 4. Algorithm Design
- Break complex problems into smaller parts
- Use logical rules when possible
- Fall back to probability when logic isn't enough

## 🎮 Try It Yourself

### Exercise 1: Modify the Display
Change how the game board looks:

1. Open `src/minesweeper_game.py`
2. Find the `print_board` method
3. Try changing the symbols used (replace '-' with '?')
4. Add colors or emojis if your terminal supports them

### Exercise 2: Add Debug Information
Help yourself understand what the AI is thinking:

1. Open `src/minesweeper_ai.py`
2. Find the `make_move` method
3. Add print statements to show what the AI is considering
4. Run the AI demo to see the extra information

### Exercise 3: Create Your Own Difficulty
Make a custom game size:

1. Open `examples/basic_game.py`
2. Create a new difficulty level
3. Test it to make sure it's fun but challenging

## 🔧 Common Issues and Solutions

### "ModuleNotFoundError"
**Problem**: Python can't find the game files
**Solution**: Make sure you're running from the project root directory

### "Game seems too easy/hard"
**Problem**: Difficulty settings don't feel right
**Solution**: Adjust the mine count - try 10-15% of total cells

### "AI makes weird moves"
**Problem**: AI behavior seems random
**Solution**: Add debug prints to understand the AI's reasoning

### "Code is confusing"
**Problem**: Hard to follow the logic
**Solution**: Start with simple functions and work your way up

## 📖 Next Steps

Once you're comfortable with the basics:

1. **Read** `docs/AI_CONCEPTS.md` to understand the theory
2. **Try** the tutorials in `docs/TUTORIALS.md`
3. **Experiment** with improving the AI
4. **Create** your own features

## 🤝 Getting Help

If you get stuck:

1. **Read the error messages** - they often tell you exactly what's wrong
2. **Add print statements** to see what your code is doing
3. **Break the problem down** into smaller pieces
4. **Check the documentation** in this folder
5. **Ask questions** - learning is a collaborative process!

## 🎯 Learning Goals

By the end of this project, you should understand:

- How to design and implement a game in Python
- Basic AI concepts like constraint satisfaction
- How to work with probability and uncertainty
- Good programming practices and code organization
- How to debug and test your code

Remember: The goal isn't to create the perfect AI immediately. It's to learn and have fun while doing it!

---

**Ready to start? Head to `examples/basic_game.py` and begin your journey! 🚀**