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
    
    def test_for_polygon_and_line3(self):
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
    
    def test_for_rectangle_and_line3(self):
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
    
    def test_for_circle_and_point1(self):
        """the first first test for intersection between a point and a
        circle with the given point being located inside the given
        circle
        """
        
        point = shapes.Point(0, 0.5)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.intersection(circle, point), None)
    
    def test_for_circle_and_point2(self):
        """the second test for intersection between a point and a
        circle with the given point being located on the given circle's
        perimeter
        """
        
        point = shapes.Point(0, 1)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.intersection(circle, point), point)
    
    def test_for_circle_and_point3(self):
        """the third test for intersection between a point and a circle
        with the given point being located outside the given circle
        """
        
        point = shapes.Point(0, 5)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.intersection(circle, point), None)
    
    def test_for_circle_and_polygon1(self):
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
        self.assertEqual(operations.intersection(circle, pol), None)
    
    def test_for_circle_and_polygon2(self):
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
        self.assertEqual(operations.intersection(circle, pol), v1)
    
    def test_for_circle_and_polygon3(self):
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
        self.assertEqual(operations.intersection(circle, pol), res)
    
    def test_for_circle_and_rectangle1(self):
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
    
    def test_for_circle_and_rectangle2(self):
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
    
    def test_for_circle_and_rectangle3(self):
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
    
    def test_for_circle_and_circle1(self):
        """the first test for intersection between two circles with one
        of them being inside another
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 2)
        circle2 = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.intersection(circle1, circle2), None)
    
    def test_for_circle_and_circle2(self):
        """the second test for intersection between two circles with
        them touching each other in one point
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 2)
        circle2 = shapes.Circle(shapes.Point(3, 0), 1)
        point = shapes.Point(2, 0)
        self.assertEqual(operations.intersection(circle1, circle2), point)
    
    def test_for_circle_and_circle3(self):
        """the third test for intersection between two circles with
        them intersecting each other in two points
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 2)
        circle2 = shapes.Circle(shapes.Point(2, 2), 2)
        res = (shapes.Point(2, 0), shapes.Point(0, 2))
        self.assertEqual(operations.intersection(circle1, circle2), res)
    
    def test_for_circle_and_circle4(self):
        """the fourth test for intersection between two circles with
        them being totally apart
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 2)
        circle2 = shapes.Circle(shapes.Point(4, 4), 1)
        self.assertEqual(operations.intersection(circle1, circle2), None)
    
    def test_for_circle_and_line1(self):
        """the first test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        being horizental
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(0, 1)
        point = shapes.Point(0, 1)
        self.assertEqual(operations.intersection(circle, line), point)
    
    def test_for_circle_and_line2(self):
        """the second test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        being vertical
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line.from_points(shapes.Point(1, -1), shapes.Point(1, 1))
        point = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(circle, line), point)
    
    def test_for_circle_and_line3(self):
        """the third test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        having an arbitrary slope
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(1, -1*np.sqrt(2))
        point = shapes.Point(np.sqrt(2)/2, -1*np.sqrt(2)/2)
        self.assertEqual(operations.intersection(circle, line), point)
    
    def test_for_circle_and_line4(self):
        """the fourth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        being horizental
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(0, 0)
        res = (shapes.Point(-1, 0), shapes(1, 0))
        self.assertEqual(operations.intersection(circle, line), res)
    
    def test_for_circle_and_line5(self):
        """the fifth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        being vertical
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 10))
        res = (shapes.Point(-1, 0), shapes.Point(1, 0))
        self.assertEqual(operations.intersection(circle, line), res)
    
    def test_for_circle_and_line6(self):
        """the sixth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        having an arbitrary slope
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(1, 0)
        res = (shapes.Point(np.sqrt(2)/2, np.sqrt(2)/2), shapes.Point(-1*np.sqrt(2)/2, -1*np.sqrt(2)/2))
        self.assertEqual(operations.intersection(circle, line), res)
    
    def test_for_circle_and_line7(self):
        """the seventh test for intersection between a circle and an
        infinite line with them being apart
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(1, 10)
        self.assertEqual(operations.intersection(circle, line), None)
    
    def test_for_circle_and_linesegment1(self):  
        """the first test for intersection between a circle and a line
        segment with the line segment being located fully inside the
        circle
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(-1, -1)
        end2 = shapes.Point(1, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(circle, line), None)
    
    def test_for_circle_and_linesegment2(self):
        """the second test for intersection between a circle and a line
        segment with them intersecting in one point
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        point = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(circle, line), point)
    
    def test_for_circle_and_linesegment3(self):
        """the third test for intersection between a circle and a line
        segment with them intersecting in two points
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(0, 10)
        end2 = shapes.Point(0, -3)
        line = shapes.LineSegment(end1, end2)
        res = (shapes.Point(0, 1), shapes.Point(0, -1))
        self.assertEqual(operations.intersection(circle, line), res)
    
    def test_for_circle_and_linesegment4(self):
        """the fourth test for intersection between a circle and a line
        segment with them being fully apart
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(5, 5)
        end2 = shapes.Point(6, 6)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(circle, line), None)
    
    def test_for_circle_and_linesegment5(self):
        """the fifth test for intersection between a circle and a line
        segment with one of the line's ends touching the perimeter of
        the circle
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(1, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(circle, line), shapes.Point(1, 0))
    
    def test_for_circle_and_linesegment6(self):
        """the sixth test for intersection between a circle and a line
        segment with them touching in one point on the line's body
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(1, 1)
        end2 = shapes.Point(1, -1)
        line = shapes.LineSegment(end1, end2)
        point = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(circle, line), point)
    
    def test_for_line_and_point1(self):
        """the first test for intersection between a point and an
        infinite line with the given line being horizental and the
        given point being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.Line(0, 0)
        self.assertEqual(operations.intersection(line, point), point)
    
    def test_for_line_and_point2(self):
        """the second test for intersection between a point and an
        infinite line with the given line being vertical and the given
        point being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 1))
        self.assertEqual(operations.intersection(line, point), point)
    
    def test_for_line_and_point3(self):
        """the third test for intersection between a point and an
        infinite line with the given line being horizental and the
        given point not being located on that line
        """
        
        point = shapes.Point(0, 1)
        line = shapes.Line(0, 0)
        self.assertEqual(operations.intersection(line, point), None)
    
    def test_for_line_and_point4(self):
        """the fourth test for intersection between a point and an
        infinite line with the given line being vertical and the given
        point not being located on that line
        """
        
        point = shapes.Point(1, 0)
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 1))
        self.assertEqual(operations.intersection(line, point), point)
    
    def test_for_line_and_point5(self):
        """the fifth test for intersection between a point and an
        infinite line with the given line having an arbitrary slope
        and the given point being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.Line(1, 0)
        self.assertEqual(operations.intersection(line, point), point)
    
    def test_for_line_and_point6(self):
        """the sixth test for intersection between a point and an
        infinite line with the given line having an arbitrary slope
        and the given point not being located on that line
        """
        
        point = shapes.Point(1, 0)
        line = shapes.Line(1, 0)
        self.assertEqual(operations.intersection(point, line), None)
    
    def test_for_line_and_polygon1(self):
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
        self.assertEqual(operations.intersection(line, pol), None)
    
    def test_for_line_and_polygon2(self):
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
        self.assertEqual(operations.intersection(line, pol), res)
    
    def test_for_line_and_polygon3(self):
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
        self.assertEqual(operations.intersection(line, pol), res)
    
    def test_for_line_and_polygon4(self):
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
        self.assertEqual(operations.intersection(line, pol), res)
    
    def test_for_line_and_polygon5(self):
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
        self.assertEqual(operations.intersection(line, pol), res)
    
    def test_for_line_and_rectangle1(self):
        """the first test for intersection between a rectangle and an
        infinite line with them not intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        line = shapes.Line(1, 6)
        self.assertEqual(operations.intersection(line, rec), None)
    
    def test_for_line_and_rectangle2(self):
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
        self.assertEqual(operations.intersection(line, rec), res)
    
    def test_for_line_and_rectangle3(self):
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
        self.assertEqual(operations.intersection(line, rec), res)
    
    def test_for_line_and_rectangle4(self):
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
        self.assertEqual(operations.intersection(line, rec), res)
    
    def test_for_line_and_rectangle5(self):
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
        self.assertEqual(operations.intersection(line, rec), res)
    
    def test_for_line_and_circle1(self):
        """the first test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        being horizental
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(0, 1)
        point = shapes.Point(0, 1)
        self.assertEqual(operations.intersection(line, circle), point)
    
    def test_for_line_and_circle2(self):
        """the second test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        being vertical
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line.from_points(shapes.Point(1, -1), shapes.Point(1, 1))
        point = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(line, circle), point)
    
    def test_for_line_and_circle3(self):
        """the third test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        having an arbitrary slope
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(1, -1*np.sqrt(2))
        point = shapes.Point(np.sqrt(2)/2, -1*np.sqrt(2)/2)
        self.assertEqual(operations.intersection(line, circle), point)
    
    def test_for_line_and_circle4(self):
        """the fourth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        being horizental
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(0, 0)
        res = (shapes.Point(-1, 0), shapes(1, 0))
        self.assertEqual(operations.intersection(line, circle), res)
    
    def test_for_line_and_circle5(self):
        """the fifth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        being vertical
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 10))
        res = (shapes.Point(-1, 0), shapes.Point(1, 0))
        self.assertEqual(operations.intersection(line, circle), res)
    
    def test_for_line_and_circle6(self):
        """the sixth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        having an arbitrary slope
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(1, 0)
        res = (shapes.Point(np.sqrt(2)/2, np.sqrt(2)/2), shapes.Point(-1*np.sqrt(2)/2, -1*np.sqrt(2)/2))
        self.assertEqual(operations.intersection(line, circle), res)
    
    def test_for_line_and_circle7(self):
        """the seventh test for intersection between a circle and an
        infinite line with them being apart
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(1, 10)
        self.assertEqual(operations.intersection(line, circle), None)
    
    def test_for_line_and_line1(self):
        """the first test for intersection between two lines with them
        being horizental and parallel
        """
        
        line1 = shapes.Line(0, 0)
        line2 = shapes.Line(0, 1)
        self.assertEqual(operations.intersection(line1, line2), None)
    
    def test_for_line_and_line2(self):
        """the second test for intersection between two lines with them
        being vertical and parallel
        """
        
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        line1 = shapes.Line.from_points(point1, point2)
        point3 = shapes.Point(1, 0)
        point4 = shapes.Point(1, 1)
        line2 = shapes.Line.from_points(point3, point4)
        self.assertEqual(operations.intersection(line1, line2), None)
    
    def test_for_line_and_line3(self):
        """the third test for intersection between two lines with them
        intersecting each other with one being horizental and the other
        vertical
        """
        
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        line1 = shapes.Line.from_points(point1, point2)
        line2 = shapes.Line(0, 0)
        self.assertEqual(operations.intersection(line1, line2), point1)
    
    def test_for_line_and_line4(self):
        """the fourth test for intersection between two lines with them
        having arbitrary slopes but parallel to each other
        """
        
        line1 = shapes.Line(1, 0)
        line2 = shapes.Line(1, 1)
        self.assertEqual(operations.intersection(line1, line2), None)
    
    def test_for_line_and_line5(self):
        """the fifth test for intersection between two lines with them
        overlapping each other
        """
        
        line1 = shapes.Line(1, 1)
        line2 = shapes.Line(1, 1)
        self.assertEqual(operations.intersection(line1, line2), line1)
    
    def test_for_line_and_line6(self):
        """the sixth test for intersection between two lines with them
        having unequal arbitrary slopes
        """
        
        line1 = shapes.Line(1, 0)
        line2 = shapes.Line(-1, 0)
        point = shapes.Point(0, 0)
        self.assertEqual(operations.intersection(line1, line2), point)
    
    def test_for_line_and_linesegment1(self):
        """the first test for intersection between an infinite line and
        a line segment with the line being horizental and the line
        segment not touching it with an unequal slope in comparison to
        the line
        """
        
        line = shapes.Line(0, 0)
        end1 = shapes.Point(1, 1)
        end2 = shapes.Point(2, 2)
        lineseg = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(line, lineseg), None)
    
    def test_for_line_and_linesegment2(self):
        """the second test for intersection between an infinite line
        and a line segment with the line having an arbitrary slope and
        one of the line segment's ends being located on the infinite
        line
        """
        
        line = shapes.Line(1, 0)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        lineseg = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(line, lineseg), end1)
    
    def test_for_line_and_linesegment3(self):
        """the third test for intersection between an infinite line and
        a line segment with them overlapping and being vertical
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        lineseg = shapes.LineSegment(end1, end2)
        line = lineseg.infinite
        self.assertEqual(operations.intersection(line, lineseg), lineseg)
    
    def test_for_line_and_linesegment4(self):
        """the fourth test for intersection between an infinite line
        and a line segment with them overlapping and being vertical
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        lineseg = shapes.LineSegment(end1, end2)
        line = lineseg.infinite
        self.assertEqual(operations.intersection(line, lineseg), lineseg)
    
    def test_for_line_and_linesegment5(self):
        """the fifth test for intersection between an infinite line and and
        a line segment with them overlapping and having an arbitrary slope
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        lineseg = shapes.LineSegment(end1, end2)
        line = lineseg.infinite
        self.assertEqual(operations.intersection(line, lineseg), lineseg)
    
    def test_for_line_and_linesegment6(self):
        """the sixth test for intersection between an infinite line and
        a line segment having arbitrary slopes and intersecting each
        other
        """
        
        end1 = shapes.Point(-1, 1)
        end2 = shapes.Point(1, -1)
        lineseg = shapes.LineSegment(end1, end2)
        line = shapes.Line(1, 0)
        point = shapes.Point(0, 0)
        self.assertEqual(operations.intersection(line, lineseg), point)
    
    def test_for_linesegment_and_point1(self):
        """the first test for intersection between a point and a line
        segment with the given line being horizental and the given
        point being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.LineSegment(shapes.Point(0, 0), shapes.Point(1, 0))
        self.assertEqual(operations.intersection(line, point), point)
    
    def test_for_linesegment_and_point2(self):
        """the second test for intersection between a point and a line
        segment with the given line being vertical and the given point
        being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.LineSegment(shapes.Point(0, -0.5), shapes.Point(0, 0.5))
        self.assertEqual(operations.intersection(line, point), point)
    
    def test_for_linesegment_and_point3(self):
        """the third test for intersection between a point and a line
        segment with the given line being horizental and the given
        point not being located on that line
        """
        
        point = shapes.Point(0, 1)
        line = shapes.LineSegment(shapes.Point(0, 0), shapes.Point(1, 0))
        self.assertEqual(operations.intersection(line, point), None)
    
    def test_for_linesegment_and_point4(self):
        """the fourth test for intersection between a point and a line
        segment with the given line being vertical and the given point
        not being located on that line
        """
        
        point = shapes.Point(1, 0)
        line = shapes.LineSegment(shapes.Point(0, -0.5), shapes.Point(0, 0.5))
        self.assertEqual(operations.intersection(line, point), point)
    
    def test_for_linesegment_and_point5(self):
        """the fifth test for intersection between a point and a line
        segment with the given line having an arbitrary slope and the
        given point being located on that line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.LineSegment(shapes.Point(-0.5, -0.5), shapes.Point(0.5, 0.5))
        self.assertEqual(operations.intersection(line, point), point)
    
    def test_for_linesegment_and_point6(self):
        """the sixth test for intersection between a point and a line
        segment with the given line having an arbitrary slope and the
        given point not being located on that line
        """
        
        point = shapes.Point(1, 0)
        line = shapes.LineSegment(shapes.Point(0, -0.5), shapes.Point(0, 0.5))
        self.assertEqual(operations.intersection(line, point), None)
    
    def test_for_linesegment_and_polygon1(self):
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
        self.assertEqual(operations.intersection(line, pol), None)
    
    def test_for_linesegment_and_polygon2(self):
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
        self.assertEqual(operations.intersection(line, pol), end1)
    
    def test_for_linesegment_and_polygon3(self):
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
        self.assertEqual(operations.intersection(line, pol), v4)
    
    def test_for_linesegment_and_polygon4(self):
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
        self.assertEqual(operations.intersection(line, pol), res)
    
    def test_for_linesegment_and_polygon5(self):
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
        self.assertEqual(operations.intersection(line, pol), res)
    
    def test_for_linesegment_and_rectangle1(self):
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
        self.assertEqual(operations.intersection(line, rec), None)
    
    def test_for_linesegment_and_rectangle2(self):
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
        self.assertEqual(operations.intersection(line, rec), end1)
    
    def test_for_linesegment_and_rectangle3(self):
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
        self.assertEqual(operations.intersection(line, rec), v4)
    
    def test_for_linesegment_and_rectangle4(self):
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
        self.assertEqual(operations.intersection(line, rec), res)
    
    def test_for_linesegment_and_rectangle5(self):
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
        self.assertEqual(operations.intersection(line, rec), res)
    
    def test_for_linesegment_and_circle1(self):  
        """the first test for intersection between a circle and a line
        segment with the line segment being located fully inside the
        circle
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(-1, -1)
        end2 = shapes.Point(1, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(line, circle), None)
    
    def test_for_linesegment_and_circle2(self):
        """the second test for intersection between a circle and a line
        segment with them intersecting in one point
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        point = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(line, circle), point)
    
    def test_for_linesegment_and_circle3(self):
        """the third test for intersection between a circle and a line
        segment with them intersecting in two points
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(0, 10)
        end2 = shapes.Point(0, -3)
        line = shapes.LineSegment(end1, end2)
        res = (shapes.Point(0, 1), shapes.Point(0, -1))
        self.assertEqual(operations.intersection(line, circle), res)
    
    def test_for_linesegment_and_circle4(self):
        """the fourth test for intersection between a circle and a line
        segment with them being fully apart
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(5, 5)
        end2 = shapes.Point(6, 6)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(line, circle), None)
    
    def test_for_linesegment_and_circle5(self):
        """the fifth test for intersection between a circle and a line
        segment with one of the line's ends touching the perimeter of
        the circle
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(1, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(line, circle), shapes.Point(1, 0))
    
    def test_for_linesegment_and_circle6(self):
        """the sixth test for intersection between a circle and a line
        segment with them touching in one point on the line's body
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(1, 1)
        end2 = shapes.Point(1, -1)
        line = shapes.LineSegment(end1, end2)
        point = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(line, circle), point)
    
    def test_for_linesegment_and_line1(self):
        """the first test for intersection between an infinite line and
        a line segment with the line being horizental and the line
        segment not touching it with an unequal slope in comparison to
        the line
        """
        
        line = shapes.Line(0, 0)
        end1 = shapes.Point(1, 1)
        end2 = shapes.Point(2, 2)
        lineseg = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(lineseg, line), None)
    
    def test_for_linesegment_and_line2(self):
        """the second test for intersection between an infinite line
        and a line segment with the line having an arbitrary slope and
        one of the line segment's ends being located on the infinite
        line
        """
        
        line = shapes.Line(1, 0)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        lineseg = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(lineseg, line), end1)
    
    def test_for_linesegment_and_line3(self):
        """the third test for intersection between an infinite line and
        a line segment with them overlapping and being vertical
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        lineseg = shapes.LineSegment(end1, end2)
        line = lineseg.infinite
        self.assertEqual(operations.intersection(lineseg, line), lineseg)
    
    def test_for_lineseg_and_line4(self):
        """the fourth test for intersection between an infinite line
        and a line segment with them overlapping and being vertical
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        lineseg = shapes.LineSegment(end1, end2)
        line = lineseg.infinite
        self.assertEqual(operations.intersection(lineseg, line), lineseg)
    
    def test_for_linesegment_and_line5(self):
        """the fifth test for intersection between an infinite line and and
        a line segment with them overlapping and having an arbitrary slope
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        lineseg = shapes.LineSegment(end1, end2)
        line = lineseg.infinite
        self.assertEqual(operations.intersection(lineseg, line), lineseg)
    
    def test_for_linesegment_and_line6(self):
        """the sixth test for intersection between an infinite line and
        a line segment having arbitrary slopes and intersecting each
        other
        """
        
        end1 = shapes.Point(-1, 1)
        end2 = shapes.Point(1, -1)
        lineseg = shapes.LineSegment(end1, end2)
        line = shapes.Line(1, 0)
        point = shapes.Point(0, 0)
        self.assertEqual(operations.intersection(lineseg, line), point)
    
    def test_for_linesegment_and_linesegment1(self):
        """the first test for intersection between two line segments
        with them being horizental and partly overlapped each other
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(-1, 0)
        end4 = shapes.Point(1, 0)
        line2 = shapes.LineSegment(end3, end4)
        line3 = shapes.LineSegment(end1, end4)
        self.assertEqual(operations.intersection(line1, line2), line3)
    
    def test_for_linesegment_and_linesegment2(self):
        """the second test for intersection between two line segments
        with them fully overlap each other
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0)
        line1 = shapes.LineSegment(end1, end2)
        line2 = shapes.LineSegment(end1, end2)
        line3 = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(line1, line2), line3)
    
    def test_for_linesegment_and_linesegment3(self):
        """the third test for intersection between two line segments
        with them having arbitrary and unequal inclinations and not
        intersecting each other
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(5, 7)
        end4 = shapes.Point(8, 4)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.intersection(line1, line2), None)
    
    def test_for_linesegment_and_linesegment(self):
        """the fourth test for intersection between two line segments
        with them having arbitrary inclinations and intersect each
        other
        """
        
        end1 = shapes.Point(-1, 1)
        end2 = shapes.Point(1, -1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(-1, -1)
        end4 = shapes.Point(1, 1)
        line2 = shapes.LineSegment(end3, end4)
        point = shapes.Point(0, 0)
        self.assertEqual(operations.intersection(line1, line2), point)


class TestIsInside(unittest.TestCase):
    """test cases for 'is_inside()" function
    """
    
    def test_for_point_and_point(self):
        """testing if a point is located inside another point with the
        same coordinates
        """
        
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 0)
        self.assertFalse(operations.is_inside(point1, point2))
    
    def test_for_point_and_polygon1(self):
        """the first test for checking if a given point is inside a
        given polygon, with the point being located inside the polygon
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        self.assertTrue(operations.is_inside(point, pol))
    
    def test_for_point_and_polygon2(self):
        """the second test for checking if a given point is inside a
        given polygon, with the point being located on the perimeter of
        the polygon
        """
        
        point = shapes.Point(0.5, -1)
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        self.assertFalse(operations.is_inside(point, pol))
    
    def test_for_point_and_polygon3(self):
        """the third test for checking if a given point is inside a
        given polygon, with the point being located outside the polygon
        """
        
        point = shapes.Point(5, 5)
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        self.assertFalse(operations.is_inside(point, pol))
    
    def test_for_point_and_rectangle1(self):
        """the first test for checking if a given point is inside a
        given rectangle, with the point being located inside the
        rectangle
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Polygon(v1, v2, v3, v4)
        self.assertTrue(operations.is_inside(point, rec))
    
    def test_for_point_and_rectangle2(self):
        """the second test for checking if a given point is inside a
        given rectangle, with the point being located on the perimeter of
        the rectangle
        """
        
        point = shapes.Point(0.5, -1)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Polygon(v1, v2, v3, v4)
        self.assertFalse(operations.is_inside(point, rec))
    
    def test_for_point_and_rectangle3(self):
        """the third test for checking if a given point is inside a
        given rectangle with the point being located outside the
        rectangle
        """
        
        point = shapes.Point(5, 5)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Polygon(v1, v2, v3, v4)
        self.assertFalse(operations.is_inside(point, rec))
    
    def test_for_point_and_circle1(self):
        """the first test for checking if a given point is inside a
        given circle, with the point being located inside the circle
        """
        
        point = shapes.Point(0, 0)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertTrue(operations.is_inside(point, circle))
    
    def test_for_point_and_circle2(self):
        """the second test for checking if a given point is inside a
        given circle, with the point being located on the perimeter of
        the circle
        """
        
        point = shapes.Point(0, -1)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(point, circle))
    
    def test_for_point_and_circle3(self):
        """the third test for checking if a given point is inside a
        given circle with the point being located outside the circle
        """
        
        point = shapes.Point(5, 5)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(point, circle))
    
    def test_for_point_and_line(self):
        """testing if a given point is located inside a given infinite
        line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.Line(0, 0)
        self.assertFalse(operations.is_inside(point, line))
    
    def test_for_point_and_linesegment(self):
        """testing if a given point is located inside a given line
        segment
        """
        
        point = shapes.Point(0, 0)
        end1 = shapes.Point(0, 1)
        end2 = shapes.Point(0, -1)
        line = shapes.LineSegment(end1, end2)
        self.assertFalse(operations.is_inside(point, line))
    
    def test_for_polygon_and_point1(self):
        """the first test for checking if a given polygon is inside a
        given point, with the point being located inside the polygon
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        self.assertFalse(operations.is_inside(pol, point))
    
    def test_for_polygon_and_point2(self):
        """the second test for checking if a given polygon is inside a
        given point, with the point being located on the perimeter of
        the polygon
        """
        
        point = shapes.Point(0.5, -1)
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        self.assertFalse(operations.is_inside(pol, point))
    
    def test_for_polygon_and_point3(self):
        """the third test for checking if a given polygon is inside a
        given point, with the point being located outside the polygon
        """
        
        point = shapes.Point(5, 5)
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        self.assertFalse(operations.is_inside(pol, point))
    
    def test_for_polygon_and_polygon1(self):
        """the first test to check if a polygon is located inside
        another polygon, with the first one being fully inside the
        second one
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-0.5, 0)
        v7 = shapes.Point(0.5, 0)
        v8 = shapes.Point(0, 0.5)
        pol2 = shapes.Polygon(v6, v7, v8)
        self.assertTrue(operations.is_inside(pol2, pol1))
    
    def test_for_polygon_and_polygon2(self):
        """the second test to check if a given polygon is located
        inside another given polygon, with the second one being loceted
        inside the first one
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-0.5, 0)
        v7 = shapes.Point(0.5, 0)
        v8 = shapes.Point(0, 0.5)
        pol2 = shapes.Polygon(v6, v7, v8)
        self.assertFalse(operations.is_inside(pol1, pol2))
    
    def test_for_polygon_and_polygon3(self):
        """the third test for checking if a given polygon is located
        inside another given polygon with the first one being inside
        the second one but touching it in one vertex
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-0.5, 0)
        v7 = shapes.Point(0.5, 0)
        v8 = shapes.Point(0, 1)
        pol2 = shapes.Polygon(v6, v7, v8)
        self.assertFalse(operations.is_inside(pol2, pol1))
    
    def test_for_polygon_and_polygon4(self):
        """the fourth test for checking if a given polygon is located
        inside another polygon with their edges intersecting each other
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-0.5, -3)
        v7 = shapes.Point(-0.5, 3)
        v8 = shapes.Point(-5, 0)
        pol2 = shapes.Polygon(v6, v7, v8)
        self.assertFalse(operations.is_inside(pol2, pol1))
    
    def test_for_polygon_and_polygon5(self):
        """the fifth test for checking if a given polygon is located
        inside another polygon with them being fully apart
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-5, 5)
        v7 = shapes.Point(-5, 6)
        v8 = shapes.Point(-4, 5.5)
        pol2 = shapes.Polygon(v6, v7, v8)
        self.assertFalse(operations.is_inside(pol2, pol1))
    
    def test_for_polygon_and_rectangle1(self):
        """the first test to check if a polygon is located inside
        a given rectangle, with the polygon being fully inside the
        rectangle
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-10, -10)
        v7 = shapes.Point(10, -10)
        v8 = shapes.Point(10, 10)
        v9 = shapes.Point(-10, 10)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        self.assertTrue(operations.is_inside(pol, rec))
    
    def test_for_polygon_and_rectangle2(self):
        """the second test to check if a given polygon is located
        inside the given rectangle, with the rectangle being loceted
        inside the polygon
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-0.1, -0.1)
        v7 = shapes.Point(0.1, -0.1)
        v8 = shapes.Point(0.1, 0.1)
        v9 = shapes.Point(-0.1, 0.1)
        rec = shapes.Rectangle(v6, v7, v8, v9)
        self.assertFalse(operations.is_inside(pol, rec))
    
    def test_for_polygon_and_rectangle3(self):
        """the third test for checking if a given polygon is located
        inside a given rectanle with the polygon being inside
        the rectangle but touching it in one vertex
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-1, 2)
        v7 = shapes.Point(-1, -2)
        v8 = shapes.Point(4, -2)
        v9 = shapes.Point(4, 2)
        rec = shapes.Rectgangle(v6, v7, v8, v9)
        self.assertFalse(operations.is_inside(pol, rec))
    
    def test_for_polygon_and_rectangle4(self):
        """the fourth test for checking if a given polygon is located
        inside a given rectangle with their edges intersecting each other
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(-0.5, 2)
        v7 = shapes.Point(-0.5, -2)
        v8 = shapes.Point(4, -2)
        v9 = shapes.Point(4, 2)
        rec = shapes.Rectgangle(v6, v7, v8, v9)
        self.assertFalse(operations.is_inside(pol, rec))
    
    def test_for_polygon_and_rectangle5(self):
        """the fifth test for checking if a given polygon is located
        inside a given rectangle with them being fully apart
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        v6 = shapes.Point(3.5, 2)
        v7 = shapes.Point(3.5, -2)
        v8 = shapes.Point(4, -2)
        v9 = shapes.Point(4, 2)
        rec = shapes.Rectgangle(v6, v7, v8, v9)
        self.assertFalse(operations.is_inside(pol, rec))
    
    def test_for_polygon_and_circle1(self):
        """the first test for checking if a polygon is located inside
        a given circle with the polygon being located inside the circle
        completely
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        circle = shapes.Circle(shapes.Point(0, 0), 5)
        self.assertTrue(operations.is_inside(pol, circle))
    
    def test_for_polygon_and_circle2(self):
        """the second test for checking if a given polygon is located
        inside a given circle with the circle being completely inside
        the polygon
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        circle = shapes.Circle(shapes.Point(0, 0), 0.1)
        self.assertFalse(operations.is_inside(pol, circle))
    
    def test_for_polygon_and_circle3(self):
        """the third test for checking if a given polygon is located
        inside a given circle with the polygon being inside the circle
        but with one vertex touching the circle's perimeter
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -0.1)
        v3 = shapes.Point(0.1, -0.1)
        v4 = shapes.Point(0.1, 0)
        v5 = shapes.Point(0, 0.1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(pol, circle))
    
    def test_for_polygon_and_circle4(self):
        """the fourth test for checking if a given polygon is located
        inside a given circle with the polygon being partly inside the
        circle but intersecting with it
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(pol, circle))
    
    def test_for_polygon_and_circle5(self):
        """the fifth test for checking if a given polygon is located
        inside a given circle with them being fully apart
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        circle = shapes.Circle(shapes.Point(5, 5), 1)
        self.assertFalse(operations.is_inside(pol, circle))
    
    def test_for_polygon_and_line(self):
        """test for checking if a given polygon is located inside a
        given line which should always return False
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        line = shapes.Line(1, 0)
        self.assertFalse(operations.is_inside(pol, line))
    
    def test_for_polygon_and_linesegment(self):
        """test for checking if a given polygon is located inside a
        given line segment which should always return False
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(0, -1)
        v3 = shapes.Point(1, -1)
        v4 = shapes.Point(1, 0)
        v5 = shapes.Point(0, 1)
        pol = shapes.Polygon(v1, v2, v3, v4, v5)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertFalse(operations.is_inside(pol, line))
    
    def test_for_rectangle_and_point(self):
        """test for checking if a given rectangle is located inside a
        given point which should always return False
        """
        
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        point = shapes.Point(0, 0)
        self.assertFalse(operations.is_inside(rec, point))
    
    def test_for_rectangle_and_polygon1(self):
        """the first test for checking if a given rectangle is located
        inside a given polygon with the rectangle being fully inside
        the polygon
        """
        
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-2, -2)
        v6 = shapes.Point(0, -4)
        v7 = shapes.Point(2, -2)
        v8 = shapes.Point(2, 2)
        v9 = shapes.Point(0, 4)
        v10 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v5, v6, v7, v8, v9, v10)
        self.assertTrue(operations.is_inside(rec, pol))
    
    def test_for_rectangle_and_polygon2(self):
        """the second test for checking if a given rectangle is located
        inside a givevn polygon with the polygon being fully inside the
        rectangel
        """
        
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-0.2, -0.2)
        v6 = shapes.Point(0, -0.4)
        v7 = shapes.Point(0.2, -0.2)
        v8 = shapes.Point(0.2, 0.2)
        v9 = shapes.Point(0, 0.4)
        v10 = shapes.Point(-0.2, 0.2)
        pol = shapes.Polygon(v5, v6, v7, v8, v9, v10)
        self.assertFalse(operations.is_inside(rec, pol))
    
    def test_for_rectangle_and_polygon3(self):
        """the third test for checking if a given rectangle is located
        inside a given polygon with the rectangle being inside the
        polygon but with two of its vertices touching the polygon's
        perimeter
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-2, -2)
        v6 = shapes.Point(0, -4)
        v7 = shapes.Point(2, -2)
        v8 = shapes.Point(2, 2)
        v9 = shapes.Point(0, 4)
        v10 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v5, v6, v7, v8, v9, v10)
        self.assertFalse(operations.is_inside(rec, pol))
    
    def test_for_rectangle_and_polygon4(self):
        """the fourth test for checking if a given rectangle is located
        inside a given polygon with them intersecting each other's
        edges
        """
        
        v1 = shapes.Point(-3, 0)
        v2 = shapes.Point(0, -3)
        v3 = shapes.Point(3, 0)
        v4 = shapes.Point(0, 3)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-2, -2)
        v6 = shapes.Point(0, -4)
        v7 = shapes.Point(2, -2)
        v8 = shapes.Point(2, 2)
        v9 = shapes.Point(0, 4)
        v10 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v5, v6, v7, v8, v9, v10)
        self.assertFalse(operations.is_inside(rec, pol))
    
    def test_for_rectangle_and_polygon5(self):
        """the fifth test for checking if a given rectangle is located
        inside a given polygon with them being fully apart
        """
        
        v1 = shapes.Point(7, 0)
        v2 = shapes.Point(10, -3)
        v3 = shapes.Point(13, 0)
        v4 = shapes.Point(10, 3)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-2, -2)
        v6 = shapes.Point(0, -4)
        v7 = shapes.Point(2, -2)
        v8 = shapes.Point(2, 2)
        v9 = shapes.Point(0, 4)
        v10 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v5, v6, v7, v8, v9, v10)
        self.assertFalse(operations.is_inside(rec, pol))
    
    def test_for_rectangle_and_rectangle1(self):
        """the first test for checking if a given rectangle is located
        inside another given rectangle with the first one being inside
        the second one
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-3, 0)
        v6 = shapes.Point(0, -3)
        v7 = shapes.Point(3, 0)
        v8 = shapes.Point(0, 3)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertTrue(operations.is_inside(rec1, rec2))
    
    def test_for_rectangle_and_rectangle2(self):
        """the second test for checking if a given rectangle is located
        inside another given rectangle with the second one being
        located iside the first one
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-1, 0)
        v6 = shapes.Point(0, -1)
        v7 = shapes.Point(1, 0)
        v8 = shapes.Point(0, 1)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertFalse(operations.is_inside(rec1, rec2))
    
    def test_for_rectangle_and_rectangle3(self):
        """the third test for checking if a given rectangle is located
        inside another given rectangle with them fully overlapping each
        other
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        rec2 = shapes.Rectangle(v1, v2, v3, v4)
        self.assertFalse(operations.is_inside(rec1, rec2))
    
    def test_for_rectangle_and_rectangle4(self):
        """the fourth test for checking if a given rectangle is located
        inside another given rectangle with the first one being inside
        the second one but its vertices touching the second rectangle's
        perimeter
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-2, -2)
        v6 = shapes.Point(2, -2)
        v7 = shapes.Point(2, 2)
        v8 = shapes.Point(-2, 2)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertFalse(operations.is_inside(rec1, rec2))
    
    def test_for_rectangle_and_rectangle5(self):
        """the fifth test for checking if a given rectangle is located
        inside another given rectangle with them intersecting each
        other
        """
        
        v1 = shapes.Point(-2.5, 0)
        v2 = shapes.Point(0, -2.5)
        v3 = shapes.Point(2.5, 0)
        v4 = shapes.Point(0, 2.5)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-2, -2)
        v6 = shapes.Point(2, -2)
        v7 = shapes.Point(2, 2)
        v8 = shapes.Point(-2, 2)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertFalse(operations.is_inside(rec1, rec2))
    
    def test_for_rectangle_and_rectangle6(self):
        """the sixth test for checking if a given rectangle is located
        inside another given rectangle with them being fully apart
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(8, -2)
        v6 = shapes.Point(12, -2)
        v7 = shapes.Point(12, 2)
        v8 = shapes.Point(8, 2)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertFalse(operations.is_inside(rec1, rec2))
    
    def test_for_rectangle_and_circle1(self):
        """the first test for checking if a rectangle is located inside
        a given circle with the rectangle being located inside the circle
        completely
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 0), 5)
        self.assertTrue(operations.is_inside(rec, circle))
    
    def test_for_rectangle_and_circle2(self):
        """the second test for checking if a given rectangle is located
        inside a given circle with the circle being completely inside
        the rectangle
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 0), 0.1)
        self.assertFalse(operations.is_inside(rec, circle))
    
    def test_for_rectangle_and_circle3(self):
        """the third test for checking if a given rectangle is located
        inside a given circle with the rectangle being inside the
        circle but with its vertices touching the circle's perimeter
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertFalse(operations.is_inside(rec, circle))
    
    def test_for_rectangle_and_circle4(self):
        """the fourth test for checking if a given rectangle is located
        inside a given circle with the rectangle being partly inside the
        circle but intersecting with it
        """
        
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(4, 0)
        v4 = shapes.Point(2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(rec, circle))
    
    def test_for_rectangle_and_circle5(self):
        """the fifth test for checking if a given rectangle is located
        inside a given circle with them being fully apart
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(5, 5), 1)
        self.assertFalse(operations.is_inside(rec, circle))
    
    def test_for_rectangle_and_line(self):
        """testing if a given rectangle is located insied a given
        infinite line which should always return False
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        line = shapes.Line(1, 0)
        self.assertFalse(operations.is_inside(rec, line))

    def test_for_rectangle_and_linesegment(self):
        """testing if a given rectangle is located inside a given
        line segment which should always return False
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        end1 = shapes.Point(0, 0)
        end2 = shapes.LineSegment(1, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertFalse(operations.is_inside(rec, line))
    
    def test_for_circle_and_point(self):
        """testing if a given circle is located inside a given point
        which should always return False
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        point = shapes.Point(0, 0)
        self.assertFalse(operations.is_inside(circle, point))
    
    def test_for_circle_and_polygon1(self):
        """the first test for checking if a given circle is located
        inside a given polygon with the circle being fully inside the
        polygon
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertTrue(operations.is_inside(circle, pol))
    
    def test_for_circle_and_polygon2(self):
        """the second test for checking if a given circle is located
        inside a given polygon with the circle being inside the polygon
        but touching one of its edges
        """
        
        circle = shapes.Circle(shapes.Point(-1, 0), 1)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertFalse(operations.is_inside(circle, pol))
    
    def test_for_circle_and_polygon3(self):
        """the third test for checking if a given circle is located
        inside a given polygon with the circle intersecting the polygon
        """
        
        circle = shapes.Circle(shapes.Point(0, -3), 2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertFalse(operations.is_inside(circle, pol))
    
    def test_for_circle_and_polygon4(self):
        """the fourth test for checking if a given circle is located
        inside a given polygon with them being fully apart
        """
        
        circle = shapes.Circle(shapes.Point(10, 10), 1)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertFalse(operations.is_inside(circle, pol))
    
    def test_for_circle_and_rectangle1(self):
        """the first test for checking if a given circle is located
        inside a given rectangle with the circle being fully inside
        the rectangle
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertTrue(operations.is_inside(circle, rec))
    
    def test_for_circle_and_rectangle2(self):
        """the second test for checking if a given circle is located
        inside a given rectangle with the circle being inside the
        rectangle but touching one of its edges
        """
        
        circle = shapes.Circle(shapes.Point(0, -1), 1)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertFalse(operations.is_inside(circle, rec))
    
    def test_for_circle_and_rectangle3(self):
        """the third test for checking if a given circle is located
        inside a given rectangle with the circle intersecting the 
        rectangle
        """
        
        circle = shapes.Circle(shapes.Point(0, -3), 2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertFalse(operations.is_inside(circle, rec))
    
    def test_for_circle_and_rectangle4(self):
        """the fourth test for checking if a given circle is located
        inside a given rectangle with them being fully apart
        """
        
        circle = shapes.Circle(shapes.Point(10, 10), 1)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertFalse(operations.is_inside(circle, rec))
    
    def test_for_circle_and_circle1(self):
        """the first test for checking if a given circle is located
        inside anoter given circle with the first one being inside the
        second one
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0 ), 1)
        circle2 = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertTrue(operations.is_inside(circle1, circle2))
    
    def test_for_circle_and_circle2(self):
        """the second test for checking if a given circle is located
        inside another given circle with them fully overlap each other
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 1)
        circle2 = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(circle1, circle2))
    
    def test_for_circle_and_circle3(self):
        """the third test for checking if a given circle is located
        inside another given circle with the second one being inside
        the first one
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 2)
        circle2 = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(circle1, circle2))
    
    def test_for_circle_and_circle4(self):
        """the fourth test for checking if a given circle is located
        inside another given circle with them intersecting
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 1)
        circle2 = shapes.Circle(shapes.Point(0, 0.5), 1)
        self.assertFalse(operations.is_inside(circle1, circle2))
    
    def test_for_circle_and_circle5(self):
        """the fifth test for checking if a given circle is located
        inside another given circle with them intersecting
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 1)
        circle2 = shapes.Circle(shapes.Point(10, 0), 1)
        self.assertFalse(operations.is_inside(circle1, circle2))
    
    def test_for_circle_and_line(self):
        """testing if a given circle is located inside a given
        inifinite line which should always return False
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(1, 0)
        self.assertFalse(operations.is_inside(circle, line))
    
    def test_for_circle_and_linesegment(self):
        """testing if a given circle is located inside a given line
        segment which should always return False
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertFalse(operations.is_inside(circle, line))
    
    def test_for_line_and_point(self):
        """testing if a given infinite line is located inside a given
        point which should always return False
        """
        
        line = shapes.Line(1, 0)
        point = shapes.Point(0, 0)
        self.assertFalse(operations.is_inside(line, point))
    
    def test_for_line_and_polygon(self):
        """testing if a given infinite line is located inside a given
        polygon which should always return False
        """
        
        line = shapes.Line(1, 0)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        pol = shapes.Polygon(v1, v2, v3)
        self.assertFalse(operations.is_inside(line, pol))
    
    def test_for_line_and_rectangle(self):
        """testing if a given infinite line is located inside a given
        rectangle which should always return False
        """
        
        line = shapes.Line(1, 0)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertFalse(operations.is_inside(line, rec))
    
    def test_for_line_and_circle(self):
        """testing if a given infinite line is located inside a given
        circle which should always return False
        """
        
        line = shapes.Line(1, 0)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(line, circle))
    
    def test_for_line_and_line(self):
        """testing if a given infinite line is located inisde another
        given infinite line which should always return False
        """
        
        line1 = shapes.Line(1, 0)
        line2 = shapes.Line(1, 1)
        self.assertFalse(operations.is_inside(line1, line2))
    
    def test_for_line_and_linesegment(self):
        """testing if a given infinite line is located inside a given
        line segment which should always return False
        """
        
        line1 = shapes.Line(1, 0)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        line2 = shapes.LineSegment(end1, end2)
        self.assertFalse(operations.is_inside(line1, line2))
    
    def test_for_linesegment_and_point(self):
        """testing if a given line segment is located inside a given
        point which should always return False
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        line = shapes.LineSegment(end1, end2)
        point = shapes.Point(0, 0)
        self.assertFalse(operations.is_inside(line, point))
    
    def test_for_linesegment_and_polygon1(self):
        """the first test for checking if a given line segment is
        located inside a given polygon with the line segment being
        fully inside the polygon
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertTrue(operations.is_inside(line, pol))
    
    def test_for_linesegment_and_polygon2(self):
        """the second test for checking if a given line segment is
        located inside a given polygon with the line segment being
        inside the polygon but with one of its ends touching the
        polygon's perimeter
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 2)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertFalse(operations.is_inside(line, pol))
    
    def test_for_linesegment_and_polygon3(self):
        """the third test for checking if a given line segment is
        located inside a given polygon with the line segment
        intersecting the polygon
        """
        
        end1 = shapes.Point(0, 1)
        end2 = shapes.Point(3, 2)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertFalse(operations.is_inside(line, pol))
    
    def test_for_linesegment_and_polygon4(self):
        """the fourth test for checking if a given line segment is
        located inside a given polygon with them being fully apart
        """
        
        end1 = shapes.Point(10, 10)
        end2 = shapes.Point(11, 11)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertFalse(operations.is_inside(line, pol))
    
    def test_for_linesegment_and_rectangle1(self):
        """the first test for checking if a given line segment is
        located inside a given rectangle with the line segment being
        fully inside the rectangle
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0.5, 0.5)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertTrue(operations.is_inside(line, rec))
    
    def test_for_linesegment_and_rectangle2(self):
        """the second test for checking if a given line segment is
        located inside a given rectangle with the line segment being
        inside the rectangle but with one of its ends touching the
        rectangle's perimeter
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertFalse(operations.is_inside(line, rec))
    
    def test_for_linesegment_and_rectangle3(self):
        """the third test for checking if a given line segment is
        located inside a given rectangle with them intersecting each
        other
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0.5)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertFalse(operations.is_inside(line, rec))
    
    def test_for_linesegment_and_rectangle4(self):
        """the fourth test for checking if a given line segment is
        located inside a given rectangle with them being fully apart
        """
        
        end1 = shapes.Point(10, 10)
        end2 = shapes.Point(11, 11)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertFalse(operations.is_inside(line, rec))
    
    def test_for_linesegment_and_circle1(self):
        """the first test for checking if a given line segment is
        located inside a given circle with the line segment being
        fully inside the circle
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0.5, 0.5)
        line = shapes.LineSegment(end1, end2)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertTrue(operations.is_inside(line, circle))
    
    def test_for_linesegment_and_circle2(self):
        """the second test for checking if a given line segment is
        located inisde a given circle with the line segment being
        inside the circle but with one of its ends touching the
        circle's perimeter
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line = shapes.LineSegment(end1, end2)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(line, circle))
    
    def test_for_linesegment_and_circle3(self):
        """the third test for checking if a given line segment is
        located inside a given circle with them intersecting each other
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(3, 3)
        line = shapes.LineSegment(end1, end2)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(line, circle))
    
    def test_for_linesegment_and_circle4(self):
        """the fourth test for checking if a given line segment is
        located inside a given circle with them being fully apart
        """
        
        end1 = shapes.Point(10, 10)
        end2 = shapes.Point(11, 11)
        line = shapes.LineSegment(end1, end2)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertFalse(operations.is_inside(line, circle))
    
    def test_for_linesegment_and_linesegment(self):
        """testing if a given line segment is located inside another
        given line segment which should always return False
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(1, 0)
        end4 = shapes.Point(2, 1)
        line2 = shapes.LineSegment(end3, end4)
        self.assertFalse(operations.is_inside(line1, line2))
    
    def test_for_linesegment_and_line(self):
        """testing if a given line segment is located inside a given
        infinite line which should always return False
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 1)
        line1 = shapes.LineSegment(end1, end2)
        line2 = shapes.Line(1, 0)
        self.assertFalse(operations.is_inside(line1, line2))


