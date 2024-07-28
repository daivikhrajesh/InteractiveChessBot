from chess_ai.board import (
    WIDTH, HEIGHT, SQ_SIZE, IMAGES, board, font, input_text, FONT_SIZE,
    ALERT_DISPLAY_TIME, EPSILON, ALPHA, GAMMA, Q_TABLE, draw_board
)

import pygame
import os
import numpy as np
import random

def load_images():
    """Load all images for the chess pieces."""
    pieces = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
    images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))
    for piece in pieces:
        path = os.path.join(images_dir, f'{piece}.png')
        try:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(path), (SQ_SIZE, SQ_SIZE))
        except FileNotFoundError:
            print(f"File {path} not found.")

def draw_text_box(screen, text):
    """Draw the text input box and the current text."""
    pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(0, HEIGHT - 40, WIDTH, 40))
    text_surface = font.render(text, True, pygame.Color('white'))
    screen.blit(text_surface, (10, HEIGHT - 30))

def draw_alert(screen, message):
    """Draw an alert message on the screen."""
    font = pygame.font.Font(None, 48)
    text_surface = font.render(message, True, pygame.Color('red'))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, pygame.Color('black'), text_rect.inflate(20, 20))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(ALERT_DISPLAY_TIME)  # Wait for ALERT_DISPLAY_TIME milliseconds

def get_q_key(board):
    """Get a unique key for the Q-table based on the board state."""
    return board.fen()  # Use FEN string as the state representation

def choose_action(state, legal_moves):
    """Choose an action using an epsilon-greedy strategy."""
    if random.uniform(0, 1) < EPSILON:
        # Exploration: choose a random move
        return random.choice(legal_moves)
    else:
        # Exploitation: choose the best move based on Q-values
        q_values = [Q_TABLE.get((state, move.uci()), 0) for move in legal_moves]
        max_q_value = max(q_values, default=0)
        best_moves = [move for move, q_value in zip(legal_moves, q_values) if q_value == max_q_value]
        return random.choice(best_moves) if best_moves else random.choice(legal_moves)

def update_q_table(state, action, reward, next_state):
    """Update the Q-table using the Q-learning formula."""
    best_next_action = choose_action(next_state, list(board.legal_moves))
    q_current = Q_TABLE.get((state, action.uci()), 0)
    q_next = Q_TABLE.get((next_state, best_next_action.uci()), 0)
    Q_TABLE[(state, action.uci())] = q_current + ALPHA * (reward + GAMMA * q_next - q_current)

def ai_move():
    """Let the AI make a move using Q-learning."""
    state = get_q_key(board)
    legal_moves = list(board.legal_moves)
    action = choose_action(state, legal_moves)
    board.push(action)
    return action

def handle_input():
    """Handle user input for moving pieces."""
    global input_text
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if len(input_text) > 0:  # Check if input is non-empty
                    try:
                        move = board.parse_san(input_text)
                        if move in board.legal_moves:
                            board.push(move)
                            # Reward or penalty
                            reward = 0
                            if board.is_checkmate():
                                reward = 10
                                draw_alert(pygame.display.get_surface(), "Checkmate!")
                            elif board.is_check():
                                reward = 1
                                draw_alert(pygame.display.get_surface(), "Check!!")
                            
                            # Update Q-table
                            next_state = get_q_key(board)
                            update_q_table(get_q_key(board), move, reward, next_state)

                            # AI makes its move after the user move
                            ai_move()

                        else:
                            print(f"Illegal move: {input_text}")
                    except Exception as e:
                        print(f"Error processing move: {e}")
                else:
                    print("Invalid move format. Move should be non-empty.")
                input_text = ""
            elif event.key == pygame.K_SPACE:
                # Clear text input
                input_text = ""
            else:
                input_text += event.unicode
    return True

def check_game_status():
    """Return the game status."""
    if board.is_checkmate():
        return "Checkmate"
    elif board.is_check():
        return "Check"
    elif board.is_stalemate():
        return "Stalemate"
    elif board.is_insufficient_material():
        return "Insufficient Material"
    elif board.is_seventyfive_moves():
        return "Draw by 75-move rule"
    elif board.is_fivefold_repetition():
        return "Draw by fivefold repetition"
    else:
        return "Ongoing"

def play_game():
    """Main function to run the chess game."""
    global font, input_text
    input_text = ""
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess Game')
    font = pygame.font.Font(None, FONT_SIZE)
    load_images()

    # AI makes the first move
    ai_move()

    running = True
    while running:
        screen.fill(pygame.Color('lightblue'))
        draw_board(screen)
        draw_text_box(screen, input_text)
        status = check_game_status()
        if status != "Ongoing":
            draw_alert(screen, f"Game Over: {status}")
            pygame.time.wait(ALERT_DISPLAY_TIME)
            running = False

        running = handle_input()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    play_game()
