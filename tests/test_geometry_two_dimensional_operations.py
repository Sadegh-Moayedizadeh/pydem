"""test cases for the functions in two_dimesional_operations module
"""

import unittest
from geometry import two_dimensional_operations as operations
from geometry import two_dimensional_entities as shapes
import numpy as np


class Testoppositesides(unittest.TestCase):
    """testing the "opposite_sides" function
    """
    
    def test_for_horizental_line(self):
        """testing the "opposite_sides" function for a given line with
        the slope of zero
        """
        
        line = shapes.Line(0, 0)
        point1 = shapes.Point(0, 1)
        point2 = shapes.Point(0, -1)
        point3 = shapes.Point(0, 2)
        self.assertTrue(operations.opposite_sides(line, point1, point2))
        self.assertFalse(operations.opposite_sides(line, point1, point3))
    
    def test_for_vertical_line(self):
        """testing the "opposite_sides" function for a given line with
        inclination of 90 degrees
        """
        
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 1))
        point1 = shapes.Point(1, 0)
        point2 = shapes.Point(-1, 0)
        point3 = shapes.Point(2, 0)
        self.assertTrue(operations.opposite_sides(line, point1, point2))
        self.assertFalse(operations.opposite_sides(line, point1, point3))
    
    def test_for_line_with_arbitrary_inclination(self):
        """testing the "opposite_sides" function for a given line with
        an arbitrary inclination
        """
        
        line = shapes.Line(0, 1)
        point1 = shapes.Point(0, 1)
        point2 = shapes.Point(0, -1)
        point3 = shapes.Point(0, 2)
        self.assertTrue(operations.opposite_sides(line, point1, point2))
        self.assertFalse(operations.opposite_sides(line, point1, point3))


