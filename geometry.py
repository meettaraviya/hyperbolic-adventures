import pygame

import cmath
import math
from typing import Any, Tuple

TOLERANCE = 1.0e-8


class HPoint:
    def __init__(self, z: complex):
        self.z = z

    def translate(self, c: complex):
        self.z = (self.z - c) / (1. - c.conjugate() * self.z)

    def rotate(self, theta: float):
        r, phi = cmath.polar(self.z)
        self.z = cmath.rect(r, phi + theta)

    def draw(self, turtle: Any):
        pass

    def distance(self, other: 'HShape | HPoint') -> float:
        if isinstance(other, HShape):
            raise NotImplementedError("Distance not implemented for HShape")
        num = abs(self.z - other.z)
        den = abs(1 - self.z.conjugate() * other.z)
        return 2 * math.atanh(num / den)
    
    def midpoint(self, other: 'HPoint') -> 'HPoint':
        z1 = self.z
        z2 = other.z
        mid_z = (z1 + z2) / (1 + z1.conjugate() * z2)
        return HPoint(mid_z)


class HShape:
    def __init__(self, components: list['HShape | HPoint']):
        self.components = components

    def translate(self, c: complex) -> None:
        for el in self.components:
            el.translate(c)

    def rotate(self, theta: float) -> None:
        for el in self.components:
            el.rotate(theta)

    def __getitem__(self, i: int) -> 'HShape | HPoint':
        return self.components[i]

    def append(self, item: 'HShape | HPoint') -> None:
        self.components.append(item)

    def draw(self, turtle: Any) -> None:
        for component in self.components:
            component.draw(turtle)
    
    def distance(self, other: 'HShape | HPoint') -> float:
        raise NotImplementedError("Distance not implemented for HShape")

class HSegment(HShape):
    def __init__(self, z1: complex, z2: complex, color: Tuple[int, int, int] = (0, 0, 0)):
        HShape.__init__(self, [HPoint(z1), HPoint(z2)])
        self.color = color
    
    def __str__(self) -> str:
        return "({x1:.2f})--({x2:.2f})".format(
            x1=self[0].z,
            x2=self[1].z
        )
    
    def __repr__(self) -> str:
        return self.__str__()

    def draw(self, turtle: Any):
        d = self[0].z.conjugate() * self[1].z - self[1].z.conjugate() * self[0].z
        # if abs
        if abs(d) < TOLERANCE:
            pygame.draw.aaline(
                turtle.surface,
                self.color,
                turtle.transform(self[0].z),
                turtle.transform(self[1].z)
            )
        else:
            # x = (self[0].z * self[1].z * (self[0].z.conjugate() - self[1].z.conjugate()) + self[1].z - self[0].z) / d
            x = ((1 + abs(self[0].z) ** 2) * self[1].z - (1 + abs(self[1].z) ** 2) * self[0].z) / d
            r = abs(x - self[0].z)
            top_left = turtle.transform(x - r * (1. + 1.j))
            rect = pygame.Rect(
                top_left[0],
                top_left[1],
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
    def __init__(self, c: complex, r: float, color: Tuple[int, int, int]):
        HShape.__init__(self, [HPoint(c)])
        self.r = r
        self.color = color

    def draw(self, turtle: Any):
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
    def __init__(self, c: complex, n: int, theta: float, phi: float, color: Tuple[int, int, int]):
        sin_hb = math.sin(theta / 2) / math.cos(math.pi / n)
        r = (math.cos(theta / 2) - sin_hb * math.sin(math.pi / n)) / math.sqrt(1 - sin_hb ** 2)
        sides : list[HSegment] = []
        for i in range(n):
            phi1 = phi + i * math.tau / n
            phi2 = phi + ((i + 1) % n) * math.tau / n
            sides.append(HSegment(
                c + cmath.rect(r, phi1),
                c + cmath.rect(r, phi2),
                color
            ))
        HShape.__init__(self, sides)
