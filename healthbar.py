import os

import pygame


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, ship, path=None, w=None, h=None):
        super().__init__()
        self.ship = ship
        self.sprites = []
        if w is not None:
            self.w = w
        else:
            self.w = 0
        if w is not None:
            self.h = h
        else:
            self.h = 0
        if path is not None:
            self.path = path
        else:
            self.path = 'Sprites/enemy_1'
        self.image = pygame.image.load(f"Sprites/{self.path}/{self.path}1.png")
        self.rect = self.image.get_rect()
        self.load_path(self.path, w, h)
        self.current_sprite = 0

    def update(self):
        self.current_sprite = ((self.ship.max_hp-self.ship.hp)/self.ship.max_hp)*len(self.sprites)
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = len(self.sprites)-1
        self.image = self.sprites[int(self.current_sprite)]

    def load_path(self, path, w=None, h=None):
        self.sprites = []
        self.path = path
        self.image = pygame.image.load(f"Sprites/{self.path}/{self.path}1.png")
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
        for i in range(0, len(os.listdir(f"Sprites/{self.path}"))):
            image = pygame.transform.scale(pygame.image.load(f"Sprites/{self.path}/{self.path}{i+1}.png"), (self.w, self.h))
            self.sprites.append(image)
