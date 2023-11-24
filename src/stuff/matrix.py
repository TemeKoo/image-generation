import pygame
import random

from .generic_classes import GenericScreenHandler, GenericLoop


CREATE_FADING = pygame.USEREVENT + 1

OVERLAY_ALPHA = 30
OVERLAY_COLOR_SCALE = 2


def get_random_color(alpha: int = None):
    if alpha is not None:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha)
    else:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color

def change_color(old_color: tuple, color_scale: int = 10):
    r, g, b = old_color[:3]
    r = max(0, min(r + random.randint(-color_scale, color_scale), 255))
    g = max(0, min(g + random.randint(-color_scale, color_scale), 255))
    b = max(0, min(b + random.randint(-color_scale, color_scale), 255))
    return (r, g, b) if len(old_color) == 3 else (r, g, b, old_color[3])


class FadingCharacter(pygame.sprite.Sprite):
    def __init__(self, size: int, pos: tuple, layer: int, color: tuple, fade_time: int):
        super().__init__()
        self._layer = layer
        self.color = color
        self.alpha = color[3]
        self.image = pygame.SurfaceType((size, size), flags=pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.counter = 0
        self.fade_time = fade_time
    
    def update(self):
        self.counter += 1
        if self.counter >= self.fade_time:
            self.counter = 0
            self.alpha//=2
            if self.alpha < 1:
                self.kill()
                return
            self.color = (self.color[0], self.color[1], self.color[2], self.alpha)
            self.image.fill(self.color)


class FallingCharacter(pygame.sprite.Sprite):
    def __init__(self, start_pos: int, kill_pos: int, layer: int):
        super().__init__()
        self._layer = layer
        self.size = random.randint(15, 20)
        self.image = pygame.Surface((self.size, self.size))
        alpha = random.randint(100, 255)
        self.color = get_random_color(alpha)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = start_pos - self.rect.width//2
        self.rect.y = 0 - self.rect.height
        self.kill_pos = kill_pos + self.size
        self.move_time = random.randint(0, 5)
        self.speed = random.randint(3, self.size-1)
        self.fade_time = random.randint(5, 10)

    def update(self):
        self.rect.y += self.speed
        for i in range(self.speed+1):
            if (self.rect.y-i)%self.size == 0:
                fading_dict = {"layer": self._layer,
                                "pos": (self.rect.x, self.rect.y-i),
                                "size": (self.size),
                                "color": self.color,
                                "fade_time": self.fade_time}
                pygame.event.post(pygame.event.Event(CREATE_FADING, fading_dict))
                break
        if self.rect.y >= self.kill_pos:
            self.kill()


class MatrixScreenHandler(GenericScreenHandler):
    def __init__(self, size: tuple = ...):
        super().__init__(size)
        self.overlay = pygame.Surface(size, flags=pygame.SRCALPHA)
        self.overlay_color = get_random_color(alpha=OVERLAY_ALPHA)

    def update(self, to_draw: pygame.sprite.Group = None):
        """
        self.overlay.fill(self.overlay_color)
        self.screen.blit(self.overlay, (0, 0))
        self.overlay_color = change_color(self.overlay_color, color_scale=OVERLAY_COLOR_SCALE)
        """
        self.screen.fill((0,0,0))
        super().update(to_draw)


class MatrixLoop(GenericLoop):
    def __init__(self, screen_size: tuple[int, int]):
        self.screen_handler = MatrixScreenHandler(size=screen_size)
        self.matrix_characters = pygame.sprite.LayeredUpdates()
        self.next_layer = 0
        super().__init__()

    def event_handler(self, events: list):
        super().event_handler(events)
        for event in events:
            if event.type == CREATE_FADING:
                self.matrix_characters.add(FadingCharacter(event.size, event.pos, event.layer, event.color, event.fade_time))

    def updater(self):
        super().updater()
        if random.randint(1, 2) == 1:
            start_pos = random.randint(0, self.screen_handler.size[0])
            self.matrix_characters.add(FallingCharacter(start_pos, self.screen_handler.size[1], self.next_layer))
            self.next_layer += 1
            if self.next_layer > len(self.matrix_characters):
                self.next_layer = 0
        self.matrix_characters.update()
        self.screen_handler.update(to_draw=self.matrix_characters)
        print(len(self.matrix_characters))
