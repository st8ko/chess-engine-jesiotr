# Chess Engine (jesiotr)

A simple chess engine written in Python, implementation from scratch rather than using ready-made modules and libraries. So far 10x12 mailbox board representation, 
pseudo-legal move generation and legal move filtering have been implemented.

I started building this to deepen my understanding of search algorithms and good software practices useful for working with AI/ML. This project extends beyond my Econometrics and Data Science curriculum.

## Architecture

**Board representation:** I chose to use 10x12 mailbox array (120 integers). I first experimented with a character string, but it proved to be a bad idea, given strings are immutable.
The two-rank padding on each side allows off-board detection in O(1) without checking bounds. Sliding pieces simply stop when they hit the off-board value (99).

![Chessboard representation with numbers representing position in the array](/images/board_representation.jpg "Chessboard representation")


**Move generation:** Two-phase approach:
1. Pseudo-legal generation - all (en passant, castling and promotion are not yet supported) valid moves in chess, without looking if the king is left in check after move
2. Legal filtering - make/unmake each move, from the pseudo-legal generated list, and check if the king is attacked by enemy pieces


**Complexity:** Legal move generation is O(M × P × D) where M is the number 
of pseudo-legal moves, P is the number of opponent pieces, and D is average 
sliding depth. This is acceptable for shallow search but motivates 
incremental attack detection as a future improvement.

## What's implemented
- [x] Board representation and initialisation
- [x] Pseudo-legal move generation for all piece types
- [x] Pawn double-push, diagonal captures
- [x] Legal move filtering (king safety)
- [x] Make/unmake move
- [x] Unit tests for rook, bishop, pawn, and legality

## What's not yet implemented
- [ ] Search (minimax with alpha-beta pruning) — next priority
- [ ] Position evaluation function
- [ ] En passant, castling, promotion
- [ ] Perft testing at depth 3+

## How to run

No external dependencies are required beyond Python 3.x.

Run the test suite from the project root:
```bash
python tests/test_moves.py
```

## Project structure

```
chess-engine-jesiotr/
├── chess_engine.py   # board representation, move generation, legal filtering
├── tests/
│   └── test_moves.py # unit tests for move generation and legality
└── images/
    └── board_representation.jpg
```

## Inspiration and design notes

This project benefited a lot from the knowledge in the [chess programming wiki](https://www.chessprogramming.org/Main_Page) and the Thomas Sahle's [sunfish](https://github.com/thomasahle/sunfish/tree/master), which I went through before writing any code.

Given this engine is written in Python, and not C, it will be significantly slower than it's C counterpart, but provides a good foundation for me to start with. 

My aim is to continue developing this project and perform different statistical tests for algorithm evaluations.