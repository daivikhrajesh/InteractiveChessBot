import pygame
import os
import chess
import random

# Define constants
WIDTH = 750
HEIGHT = 750
SQ_SIZE = 80
IMAGES = {}
board = chess.Board()
font = None  
input_text = ""
depth = 3  # Depth for minimax or other AI algorithms
FONT_SIZE = 24  # Size of the font for the labels
ALERT_DISPLAY_TIME = 2000  

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
        screen.blit(text_surface, (board_top_left_x + i * SQ_SIZE + (SQ_SIZE - text_surface.get_width()) // 2, HEIGHT - FONT_SIZE))

    # Draw rank numbers (8-1) on the left
    for i in range(8):
        text_surface = font.render(str(8 - i), True, pygame.Color('black'))
        screen.blit(text_surface, (board_top_left_x - text_surface.get_width() - 10, board_top_left_y + (7 - i) * SQ_SIZE + (SQ_SIZE - text_surface.get_height()) // 2))

    # Draw file letters (a-h) at the top
    for i in range(8):
        text_surface = font.render(chr(97 + i), True, pygame.Color('black'))
        screen.blit(text_surface, (board_top_left_x + i * SQ_SIZE + (SQ_SIZE - text_surface.get_width()) // 2, board_top_left_y - FONT_SIZE // 2))

    # Draw rank numbers (8-1) on the right
    for i in range(8):
        text_surface = font.render(str(8 - i), True, pygame.Color('black'))
        screen.blit(text_surface, (board_top_left_x + (SQ_SIZE * 8) + FONT_SIZE + 10, board_top_left_y + (7 - i) * SQ_SIZE + (SQ_SIZE - text_surface.get_height()) // 2))

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

def ai_move():
    """Let the AI make a move."""
    legal_moves = list(board.legal_moves)
    print(f"AI legal moves: {[move.uci() for move in legal_moves]}")  # Debugging line
    if legal_moves:
        move = random.choice(legal_moves)  # Placeholder: replace with a more sophisticated move selection
        board.push(move)
        print(f"AI move: {move.uci()}")  # Debugging line
        return move
    return None

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
                    print(f"Input received: {input_text}")  # Debugging line
                    try:
                        # Try parsing the input as SAN (algebraic notation)
                        move = board.parse_san(input_text)
                        uci_move = move.uci()  # Convert the SAN move to UCI
                        if move in board.legal_moves:
                            board.push(move)
                            if board.is_checkmate():
                                draw_alert(pygame.display.get_surface(), "Checkmate!")
                            elif board.is_check():
                                draw_alert(pygame.display.get_surface(), "Check!!")
                            ai_move()  # AI makes its move after the user move
                        else:
                            print(f"Invalid move: {uci_move} (UCI format)")
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

def play_game(depth=3):
    """Main function to run the chess game."""
    global font, input_text
    input_text = ""
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess Game')
    font = pygame.font.Font(None, 36)
    load_images()

    # AI makes the first move
    ai_move()

    running = True
    while running:
        screen.fill(pygame.Color('lightblue'))
        draw_board(screen)
        draw_text_box(screen, input_text)
        
        # Check for alerts
        if board.is_checkmate():
            draw_alert(screen, "Checkmate!")
        elif board.is_check():
            draw_alert(screen, "Check!!")
        
        pygame.display.flip()
        running = handle_input()

    pygame.quit()

if __name__ == "__main__":
    play_game(depth=3)
