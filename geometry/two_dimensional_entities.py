"""Contains all the classes to construct 2D entities used in the model
"""

from typing import Tuple, Any, Optional
import numpy as np
from itertools import count
from pydem.geometry.exceptions import BadEntries
from collections import defaultdict
from pydem.geometry.two_dimensional_operations import (
    is_crossed,
    is_perpendecular,
    distance,
)


class Point(object):
    """Construct two dimentional points given the 'x' and 'y'
    coordinates

    Parents:
        object: base class for all objects in Python

    methods:
        from_rtheta: creates the point from the given 'r' and 'theta'
            coordinates
        get_rtheta: returns the 'r-theta' coordinates of the point in a
            tuple
        move: moves the point with the given changes in its coordinates
    """

    def __init__(self, x: float, y: float) -> None:
        """Initialize the Point object

        Args:
            x (float): x coordinate of the point
            y (float): y coordinate of the point
        """

        self.x = x
        self.y = y

    @classmethod
    def from_rtheta(cls, r: float, theta: float) -> "Point":
        """Alternative constructor for the Point object given the
        'r-theta' coordinates

        Args:
            r (float): 'r' coordinate of the point
            theta (float): 'theta' coordinate of the point

        Returns:
            Point: the Point object
        """

        x = (r) * (np.cos(theta))
        y = (r) * (np.sin(theta))
        return cls(x, y)

    @property
    def get_rtheta(self) -> Tuple(float, float):
        """Gives the 'r-theta' coordinates of the Point object in a
        tuple

        Returns:
            coordinates (Tuple(float, float)): a tuple containing the
                'r' and 'theta' coordinates of the Point object
        """

        r = np.sqrt((self.x) ** 2 + (self.y) ** 2)
        theta = np.atan((self.y) / (self.x))
        coordinates = (r, theta)
        return coordinates

    def move(self, delta_x: float, delta_y: float) -> None:
        """moving the Point instance with the given changes in its
        coordinates

        Args:
            delta_x (float): the change in the 'x' coordinate of the
                Point instance
            delta_y (float): the change in the 'y' coordinate of the
                Point instance
        """

        self.x += delta_x
        self.y += delta_y

    def __eq__(self, other: Any) -> bool:
        """Defining the equality condition

        Args:
            other (Any): the instance to be compared with the current
                Point object

        Returns:
            True or False indicating the equality condition between two
            instances
        """

        if isinstance(other, Point) and self.x == other.x and self.y == other.y:
            return True
        return False


class Polygon(object):
    """Constructing polygons given a series of Point objects

    Parents:
        object: base class to create python objects

    Methods:
        as_regular: creates a regular polygon due to the given centre
            and radius of the circumcircle and the number of vertices
        number_of_vertices: returns the number of vertices of the
            Polygon instance
        edges: returns a tuple containing all the edges of the Polygon
            instance as LineSegment instances
        perimeter: returns the perimeter of the Polygon instance
        move: moves the Polygon instance with the given changes in the
            coordinates of its vertices
    """

    def __init__(self, *vertices: Point) -> None:
        """Initializing the Polygin object with the given series of
        Point objects

        Args:
            *vertices (Point): series of Point objects which are the
                vertices of the polygon, the order of points given is
                important and will stay the same for this object

        Raises:
            BadEntries: in three scenarios:
                when the number of the given vertices is less than three,
                    which makes it impossible to form a polygon
                when the given vertices are given in a way that the edges
                    intersect with one another
                when repetitive vertices where given
        """

        self.vertices = vertices
        if self.number_of_vertices < 3:
            raise BadEntries(
                "the number of given points should be equal or more than three"
            )
        dd = defaultdict(int)
        for vertex in vertices:
            dd[(vertex.x, vertex.y)] += 1
            if dd[(vertex.x, vertex.y)] == 2:
                raise BadEntries("the same vertex entered twice")
        for edge1 in self.edges:
            for edge2 in self.edges:
                if edge1 != edge2 and is_crossed(edge1, edge2):
                    raise BadEntries(
                        "the given vertices form a polygon with intersecting edges"
                    )

    @classmethod
    def as_regular(
        cls, centre: Point, diameter: float, number_of_vertices: int
    ) -> "Polygon":
        """Alternative constructor of Polygon instances which are
        regular, which means they can be circumscribed by a circle and
        have edges with the same length; the first vertex will be
        loaceted at the horizental diameter of the circumcircle

        Args:
            centre (Point): a Point object which is the centre of the
                circumcircle of the polygons
            diamete (float): the diameter of the circumcircle of the
                polygon
            number_of_vertices (int): the number of the vertices of the
                polygon
        """

        circumcircle = Circle(centre, diameter)
        n = number_of_vertices
        points = [
            circumcircle.get_point_on_perimeter(angle)
            for angle in count(0, 2 * np.pi, 2 * np.pi / n)
        ]
        return cls(*points)

    @property
    def number_of_vertices(self) -> int:
        """calculate the number of vertices in polygon

        Returns:
            the number of vertices of the polygon object
        """

        return len(self.vertices)

    @property
    def edges(self) -> Tuple(LineSegment):
        """Create a tuple of edges of the Polygon as LineSegment
        objects"""

        n = self.number_of_vertices
        lst = []
        for i in range(n):
            p1 = self.vertices[i - 1]
            p2 = self.vertices[i]
            edge = LineSegment(p1, p2)
            lst.append(edge)
        return tuple(lst)

    @property
    def perimeter(self) -> float:
        """Calculates the perimeter of the Polygon object"""

        return sum(edge.length for edge in self.edges)

    def move(self, delta_x: float, delta_y: float) -> None:
        """moving the Polygon instance with the given changes in its
        coordinates

        Args:
            delta_x (float): the change in the 'x' coordinate of the
                Polygon instance
            delta_y (float): the change in the 'y' coordinate of the
                Polygon instance
        """

        for vertex in self.vertices:
            vertex.move(delta_x, delta_y)

    def __eq__(self, other: Any) -> bool:
        """Defining the equality condition

        Args:
            other (Any): the instance to be compared with the current
                Polygon object

        Returns:
            True or False indicating the equality condition between two
            instances
        """

        if isinstance(other, Point) and set(self.vertices) == set(other.verteices):
            return True
        return False


