import random

class SimpleAI:
    def __init__(self, tank, target_tank, terrain, bullet_class):
        self.tank = tank
        self.target_tank = target_tank
        self.terrain = terrain
        self.bullet_class = bullet_class

    def update(self):
        min_distance = 50
        max_distance = 250
        distance = random.randint(min_distance, max_distance)

        if self.tank.x < self.target_tank.x - distance:
            self.tank.move_right()
        elif self.tank.x > self.target_tank.x + distance:
            self.tank.move_left()
        else:
            # Randomly decide whether to move right or left
            if random.random() < 0.01:
                if random.random() < 0.5:
                    self.tank.move_right()
                else:
                    self.tank.move_left()

        if random.random() < 0.01:
            self.tank.jump()

        if random.random() < 0.005:
            if self.tank.shoot():
                angle = 45 if self.tank.direction == 1 else 135
                bullet = self.bullet_class(angle, self.tank)
                return bullet

        return None
