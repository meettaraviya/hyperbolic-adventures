import math

from canvas import *
from turtle import RawTurtle, Turtle
from cli import parse
import threading

class Hypertle_BACKUP(Canvas, RawTurtle):
    def __init__(self, r: int, turtle_scale: int):
        Canvas.__init__(self, r)
        self.turtle_shape = [(1., 0.), (-1., 1.), (0., 0.), (-1., -1.)]
        self.turtle_scale = turtle_scale
        self.turtle_phase = 0.
        self.pen_down = True

    def draw(self):
        Canvas.draw(self)
        self.__draw_turtle()

    def fd(self, x):
        z = cmath.rect(math.tanh(x / (2 * self.R)), math.radians(self.turtle_phase))
        self.components.translate(z)
        if self.pen_down:
            self.add(HSegment(-z, 0., self.color))

    def pd(self): self.pen_down = True

    def pu(self): self.pen_down = False

    def rt(self, theta):
        self.turtle_phase = (self.turtle_phase + theta) % 360

    def circle(self, r):
        self.add(HCircle(0., r / self.R, self.color))

    def bk(self, x):
        self.fd(-x)

    def lt(self, theta):
        self.rt(-theta)

    def polygon(self, n: int, theta):
        self.add(HPolygon(0., n, math.radians(theta), math.radians(self.turtle_phase), self.color))

    def __draw_turtle(self):
        turtle_points = [
            pygame.math.Vector2(p).rotate(self.turtle_phase) * self.turtle_scale +
            pygame.math.Vector2(self.R, self.R)
            for p in self.turtle_shape
        ]
        pygame.draw.polygon(self.surface, self.color, turtle_points)


class Hypertle(Turtle, Hypertle_BACKUP):
    def __init__(self, R, turtle_scale):
        Turtle.__init__(self)
        Hypertle_BACKUP.__init__(self, R, turtle_scale)
        self.turtle = Turtle()

    def draw(self):
        Canvas.draw(self)
        self.__draw_turtle()
    
    def fd(self, x):
        Hypertle_BACKUP.fd(self, x)
        self.turtle.fd(x)
    
    def bk(self, x):
        Hypertle_BACKUP.bk(self, x)
        self.turtle.bk(x)
    
    def rt(self, theta):
        Hypertle_BACKUP.rt(self, theta)
        self.turtle.rt(theta)

    def lt(self, theta):
        Hypertle_BACKUP.lt(self, theta)
        self.turtle.lt(theta)

    def __draw_turtle(self):
        turtle_points = [
            pygame.math.Vector2(p).rotate(self.turtle_phase) * self.turtle_scale +
            pygame.math.Vector2(self.R, self.R)
            for p in self.turtle_shape
        ]
        pygame.draw.polygon(self.surface, self.color, turtle_points)



def background():
    while not exit_flag:
        cmd_queue = input('> ').strip('\n').split(' ')
        parse(cmd_queue)


exit_flag = False
R = 400
TURTLE_SCALE = 20
turtle = Hypertle(R, TURTLE_SCALE)

if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption("My Board")

    cmd_thread = threading.Thread(target=background)
    cmd_thread.daemon = True
    cmd_thread.start()

    while not exit_flag:
        turtle.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag = True

    pygame.display.quit()
    cmd_thread.join()


