import sys
import pygame
import config

from game import Game
from GameStates.menuscene import MenuState
from GameStates.gameplay import Gameplay
from GameStates.gameover import GameOver
from GameStates.gamewin import GameWin

# setup mixer to avoid sound lag
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((config.screen_width,
                                  config.screen_height))
states = {
    "MENU": MenuState(),
    "GAMEPLAY": Gameplay(),
    "GAMEOVER": GameOver(),
    "WIN": GameWin()
}

game = Game(screen, states, "WIN")
game.run()
pygame.quit()
sys.exit()
