import pygame
import math
from models.commons import *

class Bullet:
    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color

    def move(self):
        self.x += BULLET_SPEED * math.cos(math.radians(self.angle))
        self.y -= BULLET_SPEED * math.sin(math.radians(self.angle))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BULLET_RADIUS, 0)
