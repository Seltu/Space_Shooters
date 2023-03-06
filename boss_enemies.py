import math
import random

from config import *
from ship import Ship
from shot import Shot
from shot import TimedShot
from shot import BounceShot
from shot import SplitShot
from wave import Wave


class BossEnemy(Ship):
    def __init__(self, pos):
        super().__init__()
        self.boss_cycle = 1
        self.boss_step = 0
        self.boss_timer = 0
        self.aimed = False
        self.summon = True
        self.changed_shot = False
        self.target = None
        self.boss = True

    def set_target(self, target):
        self.target = target

    def change_shot(self, time, shot=None, h=None, w=None, speed=None):
        if self.changed_shot:
            return
        self.shot_time = time
        self.shoot_time = time
        if speed is not None:
            self.shot_speed = speed
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
        if self.boss_timer < 1:
            self.boss_timer += 1 / 600
        else:
            if self.boss_step < self.boss_cycle:
                self.boss_step += 1
            else:
                self.boss_step = 0
            self.boss_timer = 0
            self.on_step()
        self.move()

    def on_step(self):
        self.shoot_time = 0
        self.summon = True
        self.changed_shot = False
        self.shoot_time = 0


class BossBaron(BossEnemy):
    def __init__(self, pos):
        super().__init__(pos)
        self.hp = 4000
        self.shot_speed = 5
        self.shot_time = 10
        self.boss_timer = 0.9
        self.boss_step = -1
        self.boss_cycle = 4
        self.make_ship('Sprites/boss_baron', 'Sprites/baron_fire')
        self.rect.center = (pos[0], pos[1])
        self.direction = 1
        self.aux = 1

    def move(self):
        if self.boss_step < 0:
            self.rect.y += self.direction
        else:
            self.rect.x += self.direction
        if self.rect.centerx > 1200:
            self.direction = -1
        elif self.rect.centerx < 400:
            self.direction = 1
        if self.rect.centerx > 1200 or self.rect.centerx < 400:
            self.rect.y -= 10 * self.direction
        pass

    def create_shots(self):
        if self.boss_step == 0:
            self.change_shot(15, 'Sprites/baron_fire', 50, 50)
            shots = [Shot(self, random.randint(self.rect.left, self.rect.right) - self.rect.centerx, 0, 0, 1)]
            return shots
        elif self.boss_step == 1:
            shots = [Shot(self, i - self.rect.centerx + 90, 0, 0, 1) for i in
                     range(self.rect.left, self.rect.right, 400)]
            return shots
        elif self.boss_step == 2:
            self.change_shot(100, 'Sprites/baron_wave', 220, 256)
            shots = [TimedShot(self, i - self.rect.centerx + 50, 0, -math.cos(
                math.pi + math.pi * ((self.rect.width - (i - self.rect.left)) / self.rect.width)),
                               1, 0.08)
                     for i in range(self.rect.left, self.rect.right, 100)]
            return shots
        elif self.boss_step == 3:
            self.change_shot(20, 'Sprites/baron_wave', 220, 256)
            shots = [TimedShot(self, 0, 0, 0, 1, 0.08)]
            return shots
        elif self.boss_step == 4:
            self.change_shot(60, 'Sprites/baron_fire', 50, 50)
            shots = [Shot(self, i - self.rect.centerx + 150 * self.aux, 0, 0, 1) for i in
                     range(self.rect.left, self.rect.right, 150)]
            self.aux *= -1
            return shots

    def create_waves(self):
        waves = []
        if self.boss_step == 1:
            waves = [Wave(2, 3, waveline3.shift(-350, 0)), Wave(2, 3, waveline4.shift(350, 0))]
        elif self.boss_step == 2:
            waves = [Wave(4, 4, waveline1.shift(-350, 0)), Wave(4, 4, waveline2.shift(350, 0))]
        elif self.boss_step == 3:
            waves = [Wave(4, 2, waveline6), Wave(4, 2, waveline7),
                     Wave(4, 2, waveline6.shift(-60, 60)), Wave(4, 2, waveline7.shift(60, 60)),
                     Wave(4, 2, waveline6.shift(60, -60)), Wave(4, 2, waveline7.shift(-60, -60))]
        elif self.boss_step == 4:
            waves.append(Wave(4, 6, waveline5.shift(0, -400)))
        return waves


