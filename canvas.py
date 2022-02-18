from geometry import *
import pygame


class Canvas:
    def __init__(self, r: int):
        self.R = r
        self.surface = pygame.display.set_mode((2 * r, 2 * r))
        self.color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        self.components = HShape([])

    def draw(self):
        self.surface.fill((0, 0, 0))
        self.__draw_disc()
        self.components.draw(self)

    def __draw_disc(self):
        pygame.draw.circle(
            self.surface,
            self.bg_color,
            (self.R, self.R),
            self.R
        )

    def add(self, s: HShape):
        self.components.append(s)

    def transform(self, z):
        return (z.real + 1.) * self.R, (z.imag + 1.) * self.R

    def clear(self):
        self.components = HShape([])
