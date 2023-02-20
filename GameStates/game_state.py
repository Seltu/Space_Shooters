import pygame


class GameState(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.font = pygame.font.Font(None, 32)

    def check_events(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
