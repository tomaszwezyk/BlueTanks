import os
import pygame
import socket
import pickle
from game.tank import Tank
from game.terrain import Terrain
from game.bullet import Bullet

background_image = pygame.image.load(os.path.join("assets", "background-1.jpeg"))

class Game:
    def __init__(self, pygame_instance, width=800, height=600, join_game=False, server_ip=""):
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
        self.join_game = join_game
        self.server_ip = server_ip
        self.client_socket = None

        if self.join_game:
            self.connect_to_server()

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, 1234))

    def handle_events(self):
        for event in self.pygame_instance.event.get():
            if event.type == self.pygame_instance.QUIT:
                return True
            if event.type == self.pygame_instance.KEYDOWN:
                if event.key == self.pygame_instance.K_LCTRL:
                    if self.player_tank.shoot():
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
            else:
                if self.join_game:
                    data = {
                        "bullet_x": bullet.x,
                        "bullet_y": bullet.y,
                        "bullet_direction": bullet.direction,
                        "bullet_owner_id": bullet.owner_tank.id
                    }
                    self.client_socket.send(pickle.dumps(data))
        self.bullets = new_bullets

    def draw(self):
        self.game_display.blit(background_image, (0, 0))
        self.terrain.draw(self.game_display, (0, 255, 0))
        for tank in self.tanks:
            tank.draw(self.game_display)
        for bullet in self.bullets:
            bullet.draw(self.game_display)
        
        self.draw_cannon_hotness()  # Add this line to draw the hotness bar

        self.pygame_instance.display.update()

    def draw_cannon_hotness(self):
        max_bar_width = 200
        bar_height = 20
        hotness_percentage = min(self.player_tank.cannon_hotness / self.player_tank.max_hotness, 1)
        bar_width = int(max_bar_width * hotness_percentage)

        # Draw the background of the hotness bar
        background_color = (128, 128, 128)
        pygame.draw.rect(self.game_display, background_color, (10, 10, max_bar_width, bar_height))

        # Draw the hotness bar
        bar_color = (255, 0, 0)
        pygame.draw.rect(self.game_display, bar_color, (10, 10, bar_width, bar_height))

        # Draw a border around the hotness bar
        border_color = (0, 0, 0)
        border_thickness = 2
        pygame.draw.rect(self.game_display, border_color, (10, 10, max_bar_width, bar_height), border_thickness)

        # Optionally, you can display the hotness value as text
        font = pygame.font.Font(None, 24)
        text_color = (0, 0, 0)
        text = font.render(f"Hotness: {self.player_tank.cannon_hotness:.0f}/{self.player_tank.max_hotness}", True, text_color)
        self.game_display.blit(text, (10 + max_bar_width + 10, 10))

    def run(self):
        game_exit = False
        while not game_exit:
            game_exit = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Limit frame rate to 60 FPS

            if self.join_game:
                self.client_socket.close()

        self.pygame_instance.quit()
