import os
import pygame

from datetime import datetime


FILENAME = f"{datetime.now().strftime('%d%m%y_%H%M%S')}.png"
FILEPATH = os.path.join(os.path.dirname(__file__), "..", "..", "Images", FILENAME)


class GenericScreenHandler():
    def __init__(self, size: tuple = (100, 100)):
        self.screen = pygame.display.set_mode(size)

    def update(self, to_draw: pygame.sprite.Group = None):
        if to_draw is not None:
            to_draw.draw(self.screen)

    @property
    def size(self):
        return self.screen.get_width(), self.screen.get_height()


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
            pygame.display.flip()
            self.clock.tick(60)

    def updater(self):
        pass

    def event_handler(self, events: list):
        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.terminate()
                if event.key == pygame.K_s:
                    self.save()

    def terminate(self):
        pygame.quit()
        exit()

    def save(self):
        pygame.image.save(self.screen_handler.screen, FILEPATH, "png")
