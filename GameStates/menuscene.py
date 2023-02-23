import pygame.math

from level import Levels
from player import PlayerShip
from enemy_types import *
from config import *
from animation import AnimatedSprite
from GameStates.game_state import GameState


class MenuState(GameState):
    def __init__(self):
        super().__init__()
        self.done = False
        self.next_state = "GAMEPLAY"
        self.background = pygame.image.load("Sprites/MenuSprites/background_title.png")
        self.background_rect = self.background.get_rect(topleft=(0, 0))
        self.press = pygame.image.load("Sprites/MenuSprites/PRESS.png")
        self.press_rect = self.press.get_rect(topleft=(160, 700))
        self.logo = pygame.image.load("Sprites/MenuSprites/SPACE SHOOTERS.png")
        self.logo_rect = self.logo.get_rect(topleft=(125, 150))
        self.can_draw_menu = True

    # Check if an event happens
    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER:
               self.can_draw_menu = False
               self.done = True

    def update(self, dt):
        if self.can_draw_menu:
            from main import screen
            self.draw_menu(screen)

    def draw_menu(self, screen):
        screen.blit(self.background, self.background_rect)
        screen.blit(self.press, self.press_rect)
        screen.blit(self.logo, self.logo_rect)
