import math

import pygame.math
from animation import AnimatedSprite
from config import *


class Shot(AnimatedSprite):
    def __init__(self, ship, offset_x, offset_y, vel_x, vel_y):
        self.ship = ship
        self.vel = pygame.math.Vector2(vel_x*self.ship.shot_speed, vel_y*self.ship.shot_speed)
        rot = self.angle_of_velocity()
        super().__init__(0.1, False, ship.shot_sprite, ship.shot_w, ship.shot_h, rot)
        self.pos = pygame.math.Vector2(ship.rect.centerx + offset_x, ship.rect.centery + offset_y)
        self.cont = 0
        self.group = pygame.sprite.Group()
        self.rect.center = [int(self.pos.x), int(self.pos.y)]

    def update(self):
        super().update()
        self.move()

    def move(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.rect.center = [int(self.pos.x), int(self.pos.y)]
        if 0 > self.rect.x > screen_width - self.rect.width and 0 > self.rect.y > screen_height - self.rect.height:
            self.kill()

    def angle_of_velocity(self):
        rot = 0
        if self.vel.length() > 0:
            angle = self.vel.normalize().angle_to(pygame.math.Vector2(0, 1))
            rot = angle
        return rot


class TimedShot(Shot):
    def __init__(self, ship, offset_x, offset_y, vel_x, vel_y, speed):
        super().__init__(ship, offset_x, offset_y, vel_x, vel_y)
        self.speed = speed
        self.play_once = True


class BounceShot(Shot):
    def __init__(self, ship, offset_x, offset_y, vel_x, vel_y, bounce):
        super().__init__(ship, offset_x, offset_y, vel_x, vel_y)
        self.bounce = bounce

    def move(self):
        super().move()
        if self.pos.x > 1580 or self.pos.x < 20:
            self.vel.x *= -1
            self.bounce -= 1
        if self.pos.y > 900 or self.pos.y < self.rect.h / 2:
            self.vel.y *= -1
            self.bounce -= 1
        if self.bounce < 0:
            self.kill()


class SplitShot(Shot):
    def __init__(self, ship, offset_x, offset_y, vel_x, vel_y, time, split):
        super().__init__(ship, offset_x, offset_y, vel_x, vel_y)
        self.timer = time
        self.split = split
        self.shot_speed = self.ship.shot_speed
        self.shot_sprite = self.ship.shot_sprite
        self.shot_w = self.ship.shot_w * 3/4
        self.shot_h = self.ship.shot_h * 3/4

    def update(self):
        super().update()
        if self.timer > 0:
            self.timer -= 1
        else:
            shots = [Shot(self, 10 * math.cos(i * 2 * math.pi / self.split + math.pi / self.split),
                          10 * math.sin(i * 2 * math.pi / self.split + math.pi / self.split),
                          math.cos(i * 2 * math.pi / self.split + math.pi / self.split),
                          math.sin(i * 2 * math.pi / self.split + math.pi / self.split))
                     for i in range(self.split)]
            for shot in shots:
                self.ship.shot_sprites.add(shot)
            self.kill()
