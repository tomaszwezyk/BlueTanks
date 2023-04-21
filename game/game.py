import os
import pygame

from game.tank import Tank
from game.terrain import Terrain
from game.bullet import Bullet

background_image = pygame.image.load(os.path.join("assets", "background-1.jpeg"))

class Game:
    def __init__(self, pygame_instance, width=800, height=600):
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

    def handle_events(self):
        for event in self.pygame_instance.event.get():
            if event.type == self.pygame_instance.QUIT:
                return True
            if event.type == self.pygame_instance.KEYDOWN:
                if event.key == self.pygame_instance.K_LCTRL:
                    angle = 45 if self.player_tank.direction == 1 else 135
                    bullet = Bullet(angle, self.player_tank)
                    self.bullets.append(bullet)
        return False

    def update(self):
        keys = self.pygame_instance.key.get_pressed()
        if keys[self.pygame_instance.K_LEFT]:
            self.player_tank.move_left()
        if keys[self.pygame_instance.K_RIGHT]:
            self.player_tank.move_right()
        if keys[self.pygame_instance.K_SPACE]:
            self.player_tank.jump()
        for tank in self.tanks:
            tank.update(self.terrain)

        new_bullets = []
        for bullet in self.bullets:
            bullet_hit_tank = False
            for tank in self.tanks:
                if bullet.owner_tank != tank and bullet.collides_with(tank):
                    self.tanks.remove(tank)
                    bullet_hit_tank = True
                    break
            if not bullet_hit_tank and not bullet.update(self.terrain):
                new_bullets.append(bullet)
        self.bullets = new_bullets

    def draw(self):
        self.game_display.blit(background_image, (0, 0))
        self.terrain.draw(self.game_display, (0, 255, 0))
        for tank in self.tanks:
            tank.draw(self.game_display)
        for bullet in self.bullets:
            bullet.draw(self.game_display)
        self.pygame_instance.display.update()

    def run(self):
        game_exit = False
        while not game_exit:
            game_exit = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Limit frame rate to 60 FPS

        self.pygame_instance.quit()
