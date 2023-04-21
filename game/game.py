from game.tank import Tank
from game.terrain import Terrain
from game.bullet import Bullet

class Game:
    def __init__(self, pygame_instance, width=800, height=600):

        # Create objects
        self.pygame_instance = pygame_instance
        self.tank = Tank(50, 350)
        self.terrain = Terrain(width, height)
        self.width = width
        self.game_display = pygame_instance.display.set_mode((width, height))
        self.height = height
        self.clock = pygame_instance.time.Clock()
        self.bullets = []

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
            for event in self.pygame_instance.event.get():
                if event.type == self.pygame_instance.QUIT:
                    game_exit = True
                if event.type == self.pygame_instance.KEYDOWN:
                    if event.key == self.pygame_instance.K_LCTRL:
                        # Adjust angle based on tank's direction (45 degrees for right, 135 degrees for left)
                        angle = 45 if self.tank.direction == 1 else 135
                        bullet = Bullet(self.tank.x + self.tank.width/2, self.tank.y + self.tank.height/2, angle)
                        self.bullets.append(bullet)
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
        self.pygame_instance.quit()
