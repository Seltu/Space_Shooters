import pygame
import math

from enemy import EnemyShip
from shot import Shot


class Enemy1(EnemyShip):
    def __init__(self, sheet, shot, curve, shoot_delay):
        super().__init__(sheet, shot, curve, shoot_delay)
        self.hp = 20
        self.shot_speed = 5
        self.shot_time = 150
        self.damage = 1

    def create_shots(self):
        shots = [Shot(self, -20, 0, 0, 1),
                 Shot(self, +20, 0, 0, 1)]
        return shots


class Enemy2(EnemyShip):
    def __init__(self, sheet, shot, curve, shoot_delay):
        super().__init__(sheet, shot, curve, shoot_delay)
        self.hp = 40
        self.shot_speed = 5
        self.shot_time = 150
        self.damage = 1
        self.shot_tilt = 0

    def create_shots(self):
        quantity = 6
        shots = [Shot(self, 10 * math.cos(i * 2 * math.pi / quantity + self.shot_tilt),
                      10 * math.sin(i * 2 * math.pi / quantity + self.shot_tilt),
                      math.cos(i * 2 * math.pi / quantity + self.shot_tilt),
                      math.sin(i * 2 * math.pi / quantity + self.shot_tilt))
                 for i in range(quantity)]
        self.shot_tilt += math.pi / quantity
        return shots


class Enemy3(EnemyShip):
    def __init__(self, sheet, shot, curve, shoot_delay):
        super().__init__(sheet, shot, curve, shoot_delay)
        self.hp = 30
        self.aimed = True
        self.shot_speed = 8
        self.shot_time = 180
        self.damage = 1
        self.shot_tilt = 0
        self.target = pygame.math.Vector2(0, 0)

    def create_shots(self):
        shot_direction = pygame.math.Vector2(self.target.x - self.rect.centerx,
                                             self.target.y - self.rect.centery).normalize()
        shots = [Shot(self, shot_direction.x*5, shot_direction.y*5, shot_direction.x, shot_direction.y)]
        return shots

    def set_target(self, target):
        self.target = target


class Enemy4(EnemyShip):
    def __init__(self, sheet, shot, curve, shoot_delay):
        super().__init__(sheet, shot, curve, shoot_delay)
        self.hp = 10
        self.shot_speed = 6
        self.shot_time = 8
        self.damage = 1
        self.shot_tilt = math.pi/2-math.pi*0.2
        self.shot_h = 50
        self.shot_w = 50

    def create_shots(self):
        shots = [Shot(self, 10 * math.cos(2 * math.pi + self.shot_tilt),
                      10 * math.sin(2 * math.pi + self.shot_tilt),
                      math.cos(2 * math.pi + self.shot_tilt),
                      math.sin(2 * math.pi + self.shot_tilt))]
        if self.rect.centerx > 800:
            self.shot_tilt -= math.pi * 0.41
        else:
            self.shot_tilt += math.pi * 0.41
        return shots


class BaronMinion(EnemyShip):
    def __init__(self, sheet, shot, curve, shoot_delay):
        super().__init__(sheet, shot, curve, shoot_delay)
        self.hp = 10
        self.shot_speed = 4
        self.shot_time = 130
        self.damage = 1

    def create_shots(self):
        shots = [Shot(self, 0, 0, -1, 1), Shot(self, 0, 0, 1, 1)]
        return shots
