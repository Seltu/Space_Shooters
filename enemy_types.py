from enemy import *
from shot import Shot


class Enemy1(EnemyShip):
    def __init__(self, sheet, shot, curve, shoot_delay):
        super().__init__(sheet, shot, curve, shoot_delay)
        self.hp = 20
        self.shot_speed = 5
        self.shot_time = 150
        self.damage = 1

    def create_shots(self):
        shots = [Shot(self, self.rect.width / 2 - 20, 75, 0, self.shot_speed),
                 Shot(self, self.rect.width / 2 + 20, 75, 0, self.shot_speed)]
        return shots


class Enemy2(EnemyShip):
    def __init__(self, sheet, shot, curve, shoot_delay):
        super().__init__(sheet, shot, curve, shoot_delay)
        self.hp = 50
        self.shot_speed = 5
        self.shot_time = 150
        self.damage = 1
        self.shot_tilt = 0

    def create_shots(self):
        quantity = 6
        shots = [Shot(self, 10 * math.cos(i * 2 * math.pi / quantity + self.shot_tilt) + self.rect.width / 2,
                      10 * math.sin(i * 2 * math.pi / quantity + self.shot_tilt) + self.rect.height / 2,
                      self.shot_speed * math.cos(i * 2 * math.pi / quantity + self.shot_tilt),
                      self.shot_speed * math.sin(i * 2 * math.pi / quantity + self.shot_tilt))
                 for i in range(quantity)]
        self.shot_tilt += math.pi / quantity
        return shots
