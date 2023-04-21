import pygame

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.speed = 0.1  # Reduce tank speed to 1/10th of original
        self.gravity = 0.5

    def draw(self, game_display):
        pygame.draw.rect(game_display, (255, 255, 255), [self.x, self.y, self.width, self.height])

    def update(self, terrain):
        # Apply gravity
        self.speed += self.gravity
        self.y += self.speed

        # Check for collision with terrain
        tank_bottom = self.y + self.height
        terrain_bottom = terrain.get_y(self.x + self.width/2)
        if tank_bottom > terrain_bottom:
            self.speed = 0
            self.y = terrain_bottom - self.height

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def jump(self):
        self.speed = -10
