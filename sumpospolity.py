# Chess engine
import numpy as np

## CHESSBOARD

# We are going to use a 10 x 12 array to represent the chessboard. This is a more memory efficient way of representing the chessboard then the 12 x 12 array, given it is less computationally demanding and yet has the same functionalities.


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
    '''
    function to make moves
    input:
    board - initial state of the board
    start - the location on the board of the piece which is going to be moved
    end - the location towards which the moving piece is moved
    
    output: 
    capture - the number representing the piece which was just captured
    '''
    
    capture = board[end] # capturing the piece
    board[end] = board[start] # transfering the piece
    board[start] = EMPTY # emptying the initial field
    return capture

def unmake_move(board, start, end, captured = 0):
    '''
    function to unmake moves
    input:
    board - initial state of the board
    start - the location on the board of the piece which was moved and is now going to be reverted TO
    end - the location towards which the moving piece was moved and is now going to be reverted FROM
    capture - the number representing the piece which was just captured
    '''
    board[start] = board[end] # bringing back the piece which made a move into its original location
    board[end] = captured # reinstalling the captured piece
    


# Now represent the moves
# I think that generating pseudo-legal moves first is the better decision, we can quickly prune them afterwards with the move making function or eval function if they are illegal

# Directions
N, W, E, S = -10, -1, +1, +10

# Add a list of pieces which can slide (move multiple tiles at a time)
sliding_pieces = {WR, BR, WB, BB, WQ, BQ}

# Moves for each of the pieces
WP, WN, WB, WR, WQ, WK = 1, 2, 3, 4, 5, 6
BP, BN, BB, BR, BQ, BK = 7, 8, 9, 10, 11, 12

possible_moves = {
    WP: [N], # white pawn 
    BP: [S], # black pawn 
    WR: [N, S, W, E], # white rook 
    BR: [N, S, W, E], # black rook
    WB: [N+E, N+W, S+E, S+W], # white bishop 
    BB: [N+E, N+W, S+E, S+W], # black bishop 
    WK: [N, N+E, E, S+E, S, S+W, W, N+W], # white king
    BK: [N, N+E, E, S+E, S, S+W, W, N+W], # black king
    WQ: [N, N+E, E, S+E, S, S+W, W, N+W], # white queen
    BQ: [N, N+E, E, S+E, S, S+W, W, N+W], # black queen
    WN: [N+N+W, N+N+E, E+E+N, E+E+S, S+S+E, S+S+W, W+W+S, W+W+N], # white knight
    BN: [N+N+W, N+N+E, E+E+N, E+E+S, S+S+E, S+S+W, W+W+S, W+W+N] # black knight
}

def pseudolegal_move(board, white_moves):
    '''
    function generating pseudolegal moves, i.e. moves which do not check if they will leave king in check
    board - input state of the board
    white_moves = 1 if it is the white player's move and 0 if it is black player's move
    '''
    available_moves = []
    move_count = 0
    if white_moves:
        my_pieces = range(1, 7) # numbers 1-6
        enemy_pieces = range(7, 13) # numbers 7 - 12
    else:
        my_pieces = range(7, 13) # numbers 7 - 12
        enemy_pieces = range(1, 7)
    
    for tile in range(120):
        if board[tile] in my_pieces:
            piece = board[tile]
        
            if piece in sliding_pieces:
                # Slide until blocked
                for move in possible_moves[piece]:
                    original_move = move
                    while board[tile + move] not in my_pieces and board[tile + move] != OFF_BOARD:
                        available_moves.append([tile, tile + move])
                        move_count += 1 # this is not needed anymore i think
                        # break off when capturing an enemy pieces
                        if board[tile + move] in enemy_pieces:
                            break
                        move += original_move
            elif piece in [1,7]: # special moves for pawns
                #migrate all the logic for pawns here!
                #TODO check if the next square is empty
                #TODO check if you are in the starting position
                #TODO check if there is an enemy piece in front of you
                continue
            elif piece not in sliding_pieces: # this statement might not be necessary           
                # if piece == 1: # This is migrated to another part
                #     if 81 <= tile <= 88:
                #         possible_moves[WP].append(N+N) # add double move at the starting position for white pawns
                #     if board[tile + N + E] in enemy_pieces: 
                #         possible_moves[WP].append(N + E)
                #     if board[tile + N + W] in enemy_pieces:
                #         possible_moves[WP].append(N + W)
                # elif piece == 7:
                #     if 31 <= tile <= 38:
                #         possible_moves[BP].append(S+S) # add double move at the starting position for black pawns
                #     if board[tile + S + E] in enemy_pieces:
                #         possible_moves[BP].append(S + E)
                #     if board[tile + S + W] in enemy_pieces:
                #         possible_moves[BP].append(S + W)
                #TODO special cases for castling & en passant
                #TODO special cases for whatever special moves there exist besides the ones mentioned above
                if board[tile] == 7:
                    if 31 <= tile <= 38:
                        #double move if pawn in the starting position
                        possible_moves[BP].append(S + S) # remove this later
                if board[tile] == 1:
                    if 81 <= tile <= 88:
                        #double move if pawn in the starting position
                        possible_moves[WP].append(N + N) # remove this later
                for move in possible_moves[piece]:
                    if board[tile] == 1:
                        #This is a white pawn, it needs special attention                     
                        if move == N and board[tile+move] in enemy_pieces:
                            break
                    if board[tile] == 7:
                        #This is a black pawn, it needs special attention
                        if move == S and board[tile + move] in enemy_pieces:
                            break # pawn can't takeover enemy pieces if they are in front of it
 
                    if board[tile + move] not in my_pieces and board[tile + move] != OFF_BOARD:  
                        #TODO special case for pawns moved here
                        #  if make_move(board, start = tile, end = tile + move) not in my_pieces: # It doesn't have to make the moves now, only check if they are possible
                        available_moves.append([tile, tile + move])
                        if N + N in possible_moves[WP]:
                            possible_moves[WP].remove(N + N)
                        if S + S in possible_moves[BP]:
                            possible_moves[BP].remove(S + S)
                        move_count += 1 # I don't think this is needed anymore
    return(available_moves)            
                                            
                            
    

#the pseudolegal generator function should extract all moves which are possible now            
    
    
    
print(f'we are aiming to have 20 moves here, we currently have: {len(pseudolegal_move(initial_board(), 1))}')
print(f' the list of moves we have now:{pseudolegal_move(initial_board(), 1)}')


#TODO for possible_moves variable, collapse black and white pieces together, so it is more compact, and then further down the line verify by using the figures with .lower() or .upper() if needed
#TODO somehow there has to be a distinction that King can only move one tile at a time, and the queen can go as many as she can within the chessboard, and as long as there are no enemy pieces on the way
#TODO implement the moving for en-passant, and castling and pawn promotion?

# Illegal tiles on the chessboard

# illegal_tiles = (
#     "iiiiiiiiii"    # values 0 - 9
#     "iiiiiiiiii"    # values 10 - 19
#     "iiLLLLLLLL"  # values 20 - 29
#     "iiLLLLLLLL"  # values 30 - 39
#     "iiLLLLLLLL"   # values 40 - 49
#     "iiLLLLLLLL"   # values 50 - 59
#     "iiLLLLLLLL"   # values 60 - 69
#     "iiLLLLLLLL"   # values 70 - 79
#     "iiLLLLLLLL"  # values 80 - 89
#     "iiLLLLLLLL"   # values 90 - 99
#     "iiiiiiiiii"    # values 100 - 109
#     "iiiiiiiiii"    # values 110 - 119
# )

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
