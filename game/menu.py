import pygame
from game.game import Game

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

    def start_game(self):
        # Create and run the game
        game = Game(pygame, self.width, self.height)
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

            # Update screen
            self.game_display.fill((0, 0, 0))
            pygame.draw.rect(self.game_display, (255, 255, 255), self.start_button)
            start_text = self.font.render("Start Local Game", True, (0, 0, 0))
            self.game_display.blit(start_text, (self.start_button.x + 10, self.start_button.y + 10))
            pygame.display.update()

        # Quit Pygame
        pygame.quit()
