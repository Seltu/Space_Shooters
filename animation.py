import os

import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, speed, play_once, path=None, w=None, h=None, rot=None):
        super().__init__()
        self.sprites = []
        self.speed = speed
        if w is not None:
            self.w = w
        else:
            self.w = 0
        if w is not None:
            self.h = h
        else:
            self.h = 0
        self.alpha = 255
        if path is not None:
            self.path = path
        else:
            self.path = 'Sprites/enemy_1'
        self.image = pygame.image.load(f"{self.path}/tile000.png")
        self.rect = self.image.get_rect()
        self.load_path(self.path, w, h, rot)
        self.current_sprite = 0
        self.play_once = play_once

    def update(self):
        self.current_sprite += self.speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            if self.play_once:
                self.kill()
        self.image = self.sprites[int(self.current_sprite)]
        self.image.set_alpha(self.alpha)

    def load_path(self, path, w=None, h=None, rot=None):
        self.sprites = []
        self.path = path
        self.image = pygame.image.load(f"{self.path}/tile000.png")
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height
        if w is not None:
            self.w = w
        else:
            self.w = self.rect.w
        if w is not None:
            self.h = h
        else:
            self.h = self.rect.h
        for i in range(0, len(os.listdir(self.path))):
            image = pygame.transform.scale(pygame.image.load(f"{self.path}/tile{i:03d}.png"), (self.w, self.h))
            if rot is not None:
                image = self.rot_center(image, rot)
            self.sprites.append(image)

    @staticmethod
    def rot_center(image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
