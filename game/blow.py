import os
import random
import pygame

blow_image = pygame.image.load(os.path.join("assets", "blow.png"))

class BlowEffect:
    def __init__(self, x, y, duration=30):
        self.x = x - blow_image.get_width() / 2
        self.y = y - blow_image.get_height() / 2

        self.width = blow_image.get_width()
        self.height = blow_image.get_height()
        self.duration = duration
        self.current_frame = 0

    def update(self):
        self.current_frame += 1
        if self.current_frame >= self.duration:
            return True
        return False

    def draw(self, game_display):
        scale_factor = min(1, self.current_frame / (self.duration / 2))
        scaled_image_width = int(blow_image.get_width() * scale_factor)
        scaled_image_height = int(blow_image.get_height() * scale_factor)
        scaled_image = pygame.transform.scale(blow_image, (scaled_image_width, scaled_image_height))

        shake_range = 5
        shake_x = random.randint(-shake_range, shake_range)
        shake_y = random.randint(-shake_range, shake_range)

        draw_x = self.x + (blow_image.get_width() - scaled_image_width) / 2 + shake_x
        draw_y = self.y + (blow_image.get_height() - scaled_image_height) / 2 + shake_y
        game_display.blit(scaled_image, (draw_x, draw_y))
