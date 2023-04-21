import pygame
import random
import socket
import sys

from models.commons import *

from models.game import Game
from models.tank import Tank

from network.server import host_game
from network.client import join_game


def main():
    game = Game()
    game.is_host = True # or False for non-host players
    tank_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    tank = Tank(SCREEN_WIDTH/2 - TANK_WIDTH/2, SCREEN_HEIGHT - TANK_HEIGHT - 10, tank_color)
    game.add_tank(tank)

    # Connect to server or wait for clients to connect
    if game.is_host:
        host_game()
    else:
        join_game()

    while True:
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


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tanks Game - Main Menu")
    font = pygame.font.Font(None, 50)
    host_text = font.render("Host a game", True, BLACK)
    host_rect = host_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
    join_text = font.render("Join a game", True, BLACK)
    join_rect = join_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3 + 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if host_rect.collidepoint(pygame.mouse.get_pos()):
                    host_game()
                elif join_rect.collidepoint(pygame.mouse.get_pos()):
                    join_game()

        screen.fill(WHITE)
        screen.blit(host_text, host_rect)
        screen.blit(join_text, join_rect)
        pygame.display.flip()



if __name__ == "__main__":
    main_menu()

