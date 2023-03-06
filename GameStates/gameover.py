import pygame.math

from level import Levels
from player import PlayerShip
from enemy_types import *
from config import *
from animation import AnimatedSprite
from GameStates.game_state import GameState


class GameOver(GameState):
    def __init__(self):
        super().__init__()
        self.done = False
        self.next_state = "GAMEPLAY"
        self.background = pygame.image.load("Sprites/UI/background_title.png")
        self.background_rect = self.background.get_rect(topleft=(0, 0))
        self.press = pygame.image.load("Sprites/UI/PLAY AGAIN.png")
        self.press = pygame.transform.scale(self.press, (self.press.get_rect().width / 2, self.press.get_rect().height / 2))
        self.press_rect = self.press.get_rect(topleft=(400, 670))
        self.gameover = pygame.image.load("Sprites/UI/GAMEOVER.png")
        self.gameover_rect = self.gameover.get_rect(topleft=(75, 150))

    # Check if an event happens
    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
               self.done = True
               pygame.mixer.fadeout(1500)

    def draw(self, screen):
        screen.blit(self.background, self.background_rect)
        screen.blit(self.press, self.press_rect)
        screen.blit(self.gameover, self.gameover_rect)
