"""Test cases for all the classes and their methods from
two_dimensional_entities module from geometry sub-packages
"""
import unittest
import numpy as np
import os
# os.chdir('geometry/')
# print(os.getcwd())
# print(os.lisshapesir())
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations
#
class TestPoint(unittest.TestCase):
    """Testing the Point class form two_dimensional_entities module

    Parents:
        unittest.TestCase: base class to write unit tests
    """

    def test_from_rtheta(self):
        """testing construction of the Point object from the given
        'r-theta' coordinates"""

        instance = shapes.Point.from_rtheta(1, np.pi / 2)
        self.assertEqual(0, instance.x)
        self.assertEqual(1, instance.y)

    def test_get_rtheta(self):
        """testing the 'r' and 'theta' recieved form the get_rtheta
        method"""

        instance = shapes.Point(1, 0)
        self.assertEqual((1, 0), instance.get_rtheta)

    def test_get_rtheta_xzero(self):
        """testing the 'r' and 'theta' recieved from the get_rtheta
        method with the 'x' coordinate provided being zero to see if
        the method is compatible with division by zero"""

        instance = shapes.Point(0, 1)
        self.assertEqual((1, np.pi / 2), instance.get_rtheta)

    def test_equality(self):
        """testing if two points with the same coordinates are equal"""

        instance1 = shapes.Point(0, 0)
        instance2 = shapes.Point(0, 0)
        self.assertEqual(instance1, instance2)


class TestPolygon(unittest.TestCase):
    """Testing the Polygon class from two_dimensional_entities module

    Parents:
        unittest.TestCase: base class to write unit tests
    """

    def test_construction1(self):
        """testing the construction of the object with less than three
        vertices given"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 1)
        self.assertRaises(BadEntries, shapes.Polygon.__init__(p1, p2))

    def test_construction2(self):
        """testing the constuction of the object with the same vetex
        given twice"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(0, 1)
        p2 = shapes.Point(0, 0)
        self.assertRaises(BadEntries, shapes.Polygon.__init__(p1, p2, p3))

    def test_construction3(self):
        """testing the construction of the object with vertices given
        in a way that edges intersect one another"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 0)
        p3 = shapes.Point(1, 1)
        p4 = shapes.Point(0, 1)
        self.assertRaises(BadEntries, shapes.Polygon(p1, p3, p2, p4))

    def test_as_regular(self):
        """testing 'as_regular' method from Polygon class"""

        instance = shapes.Polygon.as_regular(
            centre=shapes.Point(0, 0), diameter=1, number_of_vertices=4
        )
        expected_vertices = (
            shapes.Point(1, 0),
            shapes.Point(0, 1),
            shapes.Point(-1, 0),
            shapes.Point(0, -1),
        )
        self.assertEqual(instance.vertices, expected_vertices)

    def test_number_of_vertices(self):
        """testing the number_of_vertices method from Polygon class"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 0)
        p3 = shapes.Point(1, 1)
        p4 = shapes.Point(0, 1)
        instance = shapes.Polygon(p1, p2, p3, p4)
        self.assertEqual(instance.number_of_vertices, 4)

    def test_edges(self):
        """Testing the 'edges' method from Polygon class"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 0)
        p3 = shapes.Point(1, 1)
        p4 = shapes.Point(0, 1)
        instance = shapes.Polygon(p1, p2, p3, p4)
        expected = (
            shapes.LineSegment(p4, p1),
            shapes.LineSegment(p1, p2),
            shapes.LineSegment(p2, p3),
            shapes.LineSegment(p3, p4),
        )
        self.assertEqual(instance.edges, expected)

    def test_perimeter(self):
        """Testing the 'perimeter' method of Polygon class"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 0)
        p3 = shapes.Point(1, 1)
        p4 = shapes.Point(0, 1)
        instance = shapes.Polygon(p1, p2, p3, p4)
        self.assertEqual(instance.perimeter, 4)

    def test_equality(self):
        """testing if two polygons with the same vertices are equal"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 0)
        p3 = shapes.Point(1, 1)
        p4 = shapes.Point(0, 1)
        instance1 = shapes.Polygon(p1, p2, p3, p4)
        instance2 = shapes.Polygon(p1, p2, p3, p4)
        self.assertEqual(instance1, instance2)

    def test_equality2(self):
        """testing if two polygon with the same vertices but with
        different order of entering those vertices are equal"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 0)
        p3 = shapes.Point(1, 1)
        p4 = shapes.Point(0, 1)
        instance1 = shapes.Polygon(p1, p2, p3, p4)
        instance2 = shapes.Polygon(p4, p3, p2, p1)
        self.assertEqual(instance1, instance2)


