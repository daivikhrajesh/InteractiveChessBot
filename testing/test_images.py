import pygame
import os

pygame.init()
screen = pygame.display.set_mode((100, 100))
image_path = os.path.join('images', 'wp.png')  # Adjust the path if necessary

try:
    image = pygame.image.load(image_path)
    pygame.transform.scale(image, (100, 100))
    print(f"Successfully loaded {image_path}")
except FileNotFoundError:
    print(f"Failed to load {image_path}")
