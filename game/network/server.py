import socket
import threading
import random
import pygame
import pickle
import sys
from models.commons import *
from models.game import Game
from models.tank import Tank

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(('0.0.0.0', 6666))
# server.listen()
#
# clients = []
# player_data = {}
#
# def handle_client(conn, addr):
#     global clients, player_data
#     print(f"[NEW CONNECTION] {addr} connected.")
#     clients.append(conn)
#
#     while True:
#         try:
#             data = conn.recv(1024)
#             if not data:
#                 break
#
#             for client in clients:
#                 if client != conn:
#                     client.send(data)
#         except Exception as e:
#             print(f"[EXCEPTION] {e}")
#             break
#
#     clients.remove(conn)
#     conn.close()
#
# while True:
#     conn, addr = server.accept()
#     player_data[addr] = None
#     thread = threading.Thread(target=handle_client, args=(conn, addr))
#     thread.start()


def host_game():
    game = Game()
    game.is_host = True
    tank_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    tank = Tank(SCREEN_WIDTH/2 - TANK_WIDTH/2, SCREEN_HEIGHT - TANK_HEIGHT - 10, tank_color)
    game.add_tank(tank)

    # Start hosting the game
    game.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    game.socket.bind(('localhost', 1234))
    game.socket.listen(2)
    print("Server started. Waiting for clients to connect...")
    conn, addr = game.socket.accept()
    print("Client connected:", addr)

    # Start game loop
    while True:
        # Receive client state
        data = conn.recv(1024)
        if not data:
            break
        state = pickle.loads(data)
        game.update_client_state(state)

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

        # Send game state to clients
        tanks_state = [(tank.x, tank.y, tank.color, tank.barrel_angle) for tank in game.tanks]
        bullets_state = [(bullet.x, bullet.y, bullet.color) for bullet in game.bullets]
        state = (tanks_state, bullets_state)
        data = pickle.dumps(state)
        conn.send(data)

        # Draw game
        game.draw()

        # Limit frame rate
        game.clock.tick(60)

    conn.close()
    print("Client disconnected.")
