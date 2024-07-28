# board.py

import pygame
import chess

WIDTH = 750
HEIGHT = 775
SQ_SIZE = 80
IMAGES = {}
board = chess.Board()
font = None  
input_text = ""
FONT_SIZE = 24  # Size of the font for the labels
ALERT_DISPLAY_TIME = 2000  
EPSILON = 0.1  # Exploration rate for Q-learning
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
Q_TABLE = {}  # Q-table for Q-learning

def draw_board(screen):
    """Draw the chessboard on the screen."""
    colors = [pygame.Color('white'), pygame.Color('gray')]
    board_top_left_x = (WIDTH - (SQ_SIZE * 8)) // 2
    board_top_left_y = (HEIGHT - (SQ_SIZE * 8)) // 2

    # Draw the squares on the board
    for r in range(8):
        for c in range(8):
            pygame.draw.rect(screen, colors[(r + c) % 2], pygame.Rect(board_top_left_x + c * SQ_SIZE, board_top_left_y + r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            piece = board.piece_at(r * 8 + c)
            if piece:
                piece_color = 'w' if piece.color == chess.WHITE else 'b'
                piece_type = piece.symbol().upper()
                piece_key = f'{piece_color}{piece_type}'
                if piece_key in IMAGES:
                    screen.blit(IMAGES[piece_key], pygame.Rect(board_top_left_x + c * SQ_SIZE, board_top_left_y + r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Draw file letters (a-h) at the bottom
    font = pygame.font.Font(None, FONT_SIZE)
    for i in range(8):
        text_surface = font.render(chr(97 + i), True, pygame.Color('black'))
        text_rect = text_surface.get_rect(center=(board_top_left_x + i * SQ_SIZE + SQ_SIZE // 2, board_top_left_y + 8 * SQ_SIZE + FONT_SIZE // 2))
        screen.blit(text_surface, text_rect)

    # Draw reversed rank numbers (1-8) on the left
    for i in range(8):
        text_surface = font.render(str(i + 1), True, pygame.Color('black'))
        text_rect = text_surface.get_rect(center=(board_top_left_x - FONT_SIZE, board_top_left_y + i * SQ_SIZE + SQ_SIZE // 2))
        screen.blit(text_surface, text_rect)

    # Draw file letters (a-h) at the top
    for i in range(8):
        text_surface = font.render(chr(97 + i), True, pygame.Color('black'))
        text_rect = text_surface.get_rect(center=(board_top_left_x + i * SQ_SIZE + SQ_SIZE // 2, board_top_left_y - FONT_SIZE // 2))
        screen.blit(text_surface, text_rect)

    # Draw reversed rank numbers (1-8) on the right
    for i in range(8):
        text_surface = font.render(str(i + 1), True, pygame.Color('black'))
        text_rect = text_surface.get_rect(center=(board_top_left_x + (SQ_SIZE * 8) + FONT_SIZE // 2, board_top_left_y + i * SQ_SIZE + SQ_SIZE // 2))
        screen.blit(text_surface, text_rect)
