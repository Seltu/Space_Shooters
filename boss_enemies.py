import math
import random

from config import *
from ship import Ship
from shot import Shot
from shot import TimedShot
from wave import Wave


class BossEnemy(Ship):
    def __init__(self):
        super().__init__()
        self.boss_cycle = 1
        self.boss_round = []
        self.boss_timer = 0
        self.changed_shot = False

    def change_shot(self, time, shot=None, h=None, w=None):
        if self.changed_shot:
            return
        self.shot_time = time
        if shot is not None:
            self.shot_sprite = shot
        if w is not None:
            self.shot_w = w
        if h is not None:
            self.shot_h = h
        self.changed_shot = True

    def create_waves(self):
        return []

    def update(self):
        self.shoot_()
        super().update()
        if self.boss_timer < self.boss_cycle:
            self.boss_timer += 1 / 400
        else:
            self.boss_timer = 0
            self.shoot_time = 0
        if 0 < self.boss_timer-int(self.boss_timer) <= 0.003:
            self.changed_shot = False
            self.shoot_time = 0
        self.boss_round = self.create_waves()
        self.move()


class BossBaron(BossEnemy):
    def __init__(self, pos):
        super().__init__()
        self.hp = 4000
        self.shot_speed = 5
        self.shot_time = 10
        self.damage = 1
        self.boss_timer = -0.2
        self.boss_cycle = 3
        self.make_ship('Sprites/boss_baron', 'Sprites/baron_fire', pos)
        self.direction = 1

    def move(self):
        if self.boss_timer < 0:
            self.rect.y += self.direction
        else:
            self.rect.x += self.direction
        if self.rect.centerx > 1200:
            self.direction = -1
        elif self.rect.centerx < 400:
            self.direction = 1
        if self.rect.centerx > 1200 or self.rect.centerx < 400:
            if self.boss_timer > 2:
                self.rect.y += 10
            else:
                self.rect.y -= 10
        pass

    def create_shots(self):
        if int(self.boss_timer) == 0:
            self.change_shot(15, 'Sprites/baron_fire', 50, 50)
            shots = [Shot(self, random.randint(self.rect.left, self.rect.right) - self.rect.centerx, 0, 0, 1)]
            return shots
        elif int(self.boss_timer) == 1:
            shots = [Shot(self, i - self.rect.centerx + 90, 0, 0, 1) for i in
                     range(self.rect.left, self.rect.right, 400)]
            return shots
        elif int(self.boss_timer) == 2:
            self.change_shot(100, 'Sprites/baron_wave', 200, 256)
            shots = [TimedShot(self, i - self.rect.centerx + 50,
                               0, -math.cos(math.pi + math.pi * ((self.rect.width - (i - self.rect.left)) / self.rect.width)),
                               1, 0.08)
                     for i in range(self.rect.left, self.rect.right, 100)]
            return shots

    def create_waves(self):
        waves = []
        if int(self.boss_timer) == 0:
            waves = [Wave(2, 5, waveline3.shift(-350, 0)), Wave(2, 6, waveline4.shift(350, 0))]
        if int(self.boss_timer) == 2:
            waves = [Wave(0, 2, waveline6), Wave(0, 2, waveline7),
                     Wave(0, 2, waveline6.shift(-80, 80)), Wave(0, 2, waveline7.shift(80, 80)),
                     Wave(0, 2, waveline6.shift(80, -80)), Wave(0, 2, waveline7.shift(-80, -80))]
        return waves

