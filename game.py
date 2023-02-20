import pygame.math

from player import PlayerShip
from enemy_types import *
from config import *
from animation import AnimatedSprite


class Game:
    def __init__(self, screen, level):
        self.aim_enemies = []
        self.screen = screen
        self.background = level.get_bg_color()
        self.level = level
        self.sprites = level.get_group()
        self.ship = PlayerShip('Sprites/Player', (screen_width / 2, screen_height - 140))
        self.enemies = []
        self.sprites.add(self.ship)
        self.level_progress = 0
        self.wave_progress = 1
        self.level_timer = 0

    # Check if an event happens
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
                if event.key == pygame.K_0:
                    enemy = Enemy2('Sprites/enemy_2', 'Sprites/enemy_fire2.png', waveline3, 0)
                    self.enemies.append(enemy)
                    self.sprites.add(enemy)
                if event.key == pygame.K_r:
                    self.level_progress = 0
                    self.wave_progress = 0

    def game_loop(self):
        while True:
            self.check_events()
            self.sprites.update()
            self.sprites.draw(self.screen)
            self.ship.shot_sprites.update()
            for enemy in self.enemies:
                enemy.shot_sprites.update()
                self.shoot_collision(self.ship, enemy)
                self.shoot_collision(enemy, self.ship)
            for enemy in self.aim_enemies:
                enemy.set_target(pygame.math.Vector2(self.ship.rect.centerx, self.ship.rect.centery))
            self.progress_level()
            self.draw_sprites()
            pygame.display.update()
            clk.tick(fps)

    def progress_level(self):
        if self.level_timer > 0:
            self.level_timer -= 1
            return
        if self.level_progress >= len(self.level.rounds):
            return
        current_round = self.level.rounds[self.level_progress]
        if self.wave_progress < 60:
            for wave in current_round:
                if self.wave_progress % (60 / wave.number) == 0:
                    enemy = None
                    if wave.enemy == 0:
                        enemy = Enemy1('Sprites/enemy_1', 'Sprites/enemy_fire.png',
                                       wave.curve, self.wave_progress * 3)
                    elif wave.enemy == 1:
                        enemy = Enemy2('Sprites/enemy_2', 'Sprites/enemy_fire2.png',
                                       wave.curve, self.wave_progress * 3)
                    elif wave.enemy == 2:
                        enemy = Enemy3('Sprites/enemy_3', 'Sprites/enemy_fire3.png',
                                       wave.curve, self.wave_progress * 3)
                        self.aim_enemies.append(enemy)
                    self.enemies.append(enemy)
                    self.sprites.add(enemy)
                    self.level_timer = 60 / wave.number
            self.wave_progress += 1
        else:
            self.level_timer = 470
            self.level_progress += 1
            self.wave_progress = 0

    # Draws Elements
    def draw_sprites(self):
        self.screen.fill(self.background)
        for enemy in self.enemies:
            enemy.shot_sprites.draw(self.screen)
        self.sprites.draw(self.screen)
        self.ship.shot_sprites.draw(self.screen)

    def shoot_collision(self, ship_one, ship_two):
        if ship_two.dead:
            return
        if len(ship_one.shot_list) <= 0:
            return
        close = ship_one.shot_list[0]
        closest = close.pos.distance_to(pygame.math.Vector2(ship_two.rect.centerx, ship_two.rect.centery))
        for shot in ship_one.shot_list:
            distance = shot.pos.distance_to(pygame.math.Vector2(ship_two.rect.centerx, ship_two.rect.centery))
            if distance < closest:
                closest = distance
                close = shot
        if pygame.sprite.collide_mask(close, ship_two):
            ship_two.lose_hp(ship_one.damage)
            explosion = AnimatedSprite(1, True, 'Sprites/boom')
            self.sprites.add(explosion)
            explosion.rect.center = ship_two.rect.center
            ship_one.shot_list.remove(close)
            close.kill()
            del close
