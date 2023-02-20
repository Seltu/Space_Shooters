import sys
import pygame
import config

from game import Game
from GameStates.gameplay import Gameplay

# setup mixer to avoid sound lag
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((config.screen_width,
                                  config.screen_height))
states = {
    "GAMEPLAY": Gameplay(),
}

game = Game(screen, states, "GAMEPLAY")
game.run()
pygame.quit()
sys.exit()
