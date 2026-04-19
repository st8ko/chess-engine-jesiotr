import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chess_engine import pseudolegal_move, is_legal, initial_board, EMPTY, OFF_BOARD, WP, WN, WB, WR, WQ, WK, BP, BN, BB, BR, BQ, BK # Downloading the functions from the chess engine script


def empty_board():
    '''Helper: returns a board with only OFF_BOARD tiles and empty playable squares.'''
    b = [OFF_BOARD] * 120
    for rank_start in range(20, 100, 10):
        b[rank_start + 1: rank_start + 9] = [EMPTY] * 8
    return b


def test_initial_position():
    '''Both sides should have exactly 20 moves from the starting position.'''
    assert len(pseudolegal_move(initial_board(), 1)) == 20, "White should have 20 moves at start"
    assert len(pseudolegal_move(initial_board(), 0)) == 20, "Black should have 20 moves at start"


def test_rook_mid_board():
    '''Rook on E5 with empty board should have 14 moves.'''
    b = empty_board()
    b[55] = WR
    assert len(pseudolegal_move(b, 1)) == 14, "Rook on E5 should have 14 moves"


def test_bishop_blocked():
    '''Bishop on D6, blocked by friendly on C7 and can capture enemy on G3.'''
    b = empty_board()
    b[44] = WB
    b[33] = WP  # friendly blocker
    b[77] = BP  # enemy to capture
    assert len(pseudolegal_move(b, 1)) == 9, "Bishop should have 8 moves, and the pawn should have 1 move with these obstructions"


def test_pawn_mechanics():
    '''White pawn on D4, enemy on E5 to capture, friendly knight blocking D5.'''
    b = empty_board()
    b[64] = WP
    b[55] = BP  # diagonal enemy — pawn can capture
    b[54] = WN  # friendly blocking forward — pawn cannot push
    assert len(pseudolegal_move(b, 1)) == 9, "Pawn should only have the diagonal capture, and the knight should have 8"


def test_knight_center():
    '''Knight in the center of the board should have 8 moves.'''
    b = empty_board()
    b[55] = WN
    assert len(pseudolegal_move(b, 1)) == 8, "Knight on E5 should have 8 moves"


def test_knight_corner():
    '''Knight in a corner should have only 2 moves.'''
    b = empty_board()
    b[21] = WN
    assert len(pseudolegal_move(b, 1)) == 2, "Knight on A8 should have 2 moves"


def test_black_pawn_mechanics():
    '''Mirror of the white pawn test — black pawn should behave symmetrically.'''
    b = empty_board()
    b[54] = BP   # black pawn on D5
    b[63] = WP   # diagonal enemy — black pawn can capture
    b[64] = BN   # friendly blocking forward
    assert len(pseudolegal_move(b, 0)) == 9, "Black pawn should only have the diagonal capture, and the knight should have 8"


def test_legality_removes_moves_leaving_king_in_check():
    '''Any move that leaves own king in check should be filtered out.'''
    b = empty_board()
    b[68] = BB   # black bishop threatening white's back rank
    b[81:89] = [WP] * 8
    b[91:99] = WR, WN, WB, WQ, WK, WB, WN, WR
    pseudo = pseudolegal_move(b, 1)
    legal = is_legal(b, 1, pseudo)
    assert len(legal) < len(pseudo), "Some pseudo-legal moves should be filtered as illegal"


if __name__ == "__main__":
    tests = [
        test_initial_position,
        test_rook_mid_board,
        test_bishop_blocked,
        test_pawn_mechanics,
        test_knight_center,
        test_knight_corner,
        test_black_pawn_mechanics,
        test_legality_removes_moves_leaving_king_in_check,
    ]
    for test in tests:
        try:
            test()
            print(f"PASSED: {test.__name__}")
        except AssertionError as e:
            print(f"FAILED: {test.__name__} — {e}")