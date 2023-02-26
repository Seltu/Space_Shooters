from config import *
from enemy_types import *
from boss_enemies import BossBaron
from wave import Wave


class Levels:
    levels = []

    def __init__(self, layout_type: int):
        self.group = pygame.sprite.Group()
        self.rounds = []
        self.boss = BossBaron((screen_width / 2, 0))
        self.get_waves()
        self.wall_color = "#d4a941"
        self.bg_color = "#150d28"

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

    @staticmethod
    def make_enemy(number, curve, progress):
        enemy = None
        if number == 0:
            enemy = Enemy1('Sprites/enemy_1', 'Sprites/enemy_fire',
                           curve, progress * 3)
        elif number == 1:
            enemy = Enemy2('Sprites/enemy_2', 'Sprites/enemy_fire2',
                           curve, progress * 3)
        elif number == 2:
            enemy = Enemy3('Sprites/enemy_3', 'Sprites/enemy_fire3',
                           curve, progress * 3)
        elif number == 3:
            enemy = Enemy4('Sprites/enemy_4', 'Sprites/enemy_fire4',
                           curve, progress * 3)
        elif number == 4:
            enemy = BaronMinion('Sprites/minion_baron', 'Sprites/minion_baron_fire',
                                curve, progress * 3)
        return enemy
