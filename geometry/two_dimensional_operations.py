"""module containing all the operations applicable on two
dimentional geometric shapes
"""

import numpy as np
from collections import defaultdict
from typing import Any, Type, Tuple
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


def opposite_sides(
    line: Type[shapes.Line],
    point1: Type[shapes.Point],
    point2: Type[shapes.Point]
    ) -> bool:
    """checks if the given points are located on the opposite sides of
    the given line

    Args:
        line (Type[shapes.Line]): the given shapes.Line instance
        point1 (Type[shapes.Point]): the first given shapes.Point
            instance
        point2 (Type[shapes.Point]): the second given shapes.Point
            instance

    Returns:
        bool: True or False indicating if the given points are on the
            opposite sides of the given line
    """
    
    dif1 = (point1.y) - ((line.slope) * (point1.x) + (line.width))
    dif2 = (point2.y) - ((line.slope) * (point2.x) + (line.width))
    sign1 = dif1 / abs(dif1)
    sign2 = dif2 / abs(dif2)
    return (sign1 != sign2)


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
def intersection(
    entity1: Type[shapes.Point],
    entity2: Type[shapes.Circle]
    ) -> Type[shapes.Point]:
    """find the intersection between the given point and circle

    Args:
        entity1 (Type[shapes.Point]): the shapes.Point instance
        entity2 (Type[shapes.Circle]): the shapes.Circle instance

    Returns:
        Type[shapes.Point]: the intersection between the given point
            and circle which is a point with the same coordinates as
            the given point if it is located on the perimeter of the
            circle, otherwise None
    """
    
    if distance(entity1, entity2.center) == entity2.radius:
        return shapes.Point(entity1.x, entity1.y)


@overload(shapes.Polygon, shapes.Point)
def intersection(
    entity1: Type[shapes.Polygon],
    entity2: Type[shapes.Point]
    ) -> Type[shapes.Point]:
    """finds intersection between a point and a polygon which
    basically happens when the popint is located on the perimeter of
    the polygon

    Args:
        entity1 (Type[shapes.Polygon]): the shapes.Polygon instance
        entity2 (Type[shapes.Point]): the shapes.Point instance

    Returns:
        Type[shapes.Point]: the intersection between the given point
            and polygon which could be a point with the same
            coordinates of the given point if there is any intersection
            otherwise None
    """
    
    return intersection(entity2, entity1)


@overload(shapes.Polygon, shapes.Polygon)
def intersection(
    entity1: Type[shapes.Polygon],
    entity2: Type[shapes.Polygon]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given polygons

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Rectangle]): the other given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection between the given
            entities which is a tuple of points denoting the locations
            of intersections
    """
    
    res = []
    for line1 in entity1.edges:
        for line2 in entity2.edges:
            inter = intersection(line1, line2)
            if inter:
                res.append(inter)
    return tuple(res)


@overload(shapes.Polygon, shapes.Rectangle)
def intersection(
    entity1: Type[shapes.Polygon],
    entity2: Type[shapes.Rectangle]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given polygon and rectangle

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection between the given
            entities which is a tuple of points denoting the locations
            of intersections
    """

    res = []
    for line1 in entity1.edges:
        for line2 in entity2.edges:
            inter = intersection(line1, line2)
            if inter:
                res.append(inter)
    return tuple(res)


