"""module containing all the operations applicable on two
dimentional geometric shapes
"""

from collections import defaultdict
from typing import Any, Type
from geometry import two_dimensional_entities as shapes


def determine_types(*args, **kwargs):
    """determining the type of arguments passed

    Returns:
        a tuple containing the types of the passed arguments
    """
    return tuple(
        [type(item) for item in args] + [type(item) for item in kwargs.values()]
    )


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
def intersection(
    entity1: Type[shapes.Point],
    entity2: Type[shapes.Point]
    ) -> Type[shapes.Point]:
    """finding the intersection between two points which basically
    happens when they have the same coordinates

    Args:
        entity1 (Type[shapes.Point]): the first of the two points to
            find intersection between
        entity2 (Type[shapes.Point]): the second of the two points to
            find intersection between

    Returns:
        Type[shapes.Point]: the shapes.Point instance if they intersect
            otherwise None
    """
    
    x1, y1 = entity1.x, entity1.y
    x2, y2 = entity2.x, entity2.y
    if x1 == x2 and y1 == y2:
        return shapes.Point(x1, y1)


@overload(shapes.Point, shapes.Polygon)
def intersection(
    entity1: Type[shapes.Point],
    entity2: Type[shapes.Polygon]
    ) -> Type[shapes.Point]:
    """finding intersection between a point and a polygon which
    basically happens when the popint is located on the perimeter of
    the polygon

    Args:
        entity1 (Type[shapes.Point]): the shapes.Point instance
        entity2 (Type[shapes.Polygon]): the shapes.Polygon instance

    Returns:
        Type[shapes.Point]: the intersection between the given point
            and polygon which could be a point with the same
            coordinates of the given point if there is any intersection
            otherwise None
    """

    for line in entity2.edges:
        inter = intersection(entity1, line)
        if inter:
            return inter 


@overload(shapes.Point, shapes.Rectangle)
def intersection(
    entity1: Type[shapes.Point],
    entity2: Type[shapes.Rectangle]
    ) -> Type[shapes.Point]:
    """finding intersection between a point and a rectangle which
    basically happens when the popint is located on the perimeter of
    the rectangle

    Args:
        entity1 (Type[shapes.Point]): the shapes.Point instance
        entity2 (Type[shapes.Rectangle]): the shapes.Rectangle instance

    Returns:
        Type[shapes.Point]: the intersection between the given point
            and rectangle which could be a point with the same
            coordinates of the given point if there is any intersection
            otherwise None
    """
    
    for line in entity2.edges:
        inter = intersection(entity1, line)
        if inter:
            return inter


@overload(shapes.Point, shapes.Line)
def intersection(
    entity1: Type[shapes.Point],
    entity2: Type[shapes.Line]
    ) -> Type[shapes.Point]:
    """finds the intersection between the given point and line

    Args:
        entity1 (Type[shapes.Point]): the shapes.Point instance
        entity2 (Type[shapes.Line]): the shapes.Line instance

    Returns:
        Type[shapes.Point]: the intersection between the given point
            and line which happens when the point is located on the
            line and will be a point with the same coordinates of the
            given entity1, otherwise None
    """
    
    if entity2.width == (entity1.y - (entity2.x) * (entity2.slope)):
        return shapes.Point(entity1.x, entity1.y)


@overload(shapes.Point, shapes.LineSegment)
def intersection(
    entity1: Type[shapes.Point],
    entity2: Type[shapes.LineSegment]
    ) -> Type[shapes.Point]:
    """finds the intersection between the given poin and line segment

    Args:
        entity1 (Type[shapes.Point]): the shapes.Point instance
        entity2 (Type[shapes.LineSegment]): the shapes.LineSegment
            instance

    Returns:
        Type[shapes.Point]: the intersection between the given point
            and line segment which happens when the point is located on
            the line and will be a point with the same coordinates of 
            the given entity1, otherwise None
    """
    
    inter = intersection(entity1, entity2.infinite)
    if inter and is_inside(entity1, shapes.Rectangle.from_diagonal(entity2)):
        return inter


@overload(shapes.Point, shapes.Circle)
def intersection(entity1, entity2):
    pass


@overload(shapes.Polygon, shapes.Point)
def intersection(entity1, entity2):
    return intersection(entity2, entity1)


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
