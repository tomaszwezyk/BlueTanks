import pygame
import math
from game.models.commons import *

class Tank:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.barrel_angle = 0

    def move_left(self):
        self.x -= TANK_SPEED

    def move_right(self):
        self.x += TANK_SPEED

    def adjust_barrel_up(self):
        self.barrel_angle = min(self.barrel_angle + TANK_ROTATION_SPEED, MAX_BARREL_ANGLE)

    def adjust_barrel_down(self):
        self.barrel_angle = max(self.barrel_angle - TANK_ROTATION_SPEED, MIN_BARREL_ANGLE)

    def shoot(self):
        bullet_x = self.x + (TANK_WIDTH / 2) + ((TANK_HEIGHT / 2) * math.cos(math.radians(self.barrel_angle)))
        bullet_y = self.y - ((TANK_HEIGHT / 2) * math.sin(math.radians(self.barrel_angle)))
        return Bullet(bullet_x, bullet_y, self.barrel_angle, self.color)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, TANK_WIDTH, TANK_HEIGHT), 0)
        barrel_end_x = self.x + (TANK_WIDTH / 2) + ((TANK_HEIGHT / 2) * math.cos(math.radians(self.barrel_angle)))
        barrel_end_y = self.y - ((TANK_HEIGHT / 2) * math.sin(math.radians(self.barrel_angle)))
        pygame.draw.line(surface, self.color, (self.x + (TANK_WIDTH / 2), self.y + (TANK_HEIGHT / 2)), (barrel_end_x, barrel_end_y), 5)
