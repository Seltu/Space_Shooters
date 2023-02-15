import pygame

from game import Game
from level import Levels
from config import *

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
screen_height = screen.get_height()
screen_width = screen.get_width()
pygame.display.set_caption("Space Shooters")
play = Game(screen, Levels(1))
play.game_loop()
