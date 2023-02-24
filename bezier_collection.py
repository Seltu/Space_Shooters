from copy import deepcopy

import pygame.math


class BezierCollection(object):
    def __init__(self):
        self.bezier_curves = []

    def add(self, bezier_curve):
        self.bezier_curves.append(bezier_curve)

    def number_of_quartets(self):
        return len(self.bezier_curves)

    def get_quartet(self, quartet_index):
        return self.bezier_curves[quartet_index]

    def shift(self, x, y):
        new_line = deepcopy(self)
        for i in range(new_line.number_of_quartets()):
            for j in range(len(new_line.bezier_curves[i].points)):
                new_line.bezier_curves[i].points[j] = pygame.math.Vector2(new_line.bezier_curves[i].points[j].x+x, new_line.bezier_curves[i].points[j].y+y)
        return new_line