class BossJester(BossEnemy):
    def __init__(self, pos):
        super().__init__(pos)
        self.hp = 4500
        self.health_stage = 0
        self.speed = 0.05
        self.shot_speed = 5
        self.shot_time = 10
        self.boss_timer = 0.4
        self.boss_step = -1
        self.boss_cycle = 3
        self.load_path('Sprites/boss_jester/idle', 484, 254)
        self.shot_sprite = 'Sprites/boss_jester/fireblue'
        self.rect.center = (pos[0], pos[1])
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.move_speed = 1.3
        self.direction = pygame.math.Vector2(1, 1)
        self.shot_tilt = math.pi * 1 / 3
        self.target = pygame.math.Vector2(0, 0)
        self.aimed = True
        self.blue = True
        self.aux = False

    def move(self):
        if self.boss_step < 0:
            self.pos.y += 1
        else:
            self.pos.x += self.direction[0] * self.move_speed
            self.pos.y += self.direction[1] * self.move_speed
        if self.pos.x > 1580 or self.pos.x < 300:
            self.direction.x *= -1
        if self.pos.y > 800 - self.rect.h / 2 or self.pos.y < self.rect.h / 2:
            self.direction.y *= -1
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def change_shot(self, time, shot=None, h=None, w=None, speed=None):
        super().change_shot(time, shot, h, w, speed)

    def lose_hp(self, damage):
        dead = super().lose_hp(damage)
        if self.hp <= 1500 and self.health_stage <= 1:
            self.load_path('Sprites/boss_jester/destroyed_blue', 484, 254)
            self.speed = 0.3
            self.move_speed = 2.2
            self.health_stage += 1
        elif self.hp <= 3000 and self.health_stage <= 0:
            self.speed = 0.15
            self.move_speed = 1.8
            self.load_path('Sprites/boss_jester/destroyed_pink', 484, 254)
            self.health_stage += 1
        return dead

    def create_shots(self):
        left = []
        right = []
        if self.boss_step == 0:
            if self.blue:
                self.shot_sprite = 'Sprites/boss_jester/fireblue'
            else:
                self.shot_sprite = 'Sprites/boss_jester/firepink'
            self.change_shot(70, 'Sprites/boss_jester/fireblue', 50, 50, speed=5)
            shots = [(Shot(self, - 40 - j * 200 + 40 * math.cos(
                2 * math.pi + self.shot_tilt + i / 10 + math.pi * 2 / 3 * w) * (1 - j * 2),
                           -80 + 40 * math.sin(2 * math.pi + self.shot_tilt + i / 10 + math.pi * 2 / 3 * w),
                           math.cos(2 * math.pi + self.shot_tilt + i / 10 + math.pi * 2 / 3 * w) * (1 - j * 2),
                           math.sin(2 * math.pi + self.shot_tilt + i / 10 + math.pi * 2 / 3 * w)),)
                     for i in range(3) for j in range(2) for w in range(3)
                     ]
            self.blue = not self.blue
            if self.rect.centerx > 800:
                self.shot_tilt -= 0.2
            else:
                self.shot_tilt += 0.2
            return shots
        if (self.boss_step == 1 or self.boss_step == 3) and self.health_stage <= 1:
            if self.boss_step == 1:
                self.change_shot(100, 'Sprites/boss_jester/fireblue', 70, 70, speed=15)
            shot_direction = pygame.math.Vector2(self.target.x - self.rect.centerx,
                                                 self.target.y - self.rect.centery).normalize()
            left = [
                Shot(self, -40 + shot_direction.x * 5, shot_direction.y * 5 - 80, shot_direction.x, shot_direction.y)]
            if self.boss_step == 1:
                return left
        if (self.boss_step == 2 or self.boss_step == 3) and self.health_stage <= 1:
            quantity = 5
            offset = -240
            if self.boss_step == 2:
                self.change_shot(100, 'Sprites/boss_jester/firepink', speed=15)
            if self.health_stage == 1:
                offset = -40
                quantity = 3
                self.shot_sprite = 'Sprites/boss_jester/fireblue'
            right = [Shot(self, offset + 10 * math.cos(i * 2 * math.pi / quantity + self.shot_tilt),
                          -80 + 10 * math.sin(i * 2 * math.pi / quantity + self.shot_tilt),
                          math.cos(i * 2 * math.pi / quantity + self.shot_tilt),
                          math.sin(i * 2 * math.pi / quantity + self.shot_tilt))
                     for i in range(quantity)]
            self.shot_tilt += math.pi / quantity
            if self.boss_step == 2:
                return right
        if self.boss_step == 3:
            self.change_shot(50, h=70, w=70, speed=10)
            self.aux = not self.aux
            if self.aux:
                self.blue = not self.blue
                if self.blue:
                    self.shot_sprite = 'Sprites/boss_jester/fireblue'
                    return right
                else:
                    self.shot_sprite = 'Sprites/boss_jester/firepink'
                    return left
            else:
                self.shot_sprite = 'Sprites/boss_jester/spiral'
                shot_direction = pygame.math.Vector2(self.target.x - self.rect.centerx,
                                                     self.target.y - self.rect.centery).normalize()
                spiral = [BounceShot(self, -140 + shot_direction.x * 5, shot_direction.y * 5 - 80, shot_direction.x,
                                     shot_direction.y, 5)]
                if self.blue:
                    self.shot_sprite = 'Sprites/boss_jester/fireblue'
                else:
                    self.shot_sprite = 'Sprites/boss_jester/firepink'
                return spiral

    def create_waves(self):
        waves = []
        if self.boss_step == 1:
            if self.health_stage <= 1:
                waves = [Wave(3, 1, waveline3.shift(-400, 0)), Wave(3, 1, waveline4.shift(400, 0))]
            else:
                waves = [Wave(3, 2, waveline3.shift(-400, 0)), Wave(3, 2, waveline4.shift(400, 0)),
                         Wave(2, 6, waveline5.shift(0, -200))]
        elif self.boss_step == 2:
            waves = [Wave(0, 10, waveline5.shift(0, -150)), Wave(1, 5, waveline5.shift(0, -100))]
        elif self.boss_step == 3 and self.health_stage >= 2:
            waves = [Wave(2, 2, waveline3.shift(-400, 0)), Wave(2, 2, waveline4.shift(400, 0)),
                     Wave(0, 10, waveline5.shift(0, -150))]
        return waves


