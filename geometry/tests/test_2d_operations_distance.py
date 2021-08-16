"""test cases for 'distance' function for two dimensional entities
"""

import unittest
from geometry import two_dimensional_operations as operations
from geometry import two_dimensional_entities as shapes
import numpy as np
import sys


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
        
        point = shapes.Point(2, 0)
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
        
        point = shapes.Point(3, 0)
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
        
        point = shapes.Point(1, 0)
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
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.distance(point, circle), -1)
    
    def test_for_point_and_circle2(self):
        """the second test for distance between a given point and a
        given circle with the point being located on the circle's
        perimeter
        """
        
        point = shapes.Point(0, 1)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.distance(point, circle), 0)
    
    def test_for_point_and_circle3(self):
        """the third test for distance between a given point and a
        given circle with the point being located outside the given
        circle
        """
        
        point = shapes.Point(0, 2)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
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
        self.assertEqual(operations.distance(point, line), 1)
    
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
        
        point = shapes.Point(3, 0)
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
        pol2 = shapes.Polygon(v7, v8, v9, v10, v11, v12)
        self.assertEqual(operations.distance(pol1, pol2), -0.8320502943378438)
    
    def test_for_polygon_and_polygon2(self):
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
        pol2 = shapes.Polygon(v7, v8, v9, v10, v11, v12)
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
        pol2 = shapes.Polygon(v7, v8, v9, v10, v11, v12)
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
        pol2 = shapes.Polygon(v7, v8, v9, v10, v11, v12)
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
        circle = shapes.Circle(shapes.Point(0, 0), 10)
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
        circle = shapes.Circle(shapes.Point(4, 0), 2)
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
        
        circle = shapes.Circle(shapes.Point(0, 0), 4)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(1, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, circle), -1)
    
    def test_for_linesegment_and_circle2(self):
        """the second test for distance between a given line segment
        and a given circle with them intersecting each other
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 4)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 0)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, circle), 0)
    
    def test_for_linesegment_and_circle3(self):
        """the third test for distance between a given line segment and
        a given circle with the line segment being outside the circle
        and being vertical
        """
        
        circle = shapes.Circle(shapes.Point(0, 0), 4)
        end1 = shapes.Point(3, -1)
        end2 = shapes.Point(3, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.distance(line, circle), 1)
    
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


if __name__ == '__main__':
    unittest.main()