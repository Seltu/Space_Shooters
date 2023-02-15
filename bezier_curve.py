from pygame.math import Vector2


class BezierCurve:
    def __init__(self,
                 x0, y0,
                 x1, y1,
                 x2, y2,
                 x3, y3):

        self.points = []
        self.points.append(Vector2(x0, y0))
        self.points.append(Vector2(x1, y1))
        self.points.append(Vector2(x2, y2))
        self.points.append(Vector2(x3, y3))

    def get_point(self, point_index):
        return self.points[point_index]

    def length(self):
        return len(self.points)

    def calculate_path_point(self, time_to_calculate):
        time: float = time_to_calculate - int(time_to_calculate)

        cx: float = 3.0 * (self.get_point(1).x -
                           self.get_point(0).x)
        cy: float = 3.0 * (self.get_point(1).y -
                           self.get_point(0).y)

        bx: float = 3.0 * (self.get_point(2).x -
                           self.get_point(1).x) - cx
        by: float = 3.0 * (self.get_point(2).y -
                           self.get_point(1).y) - cy

        ax: float = self.get_point(
            3).x - self.get_point(0).x - cx - bx
        ay: float = self.get_point(
            3).y - self.get_point(0).y - cy - by

        cube: float = time * time * time
        square: float = time * time

        resx: float = (ax * cube) + (bx * square) + \
            (cx * time) + self.get_point(0).x
        resy: float = (ay * cube) + (by * square) + \
            (cy * time) + self.get_point(0).y

        return Vector2(resx, resy)
