import pygame
import random

from .generic_classes import GenericLoop


SQUARE_SIZE = 25, 75
COLOR_SCALE = 15
PRISM_SCALE = 5
SPEED_SCALE = 5
MAX_SPEED = 40


def get_random_color(alpha: int = None):
    if alpha is not None:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha)
    else:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return color

def change_color(old_color: tuple[int, int, int], color_scale: int = COLOR_SCALE):
    r, g, b = old_color[:3]
    r = max(0, min(r + random.randint(-color_scale, color_scale), 255))
    g = max(0, min(g + random.randint(-color_scale, color_scale), 255))
    b = max(0, min(b + random.randint(-color_scale, color_scale), 255))
    return (r, g, b)

def reverse_sign(integer: int):
    return 1 if integer < 0 else -1


class ScreenHandler():
    def __init__(self, size: tuple = (100, 100)):
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((255, 255, 255))
        pygame.display.flip()

        self.prism = False
        self.prism_alpha = 0
        self.prism_counter = 0
        self.prism_color = None
        self.prism_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), flags=pygame.SRCALPHA)

    def update(self, to_draw: pygame.sprite.Group = None, blank: bool = False, prism: bool = False):
        if prism:
            if self.prism:
                self.prism = False
                self.prism_alpha = 0
            else:
                self.prism = True
                self.prism_color = get_random_color(alpha=self.prism_alpha)
                return True
            return

        if to_draw is not None:
            to_draw.draw(self.screen)

        if blank:
            if self.prism:
                self.prism_color = None
            else:
                self.screen.fill((255, 255, 255))

        if self.prism:
            if self.prism_counter > 0:
                self.prism_counter = 0
                if self.prism_color is None:
                    self.prism_surface.fill((255, 255, 255, 150))
                    self.prism_color = get_random_color(alpha=self.prism_alpha)
                else:
                    self.prism_surface.fill(self.prism_color)
                self.screen.blit(self.prism_surface, (0,0))
                new_color = change_color(self.prism_color, color_scale=PRISM_SCALE)
                self.prism_alpha += random.randint(0, 1)
                if self.prism_alpha > 10:
                    self.prism_alpha //= 2
                self.prism_color = (new_color[0], new_color[1], new_color[2], self.prism_alpha)
            else:
                self.prism_counter += 1

        pygame.display.flip()

    @property
    def size(self):
        return self.screen.get_width(), self.screen.get_height()


class MovingSquare(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple[int, int]):
        super().__init__()
        size = random.randint(SQUARE_SIZE[0], SQUARE_SIZE[1])
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0] - self.rect.width//2
        self.rect.y = start_pos[1] - self.rect.height//2
        self.speed = [random.randint(-SPEED_SCALE, SPEED_SCALE), random.randint(-SPEED_SCALE, SPEED_SCALE)]

        self.screen_size = (100, 100)
        self.color = None

    def update(self, screen_size: tuple[int, int] = None, change: bool = False):
        if screen_size is not None:
            self.screen_size = screen_size
            return

        self.__change_color(new=change)
        self.image.fill(self.color)

        if change:
            chance = random.randint(1, 5)
        else:
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]

            chance = random.randint(1, 200)

        if chance == 1 or not 0 < self.rect.x <= self.screen_size[0] - self.rect.width:
            abs_x_speed = abs(self.speed[0])
            self.speed[0] = reverse_sign(self.speed[0]) * (abs_x_speed + random.randint(-(abs_x_speed - abs_x_speed//5), 1))

        if chance == 2 or not 0 < self.rect.y <= self.screen_size[1] - self.rect.height:
            abs_y_speed = abs(self.speed[1])
            self.speed[1] = reverse_sign(self.speed[1]) * (abs_y_speed + random.randint(-(abs_y_speed - abs_y_speed//5), 1))

        if self.speed[1] == 0:
            self.speed[1] += random.choice((-1, 1))
        if self.speed[0] == 0:
            self.speed[0] += random.choice((-1, 1))
        
        self.speed[0] = max(-MAX_SPEED, min(self.speed[0], MAX_SPEED))
        self.speed[1] = max(-MAX_SPEED, min(self.speed[1], MAX_SPEED))

        self.rect.x = max(0, min(self.rect.x, self.screen_size[0] - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_size[1] - self.rect.height))

    def __change_color(self, new: bool = False):
        if new or self.color is None:
            self.color = get_random_color()
        else:
            self.color = change_color(self.color)


class PrismLoop(GenericLoop):
    def __init__(self, screen_size):
        super().__init__()
        self.screen_handler = ScreenHandler(screen_size)
        self.squares = pygame.sprite.Group()

    def start(self):
        self.squares.update(screen_size=self.screen_handler.size)
        self.started = False
        super().start()

    def updater(self):
        super().updater()
        if self.started:
            if len(self.squares) == 0 and self.screen_handler.prism is not True:
                self.started = False
            self.squares.update()
            self.screen_handler.update(to_draw=self.squares)

    def event_handler(self, events: list):
        super().event_handler(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    new_square = MovingSquare((x, y))
                    new_square.update(self.screen_handler.size)
                    self.squares.add(new_square)
                    self.started = True
                elif event.button == 2:
                    self.squares.update(change=True)
                    self.screen_handler.update(blank=True)
                elif event.button == 3:
                    self.squares.empty()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.terminate()
                if event.key == pygame.K_q:
                    if self.screen_handler.update(prism=True):
                        self.started = True
                if event.key == pygame.K_s:
                    self.save()
