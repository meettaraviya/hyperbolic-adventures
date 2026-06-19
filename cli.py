import math
from typing import Any, Optional

# Global function registry
_functions: dict[str, tuple[list[str], list[str]]] = {}

def execute_function(cmd_queue: list[str], turtle: Optional[Any] = None, exit_flag_ref: Optional[list[bool]] = None, local_vars: Optional[dict[str, float]] = None) -> float:
    """Execute a function body and return the final float value"""
    if turtle is None:
        turtle = globals().get('turtle')
    if exit_flag_ref is None:
        exit_flag_ref = [globals().get('exit_flag', False)]
    if local_vars is None:
        local_vars = {}
    
    result = 0.0
    while len(cmd_queue) > 0:
        token = cmd_queue[0]
        # Check if this is a float expression
        try:
            result = get_float(cmd_queue, local_vars)
        except (ValueError, IndexError):
            # Not a float, parse as command
            parse(cmd_queue, turtle, exit_flag_ref, local_vars)
    return result

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

def get_float(q: list[str], local_vars: Optional[dict[str, float]] = None) -> float:
    if local_vars is None:
        local_vars = {}
    
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
                return get_float(q, local_vars) + get_float(q, local_vars)
            case '*':
                return get_float(q, local_vars) * get_float(q, local_vars)
            case '/':
                return get_float(q, local_vars) / get_float(q, local_vars)
            case '-':
                return get_float(q, local_vars) - get_float(q, local_vars)
            case 'r':
                return math.sqrt(get_float(q, local_vars))
            case 's':
                return math.sin(get_float(q, local_vars))
            case 'c':
                return math.cos(get_float(q, local_vars))
            case 't':
                return math.tan(get_float(q, local_vars))
            case 'as':
                return math.asin(get_float(q, local_vars))
            case 'ac':
                return math.acos(get_float(q, local_vars))
            case 'at':
                return math.atan(get_float(q, local_vars))
            case 'ash':
                return math.asinh(get_float(q, local_vars))
            case 'ach':
                return math.acosh(get_float(q, local_vars))
            case 'ath':
                return math.atanh(get_float(q, local_vars))
            case 'sh':
                return math.sinh(get_float(q, local_vars))
            case 'ch':
                return math.cosh(get_float(q, local_vars))
            case 'th':
                return math.tanh(get_float(q, local_vars))
            case _:
                # Check if it's a variable reference
                if top in local_vars:
                    return local_vars[top]
                # Check if it's a user-defined function
                elif top in _functions:
                    params, body = _functions[top]
                    # Evaluate arguments
                    args = [get_float(q, local_vars) for _ in params]
                    # Create local scope and execute function body
                    turtle = globals().get('turtle')
                    exit_flag_ref = [globals().get('exit_flag', False)]
                    new_local_vars = local_vars.copy()
                    for param, arg in zip(params, args):
                        new_local_vars[param] = arg
                    # Execute function body and capture return value
                    result = execute_function(body.copy(), turtle, exit_flag_ref, new_local_vars)
                    return result
                else:
                    raise ValueError(f"Unknown operator or variable: {top}")

def parse(cmd_queue: list[str], turtle: Optional[Any] = None, exit_flag_ref: Optional[list[bool]] = None, local_vars: Optional[dict[str, float]] = None):
    """Parse and execute commands for the turtle
    
    Args:
        cmd_queue: List of command tokens to parse
        turtle: Hypertle instance (uses global if not provided)
        exit_flag_ref: List containing exit flag (uses global if not provided)
        local_vars: Local variable scope for function parameters
    """
    if turtle is None:
        turtle = globals().get('turtle')
    if exit_flag_ref is None:
        exit_flag_ref = [globals().get('exit_flag', False)]
    if local_vars is None:
        local_vars = {}
    
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
            case 'defn':
                # defn func_name [param1 param2 ...] [command1 command2 ...]
                func_name = cmd_queue.pop(0)
                if cmd_queue.pop(0) != '[':
                    raise ValueError("Expected '[' after function name")
                
                # Extract parameters
                params = []
                depth = 1
                i = 0
                for cmd in cmd_queue:
                    if cmd == '[':
                        depth += 1
                    elif cmd == ']':
                        depth -= 1
                        if depth == 0:
                            break
                    params.append(cmd)
                    i += 1
                
                cmd_queue = cmd_queue[i + 1:]
                
                if cmd_queue.pop(0) != '[':
                    raise ValueError("Expected '[' before function body")
                
                # Extract function body
                body = []
                depth = 1
                i = 0
                for cmd in cmd_queue:
                    if cmd == '[':
                        depth += 1
                    elif cmd == ']':
                        depth -= 1
                        if depth == 0:
                            break
                    body.append(cmd)
                    i += 1
                
                cmd_queue = cmd_queue[i + 1:]
                _functions[func_name] = (params, body)
            
            case 'circle':
                r = get_float(cmd_queue, local_vars)
                turtle.circle(r)
            case 'poly':
                n = int(cmd_queue.pop(0))
                theta = get_float(cmd_queue, local_vars)
                turtle.polygon(n, theta)
            case 'pd':
                turtle.pd()
            case 'pu':
                turtle.pu()
            case 'fd':
                x = get_float(cmd_queue, local_vars)
                turtle.fd(x)
            case 'bk':
                x = get_float(cmd_queue, local_vars)
                turtle.bk(x)
            case 'lt':
                theta = get_float(cmd_queue, local_vars)
                turtle.lt(theta)
            case 'rt':
                theta = get_float(cmd_queue, local_vars)
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
                        parse(sub_cmd.copy(), turtle, exit_flag_ref, local_vars)

                    cmd_queue = cmd_queue[i + 1:]
            case _:
                # Check if it's a user-defined function
                if token in _functions:
                    params, body = _functions[token]
                    # Evaluate arguments
                    args = [get_float(cmd_queue) for _ in params]
                    # Create local scope
                    new_local_vars = local_vars.copy()
                    for param, arg in zip(params, args):
                        new_local_vars[param] = arg
                    parse(body.copy(), turtle, exit_flag_ref, new_local_vars)
                # Check if it's a variable reference
                elif token in local_vars:
                    # Push the value back as a token for get_float to process
                    cmd_queue.insert(0, str(local_vars[token]))
                else:
                    # Ignore unknown tokens
                    pass