@overload(shapes.Polygon, shapes.Circle)
def intersection(
    entity1: Type[shapes.Polygon],
    entity2: Type[shapes.Circle]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given polygon and circle

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection points between the
            two given entities in a tuple
    """
    
    res = []
    for line in entity1.edges:
        inter = intersection(line, entity2)
        if inter:
            res.append(inter)
    return tuple(res)


@overload(shapes.Polygon, shapes.Line)
def intersection(
    entity1: Type[shapes.Polygon],
    entity2: Type[shapes.Line]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given polygon and line
    instance

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection points between the
            two given entities inside a tuple
    """

    res = []
    for line in entity1.edges:
        inter = intersection(line, entity2)
        if inter:
            res.append(inter)
    return tuple(res)


@overload(shapes.Polygon, shapes.LineSegment)
def intersection(
    entity1: Type[shapes.Polygon],
    entity2: Type[shapes.LineSegment]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given polygon and line
    segment entity

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection points between the
            two given entities inside a tuple
    """
    
    res = []
    for line in entity1.edges:
        inter = intersection(line, entity2)
        if inter:
            res.append(inter)
    return tuple(res)


@overload(shapes.Rectangle, shapes.Point)
def intersection(
    entity1: Type[shapes.Rectangle],
    entity2: Type[shapes.Point]
    ) -> Type[shapes.Point]:
    """finds the intersection between the given rectangle and point
    entity

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        Type[shapes.Point]: the intersection points between the
            two given entities which is a point with the same
            coordinates as the given point entity if it is located on
            the perimeter of the given rectangle entity, otherwise None
    """
    
    return intersection(entity2, entity1)


@overload(shapes.Rectangle, shapes.Polygon)
def intersection(
    entity1: Type[shapes.Rectangle],
    entity2: Type[shapes.Polygon]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given polygon and rectangle

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection between the given
            entities which is a tuple of points denoting the locations
            of intersections
    """
    
    return intersection(entity2, entity1)


@overload(shapes.Rectangle, shapes.Rectangle)
def intersection(
    entity1: Type[shapes.Rectangle],
    entity2: Type[shapes.Rectangle]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given two rectangle entities

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection between the given
            entities which is a tuple of points denoting the locations
            of intersections
    """

    res = []
    for line1 in entity1.edges:
        for line2 in entity2.edges:
            inter = intersection(line1, line2)
            if inter:
                res.append(inter)
    return tuple(res)


@overload(shapes.Rectangle, shapes.Circle)
def intersection(
    entity1: Type[shapes.Rectangle],
    entity2: Type[shapes.Circle]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given rectangle and circle
    instance

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        Tuple[Type[shapes.Point]]: a tuple of points which to denote
            the intersection between the given entities
    """

    res = []
    for line in entity1.edges:
        inter = intersection(line, entity2)
        if inter:
            res.append(inter)
    return tuple(res)


@overload(shapes.Rectangle, shapes.Line)
def intersection(
    entity1: Type[shapes.Rectangle],
    entity2: Type[shapes.Line]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given rectangle and line
    instance

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        Tuple[Type[shapes.Point]]: a tuple of points which to denote
            the intersection between the given entities
    """

    res = []
    for line in entity1.edges:
        inter = intersection(line, entity2)
        if inter:
            res.append(inter)
    return tuple(res)


@overload(shapes.Rectangle, shapes.LineSegment)
def intersection(
    entity1: Type[shapes.Rectangle],
    entity2: Type[shapes.LineSegment]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given rectangle and line segment
    instance

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        Tuple[Type[shapes.Point]]: a tuple of points which to denote
            the intersection between the given entities
    """

    res = []
    for line in entity1.edges:
        inter = intersection(line, entity2)
        if inter:
            res.append(inter)
    return tuple(res)


@overload(shapes.Circle, shapes.Point)
def intersection(
    entity1: Type[shapes.Circle],
    entity2: Type[shapes.Point]
    ) -> Type[shapes.Point]:
    """find the intersection between the given point and circle

    Args:
        entity1 (Type[shapes.Circle]): the shapes.Circle instance
        entity2 (Type[shapes.Point]): the shapes.Point instance

    Returns:
        Type[shapes.Point]: the intersection between the given point
            and circle which is a point with the same coordinates as
            the given point if it is located on the perimeter of the
            circle, otherwise None
    """
    
    return intersection(entity2, entity1)


@overload(shapes.Circle, shapes.Polygon)
def intersection(
    entity1: Type[shapes.Circle],
    entity2: Type[shapes.Polygon]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given polygon and circle

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection points between the
            two given entities in a tuple
    """
    
    return intersection(entity2, entity1)


@overload(shapes.Circle, shapes.Rectangle)
def intersection(
    entity1: Type[shapes.Circle],
    entity2: Type[shapes.Rectangle]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given rectangle and circle
    instance

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        Tuple[Type[shapes.Point]]: a tuple of points which to denote
            the intersection between the given entities
    """
    
    return intersection(entity2, entity1)


@overload(shapes.Circle, shapes.Circle)
def intersection(
    entity1: Type[shapes.Circle],
    entity2: Type[shapes.Circle]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given two circles, could be
    None if there isn't any intersection, which happens when two circles
    are far apart or one is completelpy inside another; could be a
    single point when they only touch each other; could be a tuple of
    two points when they intersect

    Args:
        entity1 (Type[shapes.Circle]): the first given shapes.Circle
            instance
        entity2 (Type[shapes.Circle]): the second given shapes.Circle
            instace

    Returns:
        Tuple[Type[shapes.Point]]: intesection points if they exist,
            otherwise None
    """
    
    dist = distance(entity1.center, entity2.center)
    if dist > (entity1.radius + entity2.radius):
        return
    if entity1.radius > (dist + entity2.radius) or entity2.radius > (dist + entity1.radius):
        return
    if dist == (entity1.radius + entity2.radius):
        ratio = entity1.radius / (entity1.radius + entity2.radius)
        return shapes.LineSegment(entity1.center, entity2.center).midpoint(ratio)
    # formula from:
    # https://math.stackexchange.com/questions/256100/how-can-i-find-the-points-at-which-two-circles-intersect
    # written by "salix alba": https://math.stackexchange.com/users/139342/salix-alba
    l = ((entity1.radius)**2 - (entity2.radius)**2 + (dist)**2) / (2*dist)
    h = np.sqrt((entity1.radius)**2 - (l)**2)
    exp1 = (l / dist) * (entity2.center.x - entity1.center.x)
    exp2 = (h / dist) * (entity2.center.y - entity1.center.y)
    x1 = exp1 + exp2 + entity1.center.x
    x2 = exp1 - exp2 + entity1.center.x
    exp1 = (l / dist) * (entity2.center.y - entity1.center.y)
    exp2 = (h / dist) * (entity2.center.x - entity1.center.x)
    y1 = exp1 - exp2 + entity1.center.y
    y2 = exp1 + exp2 + entity1.center.y
    return (shapes.Point(x1, y1), shapes.Point(x2, y2))


@overload(shapes.Circle, shapes.Line)
def intersection(
    entity1: Type[shapes.Circle],
    entity2: Type[shapes.Line]
    ) -> Tuple[Type[shapes.Point]]:
    """finds intersection between an infinite line an a circle; could
    be None, a single point, or two points

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection between the given
            instances
    """
    
    # formula from:
    # https://math.stackexchange.com/questions/228841/how-do-i-calculate-the-intersections-of-a-straight-line-and-a-circle
    # written by "Fly by Night": https://math.stackexchange.com/users/38495/fly-by-night
    a = (entity2.slope)**2 + 1
    b = 2 * (
        ((entity2.slope) * (entity2.width)) 
        - ((entity2.slope) * (entity1.center.y))
        - (entity1.center.x)
        )
    c = (
        (entity1.center.y)**2
        - (entity1.radius)**2
        + (entity1.center.x)**2
        - 2 * ((entity1.center.y) * (entity2.width))
        + (entity2.width)**2
    )
    try:
        x1 = (-1 * (b) + np.sqrt(b**2 - 4*a*c)) / (2*a)
        x2 = (-1 * (b) - np.sqrt(b**2 - 4*a*c)) / (2*a)
    except:
        return
    if x1 == x2:
        return shapes.Point(x1, entity2.get_y(x1))
    y1 = entity2.get_y(x1)
    y2 = entity2.get_y(x2)
    return (shapes.Point(x1, y1), shapes.Point(x2, y2))


@overload(shapes.Circle, shapes.LineSegment)
def intersection(
    entity1: Type[shapes.Circle],
    entity2: Type[shapes.LineSegment]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between a line segment and a circle

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instances

    Returns:
        Tuple[Type[shapes.Point]]: the intersection between the given
            entities
    """
    
    inter = intersection(entity1, entity2.infinite)
    if inter is None:
        return
    res = []
    for point in inter:
        if intersection(point, entity2):
            res.append(point)
    return tuple(res)


@overload(shapes.Line, shapes.Point)
def intersection(
    entity1: Type[shapes.Line],
    entity2: Type[shapes.Point]
    ) -> Type[shapes.Point]:
    """finds the intersection between the given point and line

    Args:
        entity1 (Type[shapes.Line]): the shapes.Line instance
        entity2 (Type[shapes.Point]): the shapes.Point instance

    Returns:
        Type[shapes.Point]: the intersection between the given point
            and line which happens when the point is located on the
            line and will be a point with the same coordinates of the
            given entity1, otherwise None
    """
    
    return intersection(entity2, entity1)


@overload(shapes.Line, shapes.Polygon)
def intersection(
    entity1: Type[shapes.Line],
    entity2: Type[shapes.Polygon]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given polygon and line
    instance

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection points between the
            two given entities inside a tuple
    """
    
    return intersection(entity2, entity1)


@overload(shapes.Line, shapes.Rectangle)
def intersection(
    entity1: Type[shapes.Line],
    entity2: Type[shapes.Rectangle]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given rectangle and line
    instance

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        Tuple[Type[shapes.Point]]: a tuple of points which to denote
            the intersection between the given entities
    """
    
    return intersection(entity2, entity1)


@overload(shapes.Line, shapes.Circle)
def intersection(
    entity1: Type[shapes.Line],
    entity2: Type[shapes.Circle]
    ) -> Tuple[Type[shapes.Point]]:
    """finds intersection between an infinite line an a circle; could
    be None, a single point, or two points

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection between the given
            instances
    """
    
    return intersection(entity2, entity1)


@overload(shapes.Line, shapes.Line)
def intersection(
    entity1: Type[shapes.Line],
    entity2: Type[shapes.Line]
    ) -> Type[shapes.Point]:
    """finds the intersection between two lines

    Args:
        entity1 (Type[shapes.Line]): the first given shapes.Line
            instance
        entity2 (Type[shapes.Line]): the socond given shapes.Line
            instance

    Returns:
        Type[shapes.Point]: the intersection between two given entities
    """
    
    if entity1.slope == entity2.slope:
        return
    x = (entity2.width - entity1.width) / (entity1.slope - entity2.slope)
    y = entity1.get_y(x)
    return shapes.Point(x, y)


@overload(shapes.Line, shapes.LineSegment)
def intersection(
    entity1: Type[shapes.Line],
    entity2: Type[shapes.LineSegment]
    ) -> Type[shapes.Point]:
    """finds the intersection between an infinite line and a finite
    line segment

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment instance

    Returns:
        Type[shapes.Point]: the intersection between the given two entities
    """
    
    inter = intersection(entity1, entity2.infinite)
    if inter and intersection(inter, entity2):
        return inter


@overload(shapes.LineSegment, shapes.Point)
def intersection(
    entity1: Type[shapes.LineSegment],
    entity2: Type[shapes.Point]
    ) -> Type[shapes.Point]:
    """finds the intersection between the given poin and line segment

    Args:
        entity1 (Type[shapes.LineSegment]): the shapes.LineSegment
            instance
        entity2 (Type[shapes.Point]): the shapes.Point instance

    Returns:
        Type[shapes.Point]: the intersection between the given point
            and line segment which happens when the point is located on
            the line and will be a point with the same coordinates of 
            the given entity1, otherwise None
    """
    
    return intersection(entity2, entity1)


@overload(shapes.LineSegment, shapes.Polygon)
def intersection(
    entity1: Type[shapes.LineSegment],
    entity2: Type[shapes.Polygon]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given polygon and line
    segment entity

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection points between the
            two given entities inside a tuple
    """
    
    return intersection(entity2, entity1)


@overload(shapes.LineSegment, shapes.Rectangle)
def intersection(
    entity1: Type[shapes.LineSegment],
    entity2: Type[shapes.Rectangle]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between the given rectangle and line segment
    instance

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        Tuple[Type[shapes.Point]]: a tuple of points which to denote
            the intersection between the given entities
    """
    
    return intersection(entity2, entity1)


@overload(shapes.LineSegment, shapes.Circle)
def intersection(
    entity1: Type[shapes.LineSegment],
    entity2: Type[shapes.Circle]
    ) -> Tuple[Type[shapes.Point]]:
    """finds the intersection between a line segment and a circle

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instances

    Returns:
        Tuple[Type[shapes.Point]]: the intersection between the given
            entities
    """
    
    return intersection(entity2, entity1)


@overload(shapes.LineSegment, shapes.Line)
def intersection(
    entity1: Type[shapes.LineSegment],
    entity2: Type[shapes.Line]
    ) -> Type[shapes.Point]:
    """finds the intersection between an infinite line and a finite
    line segment

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        Type[shapes.Point]: the intersection between the given two entities
    """
    
    return intersection(entity2, entity1)


@overload(shapes.LineSegment, shapes.LineSegment)
def intersection(
    entity1: Type[shapes.LineSegment],
    entity2: Type[shapes.LineSegment]
    ) -> Type[shapes.Point]:
    """finds the intersection between two finite line segments

    Args:
        entity1 (Type[shapes.LineSegment]): the first given shapes.LineSegment
            instance
        entity2 (Type[shapes.LineSegment]): the second given shapes.LineSegment
            instance

    Returns:
        Type[shapes.Point]: the intersection between the given entities
    """
    
    inter = intersection(entity1.infinite, entity2.infinite)
    if inter and intersection(inter, entity1) and intersection(inter, entity2):
        return inter


@overload(shapes.Point, shapes.Point)
def is_inside(
    entity1: Type[shapes.Point],
    entity2: Type[shapes.Point]
    ) -> bool:
    """specifies if the first given entity is completely located inside
    of the second given entity

    Args:
        entity1 (Type[shapes.Point]): the firts given shapes.Point
            instance
        entity2 (Type[shapes.Point]): the second given shapes.Point
            instance

    Returns:
        bool: True or False indicating if the first entity is inside
            the second one
    """
    
    return False


@overload(shapes.Point, shapes.Polygon)
def is_inside(entity1, entity2):
    # draw a semi infinite line and see how many points it intersects
    pass


@overload(shapes.Point, shapes.Rectangle)
def is_inside(entity1, entity2):
    pass


@overload(shapes.Point, shapes.Circle)
def is_inside(entity1, entity2):
    pass


@overload(shapes.Point, shapes.Line)
def is_inside(entity1, entity2):
    pass


@overload(shapes.Point, shapes.LineSegment)
def is_inside(entity1, entity2):
    pass


def distance():
    # define it with overload
    pass