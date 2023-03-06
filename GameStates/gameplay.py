import math
import random
import pygame.math

from level import Levels
from player import PlayerShip
from healthbar import HealthBar
from pickup import *
from config import *
from config import screen_height
from animation import AnimatedSprite
from GameStates.game_state import GameState

game_level = 0
on_boss = False


class Gameplay(GameState):
    def __init__(self):
        global game_level, on_boss
        super().__init__()
        self.aim_enemies = []
        level = Levels(game_level)
        self.background = level.get_bg_color()
        self.level = level
        self.sprites = level.get_group()
        self.ships = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.temp_pickups = []
        ship = PlayerShip('Sprites/Player', (screen_width / 2 - 100, screen_height - 140))
        ship2 = PlayerShip('Sprites/Player2', (screen_width / 2 + 100, screen_height - 140))
        self.health_bars = pygame.sprite.Group()
        health1 = HealthBar(ship, 'player_healthbar', 600, 420)
        health1.rect.center = (0, -50)
        health2 = HealthBar(ship2, 'player2_healthbar', 600, 420)
        health2.rect.center = (0, 100)
        self.health_bars.add(health1)
        self.health_bars.add(health2)
        self.players = [ship, ship2]
        self.ships.add(ship)
        self.ships.add(ship2)
        self.enemies = []
        for ship in self.ships.sprites():
            self.sprites.add(ship)
        self.level_progress = 0
        if on_boss:
            self.level_progress = 99
        self.wave_progress = 0
        self.level_timer = 0
        self.boss_fight = False
        self.level_power()

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

    def level_power(self):
        global game_level
        for ship in self.ships.sprites():
            ship.number_of_shots = 1+game_level
            ship.damage = 10-game_level*2
            ship.max_hp = 5+game_level
            ship.move_speed = 6+game_level
            ship.shot_time = 10
            ship.hp = ship.max_hp

    # Check if an event happens
    def check_event(self, event):
        global on_boss
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.players[0].stop(1, -1)
            if event.key == pygame.K_DOWN:
                self.players[0].stop(1, 1)
            if event.key == pygame.K_LEFT:
                self.players[0].stop(0, -1)
            if event.key == pygame.K_RIGHT:
                self.players[0].stop(0, 1)
            if event.key == pygame.K_m:
                self.players[0].stop_shoot()
        # PLAYER 2
            if event.key == pygame.K_w:
                self.players[1].stop(1, -1)
            if event.key == pygame.K_s:
                self.players[1].stop(1, 1)
            if event.key == pygame.K_a:
                self.players[1].stop(0, -1)
            if event.key == pygame.K_d:
                self.players[1].stop(0, 1)
            if event.key == pygame.K_g:
                self.players[1].stop_shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
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
            if event.key == pygame.K_g:
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
                self.done = True
                on_boss = False
                self.next_state = "GAMEPLAY"
            if event.key == pygame.K_QUOTE:
                self.level_progress = 99
                self.wave_progress = 99

    def update(self, dt):
        self.health_bars.update()
        self.sprites.update()
        self.scroll_parallax_back += 5
        self.scroll_parallax_middle += 5
        self.scroll_parallax_fore += 5
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
        if len(self.ships) == 0:
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
        if game_level > 2:
            self.done = True
            self.next_state = "WIN"
        if self.level_progress >= len(self.level.rounds):
            global on_boss
            on_boss = True
            self.enemies.append(self.level.boss)
            self.sprites.add(self.level.boss)
            if self.level.boss.aimed:
                self.aim_enemies.append(self.level.boss)
            self.boss_fight = True
            self.level_timer = 200
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
            if enemy.dead and not enemy.shot_sprites:
                self.enemies.remove(enemy)
                del enemy
        self.sprites.draw(screen)
        self.pickups.draw(screen)
        self.health_bars.draw(screen)
        for ship in self.ships.sprites():
            ship.shot_sprites.draw(screen)

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
        global game_level, on_boss
        if ship_two.dead:
            return
        if len(ship_one.shot_sprites) <= 0:
            return
        close = self.get_closest_to(ship_two, ship_one.shot_sprites)
        if pygame.sprite.collide_mask(close, ship_two):
            if ship_two.lose_hp(ship_one.damage):
                if ship_two.boss:
                    self.boss_fight = False
                    on_boss = False
                    game_level += 1
                    self.level_progress = 0
                    self.wave_progress = 0
                    while len(self.ships) < len(self.players):
                        self.revive_player()
                    self.level_power()
                    self.temp_pickups.clear()
                    self.level.get_level(game_level)
                    self.level_timer = 200
                else:
                    if random.randint(0, 100) <= 10:
                        self.random_pickup(ship_two.rect.center)
            explosion = AnimatedSprite(0.5, True, 'Sprites/Boom', 64, 64)
            self.sprites.add(explosion)
            explosion.rect.center = close.rect.midtop
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

    def revive_player(self):
        for player in self.players:
            if player.dead:
                player.hp = 2
                player.invincible_timer = player.invincibility_time
                self.ships.add(player)
                self.sprites.add(player)
                player.dead = False
                break

    def pickup_collision(self, ship, pickup):
        if pygame.sprite.collide_mask(ship, pickup):
            if pickup.type == 1 and len(self.ships) < len(self.players):
                self.revive_player()
            else:
                pickup.effect(ship)
            pickup.kill()
