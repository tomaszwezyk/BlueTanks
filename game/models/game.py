import pickle

import pygame
from game.models.commons import *
import socket
import sys
import random

from game.models.bullet import Bullet
from game.models.tank import Tank



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tanks Game")
        self.clock = pygame.time.Clock()
        self.tanks = []
        self.bullets = []
        self.is_host = False
        self.socket = None

    def add_tank(self, tank):
        self.tanks.append(tank)

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def move_tanks(self, left_pressed, right_pressed, up_pressed, down_pressed, space_pressed):
        for tank in self.tanks:
            if left_pressed:
                tank.move_left()
            if right_pressed:
                tank.move_right()
            if up_pressed:
                tank.adjust_barrel_up()
            if down_pressed:
                tank.adjust_barrel_down()
            if space_pressed:
                bullet = tank.shoot()
                self.add_bullet(bullet)
                if self.is_host:
                    self.send_bullet_to_clients(bullet)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                self.bullets.remove(bullet)
                continue
            for tank in self.tanks:
                if tank.color != bullet.color and math.sqrt((tank.x - bullet.x) ** 2 + (tank.y - bullet.y) ** 2) < TANK_HEIGHT:
                    self.bullets.remove(bullet)
                    self.tanks.remove(tank)
                    if self.is_host:
                        self.send_tanks_to_clients()

    def draw(self):
        self.screen.fill(WHITE)
        for tank in self.tanks:
            tank.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        pygame.display.update()

    def run(self):
        if self.is_host:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('localhost', 1234))
            self.socket.listen(2)
            print("Server started. Waiting for clients to connect...")
            conn, addr = self.socket.accept()
            print("Client connected:", addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                state = pickle.loads(data)
                self.update_client_state(state)
            conn.close()
            print("Client disconnected.")
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(('localhost', 1234))
            print("Connected to server.")
            while True:
                state = self.get_client_state()
                data = pickle.dumps(state)
                self.socket.send(data)

        running = True
        while running:
            left_pressed = False
            right_pressed = False
            up_pressed = False
            down_pressed = False
            space_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left_pressed = True
                    elif event.key == pygame.K_RIGHT:
                        right_pressed = True
                    elif event.key == pygame.K_UP:
                        up_pressed = True
                    elif event.key == pygame.K_DOWN:
                        down_pressed = True
                    elif event.key == pygame.K_SPACE:
                        space_pressed = True

            self.move_tanks(left_pressed, right_pressed, up_pressed, down_pressed, space_pressed)
            self.update_bullets()
            self.draw()
            self.clock.tick(60)

    def update_client_state(self, state):
        for i, tank in enumerate(self.tanks):
            tank.x = state['tanks'][i]['x']
            tank.y = state['tanks'][i]['y']
            tank.barrel_angle = state['tanks'][i]['barrel_angle']
        self.bullets = []
        for bullet_data in state['bullets']:
            bullet = Bullet(bullet_data['x'], bullet_data['y'], bullet_data['angle'], bullet_data['color'])
            self.add_bullet(bullet)

    def send_tanks_to_clients(self):
        state = {'tanks': [], 'bullets': []}
        for tank in self.tanks:
            state['tanks'].append({'x': tank.x, 'y': tank.y, 'barrel_angle': tank.barrel_angle})
        data = pickle.dumps(state)
        self.socket.send(data)

    def send_bullet_to_clients(self, bullet):
        state = {'tanks': [], 'bullets': [{'x': bullet.x, 'y': bullet.y, 'angle': bullet.angle, 'color': bullet.color}]}
        data = pickle.dumps(state)
        self.socket.send(data)

    def get_client_state(self):
        state = {'tanks': [], 'bullets': []}
        for tank in self.tanks:
            state['tanks'].append({'x': tank.x, 'y': tank.y, 'barrel_angle': tank.barrel_angle})
        for bullet in self.bullets:
            state['bullets'].append({'x': bullet.x, 'y': bullet.y, 'angle': bullet.angle, 'color': bullet.color})
        return state
