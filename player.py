import math

from ship import Ship
from shot import Shot
from config import *


class PlayerShip(Ship):
    def __init__(self, sheet, pos):
        super().__init__()
        self.score = 0
        self.shot_time = 10
        self.number_of_shots = 1
        self.shot_speed = 10
        self.move_speed = 6
        self.damage = 10
        self.hp = 500
        self.make_ship(sheet, 'Sprites/fire', pos)
        self.invincibility_time = 100
        self.invincible_timer = 0
        self.shooting = False
        self.vel = pygame.math.Vector2(0, 0)
        self.store = pygame.math.Vector2(0, 0)

    def go(self, axis, speed):
        if self.vel[axis] == speed*-1:
            self.store[axis] = self.vel[axis]
        self.vel[axis] = speed

    def stop(self, axis, speed):
        if self.vel[axis] == speed:
            self.vel[axis] = self.store[axis]
            self.store[axis] = 0
        elif speed == self.store[axis]:
            self.store[axis] = 0

    def lose_hp(self, damage):
        if self.invincible_timer <= 0:
            super().lose_hp(damage)
            self.invincible_timer = self.invincibility_time

    def shot_angle(self, i):
        spread_angle = math.pi / 18 * self.number_of_shots
        if self.number_of_shots > 1:
            return i * spread_angle / (self.number_of_shots-1) - math.pi/2 - spread_angle/2
        else:
            return -math.pi/2

    def shoot_(self):
        self.shooting = not self.shooting

    def create_shots(self):
        shots = [Shot(self, 40 * math.cos(self.shot_angle(i)),
                      40 * math.sin(self.shot_angle(i)),
                      math.cos(self.shot_angle(i)),
                      math.sin(self.shot_angle(i)))
                 for i in range(self.number_of_shots)]
        shotSoundEffect.play()
        return shots

    def move(self):
        speed = self.vel.copy()
        if speed.length() > 0:
            speed.normalize()
        if 0 < self.rect.x + speed[0] * self.move_speed < screen_width-self.rect.width:
            self.rect.x += speed[0] * self.move_speed
        if 0 < self.rect.y + speed[1] * self.move_speed < screen_height-self.rect.height:
            self.rect.y += speed[1] * self.move_speed

    def update(self):
        if self.shooting:
            self.shoot = True
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        self.alpha = 255-255*self.invincible_timer/100
        super().update()