class TestDistance(unittest.TestCase):
    """test cases for the 'distance' function"""

    def test_for_point_and_point1(self):
        """the first test for distance betweem two points with them
        being located at the same coordinates
        """

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 0)
        self.assertEqual(operations.distance(point1, point2), 0)
    
    def test_for_point_and_point2(self):
        """the second test for distance between two points with them
        being apart
        """
        
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        self.assertEqual(operations.distance(point1, point2), 1)
    
    def test_for_point_and_polygon1(self):
        """the first test for distance between a point and a polygon
        with the point being located inside the polygon
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(point, pol), -2)
    
    def test_for_point_and_polygon2(self):
        """the second test for distance between a given point and a
        given polygon with the point being located on the perimeter
        of the polygon
        """
        
        point = shapes.Point(0, 2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(point, pol), 0)
    
    def test_for_point_and_polygon3(self):
        """the third test for distance between a given point and a
        given polygon with the point being located outside of the
        polygon
        """
        
        point = shapes.Point(0, 3)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(point, pol), 1)
    
    def test_for_point_and_rectangle1(self):
        """the first test for distance between a given point and a
        given rectangle with the point being located inside the
        rectangle
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.distance(point, rec), -1)
    
    def test_for_point_and_rectangle2(self):
        """the second test for distance between a given point and a
        rectangle with the point being located on the perimeter of the
        rectangle
        """
        
        point = shapes.Point(0, 1)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.distance(point, rec), 0)
    
    def test_for_point_and_rectangle3(self):
        """the third test for distance between a give point and a given
        rectangle with the point being located outside the rectangle
        """
        
        point = shapes.Point(0, 2)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.distance(point, rec), 1)
    
    def test_for_point_and_circle1(self):
        """the first test for distance between a given point and a
        given circle with the point being located inside the circle
        """
        
        point = shapes.Point(0, 0)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(opetations.distance(point, circle), -1)
    
    def test_for_point_and_circle2(self):
        """the second test for distance between a given point and a
        given circle with the point being located on the circle's
        perimeter
        """
        
        point = shapes.Point(0, 1)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.distance(point, circle), 0)
    
    def test_for_point_and_circle3(self):
        """the third test for distance between a given point and a
        given circle with the point being located outside the given
        circle
        """
        
        point = shapes.Point(0, 2)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.distance(point, circle), 1)
    
    def test_for_point_and_line1(self):
        """the first test for distance between a given point and a
        given infinite line with the point being located on the line
        and the line being horizental
        """
        
        point = shapes.Point(0, 0)
        line = shapes.Line(0, 0)
        self.assertEqual(operations.distance(point, line), 0)
    
    def test_for_point_and_line2(self):
        """the second test for distance between a given point and a
        given infinite line with them being apart and the line being
        horizantal
        """
        
        point = shapes.Point(1, 1)
        line = shapes.Line(0, 0)
        self.assertEqual(opetations.distance(point, line), 1)
    
    def test_for_point_and_line3(self):
        """the third test for distance between a given point and a
        given infinite line with the line being vertical and the point
        being located on the line
        """
        
        point = shapes.Point(0, 0)
        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(0, 1)
        line = shapes.Line.from_points(p1, p2)
        self.assertEqual(operations.distance(point, line), 0)
    
    def test_for_point_and_line4(self):
        """the fourth test for distance between a given point and a
        given infinite line with the line being vertical and  the point
        being apart from the line
        """
        
        point = shapes.Point(1, 1)
        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(0, 1)
        line = shapes.Line.from_points(p1, p2)
        self.assertEqual(operations.distance(point, line), 1)
    
    def test_for_point_and_line5(self):
        """the fifth test for distance between a given point and a
        given infinite line with the line having an arbitrary slope
        and the point being located on the line
        """
        
        point = shapes.Point(1, 1)
        line = shapes.Line(1, 0)
        self.assertEqual(operations.distance(point, line), 0)
    
    def test_for_point_and_line6(self):
        """the sixth test for distance between a given point and a
        given infinite line with the point being apart from the line
        and the line having an arbitrary slope
        """
        
        point = shapes.Point(0, 1)
        line = shapes.Line(1, 0)
        self.assertEqual(operations.distance(point, line), np.sqrt(2)/2)
    
    def test_for_point_and_linesegment1(self):
        """the first test for distance between a given point and a
        given line segment with the point being located on the line
        segment
        """
        
        point = shapes.Point(0, 0)
        end1 = shapes.Point(-1, 0)
        end2 = shapes.Point(1, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(point, line), 0)
    
    def test_for_point_and_linesegment2(self):
        """the second test for distance between a given point and a
        given line segment with them being apart and the point being
        in the area which is between two normal vectors of the line
        segment generated from its ends
        """
        
        point = shapes.Point(0, 1)
        end1 = shapes.Point(-1, 0)
        end2 = shapes.Point(1, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(point, line), 1)
    
    def test_for_point_and_linesegment3(self):
        """the third test for distancee between a given point and a
        given line segment with them being apart and the point being
        outside the area which is between two normal vectors of the
        line segment generated from its ends
        """
        
        point = shapes.Point(-2, 0)
        end1 = shapes.Point(-1, 0)
        end2 = shapes.Point(1, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(point, line), 1)
    
    def test_for_polygon_and_point1(self):
        """the first test for distance between a point and a polygon
        with the point being located inside the polygon
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(pol, point), 0)
    
    def test_for_polygon_and_point2(self):
        """the second test for distance between a given point and a
        given polygon with the point being located on the perimeter
        of the polygon
        """
        
        point = shapes.Point(0, 2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(pol, point), 0)
    
    def test_for_polygon_and_point3(self):
        """the third test for distance between a given point and a
        given polygon with the point being located outside of the
        polygon
        """
        
        point = shapes.Point(0, 3)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(pol, point), 1)
    
    def test_for_polygon_and_polygon1(self):
        """the first test for distance between two polygons with the
        first one being inside the second one
        """

        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        v7 = shapes.Point(-3, -3)
        v8 = shapes.Point(0, -5)
        v9 = shapes.Point(3, -3)
        v10 = shapes.Point(3, 3)
        v11 = shapes.Point(0, 5)
        v12 = shapes.Point(-3, 3)
        pol2 = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(pol1, pol2), -1)
    
    def test_for_polygon_polygon2(self):
        """the second test for distance between two given polygons with
        them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        v7 = shapes.Point(-1, -1)
        v8 = shapes.Point(0, -5)
        v9 = shapes.Point(1, -1)
        v10 = shapes.Point(3, 3)
        v11 = shapes.Point(0, 5)
        v12 = shapes.Point(-3, 3)
        pol2 = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(pol1, pol2), 0)
    
    def test_for_polygon_and_polygon3(self):
        """the third test for distance between two given polygons with
        them being fully apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        v7 = shapes.Point(7, -3)
        v8 = shapes.Point(10, -5)
        v9 = shapes.Point(13, -3)
        v10 = shapes.Point(13, 3)
        v11 = shapes.Point(10, 5)
        v12 = shapes.Point(7, 3)
        pol2 = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(pol1, pol2), 5)
    
    def test_for_polygon_and_polygon4(self):
        """the first test for distance between two polygons with the
        second one being inside the first one
        """

        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol1 = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        v7 = shapes.Point(-3, -3)
        v8 = shapes.Point(0, -5)
        v9 = shapes.Point(3, -3)
        v10 = shapes.Point(3, 3)
        v11 = shapes.Point(0, 5)
        v12 = shapes.Point(-3, 3)
        pol2 = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(pol2, pol1), 0)
    
    def test_for_polygon_and_rectangle1(self):
        """the first test for distance between a given polygon and a
        given rectangle with the polygon being inside the rectangle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        v7 = shapes.Point(-5, -5)
        v8 = shapes.Point(5, -5)
        v9 = shapes.Point(5, 5)
        v10 = shapes.Point(-5, 5)
        rec = shapes.Rectangle(v7, v8, v9, v10)
        self.assertEqual(operations.distance(pol, rec), -1)
    
    def test_for_polygon_and_rectangle2(self):
        """the second test for distance between a given polygon and a
        given rectangle with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        v7 = shapes.Point(-1, -5)
        v8 = shapes.Point(5, -5)
        v9 = shapes.Point(5, 5)
        v10 = shapes.Point(-1, 5)
        rec = shapes.Rectangle(v7, v8, v9, v10)
        self.assertEqual(operations.distance(pol, rec), 0)
    
    def test_for_polygon_and_rectangle3(self):
        """the third test for distance between a given polygon and a
        given rectangle with them being fully apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        v7 = shapes.Point(3, -5)
        v8 = shapes.Point(5, -5)
        v9 = shapes.Point(5, 5)
        v10 = shapes.Point(3, 5)
        rec = shapes.Rectangle(v7, v8, v9, v10)
        self.assertEqual(operations.distance(pol, rec), 1)
    
    def test_for_polygon_and_rectangle4(self):
        """the first test for distance between a given polygon and a
        given rectangle with the rectangle being inside the polygon
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        v7 = shapes.Point(-1, -1)
        v8 = shapes.Point(1, -1)
        v9 = shapes.Point(1, 1)
        v10 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v7, v8, v9, v10)
        self.assertEqual(operations.distance(pol, rec), 0)
    
    def test_for_polygon_and_circle1(self):
        """the first test for distance between a given polygon and a
        given circle with the polygon being inside the circle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        circle = shapes.Circle(shapes.Point(0, 0), 5)
        self.assertEqual(operations.distance(pol, circle), -1)
    
    def test_for_polygon_and_circle2(self):
        """the second test for distance between a given polygon and a
        given circle with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        circle = shapes.Circle(shapes.Point(0, 0), 3)
        self.assertEqual(operations.distance(pol, circle), 0)
    
    def test_for_polygon_and_circle3(self):
        """the third test for distance between a given polygon and a
        given circle with them being fully apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        circle = shapes.Circle(shapes.Point(4, 0), 1)
        self.assertEqual(operations.distance(pol, circle), 1)
    
    def test_for_polygon_and_circle4(self):
        """the first test for distance between a given polygon and a
        given circle with the circle being inside the polygon
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.distance(pol, circle), 0)
    
    def test_for_polygon_and_line1(self):
        """the first test for distance between a given polygon and a
        given infinite line with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        line = shapes.Line(0, 0)
        self.assertEqual(operations.distance(pol, line), 0)
    
    def test_for_polygon_and_line2(self):
        """the second test for distance between a given polygon and a
        given infinite line with them being fully apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        line = shapes.Line(0, 5)
        self.assertEqual(operations.distance(pol, line), 1)
    
    def test_for_polygon_and_linesegment1(self):
        """the first test for distance between a given polygon and a
        given line segment with the line segment being inside the
        polygon
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        end1 = shapes.Poin(0, 0)
        end2 = shapes.Point(1, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(pol, line), 0)
    
    def test_for_polygon_and_linesegment2(self):
        """the second test for distance between a given polygon and a
        given line segment with the line segment being inside the
        polygon but with one of its ends touching the polygon's
        perimeter
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        end1 = shapes.Poin(0, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(pol, line), 0)
    
    def test_for_polygon_and_linesegment3(self):
        """the third test for distance between a given polygon and a
        given line segment with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        end1 = shapes.Poin(0, 0)
        end2 = shapes.Point(3, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(pol, line), 0)
    
    def test_for_polygon_and_linesegment4(self):
        """the fourth test for distance between a given polygon and a
        line segment with the line segment being located outside the
        polygon
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        end1 = shapes.Poin(3, 0)
        end2 = shapes.Point(4, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(pol, line), 1)
    
    def test_for_rectangle_and_point1(self):
        """the first test for distance between a point and a rectangle
        with the point being located inside the rectangle
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        self.assertEqual(operations.distance(rec, point), 0)
    
    def test_for_rectangle_and_point2(self):
        """the second test for distance between a given point and a
        given rectangle with the point being located on the perimeter
        of the rectangle
        """
        
        point = shapes.Point(0, 2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        self.assertEqual(operations.distance(rec, point), 0)
    
    def test_for_rectangle_and_point3(self):
        """the third test for distance between a given point and a
        given rectangle with the point being located outside of the
        rectangle
        """
        
        point = shapes.Point(0, 3)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        self.assertEqual(operations.distance(pol, point), 1)
    
    def test_for_rectangle_and_polygon1(self):
        """the first test for distance between a given rectangle and a
        given polygon with the rectangle being inside the polygon
        """

        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        v7 = shapes.Point(-3, -3)
        v8 = shapes.Point(0, -5)
        v9 = shapes.Point(3, -3)
        v10 = shapes.Point(3, 3)
        v11 = shapes.Point(0, 5)
        v12 = shapes.Point(-3, 3)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(rec, pol), -1)
    
    def test_for_rectangle_polygon2(self):
        """the second test for distance between a given rectangle and a
        given polygon them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        v7 = shapes.Point(-1, -1)
        v8 = shapes.Point(0, -5)
        v9 = shapes.Point(1, -1)
        v10 = shapes.Point(3, 3)
        v11 = shapes.Point(0, 5)
        v12 = shapes.Point(-3, 3)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(rec, pol), 0)
    
    def test_for_rectangle_and_polygon3(self):
        """the third test for distance between a given rectangle and a
        given polygon with them being apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        v7 = shapes.Point(7, -3)
        v8 = shapes.Point(10, -5)
        v9 = shapes.Point(13, -3)
        v10 = shapes.Point(13, 3)
        v11 = shapes.Point(10, 5)
        v12 = shapes.Point(7, 3)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(rec, pol), 5)
    
    def test_for_rectangle_and_polygon4(self):
        """the first test for distance between a given rectangle and a
        given polygon with the polygon being inside the rectangle
        """

        v1 = shapes.Point(-6, -6)
        v2 = shapes.Point(6, -6)
        v3 = shapes.Point(6, 6)
        v4 = shapes.Point(-6, 6)
        rec = shapes.Polygon(v1, v2, v3, v4)
        v7 = shapes.Point(-3, -3)
        v8 = shapes.Point(0, -5)
        v9 = shapes.Point(3, -3)
        v10 = shapes.Point(3, 3)
        v11 = shapes.Point(0, 5)
        v12 = shapes.Point(-3, 3)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(rec, pol), 0)
    
    def test_for_rectangle_and_rectangle1(self):
        """the first test for distance between two given rectangles
        with the first one being inside the second one
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec1 = shapes.Polygon(v1, v2, v3, v4)
        v7 = shapes.Point(-5, -5)
        v8 = shapes.Point(5, -5)
        v9 = shapes.Point(5, 5)
        v10 = shapes.Point(-5, 5)
        rec2 = shapes.Rectangle(v7, v8, v9, v10)
        self.assertEqual(operations.distance(rec1, rec2), -3)
    
    def test_for_rectangle_and_rectangle2(self):
        """the second test for distance between two given rectangles
        with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec1 = shapes.Polygon(v1, v2, v3, v4)
        v7 = shapes.Point(-1, -5)
        v8 = shapes.Point(5, -5)
        v9 = shapes.Point(5, 5)
        v10 = shapes.Point(-1, 5)
        rec2 = shapes.Rectangle(v7, v8, v9, v10)
        self.assertEqual(operations.distance(rec1, rec2), 0)
    
    def test_for_rectangle_and_rectangle3(self):
        """the third test for distance between two given rectangles
        with them being fully apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec1 = shapes.Polygon(v1, v2, v3, v4)
        v7 = shapes.Point(3, -5)
        v8 = shapes.Point(5, -5)
        v9 = shapes.Point(5, 5)
        v10 = shapes.Point(3, 5)
        rec2 = shapes.Rectangle(v7, v8, v9, v10)
        self.assertEqual(operations.distance(rec1, rec2), 1)
    
    def test_for_rectangle_and_rectangle1(self):
        """the first test for distance between two given rectangles
        with the second one being inside the first one
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec1 = shapes.Polygon(v1, v2, v3, v4)
        v7 = shapes.Point(-5, -5)
        v8 = shapes.Point(5, -5)
        v9 = shapes.Point(5, 5)
        v10 = shapes.Point(-5, 5)
        rec2 = shapes.Rectangle(v7, v8, v9, v10)
        self.assertEqual(operations.distance(rec2, rec1), 0)
    
    def test_for_recgtangle_and_circle1(self):
        """the first test for distance between a given rectangle and a
        given circle with the rectangle being inside the circle
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 0), 5)
        self.assertEqual(operations.distance(rec, circle), -3)
    
    def test_for_rectangle_and_circle2(self):
        """the second test for distance between a given rectangle and a
        given circle with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 0), 2.5)
        self.assertEqual(operations.distance(rec, circle), 0)
    
    def test_for_rectangle_and_circle3(self):
        """the third test for distance between a given rectangle and a
        given circle with them being fully apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(4, 0), 1)
        self.assertEqual(operations.distance(rec, circle), 1)
    
    def test_for_recgtangle_and_circle1(self):
        """the first test for distance between a given rectangle and a
        given circle with the circle being inside the rectangle
        """
        
        v1 = shapes.Point(-2, 0)
        v2 = shapes.Point(0, -2)
        v3 = shapes.Point(2, 0)
        v4 = shapes.Point(0, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.distance(rec, circle), 0)
    
    def test_for_rectangle_and_line1(self):
        """the first test for distance between a given rectangle and a
        given infinite line with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        line = shapes.Line(0, 0)
        self.assertEqual(operations.distance(rec, line), 0)
    
    def test_for_rectangle_and_line2(self):
        """the second test for distance between a given rectangle and a
        given infinite line with them being fully apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        line = shapes.Line(0, 3)
        self.assertEqual(operations.distance(rec, line), 1)
    
    def test_for_rectangle_and_linesegment1(self):
        """the first test for distance between a given rectangle and a
        given line segment with the line segment being inside the
        rectangle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        end1 = shapes.Poin(0, 0)
        end2 = shapes.Point(1, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(rec, line), 0)
    
    def test_for_rectangle_and_linesegment2(self):
        """the second test for distance between a given rectangle and a
        given line segment with the line segment being inside the
        rectangle but with one of its ends touching the rectangle's
        perimeter
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        end1 = shapes.Poin(0, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(rec, line), 0)
    
    def test_for_rectangle_and_linesegment3(self):
        """the third test for distance between a given rectangle and a
        given line segment with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        end1 = shapes.Poin(0, 0)
        end2 = shapes.Point(3, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(rec, line), 0)
    
    def test_for_rectangle_and_linesegment4(self):
        """the fourth test for distance between a given rectangle and a
        line segment with the line segment being located outside the
        rectangle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Polygon(v1, v2, v3, v4)
        end1 = shapes.Poin(3, 0)
        end2 = shapes.Point(4, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(rec, line), 1)
    
    def test_for_circle_and_point1(self):
        """the first test for distance between a given circle and a
        given point with the point being located on the circle's
        perimeter
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        point = shapes.Point(0, 1)
        self.assertEqual(operations.distance(circle, point), 0)
    
    def test_for_circle_and_point2(self):
        """the second test for distance between a given circle and a
        given point with the point being inside the circle
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        point = shapes.Point(0, 0)
        self.assertEqual(operations.distance(circle, point), 0)
    
    def test_for_circle_and_point3(self):
        """the third test for distance between a given circle and a
        given point with them being fully apart
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        point = shapes.Point(0, 2)
        self.assertEqual(operations.distance(circle, point), 1)
    
    def test_for_circle_and_polygon1(self):
        """the first test for distance between a given circle and a
        given polygon with the polygon being located inside the circle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        circle = shapes.Circle(shapes.Point(0, 0), 5)
        self.assertEqual(operations.distance(circle, pol), 0)
    
    def test_for_circle_and_polygon2(self):
        """the second test for distance between a given circle and a
        given polygon with the circle being inside the polygon
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.distance(circle, pol), -1)
    
    def test_for_circle_and_polygon3(self):
        """the third test for distance between a given circle and a
        given polygon with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        circle = shapes.Circle(shapes.Point(2, 0), 3)
        self.assertEqual(operations.distance(circle, pol), 0)
    
    def test_for_circle_and_polygon4(self):
        """the fourth test for distance between a given circle and a
        given polygon with them being fully apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        circle = shapes.Circle(shapes.Point(4, 0), 1)
        self.assertEqual(operations.distance(circle, pol), 1)
    
    def test_for_circle_and_rectangle1(self):
        """the first test for distance between a given circle and a
        given rectangle with the rectangle being located inside the
        circle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 0), 5)
        self.assertEqual(operations.distance(circle, rec), 0)
    
    def test_for_circle_and_rectangle2(self):
        """the second test for distance between a given circle and a
        given rectangle with the circle being inside the rectang;e
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.distance(circle, rec), -1)
    
    def test_for_circle_and_rectangle3(self):
        """the third test for distance between a given circle and a
        given rectangle with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(2, 0), 3)
        self.assertEqual(operations.distance(circle, rec), 0)
    
    def test_for_circle_and_rectangle4(self):
        """the fourth test for distance between a given circle and a
        given rectangle with them being fully apart
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(4, 0), 1)
        self.assertEqual(operations.distance(circle, rec), 1)
    
    def test_for_circle_and_circle1(self):
        """the first test for distance between two given circles with
        the first one being inside the second one
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 1)
        circle2 = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.distance(circle1, circle2), -1)
    
    def test_for_circle_and_circle2(self):
        """the second test for distance between two given circles with
        the second one being inside the first one
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 1)
        circle2 = shapes.Cirlce(shapes.Poin(0, 0), 0.5)
        self.assertEqual(operations.distance(circle1, circle2), 0)
    
    def test_for_circle_and_circle3(self):
        """the third test for distance between two given circles with
        them intersecting each other
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 1)
        circle2 = shapes.Circle(shapes.Point(0, 0.5), 1)
        self.assertEqual(operations.distance(circle1, circle2), 0)
    
    def test_for_circle_and_circle4(self):
        """the fourth test for distance between two given circles with
        them being fully apart
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 1)
        circle2 = shapes.Circle(shapes.Point(0, 3), 1)
        self.assertEqual(operations.distance(circle1, circle2), 1)
    
    def test_for_circle_and_line1(self):
        """the first test for distance between a given circle and a
        given infinite line with them intersecting each other
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(0, 0)
        self.assertEqual(operations.distance(circle, line), 0)
    
    def test_for_circle_and_line2(self):
        """the second test for distance between a given circle and a
        given infinite line with them being fully apart
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        line = shapes.Line(0, 2)
        self.assertEqual(operations.distance(circle, line), 1)
    
    def test_for_circle_and_linesegment1(self):
        """the first test for distance between a given circle and a
        given line segment with the line segment being located inside
        the circle
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 0.5)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(circle, line), 0)
    
    def test_for_circle_and_linesegment2(self):
        """the second test for distance between a given circle and a
        given line segment with them intersecting each other
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 2)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(circle, line), 0)
    
    def test_for_circle_and_linesegment3(self):
        """the third test for distance between a given circle and a
        given line segment with them being fully apart
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        end1 = shapes.Point(2, 0)
        end2 = shapes.Point(3, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(circle, line), 1)
    
    def test_for_linesegment_and_point1(self):
        """the first test for distance between a given line segment and
        a given point with the point being located on the line
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line = shapes.LineSegment(end1, end2)
        point = shapes.Point(0, 0)
        self.assertEqual(operations.distance(line, point), 0)
    
    def test_for_linesegment_and_point2(self):
        """the second test for distance between a given line segment
        and a given point with the point being located above the line
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        line = shapes.LineSegment(end1, end2)
        point = shapes.Point(0.5, 0.5)
        self.assertEqual(operations.distance(line, point), 0.5)
    
    def test_for_linesegment_and_point3(self):
        """the third test for distance between a given line segment and
        a given point with the point being located on the side of the
        line segment
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line = shapes.LineSegment(end1, end2)
        point = shapes.Point(0, 2)
        self.assertEqual(operations.distance(line, point), 1)
    
    def test_for_linesegment_and_polygon1(self):
        """the first test for distance between a given line segment and
        a given polygon with the line segment being inside the polygon
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, pol), -1)
    
    def test_for_linesegment_and_polygon2(self):
        """the second test for distance between a given line segment
        and a given polygon with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, pol), 0)
    
    def test_for_linesegment_and_polygon3(self):
        """the third test for distance between a given line segment and
        a given polygon with the line segment being outside the polygon
        and being vertical
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        end1 = shapes.Point(3, 0)
        end2 = shapes.Point(3, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, pol), 1)
    
    def test_for_linesegmnet_and_rectangle1(self):
        """the first test for distance between a given line segment and
        a given rectangle with the line segment being inside the
        rectangle
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, rec), 1)
    
    def test_for_linesegment_and_rectangle2(self):
        """the second test for distance between a given line segment
        and a given rectangle with them intersecting each other
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, rec), 0)
    
    def test_for_linesegment_and_rectangle3(self):
        """the third test for distance between a given line segment and
        a given rectangle with the line segment being outside the
        rectangle and being vertical
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        end1 = shapes.Point(3, 0)
        end2 = shapes.Point(3, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, rec), 1)
    
    def test_for_linesegment_and_circle1(self):
        """the first test for distance between a given line segment and
        a given circle with the line segment being located inside the
        circle
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, rec), 1)
    
    def test_for_linesegment_and_circle2(self):
        """the second test for distance between a given line segment
        and a given circle with them intersecting each other
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, rec), 0)
    
    def test_for_linesegment_and_circle3(self):
        """the third test for distance between a given line segment and
        a given circle with the line segment being outside the circle
        and being vertical
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(3, -1)
        end2 = shapes.Point(3, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, rec), 1)
    
    def test_for_linesegment_and_linesegment1(self):
        """the first test for distance between two given line segments
        with them intersecting each other
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(0, 0)
        end4 = shapes.Point(1, 1)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.distance(line1, line2), 0)
    
    def test_for_linesegment_and_linesegment2(self):
        """the second test for distance between two given line segments
        with them being located parallel to each other
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(0, 1)
        end4 = shapes.Point(1, 1)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.distance(line1, line2), 1)
    
    def test_for_linesegment_and_linesegment3(self):
        """the third test for distance between two given line segments
        with them being located at an alignment
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(2, 0)
        end4 = shapes.Point(3, 0)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.distance(line1, line2), 1)
    
    def test_for_linesegment_and_line1(self):
        """the first test for distance between a given line segment and
        a given infinite line with them intersecting each other
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line1 = shapes.LineSegment(end1, end2)
        line2 = shapes.Line(0, 0)
        self.assertEqual(operations.distance(line1, line2), 0)
    
    def test_for_linesegment_and_line2(self):
        """the second test for distance between a given line segmnet
        and a given infinite line with them being parallel to each
        other
        """
        
        end1 = shapes.Point(0, 1)
        end2 = shapes.Point(1, 1)
        line1 = shapes.LineSegment(end1, end2)
        line2 = shapes.Line(0, 0)
        self.assertEqual(operations.distance(line1, line2), 1)
    
    def test_for_linesegment_and_line3(self):
        """the third test for distance between a line segment and a
        given infinite line with them not being parallel to each other
        """
        
        end1 = shapes.Point(1, 1)
        end2 = shapes.Point(2, 2)
        line1 = shapes.LineSegment(end1, end2)
        line2 = shapes.Line(0, 0)
        self.assertEqual(operations.distance(line1, line2), 1)
    
    def test_for_line_and_point1(self):
        """the first test for distance between a given line and a given
        point with the point being located on the line
        """
        
        line = shapes.Line(0, 0)
        point = shapes.Point(0, 0)
        self.assertEqual(operations.distance(line, point), 0)
    
    def test_for_line_and_point2(self):
        """the second test for distance between a given infinite line
        and a given point with them being apart
        """
        
        line = shapes.Line(0, 0)
        point = shapes.Point(0, 1)
        self.assertEqual(operations.distance(line, point), 1)
    
    def test_for_line_and_polygon1(self):
        """the first test for distance between a given infinite line
        and a given polygon with them intersecting each other
        """
        
        line = shapes.Line(0, 0)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(line, pol), 0)
    
    def test_for_line_and_polygon2(self):
        """the second test for distance between a given infinite line
        and a given polygon with them being fully apart
        """
        
        line = shapes.Line(0, 3)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.distance(line, pol), 1)
    
    def test_for_line_and_rectangle1(self):
        """the first test for distance between a given infinite line
        and a given rectangle with them intersecting each other
        """
        
        line = shapes.Line(0, 0)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.distance(line, rec), 0)
    
    def test_for_line_and_rectangle2(self):
        """the second test for distance between a given infinite line
        and a given rectangle with them being fully apart
        """
        
        line = shapes.Line(0, 3)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.distance(line, rec), 1)
    
    def test_for_line_and_circle1(self):
        """the first test for distance between a given infinite line
        and a given circle with them intersecting each other
        """
        
        line = shapes.Line(0, 0)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.distance(line, circle), 0)
    
    def test_for_line_and_circle2(self):
        """the second test for distance between a given infinite line
        and a given circle with them being fully apart
        """
        
        line = shapes.Line(0, 2)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.distance(line, circle), 1)
    
    def test_for_line_and_linesegment1(self):
        """the first test for distance between a given infinite line
        and a given line segment with them intersecting each other
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line1 = shapes.LineSegment(end1, end2)
        line2 = shapes.Line(0, 0)
        self.assertEqual(operations.distance(line2, line1), 0)
    
    def test_for_line_and_linesegment2(self):
        """the second test for distance between a given infinite line 
        and a given line segment with them being parallel to each other
        """
        
        end1 = shapes.Point(0, 1)
        end2 = shapes.Point(1, 1)
        line1 = shapes.LineSegment(end1, end2)
        line2 = shapes.Line(0, 0)
        self.assertEqual(operations.distance(line2, line1), 1)
    
    def test_for_line_and_linesegment3(self):
        """the third test for distance between a given infinite line
        and agiven line segment with them not being parallel to each
        other
        """
        
        end1 = shapes.Point(1, 1)
        end2 = shapes.Point(2, 2)
        line1 = shapes.LineSegment(end1, end2)
        line2 = shapes.Line(0, 0)
        self.assertEqual(operations.distance(line2, line1), 1)
    
    def test_for_line_and_line1(self):
        """the first test for distance between two given infinite lines
        with them intersecting each other
        """
        
        line1 = shapes.Line(0, 0)
        line2 = shapes.Line(1, 1)
        self.assertEqual(opetations.distance(line1, line2), 0)
    
    def test_for_line_and_line2(self):
        """the second test for distance between two given infinite
        lines with them being parallel to each other and being
        horizental
        """
        
        line1 = shapes.Line(0, 0)
        line2 = shapes.Line(0, 1)
        self.assertEqual(opetations.distance(line1, line2), 1)
    
    def test_for_line_and_line3(self):
        """the third test for distance between two given infinite lines
        with them being parallel and vertical
        """
        
        point1 = shapes.Point(0, 0)
        point2 = shapes.point(0, 1)
        point3 = shapes.Point(1, 0)
        point4 = shapes.point(1, 1)
        line1 = shapes.Line.from_points(point1, point2)
        line1 = shapes.Line.from_points(point3, point4)
        self.assertEqual(operations.distance(line1, line2), 1)
    
    def test_for_line_and_line4(self):
        """the fourth test for distance between two given infinite
        lines with them being parallel and with an arbitrary slope
        """
        
        line1 = shapes.Line(1, 0)
        line2 = shapes.Line(1, 1)
        self.assertEqual(opetations.distance(line1, line2), np.sqrt(2)/2)