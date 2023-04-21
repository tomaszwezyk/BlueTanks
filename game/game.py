import socket
import pickle
from game.tank import Tank
from game.terrain import Terrain
from game.bullet import Bullet

class Game:
    def __init__(self, pygame_instance, width=800, height=600, join_game=False, server_address=None):
        # Create objects
        self.pygame_instance = pygame_instance
        self.tank = Tank(50, 350)
        self.terrain = Terrain(width, height)
        self.width = width
        self.game_display = pygame_instance.display.set_mode((width, height))
        self.height = height
        self.clock = pygame_instance.time.Clock()
        self.bullets = []
        self.join_game = join_game
        self.server_address = server_address
        self.sock = None

        if join_game:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((server_address, 1234))

    def run(self):
        # Game loop
        game_exit = False
        while not game_exit:
            # Handle events
            keys = self.pygame_instance.key.get_pressed()
            if keys[self.pygame_instance.K_LEFT]:
                self.tank.move_left()
            if keys[self.pygame_instance.K_RIGHT]:
                self.tank.move_right()
            if keys[self.pygame_instance.K_SPACE]:
                self.tank.jump()

            if self.join_game:
                # Send updated tank position to server
                data = pickle.dumps((self.tank.x, self.tank.y))
                self.sock.sendall(data)

            for event in self.pygame_instance.event.get():
                if event.type == self.pygame_instance.QUIT:
                    game_exit = True
                if event.type == self.pygame_instance.KEYDOWN:
                    if event.key == self.pygame_instance.K_LCTRL:
                        bullet = Bullet(self.tank.x + self.tank.width/2, self.tank.y + self.tank.height/2, 45)
                        self.bullets.append(bullet)

            if self.join_game:
                # Receive updated positions of other tanks from server
                data = self.sock.recv(4096)
                if data:
                    positions = pickle.loads(data)
                    for i, pos in enumerate(positions):
                        if i == 0:
                            continue  # Skip self position
                        self.terrain.tanks[i-1].x = pos[0]
                        self.terrain.tanks[i-1].y = pos[1]

            # Update screen
            self.game_display.fill((0, 0, 0))
            self.terrain.draw(self.game_display, (0, 255, 0))
            self.tank.update(self.terrain)
            self.tank.draw(self.game_display)
            # Update bullets and remove those that hit the ground
            self.bullets = [bullet for bullet in self.bullets if not bullet.update(self.terrain)]
            for bullet in self.bullets:
                bullet.draw(self.game_display)

            self.pygame_instance.display.update()
            self.clock.tick(60)  # Limit frame rate to 60 FPS

        # Quit Pygame
        if self.join_game:
            self.sock.close()
        self.pygame_instance.quit()
