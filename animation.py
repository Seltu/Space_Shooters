import os

import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, speed, play_once, path=None):
        super().__init__()
        self.sprites = []
        self.speed = speed
        self.w = 0
        self.h = 0
        self.alpha = 255
        self.path = 'Sprites/enemy_1'
        if path is not None:
            self.path = path
            for i in range(0, len(os.listdir(self.path))):
                image = pygame.image.load(f"{self.path}/tile{i:03d}.png")
                self.sprites.append(image)
            image = pygame.image.load(f"{self.path}/tile000.png")
            self.rect = image.get_rect()
            self.w = self.rect.w
            self.h = self.rect.h
        self.play_once = play_once
        self.current_sprite = 0
        self.image = pygame.image.load(f"{self.path}/tile000.png")

    def update(self):
        self.current_sprite += self.speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
            if self.play_once:
                self.kill()
        self.image = self.sprites[int(self.current_sprite)]
        self.image = pygame.transform.scale(self.sprites[int(self.current_sprite)], (self.w, self.h))
        self.image.set_alpha(self.alpha)
