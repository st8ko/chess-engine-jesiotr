# Function to run tests

#TODO change print statements to asserts
#starting position    
print(f'we are aiming to have 20 moves here, we currently have: {len(pseudolegal_move(initial_board(), 1))} \n')
print(f'the list of moves we have now:{pseudolegal_move(initial_board(), 1)}')
# TEST PASSED

# rook in the middle of the board
def test_rook_mid_board():
    b = [OFF_BOARD] * 120
    
    # Safely clear only the playable 8x8 area
    # rank_start will be 20, 30, 40... up to 90
    for rank_start in range(20, 100, 10): 
        b[rank_start + 1 : rank_start + 9] = [EMPTY] * 8
    
    # Place a White Rook at 55 (Square E5)
    b[55] = WR
    return b
print(f'we are aiming to have 14 moves here, we currently have: {len(pseudolegal_move(test_rook_mid_board(), 1))}\n')
print(f'the moves we have now: {pseudolegal_move(test_rook_mid_board(), 1)}')
# TEST PASSED

# caged bishop test
def test_bishop_blocked():
    b = [OFF_BOARD] * 120
    
    for rank_start in range(20, 100, 10): 
        b[rank_start + 1 : rank_start + 9] = [EMPTY] * 8
    
    # Place White Bishop at 55 (E5)
    b[44] = WB 
    
    # Obstruction 1: Friendly Pawn at 33 (C7)
    b[33] = WP 
    
    # Obstruction 2: Enemy Pawn at 77 (G3)
    b[77] = BP     
    return b

print(f'we are aiming to have 9 moves here, we currently have: {len(pseudolegal_move(test_bishop_blocked(), 1))}\n')
print(f'the moves we have now: {pseudolegal_move(test_bishop_blocked(), 1)}')
# TEST PASSED

def test_pawn_mechanics():
    b = [OFF_BOARD] * 120
    
    for rank_start in range(20, 100, 10): 
        b[rank_start + 1 : rank_start + 9] = [EMPTY] * 8
    
    # White Pawn at 64 (D4)
    b[64] = WP
    
    # Enemy at 55 (E5)
    b[55] = BP
    
    # Friendly at 54 (D5)
    b[54] = WN 
    
    return b

print(f'we are aiming to have 9 moves here, we currently have: {len(pseudolegal_move(test_pawn_mechanics(), 1))}\n')
print(f'the moves we have now: {pseudolegal_move(test_pawn_mechanics(), 1)}')
# TEST PASSED

def board_for_legality():
    b = [OFF_BOARD] * 120 # 
    # Black pieces
    b[21:29] = [EMPTY] * 8
    b[31:39] = [EMPTY] * 8
    b[41:79] = [EMPTY] * 38
    b[68] = BB
    b[81:89] = [WP] * 8
    b[91:99] = WR, WN, WB, WQ, WK, WB, WN, WR
    return b
            
print(f'we have {pseudolegal_move(board_for_legality(), 1)} pseudolegal moves')
print(f'we have {is_legal(board = board_for_legality(), white_moves = 1, list_of_moves = pseudolegal_move(board_for_legality(), 1))} legal moves')
# TEST PASSED