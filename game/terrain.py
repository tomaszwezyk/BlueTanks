import pygame
import random

class Terrain:
    def __init__(self, window_width, window_height):
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

    def draw(self, game_display, green):
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
