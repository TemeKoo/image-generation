import os
import pygame

from datetime import datetime


FILENAME = f"{datetime.now().strftime('%d%m%y_%H%M%S')}.png"
FILEPATH = os.path.join(os.path.dirname(__file__), "..", "..", "Images", FILENAME)


class GenericLoop():
    def __init__(self):
        pass

    def start(self):
        self.clock = pygame.time.Clock()
        self.loop()

    def loop(self):
        while True:
            self.event_handler(pygame.event.get())
            self.updater()
            self.clock.tick(60)

    def updater(self):
        pass

    def event_handler(self, events: list):
        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()

    def terminate(self):
        pygame.quit()
        exit()

    def save(self):
        pygame.image.save(self.screen_handler.screen, FILEPATH, "png")