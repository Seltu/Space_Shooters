import pygame.math
from config import *


def rot_center(image, angle):
    # rotate an image keeping its center and size
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Shot(pygame.sprite.Sprite):

    def __init__(self, ship, offset_x, offset_y, vel_x, vel_y):
        pygame.sprite.Sprite.__init__(self)
        self.ship = ship
        self.pos = pygame.math.Vector2(ship.rect.centerx + offset_x, ship.rect.centery + offset_y)
        self.vel = pygame.math.Vector2(vel_x*self.ship.shot_speed, vel_y*self.ship.shot_speed)
        self.cont = 0
        self.image = ship.shot_sprite
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.group = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.center = [int(self.pos.x), int(self.pos.y)]
        if self.vel.length() > 0:
            angle = self.vel.normalize().angle_to(pygame.math.Vector2(0, 1))
            self.image = rot_center(self.image, angle)

    def update(self):
        # update balls in list
        self.move()

    def move(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.rect.center = [int(self.pos.x), int(self.pos.y)]
        if 0 > self.rect.x > screen_width - self.rect.width and 0 > self.rect.y > screen_height - self.rect.height:
            self.kill()
            self.ship.shot_list.remove(self)
