from config import *
from enemy_types import *
from boss_enemies import BossBaron
from boss_enemies import BossJester
from boss_enemies import BossMonarch
from wave import Wave


class Levels:
    levels = []

    def __init__(self, layout_type: int):
        self.group = pygame.sprite.Group()
        self.rounds = []
        self.boss = BossMonarch((screen_width / 2, 0))
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
        pass

    @staticmethod
    def make_enemy(number, curve, progress):
        enemy = None
        if number == 0:
            enemy = Enemy1(curve, progress * 3)
        elif number == 1:
            enemy = Enemy2(curve, progress * 3)
        elif number == 2:
            enemy = Enemy3(curve, progress * 3)
        elif number == 3:
            enemy = Enemy4(curve, progress * 3)
        elif number == 4:
            enemy = BaronMinion(curve, progress * 3)
        elif number == 5:
            enemy = Enemy5(curve, progress * 3)
        return enemy
