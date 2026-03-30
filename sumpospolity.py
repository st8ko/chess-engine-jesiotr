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
    "  RNBQKBNR  "   # values 90 - 99
    "         \n"    # values 100 - 109
    "         \n"    # values 110 - 119
) # in total we have 120 characters


# Now represent the moves
# I think that generating pseudo-legal moves first is the better decision, we can quickly prune them afterwards with the move making function or eval function if they are illegal

# Directions
N, W, E, S = -10, -1, +1, +10

#just some trial locations
# print(board_beginning[35]) 
# print(board_beginning[25+S])

# Moves for each of the pieces

possible_moves = {
    "P": [N, N + N, N+E, N+W], # white pawn can go one or two tiles up, it can also move diagonally one tile to capture
    "p": [S, S + S, S+E, S+W], # black pawn can go one or two tiles down
    "R": [N, S, W, E], # white rook can go to each horizontal and vertical direction
    "r": [N, S, W, E], # black can do the same as the white rook
    "B": [N+E, N+W, S+E, S+W], # white bishop can go to each diagonal direction
    "b": [N+E, N+W, S+E, S+W], # black bishop can do the same as white bishop
    "K": [N, N+E, E, S+E, S, S+W, W, N+W], # white king can go any direction, one square only
    "k": [N, N+E, E, S+E, S, S+W, W, N+W], # black king can do the same as the white king
    "Q": [N, N+E, E, S+E, S, S+W, W, N+W], # white queen can go any direction
    "q": [N, N+E, E, S+E, S, S+W, W, N+W], # white queen can go any direction
    "N": [N+N+W, N+N+E, E+E+N, E+E+S, S+S+E, S+S+W, W+W+S, W+W+N], # white knight can move as is said in chess
    "n": [N+N+W, N+N+E, E+E+N, E+E+S, S+S+E, S+S+W, W+W+S, W+W+N] # and the black knight can do the same
}

#TODO somehow there has to be a distinction that King can only move one tile at a time, and the queen can go as many as she can within the chessboard, and as long as there are no enemy pieces on the way
#TODO implement the moving for en-passant, and castling and pawn promotion?

# Illegal tiles on the chessboard

illegal_tiles = (
    "iiiiiiiiii"    # values 0 - 9
    "iiiiiiiiii"    # values 10 - 19
    "iiLLLLLLLLii"  # values 20 - 29
    "iiLLLLLLLLii"  # values 30 - 39
    "iiLLLLLLLLii"   # values 40 - 49
    "iiLLLLLLLLii"   # values 50 - 59
    "iiLLLLLLLLii"   # values 60 - 69
    "iiLLLLLLLLii"   # values 70 - 79
    "iiLLLLLLLLii"  # values 80 - 89
    "iiLLLLLLLLii"   # values 90 - 99
    "iiiiiiiiii"    # values 100 - 109
    "iiiiiiiiii"    # values 110 - 119
)

def basic_move(current_state = board_beginning, start_location, end_location):
    '''
    the most basic moving function
    current_state indicates the state of the board before the move
    start_location indicates from which field a piece is going to be moved
    end_location indicates to which field the piece is going to be moved
    '''
    #TODO implement a check if the start and end location even exist on the board?
    
    #Checking if the move is not stepping outside of the chessboard
    if illegal_tiles[end_location].islower(): 
        print('Error, you can not move your piece to that tile')
        return(current_state)
    
    
    #Extracting informations about the piece and its move
    new_state = current_state
    moving_piece = new_state[start_location] # extract the piece that is going to be moving
    new_state[start_location] = " " # empty the tile from which the piece is moved
    
    #Checking if your piece is not standing on the field to which you are moving your piece
    if current_state[start_location].islower() and current_state[end_location].islower() or current_state[start_location].isupper() and current_state[end_location].isupper():
        print('You can not do this move, there is your piece standing on the tile to which you are trying to move')
    
    
    #Checking if enemy piece is captured
    if current_state[end_location] != " ":
        print(f'Taking over a piece: {current_state[end_location]}')
        
    new_state[end_location] = moving_piece #
    return(new_state)
    
    
