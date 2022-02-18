import math

from canvas import *

import threading


class Hypertle(Canvas):
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


def get_float(q):
    top = q.pop(0)
    try:
        return float(top)
    except ValueError:
        match top:
            case 'e':
                return math.e
            case 'tau':
                return math.tau
            case 'pi':
                return math.pi
            case '+':
                return get_float(q) + get_float(q)
            case '*':
                return get_float(q) * get_float(q)
            case '/':
                return get_float(q) / get_float(q)
            case '-':
                return get_float(q) - get_float(q)
            case '√':
                return math.sqrt(get_float(q))
            case 's':
                return math.sin(get_float(q))
            case 'c':
                return math.cos(get_float(q))
            case 't':
                return math.tan(get_float(q))
            case 'as':
                return math.asin(get_float(q))
            case 'ac':
                return math.acos(get_float(q))
            case 'at':
                return math.atan(get_float(q))
            case 'ash':
                return math.asinh(get_float(q))
            case 'ach':
                return math.acosh(get_float(q))
            case 'ath':
                return math.atanh(get_float(q))
            case 'sh':
                return math.sinh(get_float(q))
            case 'ch':
                return math.cosh(get_float(q))
            case 'th':
                return math.tanh(get_float(q))


def parse(cmd_queue):
    global exit_flag
    while len(cmd_queue) > 0:
        token = cmd_queue.pop(0)
        match token:
            case 'q':
                exit_flag = True
            case 'circle':
                r = get_float(cmd_queue)
                turtle.circle(r)
            case 'poly':
                n = int(cmd_queue.pop(0))
                theta = get_float(cmd_queue)
                turtle.polygon(n, theta)
            case 'pd':
                turtle.pd()
            case 'pu':
                turtle.pu()
            case 'fd':
                x = get_float(cmd_queue)
                turtle.fd(x)
            case 'bk':
                x = get_float(cmd_queue)
                turtle.bk(x)
            case 'lt':
                theta = get_float(cmd_queue)
                turtle.lt(theta)
            case 'rt':
                theta = get_float(cmd_queue)
                turtle.rt(theta)
            case 'cl':
                turtle.clear()
            case 'repeat':
                n = int(cmd_queue.pop(0))
                if cmd_queue.pop(0) == '[':
                    depth = 1
                    i = 0
                    for cmd in cmd_queue:
                        if cmd == '[':
                            depth += 1
                        elif cmd == ']':
                            depth -= 1
                            if depth == 0:
                                break
                        i += 1

                    sub_cmd = cmd_queue[:i]

                    for j in range(n):
                        parse(sub_cmd.copy())

                    cmd_queue = cmd_queue[i + 1:]



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

