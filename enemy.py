import math
from ship import Ship


class EnemyShip(Ship):
    def __init__(self, sheet, shot, curve, shoot_delay):
        super().__init__()
        self.previous_point = None
        self.aimed = False
        self.curve = curve
        self.bezier_timer = 0
        self.shoot_time = shoot_delay
        self.make_ship(sheet, shot)
        self.rect.center = self.curve.get_quartet(0).calculate_path_point(0)

    def move(self):
        control_point_index = int(self.bezier_timer)
        path_point = self.curve.get_quartet(control_point_index).calculate_path_point(self.bezier_timer)
        if self.previous_point is None:
            self.previous_point = path_point
        self.previous_point = path_point
        self.rect.centerx = path_point.x
        self.rect.centery = path_point.y
        self.bezier_timer += 0.0008 * self.curve.number_of_quartets()
        if int(self.bezier_timer) > self.curve.number_of_quartets() - 1:
            self.bezier_timer = 0
            self.kill()
            self.dead = True

    def update(self):
        super().update()
        if self.dead:
            return
        self.shoot_()
        self.move()

    @staticmethod
    def calculate_rotation(previous_point, current_point):
        dx = current_point.xpos - previous_point.xpos
        dy = current_point.ypos - previous_point.ypos
        return math.degrees(math.atan2(dx, dy)) + 180
