import pygame
import config
from GameStates.menuscene import MenuState

class Game:
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = config.fps
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        for event in pygame.event.get():
            self.state.check_event(event)

    def change_state(self):
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        self.state = self.states[self.state_name]
        self.state.__init__()

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.change_state()
        self.state.update(dt)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.state.draw(self.screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()
