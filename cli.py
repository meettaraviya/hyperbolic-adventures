import math

def get_int(q: list[str]) -> int:
    top = q.pop(0)
    try:
        return int(top)
    except ValueError:
        match top:
            case '+':
                return get_int(q) + get_int(q)
            case '*':
                return get_int(q) * get_int(q)
            case '/':
                return get_int(q) // get_int(q)
            case '-':
                return get_int(q) - get_int(q)
            case _:
                raise ValueError(f"Unknown operator: {top}")

def get_float(q: list[str]) -> float:
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
            case 'r':
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
            case _:
                raise ValueError(f"Unknown operator: {top}")

from typing import Any, Optional

def parse(cmd_queue: list[str], turtle: Optional[Any] =None, exit_flag_ref: Optional[list[bool]] =None):
    """Parse and execute commands for the turtle
    
    Args:
        cmd_queue: List of command tokens to parse
        turtle: Hypertle instance (uses global if not provided)
        exit_flag_ref: List containing exit flag (uses global if not provided)
    """
    if turtle is None:
        turtle = globals().get('turtle')
    if exit_flag_ref is None:
        exit_flag_ref = [globals().get('exit_flag', False)]
    
    # Ensure turtle is not None
    assert turtle is not None, "Turtle must be provided or set in globals"
    
    while len(cmd_queue) > 0:
        token = cmd_queue.pop(0)
        match token:
            case 'q':
                if exit_flag_ref:
                    exit_flag_ref[0] = True
                else:
                    globals()['exit_flag'] = True
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
                n = get_int(cmd_queue)
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

                    for _ in range(n):
                        parse(sub_cmd.copy(), turtle, exit_flag_ref)

                    cmd_queue = cmd_queue[i + 1:]
            case _:
                # Ignore unknown tokens
                pass
