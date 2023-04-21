import pygame

from game.tank import Tank
from game.terrain import Terrain

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

# Define terrain clas

# Create objects
tank = Tank(50, 350)
terrain = Terrain(window_width, window_height) 

# Game loop
game_exit = False
while not game_exit:
    # Handle events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tank.move_left()
    if keys[pygame.K_RIGHT]:
        tank.move_right()
    if keys[pygame.K_SPACE]:
        tank.jump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

    # Update screen
    game_display.fill(black)
    terrain.draw(game_display, green)
    tank.update(terrain)
    tank.draw(game_display)
    pygame.display.update()
    clock.tick(60)  # Limit frame rate to 60 FPS

# Quit Pygame
pygame.quit()
quit()