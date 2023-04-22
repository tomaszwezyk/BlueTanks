import pygame
import random

class Terrain:
    def __init__(self, window_width, window_height, max_slope=0.35, segment_length=40):
        self.x = 0
        self.y = 450
        self.width = window_width
        self.height = window_height - self.y
        self.window_height = window_height 
        self.texture = pygame.image.load("assets/grass.png")
        self.texture = pygame.transform.scale(self.texture, (40, 40))  # Scale the texture to the desired size

        # Generate terrain
        self.points = []
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

    def draw(self, game_display, green, offset_x, offset_y):
        offset_y -= 40
        offset_points = [(x - offset_x, y - offset_y) for x, y in self.points]

        # Render the terrain texture
        for i in range(len(offset_points) - 1):
            x1, y1 = offset_points[i]
            x2, y2 = offset_points[i + 1]
            segment_length = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

            # Calculate the number of times the texture should be repeated
            repeat_count = int(segment_length / self.texture.get_width()) + 1

            # Calculate the angle of the terrain segment
            angle = -pygame.math.Vector2(x2 - x1, y2 - y1).angle_to((1, 0))

            # Render the texture repeatedly along the terrain segment
            for j in range(repeat_count):
                x = x1 + j * self.texture.get_width()
                y = y1 + (y2 - y1) * (j * self.texture.get_width()) / (x2 - x1)
                rotated_texture = pygame.transform.rotate(self.texture, angle)
                game_display.blit(rotated_texture, (x - rotated_texture.get_width() / 2, y - rotated_texture.get_height() / 2))

        # Draw the polygon for the lower part of the terrain
        pygame.draw.polygon(game_display, green, offset_points + [(self.width - offset_x, self.window_height - offset_y), (0 - offset_x, self.window_height - offset_y)])

    def get_y(self, x):
        for i in range(len(self.points) - 1):
            if self.points[i][0] <= x <= self.points[i+1][0]:
                x1, y1 = self.points[i]
                x2, y2 = self.points[i+1]
                slope = (y2 - y1) / (x2 - x1)
                y_intercept = y1 - slope * x1
                return slope * x + y_intercept

        return self.points[-1][1]