class TestIntersection(unittest.TestCase):
    """testing the "intersection" function for different cenarios
    """
    
    def test_fot_point_and_point1(self):
        """the first test for intersection between two points
        """
        
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 0)
        point3 = shapes.Point(0, 0)
        self.assertEqual(operations.intersection(point1, point2), point3)
    
    def test_for_point_and_point2(self):
        """the second test for intersection between two points
        """
        
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        self.assertEqual(operations.intersection(point1, point2), None)
    
    def test_for_point_and_polygon1(self):
        """the first test for intersection between a point and a
        polygon with the given point being on a vertex of the given
        polygon
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        pol = shapes.Polygon(v1, v2, v3)
        self.assertEqual(operations.intersection(point, pol), point)
        
    def test_for_point_and_polygon2(self):
        """the second test for intersection between a point and a
        polygon with the given point being located outside the given
        polygon
        """
        
        point = shapes.Point(10, 10)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        pol = shapes.Polygon(v1, v2, v3)
        self.assertEqual(operations.intersection(point, pol), None)
    
    def test_for_point_and_polygon3(self):
        """the third test for intersection between a point and a
        polygon with the given point being located on an edge of the
        given polygon
        """
        
        point = shapes.Point(0, 0.5)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        pol = shapes.Polygon(v1, v2, v3)
        self.assertEqual(operations.intersection(point, pol), point)
    
    def test_for_point_and_polygon4(self):
        """the fourth test for intersection between a point and a
        polygon with the given point being inside the given polygon
        """
        
        point = shapes.Point(0.1, 0.5)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        pol = shapes.Polygon(v1, v2, v3)
        self.assertEqual(operations.intersection(point, pol), False)
    
    def test_for_point_and_rectangle1(self):
        """the first test for intersection between a point and a
        rectangle with the given point being on a vertex of the given
        rectangle
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(1, 0)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection(point, rec), point)
        
    def test_for_point_and_rectangle2(self):
        """the second test for intersection between a point and a
        rectangle with the given point being located outside the given
        rectangle
        """
        
        point = shapes.Point(10, 10)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(1, 0)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection(point, rec), None)
    
    def test_for_point_and_rectangle3(self):
        """the third test for intersection between a point and a
        rectangle with the given point being located on an edge of the
        given rectangle
        """
        
        point = shapes.Point(0, 0.5)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(1, 0)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection(point, rec), point)
    
    def test_for_point_and_rectangle4(self):
        """the fourth test for intersection between a point and a
        rectangle with the given point being inside the given rectangle
        """
        
        point = shapes.Point(0.1, 0.5)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(1, 0)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection(point, rec), False)
    
    def test_for_point_and_line1(self):
        """the first test for intersection between a point and an
        infinite line with the given line being horizental and the
        given point being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.Line(0, 0)
        self.assertEqual(operations.intersection(point, line), point)
    
    def test_for_point_and_line2(self):
        """the second test for intersection between a point and an
        infinite line with the given line being vertical and the given
        point being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 1))
        self.assertEqual(operations.intersection(point, line), point)
    
    def test_for_point_and_line3(self):
        """the third test for intersection between a point and an
        infinite line with the given line being horizental and the
        given point not being located on that line
        """
        
        point = shapes.Point(0, 1)
        line = shapes.Line(0, 0)
        self.assertEqual(operations.intersection(point, line), None)
    
    def test_for_point_and_line4(self):
        """the fourth test for intersection between a point and an
        infinite line with the given line being vertical and the given
        point not being located on that line
        """
        
        point = shapes.Point(1, 0)
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 1))
        self.assertEqual(operations.intersection(point, line), point)
    
    def test_for_point_and_line5(self):
        """the fifth test for intersection between a point and an
        infinite line with the given line having an arbitrary slope
        and the given point being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.Line(1, 0)
        self.assertEqual(operations.intersection(point, line), point)
    
    def test_for_point_and_line6(self):
        """the sixth test for intersection between a point and an
        infinite line with the given line having an arbitrary slope
        and the given point not being located on that line
        """
        
        point = shapes.Point(1, 0)
        line = shapes.Line(1, 0)
        self.assertEqual(operations.intersection(point, line), None)
    
    def test_for_point_and_linesegment1(self):
        """the first test for intersection between a point and a line
        segment with the given line being horizental and the given
        point being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.LineSegment(shapes.Point(0, 0), shapes.Point(1, 0))
        self.assertEqual(operations.intersection(point, line), point)
    
    def test_for_point_and_linesegment2(self):
        """the second test for intersection between a point and a line
        segment with the given line being vertical and the given point
        being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.LineSegment(shapes.Point(0, -0.5), shapes.Point(0, 0.5))
        self.assertEqual(operations.intersection(point, line), point)
    
    def test_for_point_and_linesegment3(self):
        """the third test for intersection between a point and a line
        segment with the given line being horizental and the given
        point not being located on that line
        """
        
        point = shapes.Point(0, 1)
        line = shapes.LineSegment(shapes.Point(0, 0), shapes.Point(1, 0))
        self.assertEqual(operations.intersection(point, line), None)
    
    def test_for_point_and_linesegment4(self):
        """the fourth test for intersection between a point and a line
        segment with the given line being vertical and the given point
        not being located on that line
        """
        
        point = shapes.Point(1, 0)
        line = shapes.LineSegment(shapes.Point(0, -0.5), shapes.Point(0, 0.5))
        self.assertEqual(operations.intersection(point, line), point)
    
    def test_for_point_and_linesegment5(self):
        """the fifth test for intersection between a point and a line
        segment with the given line having an arbitrary slope and the
        given point being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.LineSegment(shapes.Point(-0.5, -0.5), shapes.Point(0.5, 0.5))
        self.assertEqual(operations.intersection(point, line), point)
    
    def test_for_point_and_linesegment6(self):
        """the sixth test for intersection between a point and a line
        segment with the given line having an arbitrary slope and the
        given point not being located on that line
        """
        
        point = shapes.Point(1, 0)
        line = shapes.LineSegment(shapes.Point(0, -0.5), shapes.Point(0, 0.5))
        self.assertEqual(operations.intersection(point, line), None)
    
    def test_for_point_and_circle1(self):
        """the first first test for intersection between a point and a
        circle with the given point being located inside the given
        circle
        """
        
        point = shapes.Point(0, 0.5)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.intersection(point, circle), None)
    
    def test_for_point_and_circle2(self):
        """the second test for intersection between a point and a
        circle with the given point being located on the given circle's
        perimeter
        """
        
        point = shapes.Point(0, 1)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.intersection(point, circle), point)
    
    def test_for_point_and_circle3(self):
        """the third test for intersection between a point and a circle
        with the given point being located outside the given circle
        """
        
        point = shapes.Point(0, 5)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.intersection(point, circle), None)
    
    def test_for_polygon_and_point1(self):
        """the first test for intersection between a point and a
        polygon with the given point being on a vertex of the given
        polygon
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        pol = shapes.Polygon(v1, v2, v3)
        self.assertEqual(operations.intersection(pol, point), point)
        
    def test_for_polygon_and_point2(self):
        """the second test for intersection between a point and a
        polygon with the given point being located outside the given
        polygon
        """
        
        point = shapes.Point(10, 10)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        pol = shapes.Polygon(v1, v2, v3)
        self.assertEqual(operations.intersection(pol, point), None)
    
    def test_for_polygon_and_point3(self):
        """the third test for intersection between a point and a
        polygon with the given point being located on an edge of the
        given polygon
        """
        
        point = shapes.Point(0, 0.5)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        pol = shapes.Polygon(v1, v2, v3)
        self.assertEqual(operations.intersection(pol, point), point)
    
    def test_for_point_and_polygon4(self):
        """the fourth test for intersection between a point and a
        polygon with the given point being inside the given polygon
        """
        
        point = shapes.Point(0.1, 0.5)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        pol = shapes.Polygon(v1, v2, v3)
        self.assertEqual(operations.intersection(pol, point), False)
    
    def test_for_polygon_and_polygon1(self):
        """the first test for intersection between two polygons with
        one of the given polygons being located inside the other one
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-0.5, 0)
        v7 = shapes.Point(0.5, 0)
        v8 = shapes.Point(0, 0.5)
        pol2 = shapes.Polygon(v6, v7, v8)
        self.assertEqual(operations.intersection(pol1, pol2), None)
    
    def test_for_polygon_and_polygon2(self):
        """the second test for intersection between two polygons with
        the given polygons touching each other on a single point
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-1, 0)
        v7 = shapes.Point(0.5, 0)
        v8 = shapes.Point(0, 0.5)
        pol2 = shapes.Polygon(v6, v7, v8)
        self.assertEqual(operations.intersection(pol1, pol2), v6)
    
    def test_for_polygon_and_polygon3(self):
        """the third test for intersection between two polygons with
        the given polygons being completely apart
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(5, 0)
        v7 = shapes.Point(6, 0)
        v8 = shapes.Point(5.5, 0.5)
        pol2 = shapes.Polygon(v6, v7, v8)
        self.assertEqual(operations.intersection(pol1, pol2), None)
    
    def test_for_polygon_and_polygon4(self):
        """the fourth test for intersection between two polygons with
        two of their edges intersect each other
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(0.5, 0)
        v7 = shapes.Point(1.5, 0)
        v8 = shapes.Point(1.5, 0.5)
        pol2 = shapes.Polygon(v6, v7, v8)
        self.assertEqual(operations.intersection(pol1, pol2), shapes.Point(0, 1))
    
    def test_for_polygon_and_polygon5(self):
        """the fifth test for intersection between two polygons with
        overlapping edges
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(0.5, -1)
        v7 = shapes.Point(1.5, -1)
        v8 = shapes.Point(1, -2)
        pol2 = shapes.Polygon(v6, v7, v8)
        line = shapes.lineSegment(v6, v3)
        self.assertEqual(operations.intersection(pol1, pol2), line)
    
    def test_for_polygon_and_rectangle1(self):
        """the first test for intersection between a polygon and a
        rectangle with the rectangle being located inside the polygon
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-0.5, 0)
        v7 = shapes.Point(0, 0.5)
        v8 = shapes.Point(0.5, 0)
        v9 = shapes.Point(0, -0.5)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        self.assertEqual(operations.intersection(pol, rec), None)
    
    def test_for_polygon_and_rectangle2(self):
        """the second test for intersection between a polygon and a
        rectangle with them touching each other on a single point
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-2, -1)
        v7 = shapes.Point(-1, -1)
        v8 = shapes.Point(-1, 1)
        v9 = shapes.Point(-2, 1)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        self.assertEqual(operations.intersection(pol, rec), v1)
    
    def test_for_polygon_and_rectangle3(self):
        """the third test for intersection between a polygon and a
        rectangle with them being completely apart
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(5, 0)
        v7 = shapes.Point(6, 0)
        v8 = shapes.Point(6, 1)
        v9 = shapes.Point(5, 1)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        self.assertEqual(operations.intersection(pol, rec), None)
    
    def test_for_polygon_and_rectangle4(self):
        """the fourth test for intersection between a polygon and a
        rectangle with of their edges intersect each other
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(0.5, 0)
        v7 = shapes.Point(1.5, 0)
        v8 = shapes.Point(1.5, 0.5)
        v9 = shapes.Point(0.5, 0.5)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        self.assertEqual(operations.intersection(pol, rec), shapes.Point(0, 1))
    
    def test_for_polygon_and_rectangle5(self):
        """the fifth test for intersection between a polygon and a
        rectangle with overlapping edges
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(0.5, -1)
        v7 = shapes.Point(1.5, -1)
        v8 = shapes.Point(1.5, -2)
        v9 = shapes.Point(0.5, -2)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        line = shapes.lineSegment(v6, v3)
        self.assertEqual(operations.intersection(pol, rec), line)
    
    def test_for_polygon_and_circle1(self):
        """the first test for intersection between a polygon and a
        circle with the given circle being inside the given polygon
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        circle = shapes.Circle(shapes.Point(0, 0), 0.5)
        self.assertEqual(operations.intersection(pol, circle), None)
    
    def test_for_polygon_and_circle2(self):
        """the second test for intersection between a polygon and a
        circle with them the given circle touching the given polygon
        on its vertex
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        circle = shapes.Circle(shapes.Point(0, -2), 1)
        self.assertEqual(operations.intersection(pol, circle), v1)
    
    def test_for_polygon_and_circle3(self):
        """the third test for intersection between a polygon and a
        circle with them touching each other in two points on different
        edges
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        circle = shapes.Circle(shapes.Point(1, 1), 0.5)
        res = (shapes.Point(1, 0.5), shapes.Point(0.5, 1))
        self.assertEqual(operations.intersection(pol, circle), res)
    
    def test_for_polygon_and_line1(self):
        """the first test for intersection between a polygon and an
        infinite line with them not intersecting each other
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        line = shapes.Line(1, 2)
        self.assertEqual(operations.intersection(pol, line), None)
    
    def test_for_polygon_and_line2(self):
        """the second test for intersection between a polygon and an
        infinite line with them intersecting in two points and the
        given line being horizental
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        line = shapes.Line(0, 0)
        res = (v1, shapes.Point(1, 0))
        self.assertEqual(operations.intersection(pol, line), res)
    
    def test_for_polygon_and_lin32(self):
        """the third test for intersection between a polygon and an
        infinite line with them intersecting in two points and the
        given line being vertical
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 1))
        res = (shapes.Point(0, 1), shapes.Point(0, -1))
        self.assertEqual(operations.intersection(pol, line), res)
    
    def test_for_polygon_and_line4(self):
        """the fourth test for intersection between a polygon and an
        infinite line with them intersecting in two points and the
        given line having an arbitrary slope
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        line = shapes.Line(0, 1)
        res = (v4, shapes.Point(-0.5, -0.5))
        self.assertEqual(operations.intersection(pol, line), res)
    
    def test_for_polygon_and_line5(self):
        """the fifth test for intersection between a polygon and an
        infinite line with the given line overlapping with one the
        edges of the given polygon
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        line = shapes.Line(1, 0)
        res = shapes.LineSegment(v5, v4)
        self.assertEqual(operations.intersection(pol, line), res)
    
    def test_for_polygon_and_linesegment1(self):
        """the first test for intersection between a polygon and a line
        segment with the line segment being inside the given polygon
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0.5, 0.5)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(pol, line), None)
    
    def test_for_polygon_and_linesegment2(self):
        """the second test for intersection between a polygon and a
        line segment with one end of the line segment touching an edge
        of the given polygon
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        end1 = shapes.Point(1, 0)
        end2 = shapes.Point(2, 0.5)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(pol, line), end1)
    
    def test_for_polygon_and_linesegment3(self):
        """the third test for intersection between a polygon and a line
        segment with one end of the given line segment being touching a
        vertex of the given polygon
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        end1 = v4
        end2 = shapes.Point(0.5, 0.5)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(pol, line), v4)
    
    def test_for_polygon_and_linesegment4(self):
        """the fourth test for intersection between a polygon and a
        line segment with the given line segment overlapping an edge of
        the given polygon
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        end1 = shapes.Point(0.5, 1)
        end2 = shapes.Point(2, 1)
        line = shapes.LineSegment(end1, end2)
        res = shapes.LineSegment(end1, v4)
        self.assertEqual(operations.intersection(pol, line), res)
    
    def test_for_polygon_and_linesegment5(self):
        """the fifth test for intersection between a polygon and a line
        segment with the given line segment intersecting the given
        polygon in two points
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        end1 = shapes.Point(0.5, 2)
        end2 = shapes.Point(0.5, -2)
        line = shapes.LineSegment(end1, end2)
        res = (shapes.Point(0.5, 1), shapes.Point(0.5, -1))
        self.assertEqual(operations.intersection(pol, line), res)
    
    def test_for_rectangle_and_point1(self):
        """the first test for intersection between a rectangle and a
        point with the given point being on a vertex of the given
        rectangle
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(1, 0)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection(rec, point), point)
        
    def test_for_rectangle_and_point2(self):
        """the second test for intersection between a point and a
        rectangle with the given point being located outside the given
        rectangle
        """
        
        point = shapes.Point(10, 10)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(1, 0)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection(rec, point), None)
    
    def test_for_rectangle_and_point3(self):
        """the third test for intersection between a point and a
        rectangle with the given point being located on an edge of the
        given rectangle
        """
        
        point = shapes.Point(0, 0.5)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(1, 0)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection(rec, point), point)
    
    def test_for_rectangle_and_point4(self):
        """the fourth test for intersection between a point and a
        rectangle with the given point being inside the given polygon
        """
        
        point = shapes.Point(0.1, 0.5)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(1, 0)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection(rec, point), None)
    
    def test_for_rectangle_and_rectangle1(self):
        """the first test for intersection between two rectangles with
        one of the given rectangles being located inside the other one
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-1, -1)
        v6 = shapes.Point(-1, 1)
        v7 = shapes.Point(1, 1)
        v8 = shapes.Point(1, -1)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection(rec1, rec2), None)
    
    def test_for_rectangle_and_rectangle2(self):
        """the second test for intersection between twoc rectangles with
        the given rectangles touching each other on a single point
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(2, 1)
        v6 = shapes.Point(3, 2)
        v7 = shapes.Point(4, 1)
        v8 = shapes.Point(3, 0)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection(rec1, rec2), v5)
    
    def test_for_rectangle_and_rectangle3(self):
        """the third test for intersection between two rectangles with
        the given rectangles being completely apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(5, 0)
        v6 = shapes.Point(6, 0)
        v7 = shapes.Point(6, 1)
        v8 = shapes.Point(5, 1)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection(rec1, rec2), None)
    
    def test_for_rectangle_and_rectangle4(self):
        """the fourth test for intersection between two rectangles with
        two of their edges intersect each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(0, 0)
        v6 = shapes.Point(3, 0)
        v7 = shapes.Point(3, 3)
        v8 = shapes.Point(3, 0)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        res = (shapes.Point(2, 0), shapes.Point(0, 2))
        self.assertEqual(operations.intersection(rec1, rec2), res)
    
    def test_for_rectangle_and_rectangle5(self):
        """the fifth test for intersection between two rectangles with
        overlapping edges
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(0, 2)
        v6 = shapes.Point(3, 2)
        v7 = shapes.Point(3, 0)
        v8 = shapes.Point(0, 0)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        line = shapes.lineSegment(v5, v3)
        res = (line, shapes.Point(2, 0))
        self.assertEqual(operations.intersection(rec1, rec2), res)
    
    def test_for_rectangle_and_polygon1(self):
        """the first test for intersection between a polygon and a
        rectangle with the rectangle being located inside the polygon
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-0.5, 0)
        v7 = shapes.Point(0, 0.5)
        v8 = shapes.Point(0.5, 0)
        v9 = shapes.Point(0, -0.5)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        self.assertEqual(operations.intersection(rec, pol), None)
    
    def test_for_rectangle_and_polygon2(self):
        """the second test for intersection between a polygon and a
        rectangle with them touching each other on a single point
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-2, -1)
        v7 = shapes.Point(-1, -1)
        v8 = shapes.Point(-1, 1)
        v9 = shapes.Point(-2, 1)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        self.assertEqual(operations.intersection(rec, pol), v1)
    
    def test_for_rectangle_and_polygon3(self):
        """the third test for intersection between a polygon and a
        rectangle with them being completely apart
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(5, 0)
        v7 = shapes.Point(6, 0)
        v8 = shapes.Point(6, 1)
        v9 = shapes.Point(5, 1)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        self.assertEqual(operations.intersection(rec, pol), None)
    
    def test_for_rectangle_and_polygon4(self):
        """the fourth test for intersection between a polygon and a
        rectangle with of their edges intersect each other
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(0.5, 0)
        v7 = shapes.Point(1.5, 0)
        v8 = shapes.Point(1.5, 0.5)
        v9 = shapes.Point(0.5, 0.5)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        self.assertEqual(operations.intersection(rec, pol), shapes.Point(0, 1))
    
    def test_for_rectangle_and_polygon5(self):
        """the fifth test for intersection between a polygon and a
        rectangle with overlapping edges
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 1)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(0.5, -1)
        v7 = shapes.Point(1.5, -1)
        v8 = shapes.Point(1.5, -2)
        v9 = shapes.Point(0.5, -2)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        line = shapes.lineSegment(v6, v3)
        self.assertEqual(operations.intersection(rec, pol), line)
    
    def test_for_rectangle_and_circle1(self):
        """the first test for intersection between a rectangle and a
        circle with the given circle being inside the given rectangle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 0), 0.5)
        self.assertEqual(operations.intersection(rec, circle), None)
    
    def test_for_rectangle_and_circle2(self):
        """the second test for intersection between a rectangle and a
        circle with them the given circle touching the given rectangle
        on its vertex
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(3, 3), 1)
        self.assertEqual(operations.intersection(rec, circle), v3)
    
    def test_for_rectangle_and_circle3(self):
        """the third test for intersection between a rectangle and a
        circle with them touching each other in two points on different
        edges
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(3, 3), 3)
        res = (shapes.Point(3, 0), shapes.Point(0, 3))
        self.assertEqual(operations.intersection(rec, circle), res)
    
    def test_for_rectangle_and_line1(self):
        """the first test for intersection between a rectangle and an
        infinite line with them not intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        line = shapes.Line(1, 6)
        self.assertEqual(operations.intersection(rec, line), None)
    
    def test_for_rectangle_and_line2(self):
        """the second test for intersection between a rectangle and an
        infinite line with them intersecting in two points and the
        given line being horizental
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        line = shapes.Line(0, 0)
        res = (shapes.Point(2, 0), shapes.Point(-2, 0))
        self.assertEqual(operations.intersection(rec, line), res)
    
    def test_for_rectangle_and_line2(self):
        """the third test for intersection between a rectangle and an
        infinite line with them intersecting in two points and the
        given line being vertical
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 1))
        res = (shapes.Point(0, 2), shapes.Point(0, -2))
        self.assertEqual(operations.intersection(rec, line), res)
    
    def test_for_rectangle_and_line4(self):
        """the fourth test for intersection between a rectangle and an
        infinite line with them intersecting in two points and the
        given line having an arbitrary slope
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        line = shapes.Line(0, 1)
        res = (v1, v3)
        self.assertEqual(operations.intersection(rec, line), res)
    
    def test_for_rectangle_and_line5(self):
        """the fifth test for intersection between a rectangle and an
        infinite line with the given line overlapping with one the
        edges of the given rectangle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        line = shapes.Line(2, 0)
        res = shapes.LineSegment(v2, v3)
        self.assertEqual(operations.intersection(rec, line), res)
    
    def test_for_rectangle_and_linesegment1(self):
        """the first test for intersection between a rectangle and a line
        segment with the line segment being inside the given rectangle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0.5, 0.5)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(rec, line), None)
    
    def test_for_rectangle_and_linesegment2(self):
        """the second test for intersection between a rectangle and a
        line segment with one end of the line segment touching an edge
        of the given rectangle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        end1 = shapes.Point(2, 0)
        end2 = shapes.Point(2.5, 0.5)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(rec, line), end1)
    
    def test_for_rectangle_and_linesegment3(self):
        """the third test for intersection between a rectangle and a line
        segment with one end of the given line segment being touching a
        vertex of the given rectangle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        end1 = v4
        end2 = shapes.Point(0.5, 0.5)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(rec, line), v4)
    
    def test_for_rectangle_and_linesegment4(self):
        """the fourth test for intersection between a rectangle and a
        line segment with the given line segment overlapping an edge of
        the given rectangle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        end1 = shapes.Point(2, 0)
        end2 = shapes.Point(2, 4)
        line = shapes.LineSegment(end1, end2)
        res = shapes.LineSegment(end1, v3)
        self.assertEqual(operations.intersection(rec, line), res)
    
    def test_for_rectangle_and_linesegment5(self):
        """the fifth test for intersection between a rectangle and a line
        segment with the given line segment intersecting the given
        rectangle in two points
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        end1 = shapes.Point(-4, 0)
        end2 = shapes.Point(4, 0)
        line = shapes.LineSegment(end1, end2)
        res = (shapes.Point(-2, 0), shapes.Point(2, 0))
        self.assertEqual(operations.intersection(rec, line), res)