class Rectangle(Polygon):
    """Constructing a Rectangle instance

    Parents:
        Polygon: the base class for rectangle, since every rectangle is
            also a polygon

    Methods:
        from_midline: alternative constructor of the class to create a
            rectangle instance out of a midline and a tolerance
        from_diagonal: alternative constructor of the class to create a
            Rectangle instance out of the given diagonals
        area: calculates the area of the Rectangle instance
        midlines: finds the two midlines of the Rectangle instance as a
            tuple with the longer one at the index zero
        diagonals: finds the diagonals of the Rectangle instance
        centre: finds the centre of the Rectangle instance
        circumcircle: finds the circumcircle of the Rectangle instance
    """

    def __init__(self, *vertices: Point) -> None:
        """Initialize the Rectangle object

        Args:
            *vertices (Point): the vertices of the Rectangle

        Raises:
            BadEntries: raises this exception in two scenarios:
                when the number of the given vertices is not equal to
                    four
                when the given vertices are in a way that the resultant
                    polygon doesn't have perpendecular edges
        """

        super().__init__(*vertices)
        edges = self.edges
        n = self.number_of_vertices
        if n != 4:
            raise BadEntries("you should enter exactly four vertices")
        for i in range(n):
            if not is_perpendecular(edges[i], edges[i - 1]):
                raise BadEntries(
                    "the given vertices do not form a rectangle with perpendecular edges"
                )

    @classmethod
    def from_midline(cls, midline: LineSegment, tolerance: float) -> "Rectangle":
        """An alternative constructor to create a Rectangle instance
        from a given midline and a tolerance from that line

        Args:
            midline (LineSegment): the midline upon which the Rectangle
                instance will be created
            tolerance (float): the distance of each edge parallel to
                the midline from that midline

        Returns:
            the Rectangle instance created upon the given arguments
        """

        angle = midline.inclination
        vertex1 = Point(
            midline.end1.x + 2 * np.cos(np.pi / 2 - angle),
            midline.end1.y - 2 * np.sin(np.pi / 2 - angle),
        )
        vertex2 = Point(
            midline.end1.x - 2 * np.cos(np.pi / 2 - angle),
            midline.end1.y + 2 * np.sin(np.pi / 2 - angle),
        )
        vertex3 = Point(
            midline.end2.x - 2 * np.cos(np.pi / 2 - angle),
            midline.end2.y + 2 * np.sin(np.pi / 2 - angle),
        )
        vertex4 = Point(
            midline.end2.x + 2 * np.cos(np.pi / 2 - angle),
            midline.end2.y - 2 * np.sin(np.pi / 2 - angle),
        )
        return cls(vertex1, vertex2, vertex3, vertex4)

    @classmethod
    def from_diagonal(cls, diagonal: LineSegment) -> "Rectangle":
        """Alternative constructor to create a horizental rectangle
        from a given diagonal

        Args:
            diagonal (LineSegment): the diagonal of the horizental
                rectangle to build

        Returns:
            a Rectangle instance
        """

        vertex1 = Point(diagonal.end1.x, diagonal.end1.y)
        vertex2 = Point(diagonal.end1.x, diagonal.end2.y)
        vertex3 = Point(diagonal.end2.x, diagonal.end2.y)
        vertex4 = Point(diagonal.end2.x, diagonal.end1.y)
        return cls(vertex1, vertex2, vertex3, vertex4)

    @property
    def area(self) -> float:
        """Calculate the area of the Rectangle instance

        Returns:
            the area of the Rectangle instance
        """

        return self.edges[0].length * self.edges[1].length

    @property
    def midlines(self) -> Tuple(LineSegment):
        """calculate the two midlines of the Rectangle instance

        Returns:
            a two tuple containin the midlines of the Rectangle
            instance as LineSegment objects with the longer one being
            the first element
        """
        end1 = self.edges[0].midpoint
        end2 = self.edges[2].midpoint
        line1 = LineSegment(end1, end2)
        end3 = self.edges[1].midpoint
        end4 = self.edges[3].midpoint
        line2 = LineSegment(end3, end4)
        lines = sorted([line1, line2], key=lambda x: x.length, reverse=True)
        return tuple(lines)

    @property
    def diagonals(self) -> Tuple(LineSegment):
        """calculating the diagonals of the Rectangle instance

        Returns:
            a two tuple containing the diagonals of the Rectangle
            instance as LineSegment objects
        """

        end1 = self.vertices[0]
        end2 = self.vertices[2]
        line1 = LineSegment(end1, end2)
        end3 = self.vertices[1]
        end4 = self.vertices[3]
        line2 = LineSegment(end3, end4)
        lines = (line1, line2)
        return lines

    @property
    def centre(self) -> Point:
        """calculating the centre of the Rectangle instance

        Returns:
            the centre of the Rectangle instance as a Point object
        """

        return self.diagonals[0].midpoint

    @property
    def circumcircle(self) -> Circle:
        """calculating the circumcircle of the Rectangle instance

        Returns:
            the circumcircle of the Rectangle instance as a Circle
            object
        """

        return Circle(centre=self.centre, diameter=self.diagonals[0].length)


