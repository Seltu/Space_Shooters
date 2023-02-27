import pygame.math

from GameStates.game_state import GameState
from config import *


class MenuState(GameState):
    def __init__(self):
        super().__init__()
        self.done = False
        self.next_state = "GAMEPLAY"
        self.background = pygame.image.load("Sprites/UI/background_title.png")
        self.background_rect = self.background.get_rect(topleft=(0, 0))
        self.press = pygame.image.load("Sprites/UI/PRESS.png")
        self.press_rect = self.press.get_rect(topleft=(500, 650))
        self.logo = pygame.image.load("Sprites/UI/SPACE SHOOTERS.png")
        self.logo_rect = self.logo.get_rect(topleft=(125, 150))
        menuMusic.play(-1)

    # Check if an event happens
    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
               self.done = True
               menuMusic.fadeout(3000)

    def draw(self, screen):
        screen.blit(self.background, self.background_rect)
        screen.blit(self.press, self.press_rect)
        screen.blit(self.logo, self.logo_rect)
