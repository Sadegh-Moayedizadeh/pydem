"""Contains all the classes to construct 2D entities used in the model
"""


from typing import Tuple, Any, Optional, Type, Union
import numpy as np
from itertools import count
from collections import defaultdict
from geometry import two_dimensional_operations as operations


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
    def get_rtheta(self) -> Tuple[float, float]:
        """Gives the 'r-theta' coordinates of the Point object in a
        tuple

        Returns:
            coordinates (Tuple[float, float]): a tuple containing the
                'r' and 'theta' coordinates of the Point object
        """

        r = np.sqrt((self.x) ** 2 + (self.y) ** 2)
        try:
            theta = np.arctan((self.y) / (self.x))
        except ZeroDivisionError:
            theta = np.math.pi / 2
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

        if isinstance(other, Point) and abs(self.x - other.x) < 1e-10 and abs(self.y - other.y) < 1e-10:
            return True
        return False
    
    def __repr__(self):
        return f'Point({self.x}, {self.y})'
    
    def __hash__(self):
        return int(self.x**2 + self.y**2)


class Polygon(object):
    """Constructing polygons given a series of Point objects

    Parents:
        object: base class to create python objects

    Methods:
        as_regular: creates a regular polygon due to the given center
            and radius of the circumcircle and the number of vertices
        number_of_vertices: returns the number of vertices of the
            Polygon instance
        edges: returns a tuple containing all the edges of the Polygon
            instance as LineSegment instances
        perimeter: returns the perimeter of the Polygon instance
        move: moves the Polygon instance with the given changes in the
            coordinates of its vertices
    """

    def __init__(self, *vertices: Type[Point]) -> None:
        """Initializing the Polygin object with the given series of
        Point objects

        Args:
            *vertices (Type[Point]): series of Point objects which are the
                vertices of the polygon, the order of points given is
                important and will stay the same for this object

        Raises:
            RuntimeError: in three scenarios:
                when the number of the given vertices is less than three,
                    which makes it impossible to form a polygon
                when the given vertices are given in a way that the edges
                    intersect with one another
                when repetitive vertices where given
        """

        self.vertices = vertices
        if self.number_of_vertices < 3:
            raise RuntimeError(
                "the number of given points should be equal or more than three"
            )
        dd = defaultdict(int)
        for vertex in vertices:
            dd[(vertex.x, vertex.y)] += 1
            if dd[(vertex.x, vertex.y)] == 2:
                raise RuntimeError("the same vertex entered twice")
        for edge1 in self.edges:
            for edge2 in self.edges:
                if edge1 != edge2 and operations.intersection(edge1, edge2):
                    inter = operations.intersection(edge1, edge2)
                    if not(
                        inter == edge1.end1 or
                        inter == edge1.end2 or
                        inter == edge2.end1 or
                        inter == edge2.end2
                    ):
                        raise RuntimeError(
                            "the given vertices form a polygon with intersecting edges"
                        )

    @classmethod
    def as_regular(
        cls,
        center: Type[Point],
        diameter: float,
        number_of_vertices: int
    ) -> "Polygon":
        """Alternative constructor of Polygon instances which are
        regular, which means they can be circumscribed by a circle and
        have edges with the same length; the first vertex will be
        loaceted at the horizental diameter of the circumcircle

        Args:
            center (Type[Point]): a Point object which is the center of the
                circumcircle of the polygons
            diamete (float): the diameter of the circumcircle of the
                polygon
            number_of_vertices (int): the number of the vertices of the
                polygon
        """

        circumcircle = Circle(center, diameter)
        n = number_of_vertices
        points = [
            circumcircle.get_point_on_perimeter(i*(2*np.math.pi/n))
            for i in range(0, n)
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
    def center(self) -> Type[Point]:
        """calculates the center of the polygon

        Returns:
            Type[Point]: the center of the current polygon instance
        """
          
        x = sum(point.x for point in self.vertices) / len(self.vertices)
        y = sum(point.y for point in self.vertices) / len(self.vertices)
        return Point(x, y)
    
    @property
    def edges(self) -> Any:
        """Create a tuple of edges of the Polygon as LineSegment
        objects"""

        lst = []
        for i in range(self.number_of_vertices):
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

        if isinstance(other, Polygon) and set(self.vertices) == set(other.vertices):
            return True
        return False
    
    def __repr__(self):
        vertices = [point.__repr__() for point in self.vertices]
        return 'Polygon' + str(vertices)


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
        center: finds the center of the Rectangle instance
        circumcircle: finds the circumcircle of the Rectangle instance
    """

    def __init__(self, *vertices: Point) -> None:
        """Initialize the Rectangle object

        Args:
            *vertices (Point): the vertices of the Rectangle

        Raises:
            RuntimeError: raises this exception in two scenarios:
                when the number of the given vertices is not equal to
                    four
                when the given vertices are in a way that the resultant
                    polygon doesn't have perpendecular edges
        """

        super().__init__(*vertices)
        edges = self.edges
        n = self.number_of_vertices
        if n != 4:
            raise RuntimeError("you should enter exactly four vertices")
        for i in range(n):
            if abs(edges[i].inclination - edges[i - 1].inclination) != (np.math.pi / 2):
                raise RuntimeError(
                    "the given vertices do not form a rectangle with perpendecular edges"
                )

    @classmethod
    def from_midline(cls, midline: "LineSegment", tolerance: float) -> "Rectangle":
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
            midline.end1.x + tolerance * np.cos(np.pi / 2 - angle),
            midline.end1.y - tolerance * np.sin(np.pi / 2 - angle),
        )
        vertex2 = Point(
            midline.end1.x - tolerance * np.cos(np.pi / 2 - angle),
            midline.end1.y + tolerance * np.sin(np.pi / 2 - angle),
        )
        vertex3 = Point(
            midline.end2.x - tolerance * np.cos(np.pi / 2 - angle),
            midline.end2.y + tolerance * np.sin(np.pi / 2 - angle),
        )
        vertex4 = Point(
            midline.end2.x + tolerance * np.cos(np.pi / 2 - angle),
            midline.end2.y - tolerance * np.sin(np.pi / 2 - angle),
        )
        return cls(vertex1, vertex2, vertex3, vertex4)

    @classmethod
    def from_diagonal(cls, diagonal: "LineSegment") -> "Rectangle":
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
    def midlines(self) -> Tuple["LineSegment"]:
        """calculate the two midlines of the Rectangle instance

        Returns:
            a two tuple containin the midlines of the Rectangle
            instance as LineSegment objects with the longer one being
            the first element
        """
        end1 = self.edges[0].midpoint()
        end2 = self.edges[2].midpoint()
        line1 = LineSegment(end1, end2)
        end3 = self.edges[1].midpoint()
        end4 = self.edges[3].midpoint()
        line2 = LineSegment(end3, end4)
        return (line1, line2) if (line1.end1.x > line2.end2.x) else (line2, line1)

    @property
    def diagonals(self) -> Tuple["LineSegment"]:
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

    # @property
    # def center(self) -> Point:
    #     """calculating the center of the Rectangle instance

    #     Returns:
    #         the center of the Rectangle instance as a Point object
    #     """

    #     return 

    @property
    def circumcircle(self) -> "Circle":
        """calculating the circumcircle of the Rectangle instance

        Returns:
            the circumcircle of the Rectangle instance as a Circle
            object
        """

        return Circle(center=self.center, diameter=self.diagonals[0].length)
    
    def __repr__(self):
        vertices = [point.__repr__() for point in self.vertices]
        return 'Rectangle' + str(vertices)


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
            coordinates of its center
    """

    def __init__(self, center: Point, diameter: float) -> None:
        """Initialize the Circle object

        Args:
            center (Point): the center of the circle
            diameter (float): the diameter of the circle

        Raises:
            RuntimeError: when the given diameter is zero or a negative
                number
        """

        self.center = center
        self.diameter = diameter
        if self.diameter <= 0:
            raise RuntimeError("the given diameter should be a positive non-zero number")

    @property
    def area(self) -> float:
        """calculate the area of the Circle instance

        Returns:
            the area of the Circle instance
        """

        return ((np.pi) * (self.diameter) ** 2) / 4

    @property
    def radius(self) -> float:
        """calculate the radius of the Circle instance

        Returns:
            float: the radius of the Circle instance
        """
        return (self.diameter / 2)
    @property
    def perimeter(self) -> float:
        """calculate the perimeter of the Circle instance

        Returns:
            the perimeter of the Circle instance
        """

        return (np.pi) * (self.diameter)

    def get_point_on_perimeter(self, angle: float) -> Type[Point]:
        """calculating the point on the perimeter of the Circle
        instance with the given angle

        Returns:
            the point on the perimeter of the Circle instance with the
            given angle in radian
        """

        r = (self.diameter) / 2
        x0, y0 = self.center.x, self.center.y
        x = x0 + (r) * (np.cos(angle))
        y = y0 + (r) * (np.sin(angle))
        return Point(x, y)
    
    def get_angle(self, point: Type[Point]) -> float:
        """calculate the angle of the given point on the perimeter of
        the circle instance in respect to the horizental diameter

        Args:
            point (Type[Point]): the given Point istance

        Returns:
            float: the angle of the point on circle between 0 and
                2*np.math.pi radians
        """
        
        return (Line.from_points(self.center, point).inclination) % (2*np.math.pi)
    
    def navigator(self, start: float, step: float, rounds: int) -> Type[Point]:
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
            RuntimeError: when the given step is zero which makes it
                imposible to navigate on the Cirlces' perimeter

        Yields:
            Point objects located on the perimeter of the Circle instance
        """

        if step == 0:
            raise RuntimeError("the given step should not be zero")
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

        self.center = Point(self.center.x + delta_x, self.center.y + delta_y)

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
            and self.center == other.center
            and abs(self.diameter - other.diameter) < 1e-10
        ):
            return True
        return False
    
    def __repr__(self):
        return f'Circle[Point({self.center.x}, {self.center.y}), {self.diameter}]'


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

    def __init__(self, slope: float, width: float, length_if_vertical: float = None) -> None:
        """initializing the Line object

        Args:
            slope (float): slope of the line (the tangent of its
                inclination)
            width (float): width of the line from the origin of
                coordination system
        """

        self.slope = slope
        self.width = width
        self.length_if_vertical = length_if_vertical

    @classmethod
    def from_points(cls, point1: Type[Point], point2: Type[Point]) -> "Line":
        """Alternative constructor to create a Line instance given two
        Point objects located on the line

        Args:
            point1 (Type[Point]): the frist point located on the line
            point2 (Type[Point]): the second point located on the line
        """

        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        length_if_vertical = None
        try:
            slope = (y2 - y1) / (x2 - x1)
        except ZeroDivisionError:
            slope = np.tan(np.pi / 2)
            length_if_vertical = point1.x
        width = y1 - slope * x1
        return cls(slope, width, length_if_vertical)

    @classmethod
    def from_point_and_inclination(
        cls,
        point: Type[Point],
        inclination: float
        ) -> "Line":
        """Alternative constructor to create a Line instance given a
        single point on the line and an inclination angle

        Args:
            point (Type[Point]): a single point on the line
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
    
    def normal(self, point: Type[Point]) -> "Line":
        """returns a Line instance which is normal to the current Line
        instace
        
        Args:
            point (Type[Point]): the given point on the Line instace
                to draw the normal from

        Returns:
            Type[Line]: the Line instance normal to the current one
        """
        
        if self.slope == 0:
            new_slope = np.tan(np.math.pi / 2)
        else:
            new_slope = -1 / self.slope
        return Line.from_point_and_inclination(np.arctan(new_slope), point)

    def get_x(self, y: float) -> float:
        """calculate the 'x' coordinate of a point on the Line instance
        given the 'y' coordinate

        Args:
            y (float): the y coordinate of of the point on the Line

        Returns:
            the x coordinate of the point on the Line instance
        """

        if self.slope == 0:
            raise RuntimeError(
                "the line instance has the slope of zero, asking for an 'x' coordinate is invalid in this case"
            )
        if self.slope > 1e15 or self.slope < -1e15:
            if not(self.length_if_vertical is None):
                return self.length_if_vertical
            return 0
        return (y - self.width) / (self.slope)

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
            RuntimeError: when the given step is zero which makes it
                impossible to navigate on the line

        Yields:
            Point objects located on the Line instance
        """

        if step == 0:
            raise RuntimeError("the given step should be a non-zero value")
        if not operations.intersection(start, self) or not operations.intersection(end, self):
            raise RuntimeError(
                "the given start and end points should be loacated on the Line instance"
            )
        dist = 0
        limit = operations.distance(start, end)
        point = start
        delta_x = np.cos(self.inclination) * (step)
        delta_y = np.sin(self.inclination) * (step)
        while dist < limit:
            yield point
            point.move(delta_x, delta_y)
            dist = operations.distance(point, start)

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
            and abs(self.slope - other.slope) < 1e-10
            and abs(self.width - other.width) < 1e-10
        ):
            return True
        return False
    
    def __repr__(self):
        return f'Line({self.slope}, {self.width})'


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

    def __init__(self, end1: Type[Point], end2: Type[Point]) -> None:
        """Initializing the LineSegment object

        Args:
            end1 (Type[Point]): the first end of the LineSegment entity
            end2 (Type[Point]): the seconf end of the LineSegment entity

        Raises:
            RuntimeError: when the given points have the same coordinates
        """

        if end1 == end2:
            raise RuntimeError(
                "the given points have the same coordinates, they can't produce a line segment"
            )
        if end1.x == end2.x:
            if end1.y > end2.y:
                end1, end2 = end2, end1
        elif end1.x > end2.x:
            end1, end2 = end2, end1
        self.end1 = end1
        self.end2 = end2
    
    @classmethod
    def from_point_and_inclination(
        cls, point: Type[Point], inclination: float, size: float
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
    def circumcircle(self) -> Type[Circle]:
        """calculate the circumcircle of the LineSegment instance

        Returns:
            a Circle object having the LineSegment instance as its diameter
        """

        center = self.midpoint(0.5)
        diameter = self.length
        return Circle(center, diameter)

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
    def infinite(self) -> Type[Line]:
        """calculate a Line object which witholds the LineSegment
        instance

        Returns:
            a Line object built upon the current LineSegment instance
        """

        return Line.from_points(self.end1, self.end2)

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
        if not operations.intersection(point, self):
            raise RuntimeError(
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
        if not operations.intersection(point, self):
            raise RuntimeError(
                "the current LineSegment instance does not reach the given length"
            )
        return y

    def midpoint(self, ratio: float = 0.5) -> Type[Point]:
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
            raise RuntimeError("the given ratio should have a value between zero and one")
        point = Point(self.end1.x, self.end1.y)
        delta_x = (np.cos(self.inclination)) * (self.length) * (ratio)
        delta_y = (np.sin(self.inclination)) * (self.length) * (ratio)
        point.move(delta_x, delta_y)
        return point

    def navigator(self, step: float) -> Type[Point]:
        """a generator that generates Point objects that are located on
        the LineSegment instance with the given step as a ratio

        Args:
            step: the step taken to produce the next output given as
                ratio of the LineSegment length

        Yields:
            a Point object located on the LineSegment instance
        """

        if step < 0 or step > 1:
            raise RuntimeError("the given ratio should have a value between zero and one")
        point = Point(self.end1.x, self.end1.y)
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
            and ((
                self.end1 == other.end1
            and self.end2 == other.end2
            )
            or (
                self.end2 == other.end1
            and self.end1 == other.end2
            ))
        ):
            return True
        return False
    
    def __hash__(self):
        return (self.end1.__hash__() + self.end2.__hash__()) ** 3
    
    def __repr__(self):
        return f'LineSegment[Point({self.end1.x}, {self.end1.y}), Point({self.end2.x}, {self.end2.y})]'


class Arc(object):
    """construct a two dimensional arc which is basically a portion of
    a circle
    """
    
    def __init__(
        self,
        base: Type[Circle],
        end1: Type[Point],
        end2: Type[Point]
        ) -> None:
        """initialize the Arc instance

        Args:
            base (Type[Circle]): the base circle object
            end1 (Type[Point]): the first end of the arc
            end2 (Type[Point]): the second end of the arc
        
        Raises:
            RuntimeError: when any of the given points are not located
                on the base circle
        """

        if not operations.intersection(end1, base) or operations.intersection(end2, base):
            raise RuntimeError('the given points are not located on the given base circle')
        self.base = base
        self.end1 = end1
        self.end2 = end2
    
    @classmethod
    def from_angles(
        cls,
        base: Type[Circle],
        angle1: float,
        angle2: float
        ) -> "Arc":
        """Alternative constructor to create an arc from the given base
        circle and corresponding angles calculated from the horizental
        plain
        
        Args:
            base (Type[Circle]): the base circle object
            angle1 (float): the starting angle of the arc in radian
            angle2 (float): the ending angle of the arc in radian
        """
        
        end1 = base.get_point_on_perimeter(angle1)
        end2 = base.get_point_on_perimeter(angle2)
        return cls(base, end1, end2)
    
    def __eq__(self, other: Any) -> bool:
        """the equality condition of two arcs

        Args:
            other (Any): the geometrical entity with which to compare
                the equality condition of the current Arc instance
        """
        
        if isinstance(other, Arc) and self.base == other.base:
            if self.end1 == other.end1 and self.end2 == other.end2:
                return True
        return False


class LineInterval(object):
    """construct an interval object which is a collection of line
    segments on a same direction
    
    Methods:
        add: adds the given entity to the interval
        remove: removes the given entity from the interval
    
    also these methods where overridden:
        __repr__, __add__, __sub__, __eq__
    """
    
    def __init__(
        self,
        base: Type[Line]
        ) -> None:
        """initialize the Interval instance with the given base entity

        Args:
            base (Type[Line]): the base on which to construct the
                interval object
        """
        
        self.base = base
        self.entities = []
    
    def add(self, *entities: Type[LineSegment]) -> None:
        """adding the given LineSegment to the intervals in the the
        current LineInterval instance; the entities are ordered
        according to their x coordinate
        
        Raises:
            RuntimeError: when the given entity is not located
                completely on the base line
        """
        
        for entity in entities:
            if isinstance(self.base, LineSegment):
                cond1 = bool(operations.intersection(entity.end1, self.base.infinite))
                cond2 = bool(operations.intersection(entity.end2, self.base.infinite))
            else:
                cond1 = bool(operations.intersection(entity.end1, self.base))
                cond2 = bool(operations.intersection(entity.end2, self.base))
            if not cond1 or not cond2:
                raise RuntimeError('the given entity is not located on the base line')
            if isinstance(self.base, LineSegment):
                if entity.end1.x < self.base.end1.x:
                    entity.end1 = self.base.end1
                if entity.end2.x > self.base.end2.x:
                    entity.end2 = self.base.end2
            if len(self.entities) == 0:
                self.entities.append(entity)
                continue
            prev = self._find_prev(entity)
            nex  = self._find_next(entity)
            if nex > len(self.entities) - 1:
                self.entities = self.entities[:prev + 1]
            else:
                self.entities = self.entities[:prev + 1] + self.entities[nex:]
            if len(self.entities) == 0:
                self.entities.append(entity)
                continue
            if prev == -1:
                nex = prev + 1
                if entity.end2.x > self.entities[nex].end1.x:
                    line1 = entity
                    line2 = self.entities.pop(nex)
                else:
                    line1 = entity
                    line2 = entity
                prev += 1
            else:
                if prev < len(self.entities) - 1:
                    nex = prev + 1
                    if entity.end1.x < self.entities[prev].end2.x:
                        if entity.end2.x > self.entities[nex].end1.x:
                            line1 = self.entities.pop(prev)
                            line2 = self.entities.pop(prev)
                        else:
                            line1 = self.entities.pop(prev)
                            line2 = entity
                    else:
                        if entity.end2.x > self.entities[nex].end1.x:
                            line1 = entity
                            line2 = self.entities.pop(nex)
                        else:
                            line1 = entity
                            line2 = entity
                        prev += 1
                else:
                    if entity.end1.x < self.entities[prev].end2.x:
                        line1 = self.entities.pop(prev)
                        line2 = entity
                    else:
                        line1 = entity
                        line2 = entity
                        prev += 1
            new = LineSegment(line1.end1, line2.end2)
            self.entities.insert(prev, new)
    
    def remove(self, *entities: Type[LineSegment]) -> None:
        """removing the the coordinates that overlap with the given
        LineSegment entity from the current LineInterval instance's
        entities array
        
        Raises:
            RuntimeError: when the given entity is not located
                completely on the base line
        """

        for entity in entities:
            if isinstance(self.base, LineSegment):
                cond1 = bool(operations.intersection(entity.end1, self.base.infinite))
                cond2 = bool(operations.intersection(entity.end2, self.base.infinite))
            else:
                cond1 = bool(operations.intersection(entity.end1, self.base))
                cond2 = bool(operations.intersection(entity.end2, self.base))
            if not cond1 or not cond2:
                raise RuntimeError('the given entity is not located on the base line')
            if isinstance(self.base, LineSegment):
                if entity.end1.x < self.base.end1.x:
                    if entity.end2.x < self.base.end1.x:
                        continue
                    entity.end1 = self.base.end1
                if entity.end2.x > self.base.end2.x:
                    if entity.end1.x > self.base.end2.x:
                        continue
                    entity.end2 = self.base.end2
            if len(self.entities) == 0:
                return
            prev = self._find_prev(entity)
            nex  = self._find_next(entity)
            if nex > len(self.entities) - 1:
                self.entities = self.entities[:prev + 1]
            else:
                self.entities = self.entities[:prev + 1] + self.entities[nex:]
            if len(self.entities) == 0:
                return
            if prev == -1:
                nex = prev + 1
                if entity.end2.x > self.entities[nex].end1.x:
                    line2 = self.entities.pop(nex)
                    new = LineSegment(entity.end2, line2.end2)
                    self.entities.insert(0, new)
                else:
                    continue
            else:
                if prev < len(self.entities) - 1:
                    nex = prev + 1
                    if entity.end1.x < self.entities[prev].end2.x:
                        if entity.end2.x > self.entities[nex].end1.x:
                            line1 = self.entities.pop(prev)
                            line2 = self.entities.pop(prev)
                            new1 = LineSegment(line1.end1, entity.end1)
                            new2 = LineSegment(entity.end2, line2.end2)
                            self.entities.insert(prev, new1)
                            self.entities.insert(nex, new2)
                        else:
                            line1 = self.entities.pop(prev)
                            new = LineSegment(line1.end1, entity.end1)
                            self.entities.insert(prev, new)
                    else:
                        if entity.end2.x > self.entities[nex].end1.x:
                            line2 = self.entities.pop(nex)
                            new = LineSegment(entity.end2, line2.end2)
                            self.entities.insert(nex, new)
                        else:
                            continue
                else:
                    if entity.end1.x < self.entities[prev].end2.x:
                        line1 = self.entities.pop(prev)
                        new = LineSegment(line1.end1, entity.end1)
                        self.entities.insert(prev, new)
                    else:
                        continue

    def _find_prev(
        self,
        entity: Type[LineSegment]
        ) -> int:
        """finds the index of the an entity insdide the self.entities
        array with the immidiate preceding x coordinate of its first
        end using binary search

        Args:
            entity (Type[LineSegment]): the given entity to find its
                previous entity in the self.entities array

        Returns:
            int: the index of the entity prior to the given one in the
                self.entites array
        """
        
        if len(self.entities) == 0:
            return -1
        left = 0
        right = len(self.entities) - 1
        while left < right:
            mid = (left + right) // 2
            if entity.end1.x < self.entities[mid].end1.x:
                right = mid - 1
            else:
                left = mid + 1
        return left if self.entities[left].end1.x < entity.end1.x else (left - 1)      

    def _find_next(
        self,
        entity: Type[LineSegment]
        ) -> int:
        """finds the LineSegment instance in the self.entities array
        which is the first element to have an x coordinate of its
        second end bigger than the one for the given entity

        Args:
            entity (Type[LineSegment]): the given LineSegment instance
                to find its interceding element in the self.entities
                array

        Returns:
            int: the index of the next instance in the self.entities
                array
        """
        
        if len(self.entities) == 0:
            return -1
        left = 0
        right = len(self.entities) - 1
        while left < right:
            mid = (left + right) // 2
            if entity.end2.x > self.entities[mid].end2.x:
                right = mid - 1
            else:
                left = mid - 1
        return right if self.entities[right].end2.x > entity.end2.x else (right + 1)
    
    def __add__(self, other: "LineInterval") -> "LineInterval":
        """adding the given LineInterval instance to the current one

        Returns:
            Type[LineInterval]: the current LineInterval instance after
                the given being added to it
        
        Raises:
            RuntimeError: when the given object to be added does not
                have the same base line with the current instance
        """
        
        if other.base != self.base:
            raise RuntimeError(
                'the given LineInterval instances do not have the same base lines'
                )
        for line in other.entities:
            self.add(line)
        return self

    def __sub__(self, other: "LineInterval") -> "LineInterval":
        """removing the given LineInterval instance from the current
        one

        Returns:
            Type[LineInterval]: the current LineInterval instance after
                the given removed from it
        Raises:
            RuntimeError: when the given object to be subtracted does not
                have the same base line with the current instance
        """
        
        if other.base != self.base:
            raise RuntimeError(
                'the given LineInterval instances do not have the same base lines'
                )
        for line in other.entities:
            self.remove(line)
        return self
    
    def __eq__(self, other: Any) -> bool:
        """checking the equality condition between the current
        LineInterval instance and the given object

        Args:
            other (Any): the given object to check the equality
                condition with

        Returns:
            bool: True or False indicating the equality condition
        """
        
        if isinstance(other, LineInterval):
            for line1, line2 in zip(self.entities, other.entities):
                if line1 != line2:
                    return False
            return True
        return False

    def __repr__(self) -> str:
        """the string representation of the LineInterval object

        Returns:
            str: the string representation of the current instance
        """
        
        res = [[(line.end1.x, line.end1.y), (line.end2.x, line.end2.y)] for line in self.entities]
        return res.__str__


class ArcInterval(object):
    """construct an interval object which is a collection of arcs on a
    same base circle
    
    Methods:
        add: adds the given entity to the interval
        remove: removes the given entity from the interval
    
    also these methods where overridden:
        __repr__, __add__, __sub__, __eq__
    """
    
    def __init__(
        self,
        base: Type[Circle]
        ) -> None:
        """initialize the Interval instance with the given base entity

        Args:
            base (Type[Circle]): the base on which to construct the
                interval object
        """
        
        self.base = base
        self.entities = []
    
    def add(self, *entities: Type[Arc]) -> None:
        """adding the given Arc to the intervals in the the current
        ArcInterval instance; the entities are ordered according to
        their angle on the base circle
        
        Raises:
            RuntimeError: when the given entity is not located
                completely on the base circle
        """
        
        for entity in entities:
            cond1 = bool(operations.intersection(entity.end1, self.base))
            cond2 = bool(operations.intersection(entity.end2, self.base))
            if not cond1 or not cond2:
                raise RuntimeError('the given entity is not located on the base line')
            if len(self.entities) == 0:
                self.entities.append(entity)
                continue
            prev = self._find_prev(entity)
            nex  = self._find_next(entity)
            if nex > len(self.entities) - 1:
                self.entities = self.entities[:prev + 1]
            else:
                self.entities = self.entities[:prev + 1] + self.entities[nex:]
            if len(self.entities) == 0:
                self.entities.append(entity)
                continue
            if prev == -1:
                nex = prev + 1
                if self.base.get_angle(entity.end2) > self.base.get_angle(self.entities[nex].end1):
                    line1 = entity
                    line2 = self.entities.pop(nex)
                else:
                    line1 = entity
                    line2 = entity
                prev += 1
            else:
                if prev < len(self.entities) - 1:
                    nex = prev + 1
                    if self.base.get_angle(entity.end1) < self.base.get_angle(self.entities[prev].end2):
                        if self.base.get_angle(entity.end2) > self.base.get_angle(self.entities[nex].end1):
                            line1 = self.entities.pop(prev)
                            line2 = self.entities.pop(prev)
                        else:
                            line1 = self.entities.pop(prev)
                            line2 = entity
                    else:
                        if self.base.get_angle(entity.end2) > self.base.get_angle(self.entities[nex].end1):
                            line1 = entity
                            line2 = self.entities.pop(nex)
                        else:
                            line1 = entity
                            line2 = entity
                        prev += 1
                else:
                    if self.base.get_angle(entity.end1) < self.base.get_angle(self.entities[prev].end2):
                        line1 = self.entities.pop(prev)
                        line2 = entity
                    else:
                        line1 = entity
                        line2 = entity
                        prev += 1
            new = LineSegment(line1.end1, line2.end2)
            self.entities.insert(prev, new)
    
    def remove(self, *entities: Type[LineSegment]) -> None:
        """removing the the coordinates that overlap with the given
        Arc entity from the current ArcInterval instance's entities
        array
        
        Raises:
            RuntimeError: when the given entity is not located
                completely on the base circle
        """

        for entity in entities:
            cond1 = bool(operations.intersection(entity.end1, self.base))
            cond2 = bool(operations.intersection(entity.end2, self.base))
            if not cond1 or not cond2:
                raise RuntimeError('the given entity is not located on the base line')
            if len(self.entities) == 0:
                return
            prev = self._find_prev(entity)
            nex  = self._find_next(entity)
            if nex > len(self.entities) - 1:
                self.entities = self.entities[:prev + 1]
            else:
                self.entities = self.entities[:prev + 1] + self.entities[nex:]
            if len(self.entities) == 0:
                return
            if prev == -1:
                nex = prev + 1
                if self.base.get_angle(entity.end2) > self.base.get_angle(self.entities[nex].end1):
                    line2 = self.entities.pop(nex)
                    new = LineSegment(entity.end2, line2.end2)
                    self.entities.insert(0, new)
                else:
                    continue
            else:
                if prev < len(self.entities) - 1:
                    nex = prev + 1
                    if self.base.get_angle(entity.end1) < self.base.get_angle(self.entities[prev].end2):
                        if self.base.get_angle(entity.end2) > self.base.get_angle(self.entities[nex].end1):
                            line1 = self.entities.pop(prev)
                            line2 = self.entities.pop(prev)
                            new1 = LineSegment(line1.end1, entity.end1)
                            new2 = LineSegment(entity.end2, line2.end2)
                            self.entities.insert(prev, new1)
                            self.entities.insert(nex, new2)
                        else:
                            line1 = self.entities.pop(prev)
                            new = LineSegment(line1.end1, entity.end1)
                            self.entities.insert(prev, new)
                    else:
                        if self.base.get_angle(entity.end2) > self.base.get_angle(self.entities[nex].end1):
                            line2 = self.entities.pop(nex)
                            new = LineSegment(entity.end2, line2.end2)
                            self.entities.insert(nex, new)
                        else:
                            continue
                else:
                    if self.base.get_angle(entity.end1) < self.base.get_angle(self.entities[prev].end2):
                        line1 = self.entities.pop(prev)
                        new = LineSegment(line1.end1, entity.end1)
                        self.entities.insert(prev, new)
                    else:
                        continue
    
    def _find_prev(self, entity: Type[Arc]) -> int:
        """finds the Arc instance in the self.entities array which is
        the first element to have an angle on the base circle bigger
        than the one for the given entity

        Args:
            entity (Type[Arc]): the given Arc instance to find its
                interceding element in the self.entities array

        Returns:
            int: the index of the next instance in the self.entities
                array
        """
        
        if len(self.entities) == 0:
            return -1
        left = 0
        right = len(self.entities) - 1
        while left < right:
            mid = (left + right) // 2
            if self.base.get_angle(entity.end2) > self.base.get_angle(self.entities[mid].end2):
                right = mid - 1
            else:
                left = mid - 1
        if self.base.get_angle(self.entities[right].end2) > self.base.get_angle(entity.end2):
            return right 
        return (right + 1)
    
    def find_next(self, entity: Type[Arc]) -> int:
        """finds the Arc instance in the self.entities array which is
        the first element to have an angle if its second end on the
        base circle bigger than the one for the given entity

        Args:
            entity (Type[Arc]): the given Arc instance to find its
                interceding element in the self.entities array

        Returns:
            int: the index of the next instance in the self.entities
                array
        """
        
        if len(self.entities) == 0:
            return -1
        left = 0
        right = len(self.entities) - 1
        while left < right:
            mid = (left + right) // 2
            if self.base.get_angle(entity.end2) > self.base.get_angle(self.entities[mid].end2):
                right = mid - 1
            else:
                left = mid - 1
        if self.base.get_angle(self.entities[right].end2) > self.base.get_angle(entity.end2):
            return right 
        return (right + 1)
    
    def __eq__(self, other: Any) -> bool:
        """checking the equality condition between the current
        ArcInterval instance and the given object

        Args:
            other (Any): the given object to check the equality
                condition with

        Returns:
            bool: True or False indicating the equality condition
        """
        
        if isinstance(other, ArcInterval):
            for arc1, arc2 in zip(self.entities, other.entities):
                if arc1 != arc2:
                    return False
            return True
        return False
    
    def __add__(self, other: "ArcInterval") -> "ArcInterval":
        """adding the given ArcInterval instance to the current one

        Returns:
            Type[ArcInterval]: the current ArcInterval instance after
                the given being added to it
        
        Raises:
            RuntimeError: when the given object to be added does not
                have the same base circlee with the current instance
        """
        
        if other.base != self.base:
            raise RuntimeError(
                'the given LineInterval instances do not have the same base lines'
                )
        for arc in other.entities:
            self.add(arc)
        return self
    
    def __sub__(self, other: "ArcInterval") -> "ArcInterval":
        """removing the given ArcInterval instance from the current one

        Returns:
            Type[ArcInterval]: the current ArcInterval instance after
                the given removed from it
        Raises:
            RuntimeError: when the given object to be subtracted does not
                have the same base line with the current instance
        """
        
        if other.base != self.base:
            raise RuntimeError(
                'the given LineInterval instances do not have the same base lines'
                )
        for arc in other.entities:
            self.remove(arc)
        return self
    
    def __repr__(self) -> str:
        """the string representation of the ArcInterval object

        Returns:
            str: the string representation of the current instance
        """
        
        res = [(self.base.get_angle(arc.end1), self.base.get_angle(arc.end2)) for arc in self.entities]
        return res.__str__