import os
import pygame

from game.tank import Tank
from game.terrain import Terrain
from game.bullet import Bullet

background_image = pygame.image.load(os.path.join("assets", "background-1.jpeg")) 

class Game:
    def __init__(self, pygame_instance, width=800, height=600):

        # Create objects
        self.pygame_instance = pygame_instance
        self.terrain = Terrain(width, height)
        self.width = width
        self.game_display = pygame_instance.display.set_mode((width, height))
        self.height = height
        self.clock = pygame_instance.time.Clock()
        self.bullets = []
        self.tanks = [
            Tank(50, 350),
            Tank(200, 350),
            Tank(350, 350),
            Tank(500, 350),
        ]
        self.player_tank = self.tanks[0]  # Reference to the player-controlled tank

    def run(self):
        # Game loop
        game_exit = False
        while not game_exit:
            # Handle events
            keys = self.pygame_instance.key.get_pressed()
            if keys[self.pygame_instance.K_LEFT]:
                self.player_tank.move_left()
            if keys[self.pygame_instance.K_RIGHT]:
                self.player_tank.move_right()
            if keys[self.pygame_instance.K_SPACE]:
                self.player_tank.jump()
            for event in self.pygame_instance.event.get():
                if event.type == self.pygame_instance.QUIT:
                    game_exit = True
                if event.type == self.pygame_instance.KEYDOWN:
                    if event.key == self.pygame_instance.K_LCTRL:
                        angle = 45 if self.player_tank.direction == 1 else 135
                        bullet = Bullet(self.player_tank.x + self.player_tank.width/2, self.player_tank.y + self.player_tank.height/2, angle)
                        self.bullets.append(bullet)
            # Update screen
            self.game_display.blit(background_image, (0, 0))
            self.terrain.draw(self.game_display, (0, 255, 0))
            # Update and draw tanks
            for tank in self.tanks:
                tank.update(self.terrain)
                tank.draw(self.game_display)
            # Update bullets and remove those that hit the ground
            self.bullets = [bullet for bullet in self.bullets if not bullet.update(self.terrain)]
            for bullet in self.bullets:
                bullet.draw(self.game_display)

            self.pygame_instance.display.update()
            self.clock.tick(60)  # Limit frame rate to 60 FPS

        # Quit Pygame
        self.pygame_instance.quit()
