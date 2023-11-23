import os
import pygame

from datetime import datetime


FILENAME = f"{datetime.now().strftime('%d%m%y_%H%M%S')}.png"
FILEPATH = os.path.join(os.path.dirname(__file__), "..", "..", "Images", FILENAME)


class GenericLoop():
    def __init__(self):
        pass

    def save(self):
        pygame.image.save(self.screen_handler.screen, FILEPATH, "png")