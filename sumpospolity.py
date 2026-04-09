# Chess engine
import numpy as np


#Some steps to start out:
#Make a chessboard representation
#Represent pieces on the chessboard
#Represent moves which each piece can do
#Do the search algorithm
#Do the evaluation algorithm



## CHESSBOARD

# We are going to use a 10 x 12 array to represent the chessboard. This is a more memory efficient way of representing the chessboard then the 12 x 12 array, given it is less computationally demanding and yet has the same functionalities.

# board_beginning = (
#     "         \n"    # values 0 - 9
#     "         \n"    # values 10 - 19
#     " rnbkqbnr\n"  # values 20 - 29
#     " pppppppp\n"  # values 30 - 39
#     "         \n"    # values 40 - 49
#     "         \n"    # values 50 - 59
#     "         \n"    # values 60 - 69
#     "         \n"    # values 70 - 79
#     " PPPPPPPP\n"  # values 80 - 89
#     " RNBQKBNR\n"   # values 90 - 99
#     "         \n"    # values 100 - 109
#     "         \n"    # values 110 - 119
#) # in total we have 120 characters
# print(f'length of board_begining after its definition {len(board_beginning)}')

# A change of structure is necessary, the previous encodings would not be sufficient for computational goals of a chess engine

# The pieces, and fields on the chessboard, are going to be encoded as constants
EMPTY, OFF_BOARD = 0, 99
WP, WN, WB, WR, WQ, WK = 1, 2, 3, 4, 5, 6
BP, BN, BB, BR, BQ, BK = 7, 8, 9, 10, 11, 12

# The chessboard is going to be an integer array, allowing for faster computation and easier mutations than a character string
def initial_board():
    b = [OFF_BOARD] * 120 # 
    # Black pieces
    b[21:29] = BR, BN, BB, BK, BQ, BB, BN, BR
    b[31:39] = [BP] * 8
    b[41:79] = [EMPTY] * 38
    b[81:89] = [WP] * 8
    b[91:99] = WR, WN, WB, WQ, WK, WB, WN, WR
    return b

# Add a function to make a move

def make_move(board, start, end):
    capture = board[end] # capturing the piece
    board[end] = board[start] # transfering the piece
    board[start] = EMPTY # emptying the initial field
    return capture

def unmake_move(board, start, end, captured = 0):
    board[start] = board[end] # bringing back the piece which made a move into its original location
    board[end] = captured # reinstalling the captured piece
    


# Now represent the moves
# I think that generating pseudo-legal moves first is the better decision, we can quickly prune them afterwards with the move making function or eval function if they are illegal

# Directions
N, W, E, S = -10, -1, +1, +10

#just some trial locations
# print(board_beginning[35]) 
# print(board_beginning[25+S])

# Moves for each of the pieces

