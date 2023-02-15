from config import *


class Wave:
    def __init__(self, enemy, number, curve):
        self.enemy = enemy
        self.number = number
        self.curve = curve


class Levels:
    levels = []

    def __init__(self, layout_type: int):
        self.group = pygame.sprite.Group()
        self.rounds = []
        self.get_waves()
        self.wall_color = "#d4a941"
        self.bg_color = "#1C0026"

        # for layout in self.layouts[layout_type - 1]:
        #    self.group.add(wall.Wall(self.wall_color, layout[0], layout[1]))

    def get_group(self):
        return self.group

    def get_bg_color(self):
        return self.bg_color

    def get_waves(self):
        waves = [Wave(0, 6, waveline1), Wave(0, 6, waveline2)]
        self.rounds.append(waves)
        waves = [Wave(0, 3, waveline1), Wave(0, 3, waveline2), Wave(1, 5, waveline3), Wave(1, 6, waveline4)]
        self.rounds.append(waves)
        # with open('arena.txt') as f:
        #    lines = f.readlines()
        # for line in range(len(lines)):
        #    for char in range(len(lines[line])):
        #        if lines[line][char] == '1':
        #            layout_temp.append([RECT_1, (wall_width+char*RECT_1[0], wall_width+score_height+line*RECT_1[1])])

        # self.levels.append(layout_temp)
