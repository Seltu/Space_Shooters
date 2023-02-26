import random

import pygame.math

from level import Levels
from player import PlayerShip
from boss_enemies import BossEnemy
from pickup import *
from config import *
from animation import AnimatedSprite
from GameStates.game_state import GameState


class Gameplay(GameState):
    def __init__(self):
        super().__init__()
        self.aim_enemies = []
        level = Levels(0)
        self.background = level.get_bg_color()
        self.level = level
        self.sprites = level.get_group()
        self.ships = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.temp_pickups = []
        ship = PlayerShip('Sprites/Player', (screen_width / 2 - 100, screen_height - 140))
        ship2 = PlayerShip('Sprites/Player2', (screen_width / 2 + 100, screen_height - 140))
        self.players = [ship, ship2]
        self.ships.add(ship)
        self.ships.add(ship2)
        self.enemies = []
        for ship in self.ships.sprites():
            self.sprites.add(ship)
        self.level_progress = 0
        self.wave_progress = 0
        self.level_timer = 0
        self.boss_fight = False

        self.done = False
        self.next_state = "GAMEOVER"

    # Check if an event happens
    def check_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.players[0].stop(1, -1)
            if event.key == pygame.K_DOWN:
                self.players[0].stop(1, 1)
            if event.key == pygame.K_LEFT:
                self.players[0].stop(0, -1)
            if event.key == pygame.K_RIGHT:
                self.players[0].stop(0, 1)
            if event.key == pygame.K_z:
                self.players[0].shoot_()
        # PLAYER 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.players[1].stop(1, -1)
            if event.key == pygame.K_s:
                self.players[1].stop(1, 1)
            if event.key == pygame.K_a:
                self.players[1].stop(0, -1)
            if event.key == pygame.K_d:
                self.players[1].stop(0, 1)
            if event.key == pygame.K_e:
                self.players[1].shoot_()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.players[0].shoot_()
            if event.key == pygame.K_UP:
                self.players[0].go(1, -1)
            if event.key == pygame.K_DOWN:
                self.players[0].go(1, 1)
            if event.key == pygame.K_LEFT:
                self.players[0].go(0, -1)
            if event.key == pygame.K_RIGHT:
                self.players[0].go(0, 1)
            # PLAYER 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.players[1].shoot_()
            if event.key == pygame.K_w:
                self.players[1].go(1, -1)
            if event.key == pygame.K_s:
                self.players[1].go(1, 1)
            if event.key == pygame.K_a:
                self.players[1].go(0, -1)
            if event.key == pygame.K_d:
                self.players[1].go(0, 1)
        # DEBUG
            if event.key == pygame.K_r:
                self.level_progress = 0
                self.wave_progress = 0
            if event.key == pygame.K_b:
                self.level_progress = 99
                self.wave_progress = 99

    def update(self, dt):
        self.sprites.update()
        self.pickups.update()
        for ship in self.ships.sprites():
            ship.shot_sprites.update()
            for pickup in self.pickups.sprites():
                self.pickup_collision(ship, pickup)
            for pickup in self.temp_pickups:
                pickup.wear(ship)
        for enemy in self.enemies:
            enemy.shot_sprites.update()
            for ship in self.ships.sprites():
                self.shoot_collision(ship, enemy)
                self.shoot_collision(enemy, ship)
        for enemy in self.aim_enemies:
            closest = self.get_closest_to(enemy, self.ships)
            if closest is not None:
                enemy.set_target(pygame.math.Vector2(closest.rect.centerx, closest.rect.centery))
        self.progress_level()
        if self.ship.dead:
            self.done = True
            gameplayMusic.fadeout(2000)

    def progress_level(self):
        if self.level_timer > 0:
            self.level_timer -= 1
            return
        if self.boss_fight:
            if self.level.boss.summon:
                self.add_waves(self.level.boss.create_waves())
            return
        if self.level_progress >= len(self.level.rounds):
            self.enemies.append(self.level.boss)
            self.sprites.add(self.level.boss)
            self.boss_fight = True
            return
        current_round = self.level.rounds[self.level_progress]
        self.add_waves(current_round)

    def add_waves(self, current_round):
        if self.wave_progress < 60:
            for wave in current_round:
                if self.wave_progress % (60 / wave.number) == 0:
                    enemy = self.level.make_enemy(wave.enemy, wave.curve, self.wave_progress)
                    self.enemies.append(enemy)
                    if enemy.aimed:
                        self.aim_enemies.append(enemy)
                    self.sprites.add(enemy)
                    self.level_timer = 60 / wave.number
            self.wave_progress += 1
        else:
            self.level_progress += 1
            self.wave_progress = 0
            if self.boss_fight:
                self.level.boss.summon = False
            else:
                self.level_timer = 470

    # Draws Elements
    def draw(self, screen):
        screen.fill(self.background)
        for enemy in self.enemies:
            enemy.shot_sprites.draw(screen)
        self.sprites.draw(screen)
        self.pickups.draw(screen)
        for ship in self.ships.sprites():
            ship.shot_sprites.draw(screen)

    def shoot_collision(self, ship_one, ship_two):
        if ship_two.dead:
            return
        if len(ship_one.shot_sprites) <= 0:
            return
        close = self.get_closest_to(ship_two, ship_one.shot_sprites)
        if pygame.sprite.collide_mask(close, ship_two):
            if ship_two.lose_hp(ship_one.damage):
                if ship_two is BossEnemy:
                    self.boss_fight = False
                    pickup = ShotPickup()
                    self.sprites.add(pickup)
                    pickup.rect.center = close.rect.center
                else:
                    if random.randint(0, 100) <= 10:
                        self.random_pickup(ship_two.rect.center)
            explosion = AnimatedSprite(1, True, 'Sprites/Boom')
            self.sprites.add(explosion)
            explosion.rect.center = close.rect.center
            close.kill()
            del close

    def random_pickup(self, pos):
        choice = random.randint(0, 3)
        if choice == 0:
            pickup = HealthPickup()
        elif choice == 1:
            pickup = SpeedPickup()
        elif choice == 2:
            pickup = ShotSpeedPickup()
        elif choice == 3:
            pickup = ShotTempPickup()
        else:
            pickup = HealthPickup()
        self.pickups.add(pickup)
        if pickup.temporary:
            self.temp_pickups.append(pickup)
        pickup.rect.center = pos

    @staticmethod
    def get_closest_to(sprite, group):
        if len(group) == 0:
            return
        close = group.sprites()[0]
        closest = pygame.math.Vector2(close.rect.centerx, close.rect.centery).distance_to(pygame.math.Vector2(
            sprite.rect.centerx, sprite.rect.centery))
        for other in group:
            distance = pygame.math.Vector2(other.rect.centerx, other.rect.centery).distance_to(pygame.math.Vector2(
                sprite.rect.centerx, sprite.rect.centery))
            if distance < closest:
                closest = distance
                close = other
        return close

    @staticmethod
    def pickup_collision(ship, pickup):
        if pygame.sprite.collide_mask(ship, pickup):
            pickup.effect(ship)
            pickup.kill()
