# from generation import base_classes
# from simulations import simulations
# from display import charts, illustration

# particles_info = [
#     {'type': 'kaolinite', 'size_upper_bound': 200, 'size_lower_bound': 120, 'quantity': 500},
#     {'type': 'quartz', 'size_upper_bound': 1200, 'size_lower_bound': 1000, 'quantity': 80},
#     ]
# container = base_classes.Container(
#     length = 4000,
#     width = 4000,
#     particles_info = particles_info
# )
# container.generate()

# run the simulation with appropriate parameters
# sim = simulations.Triaxial(container, params)
# sim.run()

# connect charts and illustrations with the running simulation
from collections import defaultdict
from typing import Any

def determine_types(*args, **kwargs):
    """determining the type of arguments passed

    Returns:
        a tuple containing the types of the passed arguments
    """
    
    return tuple(
        [str(type(item)) for item in args] + [str(type(item)) for item in kwargs.values()]
    )


func_table = defaultdict(dict)


def overload(*types: str):
    """defineing an overload decorator to be able to use functions with
    the same name for different types of arguments

    Args:
        *types (type): types of the input arguments expected for the
            decorated function
    Returns:
        the suitable function due to the given types
    """

    def wrapper(func):
        named_func = func_table[func.__name__]
        named_func[types] = func

        def call_func(*args: Any, **kwargs: Any):
            tps = determine_types(*args, **kwargs)
            f = named_func[tps]
            return f(*args, **kwargs)

        return call_func

    return wrapper

from geometry import two_dimensional_entities as shapes

@overload("<class 'geometry.two_dimensional_entities.Line'>")
def say_hi(x):
    print('hiiiii, there\'s a line')

@overload("<class 'geometry.two_dimensional_entities.Point'>")
def say_hi(x):
    print('helllllooo, there\'s a point')

point = shapes.Point(0, 0)
line = shapes.Line(0, 0)
say_hi(point)
print('------------')
say_hi(line)