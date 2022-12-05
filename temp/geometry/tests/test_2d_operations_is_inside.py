"""test cases for the 'is_inside' function for two dimensional entities
"""

import unittest
from geometry import two_dimensional_operations as operations
from geometry import two_dimensional_entities as shapes
import numpy as np
import sys


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
        rec = shapes.Rectangle(v6, v7, v8, v9)
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
        rec = shapes.Rectangle(v6, v7, v8, v9)
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
        rec = shapes.Rectangle(v6, v7, v8, v9)
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
        end2 = shapes.Point(1, 1)
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
        
        circle = shapes.Circle(shapes.Point(-1, 0), 2)
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
        
        circle = shapes.Circle(shapes.Point(0, -1), 2)
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
        
        circle1 = shapes.Circle(shapes.Point(0.1, 0), 0.5)
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
        end2 = shapes.Point(2, 0)
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
        end2 = shapes.Point(0, 0.4)
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


if __name__ == '__main__':
    unittest.main()