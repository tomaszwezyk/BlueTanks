import pygame

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.speed = 0.1  # Reduce tank speed to 1/10th of original
        self.gravity = 0.5
        self.direction = 1  # Initialize direction to 1 (right)        

    def draw(self, game_display):
        # Tank dimensions
        wheel_size = 20
        body_width = 5 * wheel_size
        body_height = 3 * wheel_size
        turret_width = 2 * wheel_size
        turret_height = 2 * wheel_size
        gun_width = 5 * wheel_size
        gun_height = wheel_size

        # Tank position
        tank_x = self.x
        tank_y = self.y

        # Colors
        black = (0, 0, 0)
        gray = (128, 128, 128)
        dark_gray = (64, 64, 64)

        # Draw the tank
        for i in range(6):
            wheel_x = tank_x + i * wheel_size
            wheel_y = tank_y - wheel_size / 3 if i == 0 or i == 5 else tank_y
            pygame.draw.circle(game_display, gray, (int(wheel_x), int(wheel_y)), wheel_size)

        body_x = tank_x + wheel_size / 2
        body_y = tank_y - body_height
        pygame.draw.rect(game_display, dark_gray, (body_x, body_y, body_width, body_height))

        turret_x = tank_x + body_width / 2 - turret_width / 2
        turret_y = tank_y - body_height - turret_height
        pygame.draw.rect(game_display, gray, (turret_x, turret_y, turret_width, turret_height))

        gun_x = tank_x + body_width / 2 - wheel_size
        gun_y = tank_y - body_height - turret_height - gun_height
        gun_width = 6 * wheel_size
        gun_rect = pygame.Rect(gun_x, gun_y, gun_width, gun_height)
        pygame.draw.rect(game_display, gray, gun_rect)


    def update(self, terrain):
        # Apply gravity
        self.speed += self.gravity
        self.y += self.speed

        # Check for collision with terrain
        tank_bottom = self.y + self.height
        terrain_bottom = terrain.get_y(self.x + self.width/2)
        if tank_bottom > terrain_bottom:
            self.speed = 0
            self.y = terrain_bottom - self.height

    def move_left(self):
        self.x -= 1
        self.direction = -1

    def move_right(self):
        self.x += 1
        self.direction = 1

    def jump(self):
        self.speed = -10
