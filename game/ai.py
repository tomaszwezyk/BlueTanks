import random

class SimpleAI:
    def __init__(self, tank, target_tank, terrain):
        self.tank = tank
        self.target_tank = target_tank
        self.terrain = terrain
        self.random_offset = self.generate_random_offset()

    def generate_random_offset(self):
        offset_x = random.randint(-50, 50)
        offset_y = random.randint(-50, 50)
        return (offset_x, offset_y)

    def update(self):
        self.move_towards_target()
        self.fire_at_target()
        self.update_bullets()

        # Move towards the target
        if abs(self.tank.x - target_x) > 50:
            if self.tank.x > target_x:
                self.tank.move_left()
            else:
                self.tank.move_right()

        # Jump towards the target
        if self.tank.on_ground and abs(self.tank.y - target_y) > 50:  # Remove the parentheses here
            self.tank.jump()

        # Fire at the target
        if self.fire_countdown <= 0:
            angle = self.calculate_angle_to_target()
            if self.tank.shoot():
                bullet = Bullet(angle, self.tank)
                self.bullets.append(bullet)
            self.fire_countdown = self.fire_cooldown
        else:
            self.fire_countdown -= 1
