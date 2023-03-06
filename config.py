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

menuMusic = pygame.mixer.Sound("Sounds/MenuMusic.wav")
gameplayMusic = pygame.mixer.Sound("Sounds/gameplayMusic.wav")
gameplayMusic.set_volume(0.3)
gameoverMusic = pygame.mixer.Sound("Sounds/gameover.wav")
gameWinMusic = pygame.mixer.Sound("Sounds/Yippeee.wav")

shotSoundEffect = pygame.mixer.Sound("Sounds/shotBeam.wav")
shotSoundEffect.set_volume(0.15)
explosionSoundEffect = pygame.mixer.Sound("Sounds/explosionSoundEffect.wav")
explosionSoundEffect.set_volume(0.7)
warningBossSoundEffect = pygame.mixer.Sound("Sounds/bossWarning.wav")
boomBossSoundEffect = pygame.mixer.Sound("Sounds/bossBoom.wav")

vsBaronMusic = pygame.mixer.Sound("Sounds/vsBaron.wav")
vsJesterMusic = pygame.mixer.Sound("Sounds/vsJester.wav")
vsMonarchMusic = pygame.mixer.Sound("Sounds/vsMonarch.wav")
bossWarningChannel = pygame.mixer.Channel(3)
bossChannel = pygame.mixer.Channel(2)

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
    500, 50,
    500, 100,
    500, 200))
waveline3.add(BezierCurve(
    500, 200,
    500, 300,
    500, 400,
    500, 500))
waveline3.add(BezierCurve(
    500, 500,
    500, 500,
    200, 600,
    0, 600))

waveline4 = BezierCollection()
waveline4.add(BezierCurve(
    1100, -50,
    1100, 50,
    1100, 100,
    1100, 200))
waveline4.add(BezierCurve(
    1100, 200,
    1100, 300,
    1100, 400,
    1100, 500))
waveline4.add(BezierCurve(
    1100, 500,
    1100, 500,
    1400, 600,
    1600, 600))

waveline5 = BezierCollection()
waveline5.add(BezierCurve(
    0, -50,
    0, 800,
    1600, 800,
    1600, -50))
waveline5.add(BezierCurve(
    1600, -50,
    1600, 800,
    0, 800,
    0, -50
))

waveline6 = BezierCollection()
waveline6.add(BezierCurve(
    100, -50,
    100, 500,
    800, 650,
    1600, 100))

waveline7 = BezierCollection()
waveline7.add(BezierCurve(
    1500, -50,
    1500, 500,
    800, 650,
    0, 100))
