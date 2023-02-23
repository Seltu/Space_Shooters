import pygame.math

from GameStates.game_state import GameState
from config import *


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

    # Check if an event happens
    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.done = True

    def draw(self, screen):
        screen.blit(self.background, self.background_rect)
        screen.blit(self.press, self.press_rect)
        screen.blit(self.logo, self.logo_rect)
