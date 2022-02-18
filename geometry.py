import pygame

import cmath
import math

TOLERANCE = 1.0e-5


class HPoint:
    def __init__(self, z: complex):
        self.z = z

    def translate(self, c: complex):
        self.z = (self.z - c) / (1. - c.conjugate() * self.z)

    def rotate(self, theta: float):
        r, phi = cmath.polar(self.z)
        self.z = cmath.rect(r, phi + theta)

    def draw(self, turtle):
        pass


class HShape:
    def __init__(self, components):
        self.components = components

    def translate(self, c: complex):
        for el in self.components:
            el.translate(c)

    def rotate(self, theta: float):
        for el in self.components:
            el.rotate(theta)

    def __getitem__(self, item):
        return self.components[item]

    def append(self, item):
        self.components.append(item)

    def draw(self, turtle):
        for component in self.components:
            component.draw(turtle)


class HSegment(HShape):
    def __init__(self, z1: complex, z2: complex, color):
        HShape.__init__(self, [HPoint(z1), HPoint(z2)])
        self.color = color

    def draw(self, turtle):
        d = self[0].z.conjugate() * self[1].z - self[1].z.conjugate() * self[0].z
        if abs(d) < TOLERANCE:
            pygame.draw.aaline(
                turtle.surface,
                self.color,
                turtle.transform(self[0].z),
                turtle.transform(self[1].z)
            )
        else:
            x = (self[0].z * self[1].z * (self[0].z.conjugate() - self[1].z.conjugate())
                 + self[1].z - self[0].z) / d
            r = abs(x - self[0].z)
            rect = pygame.Rect(
                *turtle.transform(x - r * (1. + 1.j)),
                2 * r * turtle.R,
                2 * r * turtle.R
            )
            if d.imag > 0:
                pygame.draw.arc(
                    turtle.surface,
                    self.color,
                    rect,
                    -cmath.phase(self[0].z - x),
                    -cmath.phase(self[1].z - x)
                )
            else:
                pygame.draw.arc(
                    turtle.surface,
                    self.color,
                    rect,
                    -cmath.phase(self[1].z - x),
                    -cmath.phase(self[0].z - x)
                )


class HCircle(HShape):
    def __init__(self, c: complex, r: float, color):
        HShape.__init__(self, [HPoint(c)])
        self.r = r
        self.color = color

    def draw(self, turtle):
        c_ns = (self[0].z * self[0].z.conjugate()).real
        r_e0 = math.tanh(self.r / 2)
        r_e = r_e0 * (1. - c_ns) / (1. - c_ns * (r_e0 ** 2))
        c_e = (1. - r_e0 ** 2) / (1. - c_ns * (r_e0 ** 2)) * self[0].z
        pygame.draw.circle(
            turtle.surface,
            self.color,
            turtle.transform(c_e),
            r_e * turtle.R,
            width=1
        )


class HPolygon(HShape):
    def __init__(self, c: complex, n: int, theta: float, phi: float, color):
        sin_hb = math.sin(theta / 2) / math.cos(math.pi / n)
        r = (math.cos(theta / 2) - sin_hb * math.sin(math.pi / n)) / math.sqrt(1 - sin_hb ** 2)
        sides = []
        for i in range(n):
            phi1 = phi + i * math.tau / n
            phi2 = phi + ((i + 1) % n) * math.tau / n
            sides.append(HSegment(
                c + cmath.rect(r, phi1),
                c + cmath.rect(r, phi2),
                color
            ))
        HShape.__init__(self, sides)
