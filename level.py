from config import *
from enemy_types import *
from boss_enemies import BossBaron
from boss_enemies import BossJester
from boss_enemies import BossMonarch
from wave import Wave


class Levels:
    def __init__(self, level):
        self.group = pygame.sprite.Group()
        self.rounds = []
        self.progress = 0
        self.wave_progress = 0
        self.boss = None
        self.get_level(level)
        self.wall_color = "#d4a941"
        self.bg_color = "#150d28"

        # for layout in self.layouts[layout_type - 1]:
        #    self.group.add(wall.Wall(self.wall_color, layout[0], layout[1]))

    def get_group(self):
        return self.group

    def get_bg_color(self):
        return self.bg_color

    def get_level(self, level):
        self.progress = 0
        self.wave_progress = 0
        self.rounds = []
        if level == 0:
            waves = [Wave(0, 6, waveline1), Wave(0, 6, waveline2)]
            self.rounds.append(waves)
            waves = [Wave(0, 6, waveline5.shift(0, -200)), Wave(1, 2, waveline6), Wave(1, 2, waveline7)]
            self.rounds.append(waves)
            waves = [Wave(2, 10, waveline5.shift(0, -250))]
            self.rounds.append(waves)
            waves = [Wave(1, 3, waveline5.shift(0, -200)), Wave(2, 6, waveline5.shift(0, -250))]
            self.rounds.append(waves)
            waves = [Wave(0, 6, waveline5.shift(0, -200)),
                     Wave(2, 6, waveline5.shift(0, -250)), Wave(1, 2, waveline6), Wave(1, 2, waveline7)]
            self.rounds.append(waves)
            self.boss = BossBaron((screen_width / 2, 0))
        elif level == 1:
            waves = [Wave(3, 1, waveline3.shift(300, -150)), Wave(1, 6, waveline3.shift(300, 50)), Wave(0, 6, waveline1),
                     Wave(0, 3, waveline2), Wave(0, 6, waveline6), Wave(0, 6, waveline7)]
            self.rounds.append(waves)
            waves = [Wave(3, 3, waveline5.shift(0, -200)), Wave(1, 6, waveline5.shift(0, -150)),
                     Wave(0, 12, waveline5.shift(0, -100))]
            self.rounds.append(waves)
            waves = [Wave(3, 2, waveline3.shift(-400, 0)), Wave(1, 2, waveline3.shift(-350, 80)),
                     Wave(3, 2, waveline4.shift(400, 0)), Wave(1, 2, waveline4.shift(350, 80)),
                     Wave(2, 12, waveline5.shift(0, -400))]
            self.rounds.append(waves)
            waves = [Wave(3, 4, waveline1.shift(-300, 0)), Wave(3, 4, waveline2.shift(300, 0)),
                     Wave(1, 2, waveline1.shift(-200, 0)), Wave(1, 2, waveline2.shift(200, 0)),
                     Wave(2, 3, waveline6.shift(-400, 0)), Wave(2, 3, waveline7.shift(400, 0))]
            self.rounds.append(waves)
            waves = [Wave(3, 10, waveline6.shift(0, -200)), Wave(3, 10, waveline7.shift(0, -200))]
            self.rounds.append(waves)
            self.boss = BossJester((screen_width / 2 + 140, -300))
        elif level == 2:
            waves = [Wave(5, 10, waveline5.shift(0, -400))]
            self.rounds.append(waves)
            waves = [Wave(0, 6, waveline1.shift(0, -300)), Wave(0, 6, waveline2.shift(0, -300)),
                     Wave(5, 6, waveline1.shift(0, -250)), Wave(5, 6, waveline2.shift(0, -250))]
            self.rounds.append(waves)
            waves = [Wave(2, 4, waveline6), Wave(2, 4, waveline7),
                     Wave(5, 4, waveline6.shift(0, 50)), Wave(5, 4, waveline7.shift(0, 50))]
            self.rounds.append(waves)
            waves = [Wave(5, 6, waveline5.shift(0, -300)), Wave(1, 6, waveline5.shift(0, -350))]
            self.rounds.append(waves)
            waves = [Wave(5, 6, waveline5.shift(50, -300)), Wave(5, 6, waveline5.shift(-50, -300)),
                     Wave(3, 6, waveline5.shift(0, -350))]
            self.rounds.append(waves)
            self.boss = BossMonarch((screen_width / 2, -300))
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
