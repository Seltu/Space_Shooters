import math

from ship import Ship
from shot import Shot
from config import *


class PlayerShip(Ship):
    def __init__(self, sheet, pos):
        super().__init__()
        self.score = 0
        self.shot_time = 15
        self.number_of_shots = 6
        self.move_speed = 4
        self.damage = 10
        self.hp = 5
        self.make_ship(sheet, 'Sprites/fire.png', pos)
        self.invincibility_time = 100
        self.invincible_timer = 0

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

    def create_shots(self):
        angle = math.pi + math.pi/self.number_of_shots/2
        shots = [Shot(self, 10 * math.cos(i * math.pi / self.number_of_shots + angle) + self.rect.width / 2,
                      10 * math.sin(i * math.pi / self.number_of_shots + angle) + self.rect.height / 2,
                      self.shot_speed * math.cos(i * math.pi / self.number_of_shots + angle),
                      self.shot_speed * math.sin(i * math.pi / self.number_of_shots + angle))
                 for i in range(self.number_of_shots)]
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
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        self.alpha = 255-255*self.invincible_timer/100
        super().update()