class BossMonarch(BossEnemy):
    def __init__(self, pos):
        super().__init__(pos)
        self.hp = 10000
        self.shot_speed = 5
        self.shot_time = 10
        self.boss_timer = 0.5
        self.boss_step = -1
        self.boss_cycle = 5
        self.make_ship('Sprites/boss_monarch', 'Sprites/monarch_fire')
        self.rect.center = (pos[0], pos[1])
        self.direction = 1
        self.aux = 1
        self.aimed = True
        self.target = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.direction = pygame.math.Vector2(1, 1)
        self.move_speed = 2
        self.shot_tilt = 0
        self.entered = False

    def move(self):
        if self.boss_timer > 0.9:
            self.alpha = 255 - 255 * (self.boss_timer - 0.9) * 10
        elif self.boss_timer < 0.2:
            new_alpha = 255 - 255 * (1.1 - self.boss_timer * 11)
            if new_alpha > 0:
                self.alpha = new_alpha
            else:
                self.alpha = 0
        else:
            self.alpha = 255
        if self.boss_step < 0:
            self.pos.y += 1
        else:
            self.pos.x += self.direction.x * self.move_speed * (1 - self.boss_timer)
            self.pos.y += self.direction.y * self.move_speed * (1 - self.boss_timer)
        if self.pos.x > 1600 - self.rect.width / 2 or self.pos.x < self.rect.width / 2:
            self.direction.x *= -1
        if self.pos.y > 600 - self.rect.h / 2 or self.pos.y < self.rect.h / 2:
            self.direction.y *= -1
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def on_step(self):
        super().on_step()
        if self.entered:
            self.pos.x = random.randint(int(self.rect.width / 2), int(1600 - self.rect.width / 2))
            self.pos.y = random.randint(int(self.rect.h / 2), int(600 - self.rect.h / 2))
            self.rect.center = (int(self.pos.x), int(self.pos.y))
        else:
            self.entered = True
        self.shot_tilt = 0
        if self.boss_step == 0:
            self.move_speed = 3
        if self.boss_step == 1:
            self.move_speed = 1

    def create_shots(self):
        if self.boss_step == 0 or self.boss_step == 5:
            if self.boss_step == 0:
                self.change_shot(20, 'Sprites/monarch_fire', 50, 50, speed=5)
                quantity = 7
            else:
                self.change_shot(100, 'Sprites/monarch_fire', 50, 50, speed=5)
                quantity = 14
            shots = [Shot(self, 20 + 10 * math.cos(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity + self.shot_tilt),
                          10 * math.sin(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity + self.shot_tilt),
                          math.cos(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity + self.shot_tilt),
                          math.sin(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity + self.shot_tilt))
                     for i in range(quantity)]
            self.shot_tilt += math.pi / quantity
            return shots
        elif self.boss_step == 1:
            self.change_shot(5, speed=10)
            quantity = 7
            shots = [Shot(self, 20 + 10 * math.cos(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity + self.shot_tilt),
                          10 * math.sin(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity + self.shot_tilt),
                          math.cos(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity + self.shot_tilt),
                          math.sin(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity + self.shot_tilt))
                     for i in range(quantity)]
            if 0 < self.boss_timer < 0.1 or 0.2 < self.boss_timer < 0.3 or 0.4 < self.boss_timer < 0.5 or\
                    0.6 < self.boss_timer < 0.7 or 0.8 < self.boss_timer < 0.9:
                self.shot_tilt += 0.05
            else:
                self.shot_tilt -= 0.05
            return shots
        elif self.boss_step == 2:
            self.change_shot(200, speed=2)
            quantity = 7
            shots = [SplitShot(self, 20 + 10 * math.cos(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity),
                               10 * math.sin(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity),
                               math.cos(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity),
                               math.sin(i * 2 * math.pi / quantity + 0.5 * math.pi / quantity), 100, 6)
                     for i in range(quantity)]
            return shots
        elif self.boss_step == 3:
            self.change_shot(50, h=70, w=70, speed=5)
            shot_direction = pygame.math.Vector2(self.target.x - self.rect.centerx,
                                                 self.target.y - self.rect.centery).normalize()
            shots = [Shot(self, 20 + shot_direction.x * 100, shot_direction.y * 100, shot_direction.x, shot_direction.y)]
            return shots

    def create_waves(self):
        waves = []
        if self.boss_step == 4:
            waves = [Wave(0, 6, waveline5.shift(0, -220)), Wave(4, 6, waveline5.shift(0, -200)),
                     Wave(2, 6, waveline5.shift(0, -150)), Wave(1, 6, waveline5.shift(0, -100))]
        if self.boss_step == 5:
            waves = [Wave(5, 6, waveline6), Wave(5, 6, waveline7)]
        return waves
