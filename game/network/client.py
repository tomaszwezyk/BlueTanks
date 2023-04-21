import socket
import pygame
import sys
import socket
import threading
import random
import pygame
import pickle
import sys
from game.models.commons import *
from game.models.game import Game
from game.models.tank import Tank

# pygame.init()
#
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("2D Tank Game")
#
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('127.0.0.1', 6666))
#
# def send_data(data):
#     client.sendall(data.encode())
#
# def recv_data():
#     data = client.recv(1024)
#     return data.decode()
#
# # Add your Pygame game code here, handling the tank and barrel movement, shooting mechanics, etc.
# # You can use send_data() function to send player states to the server/host, and recv_data() function to receive updates from the server/host.
# # ...
#
# pygame.quit()
# sys.exit()

def join_game():
    game = Game()
    game.is_host = False

    # Find host IP address
    host_ip = None
    for i in range(256):
        host = f"192.168.0.{i}" # change this to your network address range
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((host, 1234))
        except:
            continue
        else:
            host_ip = host
            s.close()
            break

    if host_ip is None:
        print("Could not find any hosted game on the network.")
        return

    # Connect to host
    print(f"Connecting to host at {host_ip}...")
    game.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    game.socket.connect((host_ip, 1234))

    # Start game loop
    while True:
        # Send client state to host
        tanks_state = [(tank.x, tank.y, tank.color, tank.barrel_angle) for tank in game.tanks]
        bullets_state = [(bullet.x, bullet.y, bullet.color) for bullet in game.bullets]
        state = (tanks_state, bullets_state)
        data = pickle.dumps(state)
        game.socket.send(data)

        # Receive game state from host
        data = game.socket.recv(1024)
        if not data:
            break
        state = pickle.loads(data)
        game.update_server_state(state)

        # Handle user input
        left_pressed = False
        right_pressed = False
        up_pressed = False
        down_pressed = False
        space_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
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

        # Move tanks and update bullets
        game.move_tanks(left_pressed, right_pressed, up_pressed, down_pressed, space_pressed)
        game.update_bullets()

        # Draw game
        game.draw()

        # Limit frame rate
        game.clock.tick(60)

    game.socket.close()
    print("Disconnected from host.")

