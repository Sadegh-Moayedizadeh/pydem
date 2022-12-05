"""test cases for 'intersection' function for two dimensional entities
"""

import unittest
import sys
from geometry import two_dimensional_operations as operations
from geometry import two_dimensional_entities as shapes
import numpy as np


class TestIntersection(unittest.TestCase):
    """testing the "intersection" function for different cenarios
    """
    
    def test_for_point_and_point1(self):
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
        self.assertEqual(operations.intersection(point, pol), None)
    
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
        self.assertEqual(operations.intersection(point, rec), None)
    
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
        
        point = shapes.Point(0, 2)
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
        
        point = shapes.Point(0, 0)
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
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.intersection(point, circle), None)
    
    def test_for_point_and_circle2(self):
        """the second test for intersection between a point and a
        circle with the given point being located on the given circle's
        perimeter
        """
        
        point = shapes.Point(0, 1)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.intersection(point, circle), point)
    
    def test_for_point_and_circle3(self):
        """the third test for intersection between a point and a circle
        with the given point being located outside the given circle
        """
        
        point = shapes.Point(0, 5)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
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
    
    def test_for_polygon_and_point4(self):
        """the fourth test for intersection between a point and a
        polygon with the given point being inside the given polygon
        """
        
        point = shapes.Point(0.1, 0.5)
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(0, 1)
        v3 = shapes.Point(1, 1)
        pol = shapes.Polygon(v1, v2, v3)
        self.assertEqual(operations.intersection(pol, point), None)
    
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
        v8 = shapes.Point(1.5, 2)
        v9 = shapes.Point(0.5, 2)
        pol2 = shapes.Polygon(v6, v7, v8, v9)
        exp = (shapes.Point(1, 0), shapes.Point(0.5, 1))
        res = operations.intersection(pol1, pol2)
        self.assertEqual(set(res), set(exp))   
    
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
        line = shapes.LineSegment(v6, v3)
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
        point1 = shapes.Point(1, 0)
        point2 = shapes.Point(1, 0.5)
        exp = (point1, point2)
        self.assertEqual(set(operations.intersection(pol, rec)), set(exp))    
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
        line = shapes.LineSegment(v6, v3)
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
        circle = shapes.Circle(shapes.Point(0, 0), 1)
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
        circle = shapes.Circle(shapes.Point(-2, 0), 2)
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
        circle = shapes.Circle(shapes.Point(1, 1), 1)
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
        line = shapes.Line(1, 0)
        exp = (v4, shapes.Point(-0.5, -0.5))
        res = operations.intersection(pol, line)
        self.assertEqual(set(res), set(exp))
    
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
        line = shapes.Line(0, 1)
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
        exp = (shapes.Point(0.5, 1), shapes.Point(0.5, -1))
        res = operations.intersection(pol, line)
        self.assertEqual(set(res), set(exp))
    
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
        v8 = shapes.Point(0, 3)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        exp = (shapes.Point(2, 0), shapes.Point(0, 2))
        res = operations.intersection(rec1, rec2)
        self.assertEqual(set(res), set(exp))
    
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
        line = shapes.LineSegment(v5, v3)
        exp = (line, shapes.Point(2, 0))
        res = operations.intersection(rec1, rec2)
        self.assertEqual(set(res), set(exp))
    
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
        exp = (shapes.Point(1, 0), shapes.Point(1, 0.5))
        res = operations.intersection(rec, pol)
        self.assertEqual(set(res), set(exp))
    
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
        line = shapes.LineSegment(v6, v3)
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
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.intersection(rec, circle), None)
    
    def test_for_rectangle_and_circle2(self):
        """the second test for intersection between a rectangle and a
        circle with the given circle touching the given rectangle
        on its vertex in one point
        """
        
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(-2, 2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(2, -2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        circle = shapes.Circle(shapes.Point(0, 3), 2)
        exp = shapes.Point(0, 2)
        self.assertEqual(operations.intersection(rec, circle), exp)
    
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
        circle = shapes.Circle(shapes.Point(2, 2), 4)
        exp = (shapes.Point(2, 0), shapes.Point(0, 2))
        res = operations.intersection(rec, circle)
        self.assertEqual(set(res), set(exp))
    
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
        exp = (shapes.Point(2, 0), shapes.Point(-2, 0))
        res = operations.intersection(rec, line)
        self.assertEqual(set(res), set(exp))
    
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
        exp = (shapes.Point(0, 2), shapes.Point(0, -2))
        res = operations.intersection(rec, line)
        self.assertEqual(set(res), set(exp))
    
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
        line = shapes.Line(1, 0)
        exp = (v1, v3)
        res = operations.intersection(rec, line)
        self.assertEqual(set(res), set(exp))
    
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
        line = shapes.Line(0, 2)
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
        """the first test for intersection between a point and a
        circle with the given point being located inside the given
        circle
        """
        
        point = shapes.Point(0, 0.5)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.intersection(circle, point), None)
    
    def test_for_circle_and_point2(self):
        """the second test for intersection between a point and a
        circle with the given point being located on the given circle's
        perimeter
        """
        
        point = shapes.Point(0, 1)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.intersection(circle, point), point)
    
    def test_for_circle_and_point3(self):
        """the third test for intersection between a point and a circle
        with the given point being located outside the given circle
        """
        
        point = shapes.Point(0, 5)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
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
        circle = shapes.Circle(shapes.Point(-2, 0), 2)
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
        circle = shapes.Circle(shapes.Point(1, 1), 1)
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
        circle = shapes.Circle(shapes.Point(0, 3), 2)
        exp = shapes.Point(0, 2)
        self.assertEqual(operations.intersection(rec, circle), exp)
    
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
        circle = shapes.Circle(shapes.Point(0, 2), 4)
        exp = (shapes.Point(2, 2), shapes.Point(-2, 2))
        res = operations.intersection(rec, circle)
        self.assertEqual(set(res), set(exp))
    
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
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 4)
        circle2 = shapes.Circle(shapes.Point(3, 0), 2)
        point = shapes.Point(2, 0)
        self.assertEqual(operations.intersection(circle1, circle2), point)
    
    def test_for_circle_and_circle3(self):
        """the third test for intersection between two circles with
        them intersecting each other in two points
        """
        
        circle1 = shapes.Circle(shapes.Point(0, 0), 4)
        circle2 = shapes.Circle(shapes.Point(2, 2), 4)
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
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line(0, 1)
        point = shapes.Point(0, 1)
        self.assertEqual(operations.intersection(circle, line), point)
    
    def test_for_circle_and_line2(self):
        """the second test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        being vertical
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line.from_points(shapes.Point(1, -1), shapes.Point(1, 1))
        point = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(circle, line), point)
    
    def test_for_circle_and_line3(self):
        """the third test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        having an arbitrary slope
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line(1, -1*np.sqrt(2))
        point = shapes.Point(np.sqrt(2)/2, -1*np.sqrt(2)/2)
        self.assertEqual(operations.intersection(circle, line), point)
    
    def test_for_circle_and_line4(self):
        """the fourth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        being horizental
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line(0, 0)
        res = (shapes.Point(-1, 0), shapes.Point(1, 0))
        self.assertEqual(set(operations.intersection(circle, line)), set(res))
    
    def test_for_circle_and_line5(self):
        """the fifth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        being vertical
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 10))
        res = (shapes.Point(0, -1), shapes.Point(0, 1))
        self.assertEqual(set(operations.intersection(circle, line)), set(res))
    
    def test_for_circle_and_line6(self):
        """the sixth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        having an arbitrary slope
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line(1, 0)
        res = (shapes.Point(np.sqrt(2)/2, np.sqrt(2)/2), shapes.Point(-1*np.sqrt(2)/2, -1*np.sqrt(2)/2))
        self.assertEqual(set(operations.intersection(circle, line)), set(res))
    
    def test_for_circle_and_line7(self):
        """the seventh test for intersection between a circle and an
        infinite line with them being apart
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line(1, 10)
        self.assertEqual(operations.intersection(circle, line), None)
    
    def test_for_circle_and_linesegment1(self):  
        """the first test for intersection between a circle and a line
        segment with the line segment being located fully inside the
        circle
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(-0.5, -0.5)
        end2 = shapes.Point(0.5, 0.5)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(circle, line), None)
    
    def test_for_circle_and_linesegment2(self):
        """the second test for intersection between a circle and a line
        segment with them intersecting in one point
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        point = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(circle, line), point)
    
    def test_for_circle_and_linesegment3(self):
        """the third test for intersection between a circle and a line
        segment with them intersecting in two points
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
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
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(1, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(circle, line), shapes.Point(1, 0))
    
    def test_for_circle_and_linesegment6(self):
        """the sixth test for intersection between a circle and a line
        segment with them touching in one point on the line's body
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
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
        self.assertEqual(operations.intersection(line, point), None)
    
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
        line = shapes.Line(1, 0)
        exp = (v4, shapes.Point(-0.5, -0.5))
        res = operations.intersection(line, pol)
        self.assertEqual(set(res), set(exp))
    
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
        line = shapes.Line(0, 1)
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
        exp = (shapes.Point(2, 0), shapes.Point(-2, 0))
        res = operations.intersection(line, rec)
        self.assertEqual(set(res), set(exp))
    
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
        exp = (shapes.Point(0, 2), shapes.Point(0, -2))
        res = operations.intersection(line, rec)
        self.assertEqual(set(res), set(exp))
    
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
        line = shapes.Line(1, 0)
        exp = (v1, v3)
        res = operations.intersection(line, rec)
        self.assertEqual(set(res), set(exp))
    
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
        line = shapes.Line(0, 2)
        res = shapes.LineSegment(v2, v3)
        self.assertEqual(operations.intersection(line, rec), res)
    
    def test_for_line_and_circle1(self):
        """the first test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        being horizental
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line(0, 1)
        point = shapes.Point(0, 1)
        self.assertEqual(operations.intersection(line, circle), point)
    
    def test_for_line_and_circle2(self):
        """the second test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        being vertical
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line.from_points(shapes.Point(1, -1), shapes.Point(1, 1))
        point = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(line, circle), point)
    
    def test_for_line_and_circle3(self):
        """the third test for intersection between a circle and an
        infinite line with them intersecting in one point and the line
        having an arbitrary slope
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line(1, -1*np.sqrt(2))
        point = shapes.Point(np.sqrt(2)/2, -1*np.sqrt(2)/2)
        self.assertEqual(operations.intersection(line, circle), point)
    
    def test_for_line_and_circle4(self):
        """the fourth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        being horizental
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line(0, 0)
        exp = (shapes.Point(-1, 0), shapes.Point(1, 0))
        res = operations.intersection(line, circle)
        self.assertEqual(set(res), set(exp))
    
    def test_for_line_and_circle5(self):
        """the fifth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        being vertical
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line.from_points(shapes.Point(0, 0), shapes.Point(0, 10))
        exp = (shapes.Point(0, -1), shapes.Point(0, 1))
        res = operations.intersection(line, circle)
        self.assertEqual(set(res), set(exp))
    
    def test_for_line_and_circle6(self):
        """the sixth test for intersection between a circle and an
        infinite line with them intersecting in two points and the line
        having an arbitrary slope
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        line = shapes.Line(1, 0)
        exp = (shapes.Point(np.sqrt(2)/2, np.sqrt(2)/2), shapes.Point(-1*np.sqrt(2)/2, -1*np.sqrt(2)/2))
        res = operations.intersection(line, circle)
        self.assertEqual(set(res), set(exp))
    
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
        self.assertEqual(operations.intersection(line, point), None)
    
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
        exp = (shapes.Point(0.5, 1), shapes.Point(0.5, -1))
        res = operations.intersection(line, pol)
        self.assertEqual(set(res), set(exp))
    
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
        
        circle = shapes.Circle(shapes.Point(0, 0), 4)
        end1 = shapes.Point(-1, -1)
        end2 = shapes.Point(1, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(line, circle), None)
    
    def test_for_linesegment_and_circle2(self):
        """the second test for intersection between a circle and a line
        segment with them intersecting in one point
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        point = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(line, circle), point)
    
    def test_for_linesegment_and_circle3(self):
        """the third test for intersection between a circle and a line
        segment with them intersecting in two points
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(0, 10)
        end2 = shapes.Point(0, -3)
        line = shapes.LineSegment(end1, end2)
        res = (shapes.Point(0, 1), shapes.Point(0, -1))
        self.assertEqual(operations.intersection(line, circle), res)
    
    def test_for_linesegment_and_circle4(self):
        """the fourth test for intersection between a circle and a line
        segment with them being fully apart
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(5, 5)
        end2 = shapes.Point(6, 6)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(line, circle), None)
    
    def test_for_linesegment_and_circle5(self):
        """the fifth test for intersection between a circle and a line
        segment with one of the line's ends touching the perimeter of
        the circle
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        end1 = shapes.Point(1, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.intersection(line, circle), shapes.Point(1, 0))
    
    def test_for_linesegment_and_circle6(self):
        """the sixth test for intersection between a circle and a line
        segment with them touching in one point on the line's body
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 2)
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
    
    def test_for_linesegment_and_line4(self):
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
    
    def test_for_linesegment_and_linesegment4(self):
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
    
    def test_for_linesegment_and_linesegment5(self):
        """the fifth test for intersection between two line segments
        whith one of the first one's ends touching the other one's body
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 2)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(0, 4)
        end4 = shapes.Point(4, 0)
        line2 = shapes.LineSegment(end3, end4)
        point = shapes.Point(2, 2)
        self.assertEqual(operations.intersection(line1, line2), point)

    def test_for_linesegment_and_linesegment6(self):
        """the sixth test for intersection between two line segments
        with them touching each other's ends
        """
        
        end1 = shapes.Point(-1, 0)
        end2 = shapes.Point(1, 1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(1, 1)
        end4 = shapes.Point(2, 2)
        line2 = shapes.LineSegment(end3, end4)
        point = shapes.Point(1, 1)
        self.assertEqual(operations.intersection(line1, line2), point)
    
    def test_for_linesegment_and_linesegment7(self):
        """the seventh test for intersection between two line segments
        with one of them being horizental and the other vertical
        """
        
        p1 = shapes.Point(1, 1)
        p2 = shapes.Point(1, -1)
        l1 = shapes.LineSegment(p1, p2)
        p3 = shapes.Point(0.5, 0)
        p4 = shapes.Point(1.5, 0)
        l2 = shapes.LineSegment(p3, p4)
        exp = shapes.Point(1, 0)
        self.assertEqual(operations.intersection(l1, l2), exp)        


if __name__ == '__main__':
    unittest.main()