import pygame.math

from level import Levels
from player import PlayerShip
from enemy_types import *
from config import *
from animation import AnimatedSprite
from GameStates.game_state import GameState


class GameWin(GameState):
    def __init__(self):
        super().__init__()
        self.done = False
        self.next_state = "MENU"
        self.background = pygame.image.load("Sprites/UI/background_title.png")
        self.background_rect = self.background.get_rect(topleft=(0, 0))
        self.gamewin = pygame.image.load("Sprites/UI/VICTORY.png")
        self.gamewin = pygame.transform.scale(self.gamewin, (self.gamewin.get_rect().width / 1.5, self.gamewin.get_rect().height / 1.5))
        self.gamewin_rect = self.gamewin.get_rect(topleft=(320, 150))

    # Check if an event happens
    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
               self.done = True
               pygame.mixer.fadeout(1500)

    def draw(self, screen):
        screen.blit(self.background, self.background_rect)
        screen.blit(self.gamewin, self.gamewin_rect)
