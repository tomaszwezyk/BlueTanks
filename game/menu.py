import pygame
import threading
from game.game import Game
from game.server import Server

class Menu:
    def __init__(self, pygame_instance, width=800, height=600):
        # Set up the game window
        self.width = width
        self.height = height
        self.game_display = pygame_instance.display.set_mode((width, height))
        pygame_instance.display.set_caption("Tank Game")

        # Set up font
        self.font = pygame_instance.font.Font(None, 24)

        # Set up buttons
        self.start_button = pygame_instance.Rect(300, 200, 200, 50)
        self.server_button = pygame_instance.Rect(300, 270, 200, 50)
        self.stop_button = pygame_instance.Rect(300, 340, 200, 50)
        self.join_button = pygame_instance.Rect(550, 300, 100, 50)

        # Initialize server
        self.server = None

        # Set up input text box
        self.input_box = pygame_instance.Rect(300, 400, 200, 50)
        self.input_text = "192.168.117.206"

    def start_game(self):
        # Create and run the game
        game = Game(pygame, self.width, self.height)
        game.run()

    def start_server(self):
        # Create and run the server in a new thread
        self.server = Server()
        server_thread = threading.Thread(target=self.server.start)
        server_thread.start()

    def stop_server(self):
        # Stop the server if it is running
        if self.server:
            self.server.stop()
            self.server = None

    def join_game(self):
        # Create and run the game as a client
        print("join game"+ self.input_text)
        game = Game(pygame, self.width, self.height, True, self.input_text)
        game.run()

    def run(self):
        # Game loop
        menu_exit = False
        while not menu_exit:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_exit = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.start_button.collidepoint(event.pos):
                        self.start_game()
                    elif self.server_button.collidepoint(event.pos):
                        self.start_server()
                    elif self.stop_button.collidepoint(event.pos):
                        self.stop_server()
                    elif self.join_button.collidepoint(event.pos):
                        self.join_game()
                    elif self.input_box.collidepoint(event.pos):
                        pygame.key.start_text_input()
                    else:
                        pygame.key.stop_text_input()


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Get the IP address entered in the input box and do something with it
                        ip_address = self.input_text
                        print("IP Address entered:", ip_address)
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

            # Update screen
            self.game_display.fill((0, 0, 0))
            pygame.draw.rect(self.game_display, (255, 255, 255), self.start_button)
            start_text = self.font.render("Start Local Game", True, (0, 0, 0))
            self.game_display.blit(start_text, (self.start_button.x + 10, self.start_button.y + 10))
            pygame.draw.rect(self.game_display, (255, 255, 255), self.server_button)
            server_text = self.font.render("Start Server", True, (0, 0, 0))
            self.game_display.blit(server_text, (self.server_button.x + 10, self.server_button.y + 10))
            pygame.draw.rect(self.game_display, (255, 255, 255), self.stop_button)
            stop_text = self.font.render("Stop Server", True, (0, 0, 0))
            self.game_display.blit(stop_text, (self.stop_button.x + 10, self.stop_button.y + 10))
            pygame.draw.rect(self.game_display, (255, 255, 255), self.input_box)
            input_text = self.font.render(self.input_text, True, (0, 0, 0))
            self.game_display.blit(input_text, (self.input_box.x + 10, self.input_box.y + 10))
            pygame.draw.rect(self.game_display, (255, 255, 255), self.join_button)
            join_text = self.font.render("Join Game", True, (0, 0, 0))
            self.game_display.blit(join_text, (self.join_button.x + 10, self.join_button.y + 10))
            pygame.display.update()

        # Quit Pygame
        pygame.quit()