class Circle(object):
    """Constructing a Circle object

    Parents:
        object: base class for any object in python

    Methods:
        area: calculates the area of the Circle instance
        perimeter: calculates the area of the Circle instance
        get_point_on_perimeter: find the Point on the Circle instance's
            perimeter at a location that forms the given angle with its
            horizental diameter
        navigator: returns a generator that yields a point on the
            perimeter of the Circle instance with the given step in
            radian
        move: moves the Circle instance with the given changes in the
            coordinates of its centre
    """

    def __init__(self, centre: Point, diameter: float) -> None:
        """Initialize the Circle object

        Args:
            centre (Point): the centre of the circle
            diameter (float): the diameter of the circle

        Raises:
            BadEntries: when the given diameter is zero or a negative
                number
        """

        self.centre = centre
        self.diameter = diameter
        if self.diameter <= 0:
            raise BadEntries("the given diameter should be a positive non-zero number")

    @property
    def area(self) -> float:
        """calculate the area of the Circle instance

        Returns:
            the area of the Circle instance
        """

        return ((np.pi) * (self.diameter) ** 2) / 4

    @property
    def perimeter(self) -> float:
        """calculate the perimeter of the Circle instance

        Returns:
            the perimeter of the Circle instance
        """

        return (np.pi) * (self.diameter)

    def get_point_on_perimeter(self, angle: float) -> Point:
        """calculating the point on the perimeter of the Circle
        instance with the given angle

        Returns:
            the point on the perimeter of the Circle instance with the
            given angle in radian
        """

        r = (self.diameter) / 2
        x0, y0 = self.centre.x, self.centre.y
        x = x0 + (r) * (np.cos(angle))
        y = y0 + (r) * (np.sin(angle))
        return Point(x, y)

    def navigator(self, start: float, step: float, rounds: int) -> Point:
        """a generator that generates Point objects located on the
        Circle instance with the given starting angle, step to take to
        reach to the next point as an angle, and number of rounds to
        navigate around the Circle before the iterator terminates

        Args:
            start (float): the angle to start navigating from
            step (float): the  angle between each Point objects generated
                on the Circle perimeter
            rounds (int): the number of rounds to navigate around the
                Circle before this generator terminates

        Raises:
            BadEntries: when the given step is zero which makes it
                imposible to navigate on the Cirlces' perimeter

        Yields:
            Point objects located on the perimeter of the Circle instance
        """

        if step == 0:
            raise BadEntries("the given step should not be zero")
        r = 0
        location = (start) % (2 * np.pi)
        while r < rounds:
            yield self.get_point_on_perimeter(location)
            location += step
            r = abs((location) // (2 * np.pi))

    def move(self, delta_x: float, delta_y: float) -> None:
        """moving the Circle instance with the given changes in its
        coordinates

        Args:
            delta_x (float): the change in the 'x' coordinate of the
                Circle instance
            delta_y (float): the change in the 'y' coordinate of the
                Circle instance
        """

        self.centre.move(delta_x, delta_y)

    def __eq__(self, other: Any) -> bool:
        """Defining the equality condition of the Circle instance

        Args:
            other (Any): the other object to be compared with the
                current Circle object

        Retruns:
            True or False indicating the equality condition between two
                objects
        """

        if (
            isinstance(other, Circle)
            and self.centre == other.centre
            and self.diameter == other.diameter
        ):
            return True
        return False


class Line(object):
    """Constructing a Line object with an infinit length

    Parents:
        object: the base class to create python objects

    Methods:
        from_points: alternative constructor of the Line class that
            creates a Line instance given two points on the Line
        from_point_and_inclination: alternative constructor of the Line
            Line class that creates a Line instance given a point on the
            Line and an inclination
        from_ij: alternative constructor of the Line class that creates
            a Line instance given the 'i' and 'j' components of an
            array upon which to build the Line instance
        inclination: calculates the inclination of the Line instance in
            radian
        get_x: calculates the 'x' coordinate of a point on the Line
            instance given its 'y' coordinate
        get_y: calculates the 'y' coordinate of a point on the Line
            instance given its 'x' coordinate
        navigator: creates a generator that yields a point on the Line
            instance at every step
        move: moves the Line instance with the given changes in its 'x'
            and 'y' coordinates
    """

    def __init__(self, slope: float, width: float) -> None:
        """initializing the Line object

        Args:
            slope (float): slope of the line (the tangent of its
                inclination)
            width (float): width of the line from the origin of
                coordination system
        """

        self.slope = slope
        self.width = width

    @classmethod
    def from_points(cls, point1: Point, point2: Point) -> "Line":
        """Alternative constructor to create a Line instance given two
        Point objects located on the line

        Args:
            point1 (Point): the frist point located on the line
            point2 (Point): the second point located on the line
        """

        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        try:
            slope = (y2 - y1) / (x2 - x1)
        except ZeroDivisionError:
            slope = np.tan(np.pi / 2)
        width = y1 - slope * x1
        return cls(slope, width)

    @classmethod
    def from_point_and_inclination(cls, point: Point, inclination: float) -> "Line":
        """Alternative constructor to create a Line instance given a
        single point on the line and an inclination angle

        Args:
            point (Point): a single point on the line
            inclination (float): the inclination of the line in radian
        """

        slope = np.tan(inclination)
        width = point.y - slope * point.x
        return cls(slope, width)

    @classmethod
    def from_ij(cls, i: float, j: float) -> "Line":
        """Alternative constructor to create a Line instance given the
        'i' and 'j' components of the equvalent vector

        Args:
            i (float): the 'i' component of the  equivalent vector
            j (float): the 'j' component of the  equivalent vector
        """

        try:
            slope = j / i
        except ZeroDivisionError:
            slope = np.tan(np.pi / 2)
        width = 0
        return cls(slope, width)

    @property
    def inclination(self) -> float:
        """calculating the inclination of the Line instance

        Returns:
            the inclination of the Line instance in radians
        """

        return np.arctan(self.slope)

    def get_x(self, y: float) -> float:
        """calculate the 'x' coordinate of a point on the Line instance
        given the 'y' coordinate

        Args:
            y (float): the y coordinate of of the point on the Line

        Returns:
            the x coordinate of the point on the Line instance
        """

        try:
            res = (y - self.witdth) / (self.slope)
        except ZeroDivisionError:
            raise BadEntries(
                "the line instance has the slope of zero, asking for an 'x' coordinate is invalid in this case"
            )
        return res

    def get_y(self, x: float) -> float:
        """calculate the 'y' coordinate of a point on the Line instance
        given the 'x' coordinate

        Args:
            x (float): the x coordinate of of the point on the Line

        Returns:
            the y coordinate of the point on the Line instance
        """

        return (self.slope) * x + (self.width)

    def navigator(self, start: Point, end: Point, step: float) -> Point:
        """a generator that generates Point objects located on the Line
        instance with the given start and end point and the step as the
        distance to transfer to reach the next point

        Args:
            start (Point): the point to start navigating from
            end (Point): the point at which the navigation ends
            step (float): the distance between each point returned from
                this generator

        Raises:
            BadEntries: when the given step is zero which makes it
                impossible to navigate on the line

        Yields:
            Point objects located on the Line instance
        """

        if step == 0:
            raise BadEntries("the given step should be a non-zero value")
        if not is_on_perimeter(start, self) or not is_on_perimeter(end, self):
            raise BadEntries(
                "the given start and end points should be loacated on the Line instance"
            )
        dist = 0
        limit = distance(start, end)
        point = start
        delta_x = np.cos(self.inclination) * (step)
        delta_y = np.sin(self.inclination) * (step)
        while dist < limit:
            yield point
            point.move(delta_x, delta_y)
            dist = distance(point, start)

    def move(self, delta_x: float, delta_y: float) -> None:
        """moving the Line instance with the given changes in its
        coordinates

        Args:
            delta_x (float): the change in the 'x' coordinate of the
                Line instance
            delta_y (float): the change in the 'y' coordinate of the
                Line instance
        """

        self.width += delta_y
        self.width += (-1) * (delta_x) * (self.inclination)

    def __eq__(self, other: Any) -> bool:
        """Defining the equality condition of the Line instance

        Args:
            other (Any): the other object to be compared with the
                current Line object

        Retruns:
            True or False indicating the equality condition between two
                objects
        """

        if (
            isinstance(other, Line)
            and self.slope == other.slope
            and self.width == other.width
        ):
            return True
        return False


class LineSegment(object):
    """Constructing the  LineSegment object

    Parents:
        object: the base class for all python objects

    Methods:
        from_point_and_inclination: alternative constructor of the
            LineSegment class that creates a LineSegment instance from
            a point, an inclination and a length
        length: calculates the length of the LineSegment instance
        circumcircle: calculates the circumcircle of the LineSegment
            instance
        inclination: calculates inclination of the LineSegment instance
            in radian
        slope: calaculate the slope of the LineSegment instance
        infinite: returns a Line object which witholds the LineSegment
            instance
        get_x: calculates the 'x' coordinate of a point on the LineSegment
            instance given its 'y' coordinate
        get_y: calculates the 'y' coordinate of a point on the LineSegment
            instance given its 'x' coordinate
        midpoint: finds a point located on the LineSegment instance
            with a distance from its first end with the given ratio
        navigator: creates a generator that yields a point on the
            LineSegment instance with the given step
        move: moves the LineSegment instance with the given changes in
            its 'x' and 'y' coordinates
    """

    def __init__(self, end1: Point, end2: Point) -> None:
        """Initializing the LineSegment object

        Args:
            end1 (Point): the first end of the LineSegment entity
            end2 (Point): the seconf end of the LineSegment entity

        Raises:
            BadEntries: when the given points have the same coordinates
        """

        if end1 == end2:
            raise BadEntries(
                "the given points have the same coordinates, they can't produce a line segment"
            )
        self.end1 = end1
        self.end2 = end2

    @classmethod
    def from_point_and_inclination(
        cls, point: Point, inclination: float, size: float
    ) -> "LineSegment":
        """Alternative constructor to create a LineSegment instance
        given a point and an inclination and a size"""

        x1 = (point.x) - (np.cos(inclination)) * (size / 2)
        y1 = (point.y) - (np.sin(inclination)) * (size / 2)
        x2 = (point.x) + (np.cos(inclination)) * (size / 2)
        y2 = (point.y) + (np.sin(inclination)) * (size / 2)
        end1 = Point(x1, y1)
        end2 = Point(x2, y2)
        return cls(end1, end2)

    @property
    def length(self) -> float:
        """calculate the length of the LineSegment instance

        Returns:
            the length of the LineSegment instance
        """

        x1, y1 = self.end1.x, self.end1.y
        x2, y2 = self.end2.x, self.end2.y
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    @property
    def circumcircle(self) -> Circle:
        """calculate the circumcircle of the LineSegment instance

        Returns:
            a Circle object having the LineSegment instance as its diameter
        """

        centre = self.midpoint(0.5)
        diameter = self.length
        return Circle(centre, diameter)

    @property
    def inclination(self) -> float:
        """calculating the inclination of the LineSegment instance

        Returns:
            the inclination of the LineSegment instance as an angle in
            radian
        """

        return np.arctan(self.slope)

    @property
    def slope(self) -> float:
        """calculating the slope of the LineSegment instance

        Returns:
            the slope of the LineSegment instance as the tangent of its
            inclination angle
        """

        x1, y1 = self.end1.x, self.end1.y
        x2, y2 = self.end2.x, self.end2.y
        try:
            res = (y2 - y1) / (x2 - x1)
        except ZeroDivisionError:
            res = np.tan(np.pi / 2)
        return res

    @property
    def infinite(self) -> Line:
        """calculate a Line object which witholds the LineSegment
        instance

        Returns:
            a Line object built upon the current LineSegment instance
        """

        return Line.from_point(self.end1, self.end2)

    def get_x(self, y: float) -> float:
        """calculating the 'x' coordinate of a point on the LineSegment
        instance with the given 'y' coordinate

        Args:
            y (float): the 'y' coordinate of the point on the
                LineSegment instance

        Returns:
            the 'x' coordinate of a point on the LineSegment instance
        """

        x = self.infinite.get_x(y)
        point = Point(x, y)
        if not is_on_perimeter(point, self):
            raise BadEntries(
                "the current LineSegment instance does not reach the given width"
            )
        return x

    def get_y(self, x: float) -> float:
        """calculating the 'y' coordinate of a point on the LineSegment
        instance with the given 'x' coordinate

        Args:
            x (float): the 'x' coordinate of the point on the
                LineSegment instance

        Returns:
            the 'y' coordinate of a point on the LineSegment instance
        """

        y = self.infinite.get_y(x)
        point = Point(x, y)
        if not is_on_perimeter(point, self):
            raise BadEntries(
                "the current LineSegment instance does not reach the given length"
            )
        return y

    def midpoint(self, ratio: float) -> Point:
        """finds a point on the LineSegment object located at the given
        ratio, taken the 'end1' attribute of the object as the starting
        point

        Args:
            ratio (float): the ratio of the target point on the
            LineSegment instance

        Returns:
            a point preserving that ratio, taking the 'end1' attribute
            of the LineSegment instance as the starting point and the
            'end2' attribute as the end point
        """

        if ratio < 0 or ratio > 1:
            raise BadEntries("the given ratio should have a value between zero and one")
        point = self.end1
        delta_x = (np.cos(self.inclination)) * (self.length) * (ratio)
        delta_y = (np.sin(self.inclination)) * (self.length) * (ratio)
        point.move(delta_x, delta_y)
        return point

    def navigator(self, step: float) -> Point:
        """a generator that generates Point objects that are located on
        the LineSegment instance with the given step as a ratio

        Args:
            step: the step taken to produce the next output given as
                ratio of the LineSegment length

        Yields:
            a Point object located on the LineSegment instance
        """

        if step < 0 or step > 1:
            raise BadEntries("the given ratio should have a value between zero and one")
        point = self.end1
        dist = 0
        delta_x = (np.cos(self.inclination)) * (self.length) * (step)
        delta_y = (np.sin(self.inclination)) * (self.length) * (step)
        while dist < self.length:
            yield point
            point.move(delta_x, delta_y)

    def move(self, delta_x: float, delta_y: float) -> None:
        """moving the LineSegment instance with the given changes in its
        coordinates

        Args:
            delta_x (float): the change in the 'x' coordinate of the
                LineSegment instance
            delta_y (float): the change in the 'y' coordinate of the
                LineSegment instance
        """

        self.end1.move(delta_x, delta_y)
        self.end2.move(delta_x, delta_y)

    def __eq__(self, other: Any) -> bool:
        """Defining the equality condition

        Args:
            other(Any): the instance to be compared with the current
                LineSegment instance

        Returns:
            True or False indicating the equality condition
        """

        if (
            isinstance(other, LineSegment)
            and self.end1 == other.end1
            and self.end2 == other.end2
        ):
            return True
        return False
