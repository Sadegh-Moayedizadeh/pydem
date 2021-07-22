"""test cases for the 'projection' function for two dimensional
entities
"""

import unittest
from geometry import two_dimensional_operations as operations
from geometry import two_dimensional_entities as shapes
import numpy as np


class TestProjection(unittest.TestCase):
    """test cases for the 'projection' function from
    'two_dimensional_operations' module
    """
    
    def test_for_point_and_point(self):
        """testing the projection of a given point on another given
        point
        """
        
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(1, 1)
        self.assertEqual(operations.projection(point1, point2), point2)
    
    def test_for_point_and_polygon1(self):
        """testing the projection of a given point on a given polygon
        with the point being inside the polygon
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.projection(point, pol), None)
    
    def test_for_point_and_polygon2(self):
        """the second test for projection of a given point on a given
        polygon with the point being located on the perimeter of the
        polygon
        """
        
        point = shapes.Point(2, 0)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        self.assertEqual(operations.projection(point, pol), point)
    
    def test_for_point_and_polygon3(self):
        """the third test for projection of a given point on a given
        polygon with the point being located outside the polygon
        """
        
        point = shapes.Point(0, 3)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(0, -4)
        v3 = shapes.Point(2, -2)
        v4 = shapes.Point(2, 2)
        v5 = shapes.Point(0, 4)
        v6 = shapes.Point(-2, 2)
        pol = shapes.Polygon(v1, v2, v3, v4, v5, v6)
        res = shapes.Point(0, 2)
        self.assertEqual(operations.projection(point, pol), res)
    
    def test_for_point_and_rectangle1(self):
        """the first test for projection of a given point on a given
        rectangle with the point being located inside the rectangle
        """
        
        point = shapes.Point(0, 0)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.projection(point, rec), None)
    
    def test_for_point_and_rectangle2(self):
        """the second test for projection of a given point on a given
        rectangle with the point being located on the perimeter of the
        rectangle
        """
        
        point = shapes.Point(1, 0)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.projection(point, rec), point)
    
    def test_for_point_and_rectangle3(self):
        """the third test for projection of a given point on a given
        rectangle with the point being located outside the rectangle
        """
        
        point = shapes.Point(2, 0)
        v1 = shapes.Point(-1, -1)
        v2 = shapes.Point(1, -1)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        res = shapes.Point(1, 0)
        self.assertEqual(operations.projection(point, rec), res)
    
    def test_for_polygon_and_circle1(self):
        """the first test for projection of a given point on a given
        circle with the point being located inside the circle
        """
        
        point = shapes.Point(0, 0)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.projection(point, circle), None)
    
    def test_for_polygon_and_circle2(self):
        """the second test for projection of a given point on a given
        rectangle with the point being located on the perimeter of the
        rectangle
        """
        
        point = shapes.Point(1, 0)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        self.assertEqual(operations.projection(point, circle), point)
    
    def test_for_polygon_and_circle3(self):
        """the third test for projection of a given point on a given
        rectangle with the point being located outside the rectangle
        """
        
        point = shapes.Point(2, 0)
        circle = shapes.Circle(shapes.Point(0, 0), 1)
        res = shapes.Point(1, 0)
        self.assertEqual(operations.projection(point, circle), res)
    
    def test_for_point_and_line1(self):    
        """the first test for projection of a given point on a given
        infinite line with the point being located on the line
        """
        
        point = shapes.Point(0, 0)
        line = shapes.Line(0, 0)
        self.assertEqual(operations.projection(point, line), point)
    
    def test_for_point_and_line2(self):
        """the second test for projection of a given point on a given
        infinite line with the point being located outside the line
        """
        
        point = shapes.Point(0, 1)
        line = shapes.Line(0, 0)
        res = shapes.Point(0, 0)
        self.assertEqual(operations.projection(point, line), res)
    
    def test_for_point_and_line3(self):
        """the third test for projection of a given point on a given
        infinite line with the point located outside the line and thee
        line being vertical
        """
        
        point = shapes.Point(1, 0)
        p1 = shapes.Point(0, 0)
        p2 = shapes.Point(0, 1)
        line = shapes.Line.from_points(p1, p2)
        res = shapes.Point(0, 0)
        self.assertEqual(operations.projection(point, line), res)
    
    def test_for_point_and_linesegment1(self):
        """the first test for projection of a given point on a given
        line segment with the point being located on the line
        """
        
        point = shapes.Point(0, 0)
        end1 = shapes.Point(0, -1)
        end2 = shapes.Point(0, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.projection(point, line), point)
    
    def test_for_point_and_linesegment2(self):
        """the second test for projection of a given point on a given
        line segment with the point being located outside the line and
        in front of it
        """
        
        point = shapes.Point(1, 0)
        end1 = shapes.Point(0, -1)
        end2 = shapes.Point(0, 1)
        line = shapes.LineSegment(end1, end2)
        res = shapes.Point(0, 0)
        self.assertEqual(operations.projection(point, line), res)
    
    def test_for_point_and_linesegment3(self):
        """the third test for projection of a given point on a given
        line segment with the point being located outside the line and
        not in front of it
        """
        
        point = shapes.Point(2, 2)
        end1 = shapes.Point(0, -1)
        end2 = shapes.Point(0, 1)
        line = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.projection(point, line), None)