class TestRectangle(unittest.TestCase):
    """Testing the Rectangle class and its methods from
    two_dimensional_entities module in geometry sub-package

    Parents:
        unittest.TestCase: the base class to writes unit tests
    """

    def test_construction1(self):
        """testing the construction of Rectangle instance with less
        than four vertices given"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 1)
        p3 = shapes.Point(0, 1)
        self.assertRaises(BadEntries, shapes.Rectangle.__init__(p1, p2, p3))

    def test_construction2(self):
        """testing the construction of Rectangle instance with more
        than four vertices given"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(0, 1)
        p3 = shapes.Point(1, 2)
        p4 = shapes.Point(2, 1)
        p5 = shapes.Point(2, 0)
        self.assertRaises(BadEntries, shapes.Rectangle.__init__(p1, p2, p3, p4, p5))

    def test_construction3(self):
        """testing the construction of Rectangle instance with the
        vertices given in a way that the edges won't be perpendecular"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 0)
        p3 = shapes.Point(2, 1)
        p4 = shapes.Point(1, 0)
        self.assertRaises(BadEntries, shapes.Rectangle.__init__(p1, p2, p3, p4))

    def test_from_midline(self):
        """testing the 'from_midline' method of Rectangle class"""

        end1 = shapes.Point(1, 0)
        end2 = shapes.Point(1, 1)
        instance = shapes.Rectangle.from_midline(
            midline=shapes.LineSegment(end1, end2), tolerance=1
        )
        vertex1 = shapes.Point(0, 0)
        vertex2 = shapes.Point(2, 0)
        vertex3 = shapes.Point(2, 1)
        vertex4 = shapes.Point(0, 1)
        instance2 = shapes.Rectangle(vertex1, vertex2, vertex3, vertex4)
        self.assertEqual(instance1, instance2)

    def test_from_diagonal1(self):
        """testing the 'from_diagonal' method of Rectangle class"""

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        instance1 = shapes.Rectangle.from_diagonal(diagonal=shapes.LineSegment(end1, end2))
        vertex1 = shapes.Point(0, 0)
        vertex2 = shapes.Point(1, 0)
        vertex3 = shapes.Point(1, 1)
        vertex4 = shapes.Point(0, 1)
        instance2 = shapes.Rectangle(vertex1, vertex2, vertex3, vertex4)
        self.assertEqual(instance1, instance2)

    def test_from_diagonal2(self):
        """testing the 'from_diagonal' method of Rectangle class with
        ends given to the diagonal in an order different from
        test_from_diagonal1 test method"""

        end2 = shapes.Point(0, 0)
        end1 = shapes.Point(1, 1)
        instance1 = shapes.Rectangle.from_diagonal(diagonal=shapes.LineSegment(end1, end2))
        vertex1 = shapes.Point(0, 0)
        vertex2 = shapes.Point(1, 0)
        vertex3 = shapes.Point(1, 1)
        vertex4 = shapes.Point(0, 1)
        instance2 = shapes.Rectangle(vertex1, vertex2, vertex3, vertex4)
        self.assertEqual(instance1, instance2)

    def test_area(self):
        """testing the 'area' method of Rectangle class"""

        vertex1 = shapes.Point(0, 0)
        vertex2 = shapes.Point(1, 0)
        vertex3 = shapes.Point(1, 1)
        vertex4 = shapes.Point(0, 1)
        instance = shapes.Rectangle(vertex1, vertex2, vertex3, vertex4)
        self.assertEqual(instance.area, 1)

    def test_midlines(self):
        """testing the 'midlines' method of Rectangle class"""

        vertex1 = shapes.Point(0, 0)
        vertex2 = shapes.Point(1, 0)
        vertex3 = shapes.Point(1, 2)
        vertex4 = shapes.Point(0, 2)
        instance = shapes.Rectangle(vertex1, vertex2, vertex3, vertex4)
        midline1 = shapes.LineSegment(end1=shapes.Point(0.5, 0), end2=shapes.Point(0.5, 2))
        midline2 = shapes.LineSegment(end1=shapes.Point(0, 1), end2=shapes.Point(1, 1))
        expected = (midline1, midline2)
        self.assertEqual(instance.midlines, expected)

    def test_diagonals(self):
        """testing the 'diagonals' method of Rectangle class"""

        vertex1 = shapes.Point(0, 0)
        vertex2 = shapes.Point(1, 0)
        vertex3 = shapes.Point(1, 1)
        vertex4 = shapes.Point(0, 1)
        instance = shapes.Rectangle(vertex1, vertex2, vertex3, vertex4)
        diagonal1 = shapes.LineSegment(end1=shapes.Point(0, 0), end2=shapes.Point(1, 1))
        diagonal2 = shapes.LineSegment(end1=shapes.Point(1, 0), end2=shapes.Point(0, 1))
        expected = (diagonal1, diagonal2)
        self.assertEqual(instance.diagonals, expected)

    def test_centre(self):
        """testing the 'centre' method of Rectangle class"""

        vertex1 = shapes.Point(0, 0)
        vertex2 = shapes.Point(1, 0)
        vertex3 = shapes.Point(1, 1)
        vertex4 = shapes.Point(0, 1)
        instance = shapes.Rectangle(vertex1, vertex2, vertex3, vertex4)
        expected = shapes.Point(0.5, 0.5)
        self.assertEqual(instance.centre, expected)

    def test_circumcircle(self):
        """testing the 'circumcircle' method of Rectangle class"""

        vertex1 = shapes.Point(0, 0)
        vertex2 = shapes.Point(1, 0)
        vertex3 = shapes.Point(1, 2)
        vertex4 = shapes.Point(0, 2)
        instance = shapes.Rectangle(vertex1, vertex2, vertex3, vertex4)
        expected = shapes.Circle(centre=shapes.Point(0.5, 0.5), diameter=np.sqrt(2))
        self.assertEqual(instance.circumcircle, expected)


class TestCircle(unittest.TestCase):
    """Testing the Circle class from two_dimensional_entitie modules in
    geometry sub-package"""

    def test_construction(self):
        """testing the construction of the Circle object with an
        insvalid entry (negative diameter)"""

        c = shapes.Point(0, 0)
        d = -1
        self.assertRaises(BadEntries, shapes.Circle.__init__(centre=c, diameter=d))

    def test_area(self):
        """testing the 'area' method of Circle class"""

        c = shapes.Point(0, 0)
        d = 1
        instance = shapes.Circle(c, d)
        expected = ((np.pi) * (d) ** 2) / 4
        self.assertEqual(instance.area, expected)

    def test_perimeter(self):
        """testing the 'perimeter' method of Circle class"""

        c = shapes.Point(0, 0)
        d = 1
        instance = shapes.Circle(c, d)
        expected = (np.pi) * (d)
        self.assertEqual(instance.perimeter, expected)

    def test_get_point_on_perimeter(self):
        """testing the 'get_point_on_perimeter' method of Circle class"""

        c = shapes.Point(0, 0)
        d = 1
        instance = shapes.Circle(c, d)
        angle = (np.pi) / 4
        expected = shapes.Point(0, 1)
        test.assertEqual(instance.get_point_on_perimeter(angle), expected)

    def test_equality(self):
        """testing the equality condition of Circle class"""

        c = shapes.Point(0, 0)
        d = 1
        instance1 = shapes.Circle(c, d)
        instance2 = shapes.Circle(c, d)
        self.assertEqual(instance1, instance2)

    def test_navigator(self):
        """testing the 'navigator' method of the Circle class"""

        c = shapes.Point(0, 0)
        d = 1
        instance = shapes.Circle(c, d)
        gen = instance.navigator(0, np.pi / 4, 1)
        next(gen)
        expected = shapes.Point((np.sqrt(2) / 2), (np.sqrt(2) / 2))
        self.assertEqual(next(gen), expected)

    def test_navigator2(self):
        """testing if the 'navigator' method of the Circle class
        terminates after the specified number of rounds"""

        c = shapes.Point(0, 0)
        d = 1
        instance = shapes.Circle(c, d)
        gen = instance.navigator(0, np.pi / 4, 2)
        count = 0
        for _ in gen:
            count += 1
        self.assertEqual(count, 8)

    def test_move(self):
        """testing the 'move' method of the Circle class"""

        c1 = shapes.Point(0, 0)
        c2 = shapes.Point(1, 1)
        d = 1
        instance1 = shapes.Circle(c1, d)
        instance2 = shapes.circle(c2, d)
        self.assertEqual(instance1.move(1, 1), instance2)


class TestLine(unittest.TestCase):
    """Testing the methods of the Line class from the  two_dimensional_entities
    module in geometry sub-package"""

    def test_from_points(self):
        """testing the construction of the Line object via from_points
        method"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance = shapes.Line.from_points(point1, point2)
        self.assertEqual(instance.slope, 1)
        self.assertEqual(instance.wishapesth, 0)

    def test_from_point_and_inclination(self):
        """testing the construction of the Line object via
        from_point_and_inclination method"""

        point = shapes.Point(0, 0)
        inclination = (np.pi) / 4
        instance1 = shapes.Line.from_point_and_inclination(point, inclination)
        instance2 = shapes.Line(1, 0)
        self.assertEqual(instance1, instance2)

    def test_from_ij(self):
        """testing the construction of the Line object via from_ij
        method"""

        i = 1
        j = 1
        instance1 = shapes.Line.from_ij(i, j)
        instance2 = shapes.Line(1, 0)
        self.assertEqual(instance1, instance2)

    def test_inclination(self):
        """testing the 'inclination' method of the Line class"""

        instance = shapes.Line(1, 0)
        expected = (np.pi) / 4
        self.assertEqual(instance.inclination, expected)

    def test_get_x1(self):
        """testing the 'get_x' method of the Line class in a usual
        manner"""

        instance = shapes.Line(1, 0)
        self.assertEqual(instance.get_x(1), 1)

    def test_get_x2(self):
        """testing the 'get_x' method of the Line class with the Line
        object having the slope of infinity"""

        point1 = shapes.Point(1, 0)
        point2 = shapes.Point(1, 1)
        instance = shapes.Line.from_points(point1, point2)
        self.assertEqual(instance.get_x, 1)

    def test_get_x3(self):
        """testing the 'get_x' method of the Line class with the Line
        object having the slope of zero"""

        instance = shapes.Line(0, 1)
        self.assertRaises(BadEntries, instance.get_x(1))

    def test_get_y(self):
        """testing the 'get_y' method of the Line class"""

        instance = shapes.Line(1, 0)
        self.assertEqual(instance.get_y(1), 1)

    def test_equality(self):
        """testing the equality conditoin of the Line class"""

        instance1 = shapes.Line(1, 0)
        instance2 = shapes.Line(1, 0)
        self.assertEqual(instance1, instance2)

    def test_navigator(self):
        """testing the 'navigator' method of the Line class"""

        instance = shapes.Line(1, 0)
        start = shapes.Point(0, 0)
        end = shapes.Point(1, 1)
        gen = instance.navigator(start, end, 0.2)
        next(gen)
        expected = shapes.Point(0.2, 0.2)
        self.assertEqual(next(gen), expected)

    def test_navigator(self):
        """testing the 'navigator' method of the Line class with an invalid
        start point given, which is not located on the Line"""

        instance = shapes.Line(1, 0)
        start = shapes.Point(0, 1)
        end = shapes.Point(1, 1)
        self.assertRaises(BadEntries, instance.navigator(start, end, 0.2))

    def test_move(self):
        """testing the 'move' method of the Line class"""

        instance1 = shapes.Line(1, 0)
        instance2 = shapes.line(1, 1)
        self.assertEqual(instance1.move(0, 1), instance2)


