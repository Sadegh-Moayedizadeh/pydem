"""module containing all the operations applicable on two
dimentional geometric shapes
"""

from abc import ABC
from collections import defaultdict
from typing import Any
from pydem.geometry import two_dimensional_entities as shapes


def determine_types(*args, **kwargs):
    """determining the type of arguments passed
    
    Returns:
        a tuple containing the types of the passed arguments
    """
    return tuple([type(item) for item in args] + [type(item) for item in kwargs.values()])
func_table = defaultdict(dict)
def overload(*types: type):
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


@overload(shapes.Point, shapes.Point)
def intersection(entity1, entity2):
    pass


@overload(shapes.Point, shapes.Polygon)
def intersection(entity1, entity2):
    pass


@overload(shapes.Point, shapes.Rectangle)
def intersection(entity1, entity2):
    pass


@overload(shapes.Point, shapes.Circle)
def intersection(entity1, entity2):
    pass


@overload(shapes.Point, shapes.Line)
def intersection(entity1, entity2):
    pass


@overload(shapes.Point, shapes.LineSegment)
def intersection(entity1, entity2):
    pass


@overload(shapes.Polygon, shapes.Point)
def intersection(entity1, entity2):
    pass


@overload(shapes.Polygon, shapes.Polygon)
def intersection(entity1, entity2):
    pass


@overload(shapes.Polygon, shapes.Rectangle)
def intersection(entity1, entity2):
    pass


@overload(shapes.Polygon, shapes.Circle)
def intersection(entity1, entity2):
    pass


@overload(shapes.Polygon, shapes.Line)
def intersection(entity1, entity2):
    pass


@overload(shapes.Polygon, shapes.LineSegment)
def intersection(entity1, entity2):
    pass


@overload(shapes.Rectangle, shapes.Point)
def intersection(entity1, entity2):
    pass


@overload(shapes.Rectangle, shapes.Polygon)
def intersection(entity1, entity2):
    pass


@overload(shapes.Rectangle, shapes.Rectangle)
def intersection(entity1, entity2):
    pass


@overload(shapes.Rectangle, shapes.Circle)
def intersection(entity1, entity2):
    pass


@overload(shapes.Rectangle, shapes.Line)
def intersection(entity1, entity2):
    pass


@overload(shapes.Rectangle, shapes.LineSegment)
def intersection(entity1, entity2):
    pass
