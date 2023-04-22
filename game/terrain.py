import pygame
import random

class Terrain:
    def __init__(self, window_width, window_height, seed=None, max_slope=0.35, segment_length=40):
        self.x = 0
        self.y = 450
        self.width = window_width
        self.height = window_height - self.y
        self.window_height = window_height

        # Generate terrain
        self.points = []
        random.seed(seed)  # Set the seed
        initial_y = random.randint(self.y - self.height, self.y)  # Random initial y value
        last_point = (0, initial_y)  # Update the last_point with the random initial y value

        self.points.append(last_point)  # Add the leftmost point to the list

        for i in range(segment_length, self.width, segment_length):
            x = i
            if random.random() < 0.5:
                y = max(last_point[1] - random.randint(0, int(max_slope * segment_length)), self.y - self.height)
            else:
                y = min(last_point[1] + random.randint(0, int(max_slope * segment_length)), self.y)
            self.points.append((x, y))
            last_point = (x, y)
        self.points.append((self.width, self.y))

    def draw(self, game_display, green):
        pygame.draw.polygon(game_display, green, self.points + [(self.width, self.window_height), (0, self.window_height)]) 

    def get_y(self, x):
        for i in range(len(self.points) - 1):
            if self.points[i][0] <= x <= self.points[i+1][0]:
                x1, y1 = self.points[i]
                x2, y2 = self.points[i+1]
                slope = (y2 - y1) / (x2 - x1)
                y_intercept = y1 - slope * x1
                return slope * x + y_intercept

        return self.points[-1][1]