class TestLineSegment(unittest.TestCase):
    """Testing the methods of the LineSegment class"""

    def test_construction(self):
        """testing the construction of the LineSegment object"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 0)
        self.assertRaises(BadEntries, shapes.LineSegment.__init__(point1, point2))

    def test_equality(self):
        """testing the equality condition of the LineSegment object"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance1 = shapes.LineSegment(point1, point2)
        instance2 = shapes.LineSegment(point1, point2)
        self.assertEqual(instance1, instance2)

    def test_from_point_and_inclination(self):
        """testing the 'from_point_and_inclination' method of LineSegment
        class"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        inclination = (np.pi) / 4
        size = np.sqrt(2)
        instance1 = shapes.LineSegment(point1, point2)
        instance2 = shapes.LineSegment.from_point_and_inclination(point1, inclination, size)
        self.assertEqual(instance1, instance2)

    def test_length(self):
        """testing the 'length' method of the LineSegment class"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance1 = shapes.LineSegment(point1, point2)
        expected = np.sqrt(2)
        self.assertEqual(instance.length, expected)

    def test_circumcircle(self):
        """testing the 'circumcircle' method of the LineSegment class"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance = shapes.LineSegment(point1, point2)
        circle = shapes.Circle(shapes.Point(0.5, 0.5), np.sqrt(2))
        self.assertEqual(instance.circumcircle, circle)

    def test_inclination(self):
        """testing the 'inclination' method of the LineSegment class"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance = shapes.LineSegment(point1, point2)
        expected = (np.pi) / 4
        self.assertEqual(instance.inclination, expected)

    def test_slope(self):
        """testing the 'slope' method of the LineSegment class"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance = shapes.LineSegment(point1, point2)
        expected = 1
        self.assertEqual(instance.slope, expected)

    def test_slope2(self):
        """testing the 'slope' method of the LineSegment class for a
        vertical LineSegment"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        expected = np.tan(np.pi / 2)
        self.assertEqual(instance.slope, expected)

    def test_infinite(self):
        """testing the 'infinite' method of the LineSegment class"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance1 = shapes.LineSegment(point1, point2)
        instance2 = shapes.Line(1, 0)
        self.assertEqual(instance1.infinite, instance2)

    def test_get_x(self):
        """testing the 'get_x' method of the LineSegment class"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance = shapes.LineSegment(point1, point2)
        self.assertEqual(instance.get_x(0.5), 0.5)

    def test_get_x2(self):
        """testing the 'get_x' method of the LineSegment class expecting
        an error asking for coordinates that isn't loacated on the
        LineSegment instance"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance = shapes.LineSegment(point1, point2)
        self.assertRaises(BadEntries, instance.get_x(2))

    def test_get_y(self):
        """testing the 'get_y' method of the LineSegment class"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance = shapes.LineSegment(point1, point2)
        self.assertEqual(instance.get_x(0.5), 0.5)

    def test_get_y2(self):
        """testing the 'get_y' method of the LineSegment class expecting
        an error asking for coordinates that isn't loacated on the
        LineSegment instance"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance = shapes.LineSegment(point1, point2)
        self.assertRaises(BadEntries, instance.get_y(2))

    def test_midpoint(self):
        """testing the 'midpoint' method of the LineSegment class"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 1)
        instance = shapes.LineSegment(point1, point2)
        expected = shapes.Point(0.5, 0.5)
        self.assertEqual(instance.midpoint(0.5), expected)

    def test_midpoint2(self):
        """testing the 'midpoint' method of the LineSegment class given
        an invalid ratio"""

        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(1, 1)
        instance = shapes.LineSegment(point1, point2)
        self.assertRaises(BadEntries, instance.midpoint(2))

    def test_navigator(self):
        """testing the navigator method of the LineSegment class"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance = shapes.LineSegment(point1, point2)
        gen = instance.navigator(0.2)
        next(gen)
        expected = shapes.Point(0.2, 0.2)
        self.assertEqual(next(gen), expected)

    def test_move(self):
        """testing the 'move' method of the LineSegment class"""

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        instance1 = shapes.LineSegment(point1, point2)
        point3 = shapes.Point(1, 1)
        point4 = shapes.Point(2, 2)
        instance2 = shapes.LineSegment(point3, point4)
        self.assertEqual(instance1.move(1, 1), instance2)


if __name__ == "__main__":
    unittest.main()