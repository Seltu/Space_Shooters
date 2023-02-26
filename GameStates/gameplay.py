import math

import pygame.math

from level import Levels
from player import PlayerShip
from boss_enemies import *
from config import *
from config import screen_height
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
        self.ship = PlayerShip('Sprites/Player', (screen_width / 2, screen_height - 140))
        self.enemies = []
        self.sprites.add(self.ship)
        self.level_progress = 0
        self.wave_progress = 0
        self.level_timer = 0
        self.boss_fight = False

        self.parallax = []
        for i in range(3):
            self.image = pygame.image.load(f"Sprites/Parallax/parallax_00{i}.png").convert_alpha()
            self.parallax.append(self.image)
        self.parallax_h = self.parallax[0].get_height()
        self.scroll_parallax_back = 0
        self.scroll_parallax_middle = 0
        self.scroll_parallax_fore = 0
        self.tiles = math.ceil(screen_height / self.parallax_h) + 1

        self.done = False
        self.next_state = "GAMEOVER"

    # Check if an event happens
    def check_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.ship.stop(1, -1)
            if event.key == pygame.K_DOWN:
                self.ship.stop(1, 1)
            if event.key == pygame.K_LEFT:
                self.ship.stop(0, -1)
            if event.key == pygame.K_RIGHT:
                self.ship.stop(0, 1)
            if event.key == pygame.K_z:
                self.ship.shoot_()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.ship.shoot_()
            if event.key == pygame.K_UP:
                self.ship.go(1, -1)
            if event.key == pygame.K_DOWN:
                self.ship.go(1, 1)
            if event.key == pygame.K_LEFT:
                self.ship.go(0, -1)
            if event.key == pygame.K_RIGHT:
                self.ship.go(0, 1)
            if event.key == pygame.K_r:
                self.level_progress = 0
                self.wave_progress = 0
            if event.key == pygame.K_b:
                self.level_progress = 99
                self.wave_progress = 99

    def update(self, dt):
        self.sprites.update()
        self.ship.shot_sprites.update()
        self.scroll_parallax_back += 5
        self.scroll_parallax_middle += 5
        self.scroll_parallax_fore += 5
        for enemy in self.enemies:
            enemy.shot_sprites.update()
            self.shoot_collision(self.ship, enemy)
            self.shoot_collision(enemy, self.ship)
        for enemy in self.aim_enemies:
            enemy.set_target(pygame.math.Vector2(self.ship.rect.centerx, self.ship.rect.centery))
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

        self.draw_parallax_back(screen)
        self.draw_parallax_middle(screen)
        self.draw_parallax_fore(screen)
        screen.blit(self.parallax[1], (0, self.scroll_parallax_middle * 0.5))
        screen.blit(self.parallax[2], (0, self.scroll_parallax_fore * 0.7))

        for enemy in self.enemies:
            enemy.shot_sprites.draw(screen)
        self.sprites.draw(screen)
        self.ship.shot_sprites.draw(screen)

    def draw_parallax_back(self, screen):
        speed = 0.3
        for i in range(self.tiles):
            screen.blit(self.parallax[0], (0, self.scroll_parallax_back * speed))
            screen.blit(self.parallax[0], (0, -self.parallax_h + self.scroll_parallax_back * speed))

        if abs(self.scroll_parallax_back) > self.parallax_h / 0.3:
            self.scroll_parallax_back = 0

    def draw_parallax_middle(self, screen):
        speed = 0.5
        for i in range(self.tiles):
            screen.blit(self.parallax[1], (0, -self.parallax_h + self.scroll_parallax_middle * speed))
            screen.blit(self.parallax[1], (0, -self.parallax_h * 2 + self.scroll_parallax_middle * speed))

        if abs(self.scroll_parallax_middle) > self.parallax_h * 2:
            self.scroll_parallax_middle = 0

    def draw_parallax_fore(self, screen):
        speed = 0.7
        for i in range(self.tiles):
            screen.blit(self.parallax[2], (0, -self.parallax_h + self.scroll_parallax_fore * speed))
            screen.blit(self.parallax[2], (0, -self.parallax_h * 2 + self.scroll_parallax_fore * speed))

        if abs(self.scroll_parallax_fore) > self.parallax_h * 1.42:
            self.scroll_parallax_fore = 0

    def shoot_collision(self, ship_one, ship_two):
        if ship_two.dead:
            return
        if len(ship_one.shot_sprites) <= 0:
            return
        close = ship_one.shot_sprites.sprites()[0]
        closest = close.pos.distance_to(pygame.math.Vector2(ship_two.rect.centerx, ship_two.rect.centery))
        for shot in ship_one.shot_sprites:
            distance = shot.pos.distance_to(pygame.math.Vector2(ship_two.rect.centerx, ship_two.rect.centery))
            if distance < closest:
                closest = distance
                close = shot
        if pygame.sprite.collide_mask(close, ship_two):
            if ship_two.lose_hp(ship_one.damage):
                if ship_two is BossEnemy:
                    self.boss_fight = False
            explosion = AnimatedSprite(0.5, True, 'Sprites/Boom', 64, 64)
            self.sprites.add(explosion)
            explosion.rect.center = close.rect.midtop
            close.kill()
            del close

