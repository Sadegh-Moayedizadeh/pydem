"""test cases for miscellaneous functions for two dimensional entities
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


class TestBisector(unittest.TestCase):
    """test cases for the 'bisector' function in two_dimensional_operations'
    module
    """
    
    def test_for_parallel_lines(self):
        """testing for a condition where the given lines are parallel
        to each other
        """

        line1 = shapes.Line(0, 0)
        line2 = shapes.Line(0, 2)
        res = shapes.Line(0, 1)
        self.assertEqual(operations.bisector(line1, line2), res)
    
    def test_for_overlapping_linesegments(self):
        """testing for a condition where the given lines are LineSegment
        instances and overlap each other
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(2, 2)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(1, 1)
        end4 = shapes.Point(3, 3)
        line2 = shapes.LineSegment(end3, end4)
        res = shapes.Line(1, 0)
        self.assertEqual(operations.bisector(line1, line2), res)
    
    def test_for_orthogonal_lines1(self):
        """the first test for two orthogonal lines which are located
        both within the first quarter of the trigonomic circle
        """

        line1 = shapes.Line(0, 0)
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        line2 = shapes.Line.from_points(point1, point2)
        res = shapes.Line(1, 0)
        self.assertEqual(operations.bisector(line1, line2), res)
    
    def test_for_orthogonal_lines2(self):
        """the second test for two orthogonal lines in a way that their
        bisector is a vertical line
        """

        line1 = shapes.Line(1, 0)
        line2 = shapes.Line(-1, 0)
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        res = shapes.Line.from_points(point1, point2)
        self.assertEqual(operations.bisector(line1, line2), res)
    
    def test_for_arbitrary_slopes1(self):
        """the first test for finding the bisector of two line segments
        with arbitrary slopes both located in the second quarter of the
        trigonometric circle
        """

        end1 = shapes.Point(-2, 1)
        end2 = shapes.Point(-4, 2)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(-1, 2)
        end4 = shapes.Point(-2, 4)
        line2 = shapes.LineSegment(end3, end4)
        res = shapes.Line(-1, 0)
        self.assertEqual(operations.bisector(line1, line2), res)

    def test_for_arbitrary_slopes2(self):
        """the second test for two line segments that one of them is
        located at the first quarter and the other at the second quarter
        of the trigonomical circle
        """
        
        end1 = shapes.Point(-2, 1)
        end2 = shapes.Point(-4, 2)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(2, 1)
        end4 = shapes.Point(4, 2)
        line2 = shapes.LineSegment(end3, end4)
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        res = shapes.Line.from_points(point1, point2)
        self.assertEqual(operations.bisector(line1, line2), res)


class TestNormal(unittest.TestCase):
    """test cases for the 'normal' function in two_dimensional_operations
    module
    """

    def test_for_point_on_line(self):
        """test for the normal line of a given line from a given point
        located on that line
        """

        point = shapes.Pont(0, 0)
        line = shapes.Line(0, 0)
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        res = shapes.Line.from_points(point1, point2)
        self.assertEqual(operations.normal(point, line), res)
    
    def test_for_vertical_line(self):
        """test for the normal line of a vertical line
        """

        point = shapes.Point(1, 1)
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        line = shapes.Line.from_points(point1, point2)
        res = shapes.Line(0, 1)
        self.assertEqual(operations.normal(point, line), res)
    
    def test_for_line_with_arbitrary_slope(self):
        """test for the normal line of a given line with and arbitrarry
        slope
        """

        point = shapes.Point(-1, -1)
        line = shapes.Line(1, 0)
        res = shapes.Line(-1, 0)
        self.assertEqual(operations.normal(point, line), res)


class TestIntersectionLength(unittest.TestCase):
    """test cases for the 'intersection_length' function in the
    two_dimensional_operations module
    """

    def test_for_non_intersecting_line(self):
        """test for intersection length of two given lines that do not
        intersect each other
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(1, 0)
        end4 = shapes.Point(3, 2)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.intersection_length(line1, line2), 0)
    
    def test_for_lines_touching_others_ends(self):
        """test for intersection length of two given line segments that
        touch each other's ends
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(1, 0)
        end4 = shapes.Point(0, 1)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.intersection_length(line1, line2), 0)
    
    def test_for_overlapping_lines(self):
        """test for intersection length of two given line segments that
        are overlapping each other
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(0, -0.25)
        end4 = shapes.Point(0, 0.75)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.intersection_length(line1, line2), 0.75)
    
    def test_for_intersecting_lines1(self):
        """a general test for two line segments intersecting each other
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(-1, 0.5)
        end4 = shapes.Point(1, 0.5)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.intersection_length(line1, line2), 0.5)
    
    def test_for_intersecting_lines2(self):
        """basically the previous test but with the order of the lines
        given reversed
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(-1, 0.5)
        end4 = shapes.Point(1, 0.5)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.intersection_length(line2, line1), 1)
    
    def test_for_intersecting_lines3(self):
        """the third test for intersection length between two line
        segments with the first one only touching the second one
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(-1, 0.5)
        end4 = shapes.Point(0, 0.5)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.intersection_length(line2, line1), 0)
    
    def test_for_intersecting_lines4(self):
        """the fourth test for intersection length between two line
        segments with the second one only touching the first one
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(-1, 0.25)
        end4 = shapes.Point(0, 0.25)
        line2 = shapes.LineSegment(end3, end4)
        self.assertEqual(operations.intersection_length(line1, line2), 0.25)
    
    def test_for_line_and_rectangle1(self):
        """the first test for intersection length of a line segment and
        a rectangle with the line segment being located inside the
        rectangle
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection_length(line, rec), 0)
    
    def test_for_line_and_rectangle2(self):
        """the second test for intersection length of a line segment and
        a rectangle with the line segment being located inside the
        rectangle but one of its ends touching rectangle's perimeter
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 2)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection_length(line, rec), 0)
    
    def test_for_line_and_rectangle3(self):
        """the third test for intersection length of a line segment and
        a rectangle with the line segment simply intersecting the
        rectangle
        """

        end1 = shapes.Point(0, 4)
        end2 = shapes.Point(0, 1)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection_length(line, rec), 1)
    
    def test_for_line_and_rectangle4(self):
        """the fourth test for intersection length of a line segment
        and a rectangle with the line segment passing through the
        rectangle
        """

        end1 = shapes.Point(0, 4)
        end2 = shapes.Point(0, -4)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection_length(line, rec), 4)
    
    def test_for_line_and_rectangle5(self):
        """the fifth test for intersection length of a line segment and
        a rectangle with the line segment overlapping a part of the
        rectangle's perimeter
        """

        end1 = shapes.Point(2, 0)
        end2 = shapes.Point(2, 5)
        line = shapes.LineSegment(end1, end2)
        v1 = shapes.Point(-2, -2)
        v2 = shapes.Point(2, -2)
        v3 = shapes.Point(2, 2)
        v4 = shapes.Point(-2, 2)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(operations.intersection_length(line, rec), 2)


if __name__ == '__main__':
    unittest.main()