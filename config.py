import pygame
from bezier_collection import BezierCollection
from bezier_curve import BezierCurve

pygame.font.init()
pygame.mixer.init()
screen_width = 1600
screen_height = 900
clk = pygame.time.Clock()
fps = 60
shot_time = 15

waveline1 = BezierCollection()
waveline1.add(BezierCurve(
    1100, -50,
    600, 151,
    800, 650,
    0, 400))

waveline2 = BezierCollection()
waveline2.add(BezierCurve(
    500, -50,
    1000, 151,
    800, 650,
    1600, 400))

waveline3 = BezierCollection()
waveline3.add(BezierCurve(
    500, -50,
    500, -50,
    500, 1100,
    500, 1100))

waveline4 = BezierCollection()
waveline4.add(BezierCurve(
    1100, -50,
    1100, -50,
    1100, 1100,
    1100, 1100))


