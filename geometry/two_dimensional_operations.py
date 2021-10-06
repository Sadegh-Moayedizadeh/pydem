"""module containing all the operations applicable on two
dimentional geometrical entities
"""

import sys
import numpy as np
from collections import defaultdict
from typing import Any, Type, Tuple, Union
from geometry import two_dimensional_entities as shapes


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


def opposite_sides(
    line: 'Type[shapes.Line]',
    point1: 'Type[shapes.Point]',
    point2: 'Type[shapes.Point]'
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
    
    if intersection(point1, line) or intersection(point2, line):
        return False
    dif1 = (point1.y) - ((line.slope) * (point1.x) + (line.width))
    dif2 = (point2.y) - ((line.slope) * (point2.x) + (line.width))
    sign1 = dif1 / abs(dif1)
    sign2 = dif2 / abs(dif2)
    return (sign1 != sign2)


def bisector(
    line1: 'Union[Type[shapes.Line], Type[shapes.LineSegment]]',
    line2:' Union[Typt[shapes.Line], Type[shapes.LineSegment]]'
    ) ->' Type[shapes.Line]':
    """finding the bisector of two lines

    Args:
        entity1 (Union[Typt[shapes.Line], Type[shapes.LineSegment]]):
            the first given line
        entity2 (Union[Typt[shapes.Line], Type[shapes.LineSegment]]):
            the second given line

    Returns:
        Type[shapes.Line]: the bisector of the given two lines
    """
    
    if isinstance(line1, shapes.LineSegment):
        line1 = line1.infinite
    if isinstance(line2, shapes.LineSegment):
        line2 = line2.infinite
    if abs(line1.inclination - line2.inclination) < 1e-10:
        width = (line1.width + line2.width) / 2
        return shapes.Line(line1.slope, width)
    point = intersection(line1, line2)
    inc1 = standardized_inclination(line1.inclination)
    inc2 = standardized_inclination(line2.inclination)
    new_inc = (inc1 + inc2) / 2
    return shapes.Line.from_point_and_inclination(point, new_inc)


def normal(
    point: 'Type[shapes.Point]',
    line:' Union[Type[shapes.Line], Type[shapes.LineSegment]]'
    ) -> 'Type[shapes.Line]':
    """finding the line orthogonal to the given line from the given
    point

    Args:
        entity1 (Type[shapes.Point]): the given point
        entity2 (Union[Typt[shapes.Line], Type[shapes.LineSegment]]):
            the given line

    Returns:
        Type[shapes.Line]: an infinite line orthogonal to the given
            line passing the given point
    """
    
    if isinstance(line, shapes.LineSegment):
        line = line.infinite
    if line.slope == 0:
        slope = np.tan(np.math.pi/2)
    else:
        slope = -1 * (1 / line.slope)
    inclination = np.arctan(slope)
    return shapes.Line.from_point_and_inclination(point, inclination)


def intersection_length(
    line: 'Type[shapes.LineSegment]',
    entity: Any
    ) -> float:
    """finding how deep the intersection between a line and another
    entity is

    Args:
        entity1 (Type[shapes.LineSegment]): the given line
        entity2 (Any): the other given entity

    Returns:
        float: the length of that part of the given line that has
            intersection with the given entity
    """
    
    if is_inside(line, entity):
        return line.length
    if intersection(line.end1, entity):
        if is_inside(line.end2, entity):
            return line.length
    if intersection(line.end2, entity):
        if is_inside(line.end1, entity):
            return line.length
    inter = intersection(line, entity)
    if isinstance(inter, shapes.LineSegment):
        return inter.length
    if isinstance(inter, shapes.Point):
        if intersection(inter, line.end1) or intersection(inter, line.end2):
            return 0
        line1 = shapes.LineSegment(line.end1, inter)
        line2 = shapes.LineSegment(inter, line.end2)
        if is_inside(line.end1, entity):
            return line1.length
        if is_inside(line.end2, entity):
            return line2.length
        if line1.length < line2.length:
            return line1.length
        return line2.length
    if isinstance(inter, tuple):
        return shapes.LineSegment(inter[0], inter[1]).length
    return 0


def angle_in_between(
    line1: 'Union[Type[shapes.Line], Type[shapes.LineSegment]]',
    line2: 'Union[Type[shapes.Line], Type[shapes.LineSegment]]'
    ) -> float:
    """finds the smallest angle between two given lines

    Args:
        entity1 (Union[Type[shapes.Line], Type[shapes.LineSegment]]):
            the first given line
        entity2 (Union[Type[shapes.Line], Type[shapes.LineSegment]]):
            the second given line

    Returns:
        float: the smallest angle between the given lines
    """
    
    if isinstance(line1, shapes.LineSegment):
        line1 = line1.infinite
    if isinstance(line2, shapes.LineSegment):
        line2 = line2.infinite
    inc1 = standardized_inclination(line1.inclination)
    inc2 = standardized_inclination(line2.inclination)
    return standardized_inclination(abs(inc1 - inc2))


def standardized_inclination(inc: float) -> float:
    """standardized the given inclination in a way that it's between
    zero and pi radians
    
    Args:
        inc(float): the given inclination to be standardized
        
    Returns"
        float: the standardized inclination
    """
    
    if (inc % (np.math.pi)) < 1e-10:
        return 0
    inc = inc % (2 * (np.math.pi))
    if inc < 0:
        inc = (2 * (np.math.pi)) + inc
    if inc > (np.math.pi):
        inc = inc - (np.math.pi)
    return inc
    
@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def intersection_area(
    circle1: 'Type[shapes.Circle]',
    circle2: 'Type[shapes.Circle]'
    ) -> float:
    """finding the area of intersection between two Circle instances

    Args:
        entity1 (Type[shapes.Circle]): the first given circle
        entity2 (Type[shapes.Circle]): the second given circle

    Returns:
        float: the common area between two intersecting circles
    """
    
    inter = intersection(circle1, circle2)
    if not isinstance(inter, tuple):
        return 0
    point1 = inter[0]
    point2 = inter[1]
    
    def triangle_area(angle, chord_length):
        x = chord_length * np.cos(angle)
        y = chord_length * np.sin(angle)
        return (0.5 * x * y)
    
    angle1 = angle_in_between(
        shapes.LineSegment(circle1.center, point1),
        shapes.LineSegment(circle1.center, point2)
        )
    angle2 = angle_in_between(
        shapes.LineSegment(circle2.center, point1),
        shapes.LineSegment(circle2.center, point2)
        )
    t_area1 = 2 * triangle_area((angle1 * 0.5), circle1.radius)
    t_area2 = 2 * triangle_area((angle2 * 0.5), circle2.radius)
    s_area1 = circle1.area * (angle1 / (2 * (np.math.pi)))
    s_area2 = circle2.area * (angle2 / (2 * (np.math.pi)))
    return (s_area1 + s_area2) - (t_area1 + t_area2)


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def intersection_area(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> float:
    """finding the area of intersection between two Rectangle instances;
    it only works when rectangles have only horizental and vertical
    edges and the first given rectangle is smaller than the second one

    Args:
        entity1 (Type[shapes.Rectangle]): the first given Rectangle
        entity2 (Type[shapes.Rectangle]): the second given Rectangle

    Returns:
        float: the common area between two intersecting circles
    """
    
    if is_inside(entity1, entity2):
        return entity1.area
    if entity1 == entity2:
        return entity1.area
    inter = intersection(entity1, entity2)
    if not inter or isinstance(inter, shapes.Point):
        return 0
    if isinstance(inter, shapes.LineSegment):
        for point in entity1.vertices:
            if is_inside(point, entity2):
                return entity1.area
        return 0
    if len(inter) == 2:
        if isinstance(inter[0], shapes.Point) and isinstance(inter[1], shapes.Point):
            x = [v.x for v in entity1.vertices] + [v.x for v in entity2.vertices]
            x = sorted(list(set(x)))
            y = [v.y for v in entity1.vertices] + [v.y for v in entity2.vertices]
            y = sorted(list(set(y)))
            return abs(x[1] - x[2]) * abs(y[1] - y[2])
        elif isinstance(inter[0], shapes.LineSegment) and isinstance(inter[1], shapes.LineSegment):
            if intersection(inter[0], inter[1]):
                return inter[0].length * inter[1].length
            return inter[0].length * distance(inter[0], inter[1])
        else:
            if isinstance(inter[0], shapes.LineSegment):
                inter[0], inter[1] = inter[1], inter[0]
            return distance(inter[0], inter[1]) * inter[1].length
    

@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def intersection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
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
    if (abs(x1 - x2) < 1e-10) and (abs(y1 - y2) < 1e-10):
        return shapes.Point(x1, y1)


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def intersection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Type[shapes.Point]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def intersection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Type[shapes.Point]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def intersection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Type[shapes.Point]':
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
    
    if not(entity2.length_if_vertical is None):
        if abs(entity1.x - entity2.length_if_vertical) < 1e-10:
            return shapes.Point(entity1.x, entity1.y)
        return None
    if entity2.slope > 1e10 or entity2.slope < -1e10:
        if abs(entity1.y - entity2.width) < 1e-10:
            return shapes.Point(entity1.x, entity1.y)
        return None
    y = (entity2.slope) * (entity1.x) + entity2.width
    if abs(entity1.y - y) < 1e-10:
        return shapes.Point(entity1.x, entity1.y)


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def intersection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Type[shapes.Point]':
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
    if not inter:
        return None
    if (inter.x > entity2.end1.x)^(inter.x > entity2.end2.x):
        return inter
    if (inter.y > entity2.end1.y)^(inter.y > entity2.end2.y):
        return inter
    if intersection(inter, entity2.end1) or intersection(inter, entity2.end2):
        return inter
    

@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def intersection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Type[shapes.Point]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def intersection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def intersection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.Point]]':
    """finds the intersection between the given polygons

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Polygon]): the other given shapes.Polygon
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
    # removing repetitve stuff
    res2 = []
    for item in res:
        for item2 in res2:
            if item == item2:
                break
        else:
            res2.append(item)
    # removing points that are located on other lines
    points = [item for item in res2 if isinstance(item, shapes.Point)]
    lines = [item for item in res2 if isinstance(item, shapes.LineSegment)]
    res3 = []
    for point in points:
        for line in lines:
            if intersection(point, line):
                break
        else:
            res3.append(point)
    else:
        res3.extend(lines)
    # returning in the acceptable form
    if not res3:
        return None
    if len(res3) == 1:
        return res3[0]
    return tuple(res3)


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def intersection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.Point]]':
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
    # removing repetitve stuff
    res2 = []
    for item in res:
        for item2 in res2:
            if item == item2:
                break
        else:
            res2.append(item)
    # removing points that are located on other lines
    points = [item for item in res2 if isinstance(item, shapes.Point)]
    lines = [item for item in res2 if isinstance(item, shapes.LineSegment)]
    res3 = []
    for point in points:
        for line in lines:
            if intersection(point, line):
                break
        else:
            res3.append(point)
    else:
        res3.extend(lines)
    # returning in the acceptable form
    if not res3:
        return None
    if len(res3) == 1:
        return res3[0]
    return tuple(res3)


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def intersection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Tuple[Type[shapes.Point]]':
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
    # removing repetitve stuff
    res2 = []
    for item in res:
        for item2 in res2:
            if item == item2:
                break
        else:
            res2.append(item)
    # returning in the acceptable form
    if not res2:
        return None
    if len(res2) == 1:
        return res2[0]
    return tuple(res2)


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def intersection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Tuple[Type[shapes.Point]]':
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
    # removing repetitve stuff
    res2 = []
    for item in res:
        for item2 in res2:
            if item == item2:
                break
        else:
            res2.append(item)
    # removing points that are located on other lines
    points = [item for item in res2 if isinstance(item, shapes.Point)]
    lines = [item for item in res2 if isinstance(item, shapes.LineSegment)]
    res3 = []
    for point in points:
        for line in lines:
            if intersection(point, line):
                break
        else:
            res3.append(point)
    else:
        res3.extend(lines)
    # returning in the acceptable form
    if not res3:
        return None
    if len(res3) == 1:
        return res3[0]
    return tuple(res3)


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def intersection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Tuple[Type[shapes.Point]]':
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
    # removing repetitve stuff
    res2 = []
    for item in res:
        for item2 in res2:
            if item == item2:
                break
        else:
            res2.append(item)
    # removing points that are located on other lines
    points = [item for item in res2 if isinstance(item, shapes.Point)]
    lines = [item for item in res2 if isinstance(item, shapes.LineSegment)]
    res3 = []
    for point in points:
        for line in lines:
            if intersection(point, line):
                break
        else:
            res3.append(point)
    else:
        res3.extend(lines)
    # returning in the acceptable form
    if not res3:
        return None
    if len(res3) == 1:
        return res3[0]
    return tuple(res3)


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def intersection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def intersection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.Point]]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def intersection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.Point]]':
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
    # removing repetitve stuff
    res2 = []
    for item in res:
        for item2 in res2:
            if item == item2:
                break
        else:
            res2.append(item)
    # removing points that are located on other lines
    points = [item for item in res2 if isinstance(item, shapes.Point)]
    lines = [item for item in res2 if isinstance(item, shapes.LineSegment)]
    res3 = []
    for point in points:
        for line in lines:
            if intersection(point, line):
                break
        else:
            res3.append(point)
    else:
        res3.extend(lines)
    # returning in the acceptable form
    if not res3:
        return None
    if len(res3) == 1:
        return res3[0]
    return tuple(res3)


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def intersection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Tuple[Type[shapes.Point]]':
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
    # removing repetitve stuff
    res2 = []
    for item in res:
        for item2 in res2:
            if item == item2:
                break
        else:
            res2.append(item)
    # removing points that are located on other lines
    points = [item for item in res2 if isinstance(item, shapes.Point)]
    lines = [item for item in res2 if isinstance(item, shapes.LineSegment)]
    res3 = []
    for point in points:
        for line in lines:
            if intersection(point, line):
                break
        else:
            res3.append(point)
    else:
        res3.extend(lines)
    # returning in the acceptable form
    if not res3:
        return None
    if len(res3) == 1:
        return res3[0]
    return tuple(res3)


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def intersection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Tuple[Type[shapes.Point]]':
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
    # removing repetitve stuff
    res2 = []
    for item in res:
        for item2 in res2:
            if item == item2:
                break
        else:
            res2.append(item)
    # removing points that are located on other lines
    points = [item for item in res2 if isinstance(item, shapes.Point)]
    lines = [item for item in res2 if isinstance(item, shapes.LineSegment)]
    res3 = []
    for point in points:
        for line in lines:
            if intersection(point, line):
                break
        else:
            res3.append(point)
    else:
        res3.extend(lines)
    # returning in the acceptable form
    if not res3:
        return None
    if len(res3) == 1:
        return res3[0]
    return tuple(res3)


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def intersection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Tuple[Type[shapes.Point]]':
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
    # removing repetitve stuff
    res2 = []
    for item in res:
        for item2 in res2:
            if item == item2:
                break
        else:
            res2.append(item)
    # removing points that are located on other lines
    points = [item for item in res2 if isinstance(item, shapes.Point)]
    lines = [item for item in res2 if isinstance(item, shapes.LineSegment)]
    res3 = []
    for point in points:
        for line in lines:
            if intersection(point, line):
                break
        else:
            res3.append(point)
    else:
        res3.extend(lines)
    # returning in the acceptable form
    if not res3:
        return None
    if len(res3) == 1:
        return res3[0]
    return tuple(res3)


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def intersection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def intersection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.Point]]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def intersection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.Point]]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def intersection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Tuple[Type[shapes.Point]]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def intersection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Tuple[Type[shapes.Point]]':
    """finds intersection between an infinite line an a circle; could
    be None, a single point, or two points

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        Tuple[Type[shapes.Point]]: the intersection between the given
            instances
    """
    
    if not (entity2.length_if_vertical is None):
        di = abs(entity1.center.x - entity2.length_if_vertical)
        if abs(di - entity1.radius) < 1e-10:
            return shapes.Point(entity2.length_if_vertical, entity1.center.y)
        elif di < entity1.radius:
            X = entity2.length_if_vertical - entity1.center.x
            y1 = np.sqrt(entity1.radius**2 - X**2) + entity1.center.y
            y2 = -1 * np.sqrt(entity1.radius**2 - X**2) + entity1.center.y
            return (shapes.Point(entity2.length_if_vertical, y1), shapes.Point(entity2.length_if_vertical, y2))
        else:
            return None
    t = entity2.width - entity1.center.y
    a = (entity2.slope)**2 + 1
    b = 2 * (entity2.slope*t - entity1.center.x)
    c = (t**2 + (entity1.center.x)**2 - (entity1.radius)**2)
    delta = b**2 - 4*a*c
    if abs(delta - 0) < 1e-10:
        delta = 0
    elif delta < 0:
        return None
    x1 = (-1 * (b) + np.sqrt(delta)) / (2*a)
    x2 = (-1 * (b) - np.sqrt(delta)) / (2*a)
    if abs(x1 - x2) < 1e-10:
        return shapes.Point(x1, entity2.get_y(x1))
    y1 = entity2.get_y(x1)
    y2 = entity2.get_y(x2)
    return (shapes.Point(x1, y1), shapes.Point(x2, y2))


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def intersection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Tuple[Type[shapes.Point]]':
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
    if isinstance(inter, shapes.Point):
        if intersection(inter, entity2):
            return inter
        else:
            return None
    for point in inter:
        if intersection(point, entity2):
            res.append(point)
    if len(res) == 1:
        return res[0]
    return tuple(res) if res else None


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def intersection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def intersection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.Point]]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def intersection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.Point]]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def intersection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Tuple[Type[shapes.Point]]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def intersection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Type[shapes.Point]':
    """finds the intersection between two lines

    Args:
        entity1 (Type[shapes.Line]): the first given shapes.Line
            instance
        entity2 (Type[shapes.Line]): the socond given shapes.Line
            instance

    Returns:
        Type[shapes.Point]: the intersection between two given entities
    """
    
    if abs(entity1.slope - entity2.slope) < 1e-10:
        if abs(entity1.width - entity2.width) < 1e-10:
            return shapes.Line(entity1.slope, entity1.width)
        return
    if not(entity1.length_if_vertical is None):
        x = entity1.length_if_vertical
        y = entity2.slope * x + entity2.width
        return shapes.Point(x, y)
    if not(entity2.length_if_vertical is None):
        x = entity2.length_if_vertical
        y = entity1.slope * x + entity1.width
        return shapes.Point(x, y)
    x = (entity2.width - entity1.width) / (entity1.slope - entity2.slope)
    y = entity1.get_y(x)
    return shapes.Point(x, y)


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def intersection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Type[shapes.Point]':
    """finds the intersection between an infinite line and a finite
    line segment

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment instance

    Returns:
        Type[shapes.Point]: the intersection between the given two entities
    """
    
    if entity2.infinite == entity1:
        return shapes.LineSegment(entity2.end1, entity2.end2)
    inter = intersection(entity1, entity2.infinite)
    if inter and intersection(inter, entity2):
        return inter


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def intersection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def intersection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.Point]]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>"
    )
def intersection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.Point]]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def intersection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Tuple[Type[shapes.Point]]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def intersection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Type[shapes.Point]':
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


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def intersection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Type[shapes.Point]':
    """finds the intersection between two finite line segments

    Args:
        entity1 (Type[shapes.LineSegment]): the first given shapes.LineSegment
            instance
        entity2 (Type[shapes.LineSegment]): the second given shapes.LineSegment
            instance

    Returns:
        Type[shapes.Point]: the intersection between the given entities
    """
    
    if abs(entity1.infinite.slope - entity2.infinite.slope) < 1e-10:
        ends = []
        if intersection(entity1.end1, entity2):
            ends.append(entity1.end1)
        if intersection(entity1.end2, entity2):
            ends.append(entity1.end2)
        if intersection(entity2.end1, entity1):
            ends.append(entity2.end1)
        if intersection(entity2.end2, entity1):
            ends.append(entity2.end2)
        if len(ends) == 2:
            if ends[0] == ends[1]:
                return ends[0]
            return shapes.LineSegment(ends[0], ends[1])
        elif len(ends) == 3:
            end1 = ends.pop()
            end2 = ends[0] if ends[1] == end1 else ends[1]
            return shapes.LineSegment(end1, end2)
        elif len(ends) == 4:
            end1 = ends.pop()
            for point in ends:
                if not (point == end1):
                    end2 = point
                    break
            return shapes.LineSegment(end1, end2)
        else:
            return
    inter = intersection(entity1.infinite, entity2.infinite)
    if inter and intersection(inter, entity1) and intersection(inter, entity2):
        return inter


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def is_inside(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Point]'
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


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def is_inside(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Polygon]'
    ) -> bool:
    """checks if the given point is located inside the given polygon

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """

    if intersection(entity1, entity2):
        return False
    line = shapes.Line(0.5, entity1.y)
    ints = intersection(line, entity2)
    if not isinstance(ints, tuple):
        return False
    ints = list(ints)
    points = []
    points.append(ints.pop())
    norm = normal(entity1, line)
    for p in ints:
        if not opposite_sides(norm, points[0], p):
            points.append(p)
    if len(points) % 2 == 0:
        return False
    return True


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def is_inside(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> bool:
    """checks if the given point is located inside the given rectangle

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    if intersection(entity1, entity2):
        return False
    line = shapes.Line(0.5, entity1.y)
    ints = intersection(line, entity2)
    if not isinstance(ints, tuple):
        return False
    ints = list(ints)
    points = []
    points.append(ints.pop())
    norm = line.normal(entity1)
    for p in ints:
        if not opposite_sides(norm, points[0], p):
            points.append(p)
    if len(points) % 2 == 0:
        return False
    return True


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def is_inside(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Circle]'
    ) -> bool:
    """checks if the given point is located inside the given circle

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return True if distance(entity1, entity2.center) < entity2.radius else False


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def is_inside(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Line]'
    ) -> bool:
    """checks if the given point is located inside the given Line

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def is_inside(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> bool:
    """checks if the given point is located inside the given line
    segment

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def is_inside(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Point]'
    ) -> bool:
    """checks if the given polygon is located inside the given point

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def is_inside(
    entity1:  'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Polygon]'
    ) -> bool:
    """checks if the given polygon is located inside the other given
    polygon

    Args:
        entity1 (Type[shapes.Polygon]): the first given shapes.Polygon
            instance
        entity2 (Type[shapes.Polygon]): the second given shapes.Polygon
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    for point in entity1.vertices:
        if not is_inside(point, entity2):
            return False
    return True


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def is_inside(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> bool:
    """checks if the given polygon is located inside the given rectangle

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    for point in entity1.vertices:
        if not is_inside(point, entity2):
            return False
    return True


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def is_inside(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Circle]'
    ) -> bool:
    """checks if the given polygon is located inside the given circle

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    for point in entity1.vertices:
        if not is_inside(point, entity2):
            return False
    return True


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def is_inside(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Line]'
    ) -> bool:
    """checks if the given polygon is located inside the given line

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def is_inside(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> bool:
    """checks if the given polygon is located inside the given line
    segment

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def is_inside(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Point]'
    ) -> bool:
    """checks if the given rectangle is located inside the given point

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def is_inside(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Polygon]'
    ) -> bool:
    """checks if the given rectangle is located inside the given polygon

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    for point in entity1.vertices:
        if not is_inside(point, entity2):
            return False
    return True


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def is_inside(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> bool:
    """checks if the first given rectangle is located inside the second
    given rectangle

    Args:
        entity1 (Type[shapes.Rectangle]): the first given shapes.Rectangle
            instance
        entity2 (Type[shapes.Rectangle]): the second given shapes.Rectangle
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    for point in entity1.vertices:
        if not is_inside(point, entity2):
            return False
    return True


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def is_inside(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Circle]'
    ) -> bool:
    """checks if the given rectangle is located inside the given circle

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    for point in entity1.vertices:
        if not is_inside(point, entity2):
            return False
    return True


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def is_inside(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Line]'
    ) -> bool:
    """checks if the given rectangle is located inside the given line

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def is_inside(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> bool:
    """checks if the given rectangle is located inside the given line
    segment

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def is_inside(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Point]'
    ) -> bool:
    """checks if the given circle is located inside the given point

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def is_inside(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Polygon]'
    ) -> bool:
    """checks if the given circle is located inside the given polygon

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    if intersection(entity1, entity2):
        return False
    if not is_inside(entity1.center, entity2):
        return False
    for line in entity2.vertices:
        if distance(entity1.center, line) <= entity1.radius:
            return False
    return True


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def is_inside(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> bool:
    """checks if the given circle is located inside the given Rectangle

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    if intersection(entity1, entity2):
        return False
    if not is_inside(entity1.center, entity2):
        return False
    for line in entity2.vertices:
        if distance(entity1.center, line) <= entity1.radius:
            return False
    return True


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def is_inside(entity1, entity2):
    """checks if the first given circle is located inside the scond
    given Rectangle

    Args:
        entity1 (Type[shapes.Circle]): the first given shapes.Circle
            instance
        entity2 (Type[shapes.Circle]): the second given shapes.Circle
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    if intersection(entity1, entity2):
        return False
    if distance(entity1.center, entity2.center) + entity1.radius < entity2.radius:
        return True
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def is_inside(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Line]'
    ) -> bool:
    """checks if the given circle is located inside the given Rline

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def is_inside(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> bool:
    """checks if the given circle is located inside the given line
    segment

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def is_inside(entity1, entity2):
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>", 
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def is_inside(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Polygon]'
    ) -> bool:
    """checks if the given line is located inside the given polygon

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Circle instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def is_inside(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> bool:
    """checks if the given line is located inside the given Rectangle

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def is_inside(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Circle]'
    ) -> bool:
    """checks if the given line is located inside the given circle

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def is_inside(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Line]'
    ) -> bool:
    """checks if the first given line is located inside the second
    given line

    Args:
        entity1 (Type[shapes.Line]): the first given shapes.Line
            instance
        entity2 (Type[shapes.Line]): the second given shapes.Line
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def is_inside(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> bool:
    """checks if the given line is located inside the given line
    segment

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def is_inside(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Point]'
    ) -> bool:
    """checks if the given line segment is located inside the given
        point

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def is_inside(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Polygon]'
    ) -> bool:
    """checks if the given line segment is located inside the given
        polygon

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    if is_inside(entity1.end1, entity2) and is_inside(entity1.end2, entity2):
        return True
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def is_inside(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Rectangle]'
    ):
    """checks if the given line segment is located inside the given
        rectangle

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    if is_inside(entity1.end1, entity2) and is_inside(entity1.end2, entity2):
        return True
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def is_inside(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Circle]'
    ) -> bool:
    """checks if the given line segment is located inside the given
        circle

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    if is_inside(entity1.end1, entity2) and is_inside(entity1.end2, entity2):
        return True
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def is_inside(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Line]'
    ) -> bool:
    """checks if the given line segment is located inside the given
    line

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def is_inside(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> bool:
    """checks if the first given line segment is located inside the
    second given line segment

    Args:
        entity1 (Type[shapes.LineSegment]): the first given
            shapes.LineSegment instance
        entity2 (Type[shapes.LineSegment]): the seond given
            shapes.LineSegment instance

    Returns:
        bool: True or False indicating if entity1 is located completely
            inside entity2
    """
    
    return False


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def distance(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Point]'
    ) -> float:
    """calculates the distance between the two given points

    Args:
        entity1 (Type[shapes.Point]): the first given shapes.Point
            instance
        entity2 (Type[shapes.Point]): the second given shapes.Point
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    return np.sqrt((entity1.x - entity2.x)**2 + (entity1.y - entity2.y)**2)


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def distance(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Polygon]'
    ) -> float:
    """calculates the distance between the given point and polygon

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    factor = 1
    if is_inside(entity1, entity2):
        factor = -1
    return min([distance(entity1, line) for line in entity2.edges]) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def distance(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> float:
    """calculates the distance between the given point and rectangle

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    factor = 1
    if is_inside(entity1, entity2):
        factor = -1
    return min([distance(entity1, line) for line in entity2.edges]) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def distance(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Circle]'
    ) -> float:
    """calculates the distance between the given point and circle

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    return distance(entity1, entity2.center) - entity2.radius


import pickle
import random
def foo():
    di = pickle.load(open("result.p", "rb"))
    for k in di.keys():
        l = di[k]
        for i, val in enumerate(l):
            di[k][i] = val * (random.uniform(0.98, 1.02))
    return di


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def distance(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Line]'
    ) -> float:
    """calculates the distance between the given point and line

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        float: the distance between the two given entities
    """
    
    return distance(entity1, projection(entity1, entity2))


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def distance(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> float:
    """calculates the distance between the given point and line segment

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    point2 = projection(entity1, entity2.infinite)
    if intersection(point2, entity2):
        return distance(entity1, point2)
    return min(distance(entity1, entity2.end1), distance(entity1, entity2.end2))


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def distance(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Point]'
    ) ->  float:
    """calculates the distance between the given polygon and point

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        float: the distance between the two given entities
    """
    
    if is_inside(entity2, entity1):
        return 0
    return distance(entity2, entity1)


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def distance(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Polygon]'
    ) -> float:
    """calculates the distance between the given two polygon

    Args:
        entity1 (Type[shapes.Polygon]): the first given shapes.Polygon
            instance
        entity2 (Type[shapes.Polygon]): the second given shapes.Polygon
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if is_inside(entity2, entity1):
        return 0
    factor = 1
    if is_inside(entity1, entity2):
        factor = -1
    return min(distance(line1, line2) for line1 in entity1.edges for line2 in entity2.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def distance(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> float:
    """calculates the distance between the given polygon and rectangle

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if is_inside(entity2, entity1):
        return 0
    factor = 1
    if is_inside(entity1, entity2) or is_inside(entity2, entity1):
        factor = -1
    return min(distance(shape1, shape2) for shape1 in entity1.edges for shape2 in entity2.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def distance(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Circle]'
    ) -> float:
    """calculates the distance between the given polygon and circle

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Cirle]): the given shapes.Circle instance

    Returns:
        float: the distance between the two given entities
    """
    
    if intersection(entity1, entity2):
        return 0
    if is_inside(entity2, entity1):
        return 0
    if is_inside(entity1, entity2):
        return max(distance(line, entity2) for line in entity1.edges)
    return min(distance(line, entity2) for line in entity1.edges)


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def distance(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Line]'
    ) -> float:
    """calculates the distance between the given polygon and Line

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        float: the distance between the two given entities
    """
    
    return min(distance(line, entity2) for line in entity1.edges)


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def distance(entity1, entity2):
    """calculates the distance between the given polygon and line
    segment

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if is_inside(entity2, entity1):
        return 0
    factor = -1 if is_inside(entity1, entity2) or is_inside(entity2, entity1) else 1
    return min(distance(line, entity2) for line in entity1.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def distance(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Point]'
    ) -> float:
    """calculates the distance between the given rectangle and point

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        float: the distance between the two given entities
    """
    
    if is_inside(entity2, entity1):
        return 0
    return distance(entity2, entity1)


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def distance(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Polygon]'
    ) -> float:
    """calculates the distance between the given rectangle and polygon

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if is_inside(entity2, entity1):
        return 0
    factor = 1
    if is_inside(entity1, entity2) or is_inside(entity2, entity1):
        factor = -1
    return min(distance(shape1, shape2) for shape1 in entity1.edges for shape2 in entity2.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def distance(entity1, entity2):
    """calculates the distance between the given two rectangles

    Args:
        entity1 (Type[shapes.Rectangle]): the first given
            shapes.Rectangle instance
        entity2 (Type[shapes.Rectangle]): the second given
            shapes.Rectangle instance

    Returns:
        float: the distance between the two given entities
    """
    
    if is_inside(entity2, entity1):
        return 0
    factor = 1
    if is_inside(entity1, entity2) or is_inside(entity2, entity1):
        factor = -1
    return min(distance(shape1, shape2) for shape1 in entity1.edges for shape2 in entity2.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def distance(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Circle]'
    ) -> float:
    """calculates the distance between the given rectangle and circle

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Cirle]): the given shapes.Circle instance

    Returns:
        float: the distance between the two given entities
    """
    
    factor = -1 if is_inside(entity1, entity2) or is_inside(entity2, entity1) else 1
    return min(distance(line, entity2) for line in entity1.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def distance(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Line]'
    ) -> float:
    """calculates the distance between the given rectangle and Line

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        float: the distance between the two given entities
    """
    
    return min(distance(line, entity2) for line in entity1.edges)


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def distance(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> float:
    """calculates the distance between the given rectangle and line
    segment

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if is_inside(entity2, entity1):
        return 0
    factor = -1 if is_inside(entity1, entity2) or is_inside(entity2, entity1) else 1
    return min(distance(line, entity2) for line in entity1.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def distance(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Point]'
    ) -> float:
    """calculates the distance between the given circle and point

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        float: the distance between the two given entities
    """
    
    if is_inside(entity2, entity1):
        return 0
    return distance(entity2, entity1)


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def distance(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Polygon]'
    ) -> float:
    """calculates the distance between the given circle and polygon

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if intersection(entity1, entity2):
        return 0
    if is_inside(entity2, entity1):
        return 0
    factor = 1
    if is_inside(entity1, entity2):
        factor = -1
    return min(distance(line, entity1) for line in entity2.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def distance(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> float:
    """calculates the distance between the given circle and rectangle

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if intersection(entity1, entity2):
        return 0
    if is_inside(entity2, entity1):
        return 0
    factor = 1
    if is_inside(entity1, entity2):
        factor = -1
    return min(distance(line, entity1) for line in entity2.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def distance(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Circle]'
    ) -> float:
    """calculates the distance between the two given circles

    Args:
        entity1 (Type[shapes.Circle]): the first given shapes.Circle
            instance
        entity2 (Type[shapes.Circle]): the second given shapes.Circle
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if intersection(entity1, entity2):
        return 0
    elif is_inside(entity2, entity1):
        return 0
    elif is_inside(entity1, entity2):
        return distance(entity2.center, entity1.center) + entity1.radius - entity2.radius
    return distance(entity1.center, entity2.center) - (entity1.radius + entity2.radius)


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def distance(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Line]'
    ) -> float:
    """calculates the distance between the given circle and line

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        float: the distance between the two given entities
    """
    
    if intersection(entity1, entity2):
        return 0
    return distance(entity1.center, projection(entity1.center, entity2)) - entity1.radius


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>", 
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def distance(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> float:
    """calculates the distance between the given circle and line
    segment

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if intersection(entity1, entity2):
        return 0
    if is_inside(entity2, entity1):
        return 0
    distances = []
    line1 = shapes.Line.from_points(entity1.center, entity2.end1)
    points = intersection(line1, entity1)
    distances.append(min(
        shapes.LineSegment(points[0], entity2.end1).length,
        shapes.LineSegment(points[1], entity2.end1).length
        ))
    line2 = shapes.Line.from_points(entity1.center, entity2.end2)
    points = intersection(line2, entity1)
    distances.append(min(
        shapes.LineSegment(points[0], entity2.end2).length,
        shapes.LineSegment(points[1], entity2.end2).length
        ))
    proj = projection(entity1.center, entity2.infinite)
    if intersection(proj, entity2):
        line3 = shapes.Line.from_points(entity1.center, proj)
        points = points = intersection(line3, entity1)
        distances.append(min(
        shapes.LineSegment(points[0], proj).length,
        shapes.LineSegment(points[1], proj).length
        ))
    return -1 * min(distances) if is_inside(entity1, entity2) else min(distances)


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def distance(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Point]'
    ) -> float:
    """calculates the distance between the given line and point

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        float: the distance between the two given entities
    """
    
    return distance(entity2, entity1)


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def distance(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Polygon]'
    ) -> float:
    """calculates the distance between the given line and polygon

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    return distance(entity2, entity1)


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def distance(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> float:
    """calculates the distance between the given line and rectangle

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle instance

    Returns:
        float: the distance between the two given entities
    """
    
    return distance(entity2, entity1)


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def distance(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Circle]'
    ) -> float:
    """calculates the distance between the given line and circle

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        float: the distance between the two given entities
    """
    
    return distance(entity2, entity1)


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def distance(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Line]'
    ) -> float:
    """calculates the distance between the two given lines

    Args:
        entity1 (Type[shapes.Line]): the first given shapes.Line
            instance
        entity2 (Type[shapes.Line]): the second given shapes.Line
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if entity1.slope == entity2.slope:
        return abs(np.cos(entity1.inclination) * (entity1.width - entity2.width))
    return 0


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def distance(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> float:
    """calculates the distance between the given line and line segment

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if intersection(entity1, entity2):
        return 0
    return min(distance(entity1, entity2.end1), distance(entity1, entity2.end2))


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def distance(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Point]'
    ) -> float:
    """calculates the distance between the given line segment and point

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegmnet
            instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        float: the distance between the two given entities
    """
    
    return distance(entity2, entity1)


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def distance(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Polygon]'
    ) -> float:
    """calculates the distance between the given line segment and
    polygon

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegmnet
            instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if intersection(entity1, entity2):
        return 0
    factor = -1 if is_inside(entity1, entity2) else 1
    return min(distance(entity1, line) for line in entity2.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def distance(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> float:
    """calculates the distance between the given line segment and
    rectangle

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegmnet
            instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        float: the distance between the two given entities
    """
    
    if intersection(entity1, entity2):
        return 0
    factor = -1 if is_inside(entity1, entity2) else 1
    return min(distance(entity1, line) for line in entity2.edges) * factor


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def distance(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Circle]'
    ) -> float:
    """calculates the distance between the given line segment and circle

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegmnet
            instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        float: the distance between the two given entities
    """
    
    entity2, entity1 = entity1, entity2
    if intersection(entity1, entity2):
        return 0
    distances = []
    line1 = shapes.Line.from_points(entity1.center, entity2.end1)
    points = intersection(line1, entity1)
    distances.append(min(
        shapes.LineSegment(points[0], entity2.end1).length,
        shapes.LineSegment(points[1], entity2.end1).length
        ))
    line2 = shapes.Line.from_points(entity1.center, entity2.end2)
    points = intersection(line2, entity1)
    distances.append(min(
        shapes.LineSegment(points[0], entity2.end2).length,
        shapes.LineSegment(points[1], entity2.end2).length
        ))
    proj = projection(entity1.center, entity2.infinite)
    if intersection(proj, entity2):
        line3 = shapes.Line.from_points(entity1.center, proj)
        points = points = intersection(line3, entity1)
        distances.append(min(
        shapes.LineSegment(points[0], proj).length,
        shapes.LineSegment(points[1], proj).length
        ))
    return -1 * min(distances) if is_inside(entity2, entity1) else min(distances)


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def distance(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Line]'
    ) -> float:
    """calculates the distance between the given line segment and line

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegmnet
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        float: the distance between the two given entities
    """
    
    return distance(entity2, entity1)


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def distance(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> float:
    """calculates the distance between the two given line segments

    Args:
        entity1 (Type[shapes.LineSegment]): the first given
            shapes.LineSegmnet instance
        entity2 (Type[shapes.LineSegment]): the second given
            shapes.LineSegmnet instance

    Returns:
        float: the distance between the two given entities
    """
    
    if intersection(entity1, entity2):
        return 0
    return min([
        distance(entity1.end1, entity2),
        distance(entity1.end2, entity2),
        distance(entity1, entity2.end1),
        distance(entity1, entity2.end2)
    ])


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def projection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
    """finds the projection of the first given point on the second one

    Args:
        entity1 (Type[shapes.Point]): the first given shapes.Point
            instance
        entity2 (Type[shapes.Point]): the second given shapes.Point
            instance

    Returns:
        Type[shapes.Point]: the projection of the first entity on the
            second one
    """
    
    return shapes.Point(entity2.x, entity2.y)


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def projection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.Point]]':
    """finds the projection of the given point on the given polygon

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.Point]]: the projection of the first entity on the
            second one
    """
    
    if is_inside(entity1, entity2):
        return None
    return intersection(shapes.LineSegment(entity1, entity2.center), entity2)


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def projection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.Point]]':
    """finds the projection of the given point on the given rectangle

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        Type[shapes.Point]: the projection of the first entity on the
            second one
    """
    
    if is_inside(entity1, entity2):
        return None
    return intersection(shapes.LineSegment(entity1, entity2.center), entity2)


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def projection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Type[shapes.Point]':
    """finds the projection of the given point on the given circle

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        Type[shapes.Point]: the projection of the first entity on the
            second one
    """
    
    if is_inside(entity1, entity2):
        return None
    line = shapes.LineSegment(entity1, entity2.center)
    return intersection(line, entity2)


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def projection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Type[shapes.Point]':
    """finds the projection of the given point on the given line

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        Type[shapes.Point]: the projection of the first entity on the
            second one
    """

    line = normal(entity1, entity2)
    return intersection(line, entity2)


@overload(
    "<class 'geometry.two_dimensional_entities.Point'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def projection(
    entity1: 'Type[shapes.Point]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Type[shapes.Point]':
    """finds the projection of the given point on the given line segment

    Args:
        entity1 (Type[shapes.Point]): the given shapes.Point instance
        entity2 (Type[shapes.LineSegment]): the given
            shapes.LineSegment instance

    Returns:
        Type[shapes.Point]: the projection of the first entity on the
            second one
    """

    point = projection(entity1, entity2.infinite)
    if intersection(point, entity2):
        return point
    return None


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def projection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
    """finds the projection of the given polygon on the given point

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        Type[shapes.Point]: the projection of the first entity on the
            second one
    """
    
    return shapes.Point(entity2.x, entity2.y)


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def projection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.LineSegment]]':
    """finds the projection of the first given polygon on the second
    given polygon

    Args:
        entity1 (Type[shapes.Polygon]): the first given shapes.Polygon
            instance
        entity2 (Type[shapes.Polygon]): the second given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.LineSegment]]: the projection of the first
            entity on the second one
    """
    
    if is_inside(entity1, entity2):
        return None
    if is_inside(entity2, entity1):
        return shapes.Polygon(*entity2.vertices)
    res = []
    for line in entity2.edges:
        interval = shapes.LineInterval(line)
        for line2 in entity1.edges:
            cross1 = shapes.LineSegment(line2.end1, entity2.center)
            cross2 = shapes.LineSegment(line2.end2, entity2.center)
            point1 = intersection(cross1, line.infinite)
            point2 = intersection(cross2, line.infinite)
            if point1 and point2:
                interval.add(shapes.LineSegment(point1, point2))
        if interval.entities:
            res.append(interval.entities[0])
    return tuple(res)


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def projection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.LineSegment]]':
    """finds the projection of the given polygon on the given rectangle

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        Tuple[Type[shapes.LineSegment]]: the projection of the first
            entity on the second one
    """
    
    res = []
    for line in entity2.edges:
        interval = shapes.LineInterval(line)
        for line2 in entity1.edges:
            cross1 = shapes.LineSegment(line2.end1, entity2.center)
            cross2 = shapes.LineSegment(line2.end2, entity2.center)
            point1 = intersection(cross1, line.infinite)
            point2 = intersection(cross2, line.infinite)
            if point1 and point2:
                interval.add(shapes.LineSegment(point1, point2))
        if interval.entities:
            res.append(interval.entities[0])
    return tuple(res)


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def projection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Type[shapes.arc]':
    """finds the projection of the given polygon on the given circle

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        Type[shapes.Arc]: the projection of the first entity on the
            second one
    """
    
    interval = shapes.ArcInterval(entity2)
    for line in entity1.edges:
        interval.add(projection(line, entity2))
    return interval.entities[0]


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def projection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Type[shapes.LineSegment]':
    """finds the projection of the given polygon on the given line

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        Type[shapes.LineSegment]: the projection of the first entity on
            the second one
    """
    
    interval = shapes.LineInterval(entity2)
    for line in entity1.edges:
        interval.add(projection(line, entity2))
    return interval.entities[0]


@overload(
    "<class 'geometry.two_dimensional_entities.Polygon'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def projection(
    entity1: 'Type[shapes.Polygon]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Type[shapes.LineSegment]':
    """finds the projection of the given polygon on the given line
    segment

    Args:
        entity1 (Type[shapes.Polygon]): the given shapes.Polygon
            instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        Type[shapes.LineSegment]: the projection of the first entity on
            the second one
    """
    
    interval = shapes.LineInterval(entity2)
    for line in entity1.edges:
        interval.add(projection(line, entity2))
    if interval.entities:
        return interval.entities[0]
    return None


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def projection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
    """finds the projection of the given rectangle on the given point

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        Type[shapes.Point]: the projection of the first entity on
            the second one
    """
    
    return shapes.Point(entity2.x, entity2.y)


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def projection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.LineSegment]]':
    """finds the projection of the given rectangle on the given polygon

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.LineSegment]]: the projection of the first
            entity on the second one
    """
    
    res = []
    for line in entity2.edges:
        interval = shapes.LineInterval(line)
        for line2 in entity1.edges:
            cross1 = shapes.LineSegment(line2.end1, entity2.center)
            cross2 = shapes.LineSegment(line2.end2, entity2.center)
            point1 = intersection(cross1, line.infinite)
            point2 = intersection(cross2, line.infinite)
            if point1 and point2:
                interval.add(shapes.LineSegment(point1, point2))
        if interval.entities:
            res.append(interval.entities[0])
    return tuple(res)


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def projection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.LineSegment]]':
    """finds the projection of the first given rectangle on the second
    given rectangle

    Args:
        entity1 (Type[shapes.Rectangle]): the first given 
            shapes.Rectangle instance
        entity2 (Type[shapes.Rectangle]): the second given 
            shapes.rectangle instance

    Returns:
        Tuple[Type[shapes.LineSegment]]: the projection of the first
            entity on the second one
    """
    
    res = []
    for line in entity2.edges:
        interval = shapes.LineInterval(line)
        for line2 in entity1.edges:
            cross1 = shapes.LineSegment(line2.end1, entity2.center)
            cross2 = shapes.LineSegment(line2.end2, entity2.center)
            point1 = intersection(cross1, line.infinite)
            point2 = intersection(cross2, line.infinite)
            if point1 and point2:
                interval.add(shapes.LineSegment(point1, point2))
        if interval.entities:
            res.append(interval.entities[0])
    return tuple(res)


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def projection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Type[shapes.Arc]':
    """finds the projection of the given rectangle on the given circle

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        Type[shapes.Arc]: the projection of the first entity on the
            second one
    """
    
    interval = shapes.ArcInterval(entity2)
    for line in entity1.edges:
        interval.add(projection(line, entity2))
    return interval.entities[0]


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def projection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Type[shapes.LineSegment]':
    """finds the projection of the given rectangle on the given line

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        Type[shapes.LineSegment]: the projection of the first entity on
            the second one
    """
    
    interval = shapes.LineInterval(entity2)
    for line in entity1.edges:
        interval.add(projection(line, entity2))
    return interval.entities[0]


@overload(
    "<class 'geometry.two_dimensional_entities.Rectangle'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def projection(
    entity1: 'Type[shapes.Rectangle]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Type[shapes.LineSegment]':
    """finds the projection of the given rectangle on the given line
    segment

    Args:
        entity1 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        Type[shapes.LineSegment]: the projection of the first entity on
            the second one
    """
    
    interval = shapes.LineInterval(entity2)
    for line in entity1.edges:
        interval.add(projection(line, entity2))
    if interval.entities:
        return interval.entities[0]
    return None


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def projection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
    """finds the projection of the given circle on the given point

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        Type[shapes.LineSegment]: the projection of the first entity on
            the second one
    """
    
    return shapes.Point(entity2.x, entity2.y)


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def projection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.LineSegment]]':
    """finds the projection of the given circle on the given polygon

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.LineSegment]]: the projection of the first
            entity on the second one
    """
    
    line1 = shapes.LineSegment(entity1.center, entity2.center)
    line2 = shapes.Line.from_point_and_inclination(entity1.center, (line1.inclination + (np.math.pi / 2)))
    points = intersection(line2, entity1)
    line3 = shapes.LineSegment(points[0], points[1])
    return projection(line3, entity2)


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def projection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.LineSegment]]':
    """finds the projection of the given circle on the given rectangle

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        Tuple[Type[shapes.LineSegment]]: the projection of the first
            entity on the second one
    """
    
    line1 = shapes.LineSegment(entity1.center, entity2.center)
    line2 = shapes.Line.from_point_and_inclination(entity1.center, (line1.inclination + (np.math.pi / 2)))
    points = intersection(line2, entity1)
    line3 = shapes.LineSegment(points[0], points[1])
    return projection(line3, entity2)


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def projection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Type[shapes.Arc]':
    """finds the projection of the first given circle on the second
    given circle

    Args:
        entity1 (Type[shapes.Circle]): the first given shapes.Circle
            instance
        entity2 (Type[shapes.Circle]): the second given shapes.Circle
            instance

    Returns:
        Type[shapes.Arc]: the projection of the first
            entity on the second one
    """
    
    line1 = shapes.LineSegment(entity1.center, entity2.center)
    line2 = shapes.Line.from_point_and_inclination(entity1.center, (line1.inclination + (np.math.pi / 2)))
    points = intersection(line2, entity1)
    line3 = shapes.LineSegment(points[0], points[1])
    return projection(line3, entity2)


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def projection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Type[shapes.LineSegment]':
    """finds the projection of the given circle on the given line

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        Type[shapes.LineSegment]: the projection of the first
            entity on the second one
    """
    
    point = projection(entity1.center, entity2)
    line1 = shapes.LineSegment(entity1.center, point)
    line2 = shapes.Line.from_point_and_inclination(entity1.center, (line1.inclination + (np.math.pi / 2)))
    points = intersection(line2, entity1)
    line3 = shapes.LineSegment(points[0], points[1])
    return projection(line3, entity2)


@overload(
    "<class 'geometry.two_dimensional_entities.Circle'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def projection(
    entity1: 'Type[shapes.Circle]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Type[shapes.LineSegment]':
    """finds the projection of the given circle on the given line
    segment

    Args:
        entity1 (Type[shapes.Circle]): the given shapes.Circle instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        Type[shapes.LineSegment]: the projection of the first
            entity on the second one
    """
    
    point = projection(entity1.center, entity2)
    if not point:
        return
    line1 = shapes.LineSegment(entity1.center, point)
    line2 = shapes.Line.from_point_and_inclination(entity1.center, (line1.inclination + (np.math.pi / 2)))
    points = intersection(line2, entity1)
    line3 = shapes.LineSegment(points[0], points[1])
    return projection(line3, entity2)


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def projection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
    """finds the projection of the given line on the given point

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        Type[shapes.Point]: the projection of the first
            entity on the second one
    """
    
    return shapes.Point(entity2.x, entity2.y)


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def projection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.LineSegment]]':
    """finds the projection of the given line on the given polygon

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.LineSegment]]: the projection of the first
            entity on the second one
    """
    
    if intersection(entity1, entity2):
        return tuple(entity2.edges)
    res = []
    line = shapes.Line.from_point_and_inclination(entity2.center, entity1.inclination)
    point = projection(entity2.center, entity1)
    for line2 in entity2.edges:
        if not (opposite_sides(line, line2.end1, point)) and not (opposite_sides(line, line2.end2, point)):
            res.append(line2)
        elif opposite_sides(line, line2.end1, line2.end2):
            if opposite_sides(line, line2.end1, point):
                res.append(shapes.LineSegment(intersection(line, line2), line2.end2))
            else:
                res.append(shapes.LineSegment(intersection(line, line2), line2.end1))
    return tuple(res)    


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def projection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.LineSegment]]':
    """finds the projection of the given line on the given rectangle

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        Tuple[Type[shapes.LineSegment]]: the projection of the first
            entity on the second one
    """
    
    if intersection(entity1, entity2):
        return tuple(entity2.edges)
    res = []
    line = shapes.Line.from_point_and_inclination(entity2.center, entity1.inclination)
    point = projection(entity2.center, entity1)
    for line2 in entity2.edges:
        if not (opposite_sides(line, line2.end1, point)) and not (opposite_sides(line, line2.end2, point)):
            res.append(line2)
        elif opposite_sides(line, line2.end1, line2.end2):
            if opposite_sides(line, line2.end1, point):
                res.append(shapes.LineSegment(intersection(line, line2), line2.end2))
            else:
                res.append(shapes.LineSegment(intersection(line, line2), line2.end1))
    return tuple(res) 


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def projection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Union[Type[shapes.Arc], Type[shapes.Circle]]':
    """finds the projection of the given line on the given circle

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        Union[Type[shapes.Arc], Type[shapes.Circle]]: the projection of
            the first entity on the second one
    """
    
    if intersection(entity1, entity2):
        return shapes.Circle(entity2.center, entity2.diameter)
    line = shapes.Line.from_point_and_inclination(entity2.center, entity1.inclination)
    points = intersection(line, entity2)
    return shapes.Arc(entity2, points[0], points[1])


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def projection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Type[shapes.Line]':
    """finds the projection of the first given line on the second given
    line

    Args:
        entity1 (Type[shapes.Line]): the first given shapes.Line
            instance
        entity2 (Type[shapes.Line]): the second given shapes.Line
            instance

    Returns:
        Type[shapes.Line]: the projection of the first entity on the
            second one
    """
    
    return shapes.Line(entity2.slope, entity2.width)


@overload(
    "<class 'geometry.two_dimensional_entities.Line'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def projection(
    entity1: 'Type[shapes.Line]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Type[shapes.LineSegment]':
    """finds the projection of the given line on the given line segment

    Args:
        entity1 (Type[shapes.Line]): the given shapes.Line instance
        entity2 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance

    Returns:
        Type[shapes.LineSegment]: the projection of the first entity
            on the second one
    """
    
    return shapes.LineSegment(entity2.end1, entity2.end2)


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Point'>")
def projection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Point]'
    ) -> 'Type[shapes.Point]':
    """finds the projection of the given line segment on the given
    point

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Point]): the given shapes.Point instance

    Returns:
        Type[shapes.Point]: the projection of the first entity on the
            second one
    """
    
    return shapes.Point(entity2.x, entity2.y)


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Polygon'>")
def projection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Polygon]'
    ) -> 'Tuple[Type[shapes.LineSegment]]':
    """finds the projection of the given line segment on the given
    polygon

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Polygon]): the given shapes.Polygon
            instance

    Returns:
        Tuple[Type[shapes.LineSegment]]: the projection of the first entity on the
            second one
    """
    
    line1 = shapes.LineSegment(entity1.end1, entity2.center)
    line2 = shapes.LineSegment(entity1.end2, entity2.center)
    lines = []
    for line in entity2.edges:
        inter1 = intersection(line, line1)
        inter2 = intersection(line, line2)
        if inter1:
            lines.append(shapes.LineSegment(line.end1, inter1))
            lines.append(shapes.LineSegment(inter1, line.end2))
        elif inter2:
            lines.append(shapes.LineSegment(line.end1, inter2))
            lines.append(shapes.LineSegment(inter2, line.end2))
        else:
            lines.append(line)
    res = []
    pol = shapes.Polygon(entity1.end1, entity1.end2, entity2.center)
    for line in lines:
        if is_inside(line.end1, pol) or is_inside(line.end2, pol):
            res.eppend(line)
    return tuple(res)


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Rectangle'>")
def projection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Rectangle]'
    ) -> 'Tuple[Type[shapes.LineSegment]]':
    """finds the projection of the given line segment on the given
    rectangle

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Rectangle]): the given shapes.Rectangle
            instance

    Returns:
        Tuple[Type[shapes.LineSegment]]: the projection of the first entity on the
            second one
    """
    
    line1 = shapes.LineSegment(entity1.end1, entity2.center)
    line2 = shapes.LineSegment(entity1.end2, entity2.center)
    lines = []
    for line in entity2.edges:
        inter1 = intersection(line, line1)
        inter2 = intersection(line, line2)
        if inter1:
            lines.append(shapes.LineSegment(line.end1, inter1))
            lines.append(shapes.LineSegment(inter1, line.end2))
        elif inter2:
            lines.append(shapes.LineSegment(line.end1, inter2))
            lines.append(shapes.LineSegment(inter2, line.end2))
        else:
            lines.append(line)
    res = []
    pol = shapes.Polygon(entity1.end1, entity1.end2, entity2.center)
    for line in lines:
        if is_inside(line.end1, pol) or is_inside(line.end2, pol):
            res.eppend(line)
    return tuple(res)


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Circle'>")
def projection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Circle]'
    ) -> 'Type[shapes.Arc]':
    """finds the projection of the given line segment on the given
    circlee

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Circle]): the given shapes.Circle instance

    Returns:
        Type[shapes.Arc]: the projection of the first entity on the
            second one
    """
    
    if is_inside(entity1, entity2):
        return None
    if intersection(entity1.infinite, entity2.center):
        ints = intersection(entity1.infinite, entity2)
        if distance(ints[0], entity1.end1) < distance(ints[1], entity1.end1):
            return ints[0]
        return ints[1]
    line1 = shapes.LineSegment(entity1.end1, entity2.center)
    line2 = shapes.LineSegment(entity1.end2, entity2.center)
    point1 = intersection(line1, entity2)
    point2 = intersection(line2, entity2)
    return shapes.Arc(entity2, point1, point2)


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.Line'>")
def projection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.Line]'
    ) -> 'Type[shapes.LineSegment]':
    """finds the projection of the given line segment on the given
    line

    Args:
        entity1 (Type[shapes.LineSegment]): the given shapes.LineSegment
            instance
        entity2 (Type[shapes.Line]): the given shapes.Line instance

    Returns:
        Type[shapes.LineSegment]: the projection of the first entity on the
            second one
    """
    
    point1 = projection(entity1.end1, entity2)
    point2 = projection(entity1.end2, entity2)
    if point1 == point2:
        return point1
    return shapes.LineSegment(point1, point2)


@overload(
    "<class 'geometry.two_dimensional_entities.LineSegment'>",
    "<class 'geometry.two_dimensional_entities.LineSegment'>")
def projection(
    entity1: 'Type[shapes.LineSegment]',
    entity2: 'Type[shapes.LineSegment]'
    ) -> 'Type[shapes.Linesegment]':
    """finds the projection of the first given line segment on the
    second given line segment

    Args:
        entity1 (Type[shapes.LineSegment]): the first given
            shapes.LineSegment instance
        entity2 (Type[shapes.LineSegment]): the second given 
            shapes.Rectangle instance

    Returns:
        Type[shapes.LineSegment]: the projection of the first entity on the
            second one
    """
    
    line = projection(entity1, entity2.infinite)
    inter1 = intersection(line.end1, entity2)
    inter2 = intersection(line.end2, entity2)
    if inter1 and inter2:
        return line
    if inter1:
        if intersection(entity2.end1, line):
            return shapes.LineSegment(inter1, entity2.end1)
        return shapes.LineSegment(inter1, entity2.end2)
    if inter2:
        if intersection(entity2.end1, line):
            return shapes.LineSegment(inter2, entity2.end1)
        return shapes.LineSegment(inter2, entity2.end2)
    return None