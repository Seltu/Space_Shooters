import pygame


class Pickup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/fire/tile000.png")
        self.rect = self.image.get_rect()
        self.temporary = False
        self.type = 0

    def update(self):
        super().update()
        self.rect.y += 2

    def effect(self, ship):
        pass


class HealthPickup(Pickup):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/pickup_hp.png")
        self.rect = self.image.get_rect()
        self.type = 1

    def effect(self, ship):
        if ship.hp < 5:
            ship.hp += 1


class TemporaryPickup(Pickup):
    def __init__(self):
        super().__init__()
        self.timer = 0
        self.wore_out = True
        self.temporary = True

    def wear(self, ship):
        if self.wore_out:
            return
        if self.timer > 0:
            self.timer -= 1
        else:
            self.wore_out = True
            self.wear_out(ship)

    def effect(self, ship):
        self.timer = 400
        self.wore_out = False

    def wear_out(self, ship):
        pass


class SpeedPickup(TemporaryPickup):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/pickup_speed.png")
        self.rect = self.image.get_rect()

    def effect(self, ship):
        super().effect(ship)
        ship.move_speed += 5

    def wear_out(self, ship):
        ship.move_speed -= 5


class ShotSpeedPickup(TemporaryPickup):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/pickup_boost.png")
        self.rect = self.image.get_rect()

    def effect(self, ship):
        super().effect(ship)
        ship.shot_time = 5

    def wear_out(self, ship):
        ship.shot_time = 10


class ShotTempPickup(TemporaryPickup):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/pickup_shot.png")
        self.rect = self.image.get_rect()

    def effect(self, ship):
        super().effect(ship)
        ship.number_of_shots += 1

    def wear_out(self, ship):
        ship.number_of_shots -= 1
