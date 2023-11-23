import pygame

from .moving_square import MovingSquareLoop

SAVE = False
WIDTH = 500
HEIGHT = 500
X = 1200
Y = 700

pygame.init()

class GameLoop(MovingSquareLoop):
    def __init__(self):
        super().__init__((X, Y))