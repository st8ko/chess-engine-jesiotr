# Chess engine



#Some steps to start out:
#Make a chessboard representation
#Represent pieces on the chessboard
#Represent moves which each piece can do
#Do the search algorithm
#Do the evaluation algorithm



## CHESSBOARD

# We are going to use a 10 x 12 array to represent the chessboard. This is a more memory efficient way of representing the chessboard then the 12 x 12 array, given it is less computationally demanding and yet has the same functionalities.

board_beginning = (
    "         \n"    # values 0 - 9
    "         \n"    # values 10 - 19
    "  rnbkqbnr \n"  # values 20 - 29
    "  pppppppp \n"  # values 30 - 39
    "         \n"    # values 40 - 49
    "         \n"    # values 50 - 59
    "         \n"    # values 60 - 69
    "         \n"    # values 70 - 79
    "  PPPPPPPP \n"  # values 80 - 89
    "  RKBQKBKR  "   # values 90 - 99
    "         \n"    # values 100 - 109
    "         \n"    # values 110 - 119
) # in total we have 120 characters


# Now represent the moves
# I think that generating pseudo-legal moves first is the better decision, we can quickly prune them afterwards with the move making function or eval function if they are illegal

# Directions
N, W, E, S = -10, -1, +1, +10

print(board_beginning[35+N])
print(board_beginning[25+S])



