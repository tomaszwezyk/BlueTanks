import pygame
import random

from game.tank import Tank

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

# Define terrain class
class Terrain:
    def __init__(self):
        self.x = 0
        self.y = 400
        self.width = window_width
        self.height = window_height - self.y

        # Generate terrain
        self.points = []
        last_point = (0, self.y)
        for i in range(20, self.width, 20):
            x = i
            if random.randint(0, 1):
                y = last_point[1] - random.randint(0, 20)
            else:
                y = last_point[1] + random.randint(0, 20)
            self.points.append((x, y))
            last_point = (x, y)
        self.points.append((self.width, self.y))

    def draw(self):
        pygame.draw.polygon(game_display, green, self.points)

    def get_y(self, x):
        for i in range(len(self.points) - 1):
            if self.points[i][0] <= x <= self.points[i+1][0]:
                x1, y1 = self.points[i]
                x2, y2 = self.points[i+1]
                slope = (y2 - y1) / (x2 - x1)
                y_intercept = y1 - slope * x1
                return slope * x + y_intercept

        return self.points[-1][1]

# Create objects
tank = Tank(50, 350)
terrain = Terrain()

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
    terrain.draw()
    tank.update(terrain)
    tank.draw(game_display)
    pygame.display.update()
    clock.tick(60)  # Limit frame rate to 60 FPS

# Quit Pygame
pygame.quit()
quit()