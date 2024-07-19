import pygame
import os

WIDTH = 400
HEIGHT = 400
SQ_SIZE = 80
IMAGES = {}

def load_images():
    pieces = ['wP', 'bP']
    images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images'))
    print(f"Images directory: {images_dir}")  # Debugging line
    for piece in pieces:
        path = os.path.join(images_dir, f'{piece}.png')
        print(f"Attempting to load: {path}")  # Debugging line
        print(f"Full path to {piece}.png: {path}")  # Debugging line
        try:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(path), (SQ_SIZE, SQ_SIZE))
            print(f"Loaded {path}")
        except FileNotFoundError:
            print(f"File {path} not found.")

def draw_pawns(screen):
    """Draw only pawns on the screen."""
    screen.fill(pygame.Color('lightblue'))
    for i, piece in enumerate(['wP', 'bP']):
        image = IMAGES.get(piece)
        if image:
            screen.blit(image, pygame.Rect(i * SQ_SIZE, 0, SQ_SIZE, SQ_SIZE))
    pygame.display.flip()

def test_pawns():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Test Pawns')
    load_images()
    draw_pawns(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.time.wait(1000)  # Wait for 1 second to view the result

    pygame.quit()

if __name__ == "__main__":
    test_pawns()