possible_moves = {
    "P": [N], # white pawn can go one or two tiles up, it can also move diagonally one tile to capture, the extra moves are enabled based on the pieces position on the board and enemy pieces
    "p": [S], # black pawn can go one or two tiles down, check above
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

#TODO for possible_moves variable, collapse black and white pieces together, so it is more compact, and then further down the line verify by using the figures with .lower() or .upper() if needed
#TODO somehow there has to be a distinction that King can only move one tile at a time, and the queen can go as many as she can within the chessboard, and as long as there are no enemy pieces on the way
#TODO implement the moving for en-passant, and castling and pawn promotion?

# Illegal tiles on the chessboard

illegal_tiles = (
    "iiiiiiiiii"    # values 0 - 9
    "iiiiiiiiii"    # values 10 - 19
    "iiLLLLLLLL"  # values 20 - 29
    "iiLLLLLLLL"  # values 30 - 39
    "iiLLLLLLLL"   # values 40 - 49
    "iiLLLLLLLL"   # values 50 - 59
    "iiLLLLLLLL"   # values 60 - 69
    "iiLLLLLLLL"   # values 70 - 79
    "iiLLLLLLLL"  # values 80 - 89
    "iiLLLLLLLL"   # values 90 - 99
    "iiiiiiiiii"    # values 100 - 109
    "iiiiiiiiii"    # values 110 - 119
)

# mozemy zrobic padding po lewej stronie i nie po prawej, bo i tak bedzie przeskok z prawej strony szachownicy na lewa jesli zrobimy jeden ruch w prawo


def basic_move(input_state = board_beginning, start_location = 0, end_location = 0):
    '''
    the most basic moving function
    input_state indicates the state of the board before the move
    start_location indicates from which field a piece is going to be moved
    end_location indicates to which field the piece is going to be moved
    the output of the function is new_state, the state of the board after the move is made
    '''
    
    #Checking if the start and end location even exist
    if start_location == end_location:
        raise Exception('Invalid move, the end location cannot be the same as the start locaiton')
    
    #Checking if the start and end locations are within the chessboard string
    if start_location < 0 or start_location > 120 or end_location < 0 or end_location > 120:
        raise Exception('Invalid moves, the moves are outside of the chessboard')
    
    #Checking if the move is not stepping outside of the chessboard
    if illegal_tiles[end_location].islower(): 
        raise Exception("Error, you can not move your piece to that tile")
    
    #Checking if your piece is not standing on the field to which you are moving your piece
    if input_state[start_location].islower() and input_state[end_location].islower() or input_state[start_location].isupper() and input_state[end_location].isupper():
        raise Exception("You can not do this move, your piece is standing on the tile to which you are trying to move")
    
    #Extracting informations about the piece and its move
    modifying_state = input_state
    moving_piece = modifying_state[start_location] # extract the piece that is going to be moving
    print(f'the moving piece is {moving_piece}')
    modifying_state = modifying_state[:start_location] + ' ' + modifying_state[start_location+1:]

    #Checking if there is a piece on the tile from which you want to move
    if moving_piece == " ":
        raise Exception('There is no piece on the field from which you are trying to move')
    
    #TODO check if the move which is made is actually possible, according to the set of legal moves by each piece
    # currently the list of moves does not include castling nor en passant, they are going to be added later
    the_move = end_location - start_location
    
    # Move logic for the pawns
    if moving_piece == "P" or moving_piece == "p":
        if start_location in [range(30, 39), range(80, 89)]:
            #extra moves from the starting tile for the pawns
            possible_moves["P"] = [N, N + N]
            possible_moves["p"] = [S, S + S]
        if moving_piece.isupper() and modifying_state[end_location].islower() or moving_piece.islower() and modifying_state[end_location].isupper():
            aa0 = 0 #placeholder
            # possible_moves["P"] = possible_moves["P"].join(N+E) 
            #TODO this logic doesn't work out yet -> consider: there would have to be separate function for movign diagonally to the right or left -> that would be 4 separate cases afterwards, maybe there is a simpler way?
            # nie wiem czy to jest dobre podejście, bo w ten sposób sprawdzane są tylko ruchy które mozna wykonac, a nie wszystkie mozliwe ruchy?
    
    if the_move not in possible_moves[moving_piece]:
        print(f'the move you are trying to make: {the_move}, while the allowed moves are {possible_moves[moving_piece]}')
        raise Exception('The piece you are trying to move doesn\'t move like that')
    
    #TODO expand the list of possible moves, make it more sophisticated
    # pawns can move two tiles only from their starting position
    # pawns can go one step diagonally only when there is an enemy piece on the tile on the diagonal
    # pieces can't jump over other pieces, unless it is a rook (or castling?)
    # extend rooks, bishops and queens moves so they can move as much as they would like towards each of the directions
    
    
    #Checking if enemy piece is captured
    if modifying_state[end_location] != " ":
        print(f'Taking over a piece: {modifying_state[end_location]}')
        captured_piece = modifying_state[end_location]
        output_state = modifying_state[:end_location] + moving_piece + modifying_state[end_location+1:]
        return(output_state)
    
    #Checking if the end location tile is empty
    if modifying_state[end_location] == " ":
        # Modifying the tile onto which you are moving
        output_state = modifying_state[:end_location] + moving_piece + modifying_state[end_location+1:]
        return(output_state)
    

#TODO there is something wrong with capturing the pieces, once a capture happens, the piece doubles (appears both in the its starting location, and the location at which it takes over an enemy piece)
# Moreover it seems that the state of the game does not see that a piece changes in a given position, loko at Move 3 and the fact that the engine does not recognize any pieces standing on position 55, while it definitely should, given the piece that stands there is captured    
    
#TODO there is a problem with how the pieces are moved, it seems to me that the indexes are changed in an inappropriate manner    

# state1 = basic_move(start_location = 86, end_location = 66)  
# # print("="*30 + "MOVE 1" + "=" * 30)
# print(state1)
# # print("="*30 + "MOVE 2" + "=" * 30)
# state2 = basic_move(input_state = state1, start_location = 35, end_location = 55)
# print(state2)
# print(f'the piece on the 55th field is {state2[55]}')

# state3 = basic_move(input_state = state2, start_location = 65, end_location = 55)    
# print(state3)

# state1 = basic_move(start_location = 88, end_location = 68)
# print(f'the piece which just moved is: {state1[67]}')
# state2 = basic_move(input_state = state1, start_location = 68, end_location = 48) #let's forget that this move is illegal now
# state3 = basic_move(input_state = state2, start_location = 48, end_location = 37)
# state4 = basic_move(input_state = state3, start_location = 37, end_location = 26)
# print(state4)


#TODO enable sequential playing, so that the state of the game is remembered and saved as the current state of the game, after a move is made

#TODO: enable the evaluation function, with the ability to determine whether the game has ended (so once you can capture the king)
