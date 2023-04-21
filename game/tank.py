import pygame
import time
import uuid

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 30
        self.speed = 0.1  # Reduce tank speed to 1/10th of original
        self.gravity = 0.5
        self.direction = 1  # Initialize direction to 1 (right)     

        self.uuid = uuid.uuid4()
        
        self.cannon_hotness = 0
        self.cannon_jammed = False
        self.jam_time = None
        self.jam_duration = 3  # Jammed for 3 seconds
        self.max_hotness = 100  # Maximum hotness before the cannon gets jammed		

    def draw(self, game_display, offset_x, offset_y):
        # Load tank image
        tank_img = pygame.image.load('assets/tank.gif')

        # Tank dimensions
        tank_width = int(2.5 * tank_img.get_width())
        tank_height = int(1.5 * tank_img.get_height())

        # Tank position
        tank_rect = tank_img.get_rect()
        tank_rect.center = (self.x - offset_x, self.y - offset_y)

        # Flip tank image if facing left
        if self.direction == 1:
            tank_img = pygame.transform.flip(tank_img, True, False)

        # Draw the tank
        game_display.blit(tank_img, tank_rect)

    def shoot(self):
        if not self.cannon_jammed:
            self.cannon_hotness += 20  # Increase hotness by 20 for each shot
            if self.cannon_hotness >= self.max_hotness:
                self.cannon_jammed = True
                self.jam_time = time.time()
            return True
        return False

    def update_cannon_hotness(self):
        if self.cannon_jammed:
            if time.time() - self.jam_time >= self.jam_duration:
                self.cannon_jammed = False
                self.cannon_hotness = self.max_hotness
        else:
            self.cannon_hotness = max(0, self.cannon_hotness - 0.5)  # Cool down the cannon by 0.5 units

    def update(self, terrain):
        self.update_cannon_hotness()
        
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
        self.x -= 10
        self.direction = -1

    def move_right(self):
        self.x += 10
        self.direction = 1

    def jump(self):
        self.speed = -10
