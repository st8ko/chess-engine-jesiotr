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
    return([board, capture]) 

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
    return(board)
    


# Move Representations

# Directions
N, W, E, S = -10, -1, +1, +10

# Add a list of pieces which can slide (move multiple tiles at a time)
sliding_pieces = {WR, BR, WB, BB, WQ, BQ}


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
    if white_moves:
        my_pieces = range(1, 7) # numbers 1-6
        enemy_pieces = range(7, 13) # numbers 7 - 12
    else:
        my_pieces = range(7, 13)
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
                        # break off when capturing an enemy pieces
                        if board[tile + move] in enemy_pieces: #TODO fix this logic
                            break  #get out to the next iteration of loopu #108
                        else:
                            move += original_move
                            continue
                        continue  #get out to the next iteration of loop #106  
                            
            elif piece in [1,7]: # special moves for pawns
                if piece == 1: # white pawn logic
                    if board[tile + N] == EMPTY:
                        available_moves.append([tile, tile + N])
                    if 81 <= tile <= 88: # check if the pawn is in the starting position
                        if board[tile + N + N] == EMPTY and board[tile + N] == EMPTY: 
                            available_moves.append([tile, tile + N + N])
                    if board[tile + N + E] in enemy_pieces:
                        available_moves.append([tile, tile + N + E])
                    if board[tile + N + W] in enemy_pieces:
                        available_moves.append([tile, tile + N + W])
                
                if piece == 7: # black pawn logic
                    if board[tile + S] == EMPTY:
                        available_moves.append([tile, tile + S])
                    if 31 <= tile <= 38: # check if the pawn is in the starting position
                        if board[tile + S + S] == EMPTY and board[tile + S] == EMPTY:
                            available_moves.append([tile, tile + S + S])
                    if board[tile + S + E] in enemy_pieces:
                        available_moves.append([tile, tile + S + E])
                    if board[tile + S + W] in enemy_pieces:
                        available_moves.append([tile, tile + S + W])

            else: # elif piece not in sliding_pieces and piece not in [1,7]: # this statement might not be necessary           
                #TODO special cases for castling & en passant
                #TODO special cases for whatever special moves there exist besides the ones mentioned above
                for move in possible_moves[piece]: 
                    if board[tile + move] not in my_pieces and board[tile + move] != OFF_BOARD:  
                        available_moves.append([tile, tile + move])
    return(available_moves)            
                                            
                            
    

# Legal Move Filtering

def is_legal(board, white_moves, list_of_moves):
    '''
    inputs: 
    board -> input of the board state
    white_moves -> 1 if white player moves, 0 if black player moves
    list_of_moves -> list of moves are to be checked if they are legal or not
    output:
    legal_moves -> a list of moves which are legal out of the initial list_of_moves
    '''
    if white_moves == 1:
        my_king = WK
    elif white_moves == 0:
        my_king = BK
    
    legal_moves = []
    # now we want to scan what pieces does the enemy have currently, to attack our king
    for start, end in list_of_moves:
        board, captured_piece = make_move(board, start, end)
        your_king_tile = board.index(my_king)
        
        if any(len(sublist) > 1 and sublist[1] == your_king_tile for sublist in pseudolegal_move(board, white_moves = not(white_moves))):
            pass
        else: 
            legal_moves.append([start, end])
        board = unmake_move(board, start, end, captured = captured_piece)
    return(legal_moves)

        
#TODO do some more testing for the legality function
#TODO enable sequential playing so that I can check the perft at depth 3
#TODO I don't know if the perft depth 3 test requires or not the implementation of en passant and castling, add that if needed -> It doesn't, hence its not needed noww