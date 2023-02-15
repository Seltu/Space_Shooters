import os
import pygame.math
from animation import AnimatedSprite
from config import *


class Ship(AnimatedSprite):
    def __init__(self):
        super().__init__(0.1, False)
        self.damage = 0
        self.hp = 1
        self.img_ship = []
        self.shot_speed = 5
        self.shot_list = []
        self.shot_time = 0
        self.shot_sprites = pygame.sprite.Group()
        self.shot_sprite = pygame.image.load("Sprites/testeball.png")
        self.vel = pygame.math.Vector2(0, 0)
        self.store = pygame.math.Vector2(0, 0)
        self.shoot = False
        self.shoot_time = 0
        self.dead = False

    def make_ship(self, path, shot, pos):
        self.path = path
        image = pygame.image.load(f"{self.path}/tile000.png")
        self.rect = image.get_rect()
        self.w = self.rect.w
        self.h = self.rect.h
        for i in range(0, len(os.listdir(self.path))):
            image = pygame.image.load(f"{self.path}/tile{i:03d}.png")
            self.sprites.append(image)
        self.shot_sprite = pygame.image.load(shot)
        self.rect.center = (pos[0], pos[1])

    def shoot_(self):
        self.shoot = True

    def create_shots(self):
        pass

    def lose_hp(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
            self.dead = True

    def move(self):
        pass

    def update(self):
        super().update()
        if self.dead:
            return
        self.move()
        if self.shoot_time > 0:
            self.shoot_time -= 1
        if self.shoot and self.shoot_time <= 0:
            self.shoot_time = self.shot_time
            shots = self.create_shots()
            for shot in shots:
                self.shot_sprites.add(shot)
                self.shot_list.append(shot)
            self.shoot = False
            # shot_sound_effect.play()
