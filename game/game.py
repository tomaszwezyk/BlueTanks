import os
import pygame
import socket
import pickle
import random
import random
from game.tank import Tank
from game.terrain import Terrain
from game.bullet import Bullet
from game.blow import BlowEffect

from pygame import mixer

background_image = pygame.image.load(os.path.join("assets", "background-1.jpeg"))

class Game:
    def __init__(self, pygame_instance, width=800, height=600, join_game=False, server_ip=""):
        self.pygame_instance = pygame_instance
        self.terrain = Terrain(width * 20, height)
        self.width = width
        self.screen_shake_points = []
        self.game_display = pygame_instance.display.set_mode((width, height))
        self.height = height
        self.clock = pygame_instance.time.Clock()
        self.bullets = []
        self.blow_effects = []
        self.tanks = [
            Tank(550, 350),
            Tank(700, 350),
            Tank(950, 350),
            Tank(1000, 350),
        ]
        self.player_tank = self.tanks[0]  # Reference to the player-controlled tank

        mixer.init()
        self.blow_sound = mixer.Sound(os.path.join("assets", "blow.wav"))

        self.player2_tank = self.tanks[1]  # Reference to the player2-controlled tank
        self.join_game = join_game
        self.server_ip = server_ip
        self.client_socket = None

        if self.join_game:
            self.connect_to_server()

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, 1234))

    def handle_shooting(self, tank, shoot_keys):
        for key in shoot_keys:
            if self.pygame_instance.key.get_pressed()[key]:
                if tank.shoot():
                    angle = 45 if tank.direction == 1 else 135
                    bullet = Bullet(angle, tank)
                    self.bullets.append(bullet)

    def handle_events(self):
        for event in self.pygame_instance.event.get():
            if event.type == self.pygame_instance.QUIT:
                return True
            if event.type == self.pygame_instance.KEYDOWN:
                # Player1 shoot with LCTRL or LSHIFT
                self.handle_shooting(self.player_tank, [self.pygame_instance.K_LCTRL, self.pygame_instance.K_LSHIFT])

                # Player2 shoot with RCTRL or RSHIFT
                self.handle_shooting(self.player2_tank, [self.pygame_instance.K_RCTRL, self.pygame_instance.K_RSHIFT])
        return False
    
    def update(self):
        keys = self.pygame_instance.key.get_pressed()

        # Player1 controls
        if keys[self.pygame_instance.K_a]:
            self.player_tank.move_left()
        if keys[self.pygame_instance.K_d]:
            self.player_tank.move_right()
        if keys[self.pygame_instance.K_w]:
            self.player_tank.jump()

        # Player2 controls
        if keys[self.pygame_instance.K_LEFT]:
            self.player2_tank.move_left()
        if keys[self.pygame_instance.K_RIGHT]:
            self.player2_tank.move_right()
        if keys[self.pygame_instance.K_UP]:
            self.player2_tank.jump()


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
                if bullet_hit_tank:
                    self.blow_sound.play()
                    blow_effect_x = tank.x + tank.width / 2 
                    blow_effect_y = tank.y + tank.height / 2
                    blow_effect = BlowEffect(blow_effect_x, blow_effect_y)
                    self.blow_effects.append(blow_effect)
                    self.screen_shake_points = self.generate_screen_shake(30, 5)  # 60 frames (1 second) duration, 5 pixels intensity
                if self.join_game:
                        data = {
                            "bullet_x": bullet.x,
                            "bullet_y": bullet.y,
                            "bullet_direction": bullet.direction,
                            "bullet_owner_id": bullet.owner_tank.id
                        }
                        self.client_socket.send(pickle.dumps(data))
        self.bullets = new_bullets

    def generate_screen_shake(self, duration, intensity):
        shake_points = []
        for _ in range(duration):
            shake_x = random.randint(-intensity, intensity)
            shake_y = random.randint(-intensity, intensity)
            shake_points.append((shake_x, shake_y))
        return shake_points

    def draw_player(self, player_tank, drawing_area):
        # Calculate the horizontal offset
        offset_x = player_tank.x - self.width // 2

        # Calculate the vertical offset
        offset_y = player_tank.y - drawing_area.get_height() // 2

        # Clip the horizontal and vertical offsets to the limits of the terrain
        offset_x = max(min(offset_x, self.terrain.width - self.width), 0)
        #offset_y = max(min(offset_y, self.terrain.height - drawing_area.get_height()), 0)

        if self.screen_shake_points:
            shake_x, shake_y = self.screen_shake_points.pop(0)
            offset_x += shake_x
            offset_y += shake_y

        drawing_area.blit(background_image, (0, 0))
        self.terrain.draw(drawing_area, (139, 69, 19), offset_x, offset_y)
        for tank in self.tanks:
            tank.draw(drawing_area, offset_x, offset_y)
        for bullet in self.bullets:
            bullet.draw(drawing_area, offset_x, offset_y)
        for blow_effect in self.blow_effects:
            blow_effect.draw(drawing_area, offset_x, offset_y)


    def draw(self):
        # Create surfaces for each player's view
        player1_view = pygame.Surface((self.width, self.height // 2))
        player2_view = pygame.Surface((self.width, self.height // 2))

        # Draw each player's view
        self.draw_player(self.player_tank, player1_view)
        self.draw_player(self.player2_tank, player2_view)

        # Render the views on the main game display
        self.game_display.blit(player1_view, (0, 0))
        self.game_display.blit(player2_view, (0, self.height // 2))

        # Draw the cannon hotness for both players
        self.draw_cannon_hotness(self.player_tank, (10, 10))
        self.draw_cannon_hotness(self.player2_tank, (10, self.height // 2 + 10))

        self.pygame_instance.display.update()

    def draw_cannon_hotness(self, player_tank, position):
        max_bar_width = 200
        bar_height = 20
        hotness_percentage = min(player_tank.cannon_hotness / player_tank.max_hotness, 1)
        bar_width = int(max_bar_width * hotness_percentage)

        # Draw the background of the hotness bar
        background_color = (128, 128, 128)
        pygame.draw.rect(self.game_display, background_color, (position[0], position[1], max_bar_width, bar_height))

        # Draw the hotness bar
        bar_color = (255, 0, 0)
        pygame.draw.rect(self.game_display, bar_color, (position[0], position[1], bar_width, bar_height))

        # Draw a border around the hotness bar
        border_color = (0, 0, 0)
        border_thickness = 2
        pygame.draw.rect(self.game_display, border_color, (position[0], position[1], max_bar_width, bar_height), border_thickness)

        # Optionally, you can display the hotness value as text
        font = pygame.font.Font(None, 24)
        text_color = (0, 0, 0)
        text = font.render(f"Hotness: {player_tank.cannon_hotness:.0f}/{player_tank.max_hotness}", True, text_color)
        self.game_display.blit(text, (position[0] + max_bar_width + 10, position[1]))

    def run(self):
        game_exit = False
        while not game_exit:
            game_exit = self.handle_events()
            self.update()
            self.draw()

            new_blow_effects = []
            for blow_effect in self.blow_effects:
                if not blow_effect.update():
                    new_blow_effects.append(blow_effect)
            self.blow_effects = new_blow_effects

            self.clock.tick(60)  # Limit frame rate to 60 FPS

            if self.join_game:
                self.client_socket.close()

        self.pygame_instance.quit()
