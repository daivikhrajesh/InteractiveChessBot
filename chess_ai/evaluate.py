#evaluate.py

import chess
import numpy as np

def evaluate_board(board):
    if board.is_checkmate():
        if board.turn:
            return -np.inf
        else:
            return np.inf
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0
    material_count = sum([piece_value(piece) for piece in board.piece_map().values()])
    return material_count

def piece_value(piece):
    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    return values.get(piece.piece_type, 0)
