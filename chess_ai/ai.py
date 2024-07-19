#ai.py 

import numpy as np
import chess
from .evaluate import evaluate_board

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizing_player:
        max_eval = -np.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = np.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def select_best_move(board, depth):
    best_move = None
    best_value = -np.inf
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, -np.inf, np.inf, False)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_move = move
    return best_move
