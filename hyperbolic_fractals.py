from geometry import HSegment
from typing import Generator
import math
import cmath

from canvas import Canvas
from hypertle import Hypertle
from geometry import HCircle, HPolygon, HSegment
import pygame
import time

import threading

counter = 0

exit_flag = False
R = 540
TURTLE_SCALE = 20
turtle = Hypertle(R, TURTLE_SCALE)
turtle.pu()

initial_segments: list[HSegment] = [HSegment(complex(-0.5, 0.), complex(0.5, 0.))]
rendered_segments: list[HSegment] = initial_segments.copy()

def substitute_segment(seg: HSegment, scale_factor: float, rotation_angle: int) -> list[HSegment]:
    dist = seg[0].distance(seg[1])
    displacement_vec = (seg[1].z - seg[0].z) * cmath.exp(math.radians(rotation_angle) * 1j) * scale_factor / 2

    return [
        HSegment(seg[0].z - displacement_vec, seg[0].z + displacement_vec),
        HSegment(seg[1].z - displacement_vec, seg[1].z + displacement_vec)
    ]

def fractal_iterate(segments: list[HSegment], depth: int, scale_factor: float = 1/6, rotation_angle: int = 90, resolution: float = 1e-10) -> Generator[HSegment, None, None]:
    if depth == 0:
        yield from segments
    else:
        tmp_segments = segments.copy()
        # segments.clear()
        for seg in tmp_segments:
            if abs(seg[1].z - seg[0].z) < resolution:
                continue
            segments.extend(substitute_segment(seg, scale_factor, rotation_angle))
        tmp_segments.clear()
        del tmp_segments
        yield from fractal_iterate(segments, depth - 1, scale_factor, rotation_angle, resolution)
    
def background():

    while not exit_flag:
        time.sleep(1.0)
        turtle.clear()
        global counter
        counter += 1
        for edge in fractal_iterate(
            segments=rendered_segments,
            depth= 1 + (counter - 1) % 13,
            scale_factor=0.9,
            rotation_angle=90,
            # segments=[
            #     HSegment(complex(1, 0), complex(-1, 0))
            #     ],
            # depth=counter,
            # scale_factor=1/2,
            # rotation_angle=90,
        ):
            turtle.add(edge)

        rendered_segments.clear()
        rendered_segments.extend(initial_segments)

if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption("My Board")

    cmd_thread = threading.Thread(target=background)
    cmd_thread.daemon = True
    cmd_thread.start()
    screen = pygame.display.set_mode((1080, 1080))
    pygame.display.set_caption("Hyperbolic fractal fun")

    while not exit_flag:
        turtle.draw()
        pygame.display.update()
        # screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit_flag = True

    pygame.display.quit()
    cmd_thread.join()

