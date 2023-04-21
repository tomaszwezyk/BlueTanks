import pygame

from game.tank import Tank
from game.terrain import Terrain
from game.game import Game

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)  # Choose a font and size

# Set up the game window
window_width = 800
window_height = 600
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tank Game")

clock = pygame.time.Clock()
clock.tick(60)  # Limit frame rate to 60 FPS
font = pygame.font.Font(None, 24)  # Choose a font and size


# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)

game = Game(pygame)

# Run the game
game.run()

# Quit Pygame
pygame.quit()
quit()