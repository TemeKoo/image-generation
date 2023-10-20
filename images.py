import pygame
import random
import os
from datetime import datetime

FILENAME = f"{datetime.now().strftime('%d%m%y_%H%M%S')}.png"
FILEPATH = os.path.join(os.path.dirname(__file__) , "Images", FILENAME)

SAVE = True
WIDTH = 500
HEIGHT = 500
X = 1200
Y = 700

class Image():
    def __init__(self, width, height, screen):
        self.surface = pygame.Surface((width, height))
        self.surface.fill((255,255,255))
        self.screen = screen
        self.width = width
        self.height = height
        self.pos = None

        self.start_color = (0, 0, 102)
        # (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color_range = 10

        self.next = None
        self.visited = None
        self.to_visit = None
        self.complete = False
        self.animation_step = 500
        self.final = []
    
    def get_pos(self):
        if self.pos is None:
            screen_width, screen_height = self.screen.get_width(), self.screen.get_height()
            image_width, image_height = self.surface.get_width(), self.surface.get_height()
            self.pos = ((screen_width//2 - image_width//2, screen_height//2 - image_height//2))
        return self.pos

    def draw(self):
        draw_pos = self.get_pos()
        self.screen.blit(self.surface, draw_pos)

    def start(self, pos):
        if (self.pos[0] <= pos[0] <= self.pos[0]+self.width) and (self.pos[1] <= pos[1] <= self.pos[1]+self.height):
            rel_x = pos[0] - self.pos[0] 
            rel_y = pos[1] - self.pos[1]
            start_pos = (rel_x, rel_y)
            next = (start_pos, (self.start_color))
            if self.next is None:
                self.next = []
            self.next.append(next)
            if self.visited is None:
                self.visited = set()
            if self.to_visit is None:
                self.to_visit = set()
        self.compute()

    def compute(self):
        while len(self.next) > 0:
            # Set color of next pixel                
            if random.randint(1, 2) == 1:
                next_pixel = self.next.pop(random.randint(0, len(self.next)-1))
            elif len(self.next) > 3:
                next_pixel = self.next.pop(-random.randint(1, 3))
            else:
                next_pixel = self.next.pop(-1)
            pos = next_pixel[0]
            self.visited.add(pos)
            self.final.append(next_pixel)

            # Calculate next positions
            next_positions = set()
            for i in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                x = max(0, min(pos[0]+i[0], self.width))
                y = max(0, min(pos[1]+i[1], self.height))
                to_add = (x, y)
                if to_add not in self.visited and to_add not in self.to_visit:
                    if ((0,0) <= to_add <= (self.width, self.height)):
                        next_positions.add(to_add)

            # Assign colors to next pixels and append to queue
            color = next_pixel[1]
            for position in next_positions:
                next_color = [color[0], color[1], color[2]]
                if random.randint(1, 3) == 1:
                    next_color[0] = (self.start_color[0] + next_color[0])//2
                    next_color[1] = (self.start_color[1] + next_color[1])//2
                    next_color[2] = (self.start_color[2] + next_color[2])//2
                elif random.randint(1, 100) == 1:
                    next_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                else:
                    random_index = random.randint(0, 2)
                    color_change = max(0, min(next_color[random_index] + random.randint(-self.color_range, self.color_range), 255))
                    next_color[random_index] = color_change
                self.next.append((position, tuple(next_color)))
                self.to_visit.add(position)
        else:
            self.complete = True

    def update(self, screen_change=False):
        if screen_change:
            self.pos = None
        elif self.complete:
            for _ in range(self.animation_step):
                if len(self.final) > 0:
                    pos, color = self.final.pop(0)
                    self.surface.set_at(pos, color)
                else:
                    self.complete = False
                    return True


def main():
    pygame.init()
    screen = pygame.display.set_mode(size=(X, Y), flags=(pygame.RESIZABLE))
    image = Image(WIDTH, HEIGHT, screen)

    event_queue = []
    while True:
        event_queue.extend(pygame.event.get())
        if len(event_queue) > 0:
            event = event_queue.pop(0)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(size=(event.w,event.h), flags=(pygame.RESIZABLE))
                image.update(screen_change=True)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    image.start(event.pos)

        screen.fill((0,0,0))
        save = image.update()
        image.draw()
        if save and SAVE:
            pygame.image.save(screen, FILEPATH, "png")
        pygame.display.flip()

main()