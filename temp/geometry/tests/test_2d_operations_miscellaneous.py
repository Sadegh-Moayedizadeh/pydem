"""test cases for miscellaneous functions for two dimensional entities
"""

import sys
import unittest

import numpy as np
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations


class TestOppositeSides(unittest.TestCase):
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
        
        line = shapes.Line(1, 0)
        point1 = shapes.Point(0, 1)
        point2 = shapes.Point(0, -1)
        point3 = shapes.Point(0, 2)
        self.assertTrue(operations.opposite_sides(line, point1, point2))
        self.assertFalse(operations.opposite_sides(line, point1, point3))
    
    def test_for_point_on_the_line(self):

        line = shapes.Line(0, 1)
        point1 = shapes.Point(0, 1)
        point2 = shapes.Point(0, -1)
        self.assertFalse(operations.opposite_sides(line, point1, point2))


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

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(-1, 2)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(0, 0)
        end4 = shapes.Point(-2, 1)
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

        point = shapes.Point(0, 0)
        line = shapes.Line(0, 0)
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        res = shapes.Line.from_points(point1, point2)
        self.assertEqual(operations.normal(point, line), res)
    
    def test_for_vertical_line(self):
        """test for the normal line of a vertical line with the point
        being located on the line
        """

        point = shapes.Point(0, 2)
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        line = shapes.Line.from_points(point1, point2)
        res = shapes.Line(0, 2)
        self.assertEqual(operations.normal(point, line), res)
    
    def test_for_vertical_line2(self):
        """second test for a vertical line with the point not being
        located on the line
        """

        p1 = shapes.Point(1, 0)
        p2 = shapes.Point(1, 1)
        line = shapes.Line.from_points(p1, p2)
        point = shapes.Point(-1, -2)
        exp = shapes.Line(0, -2)
        res = operations.normal(point, line)
        self.assertEqual(res, exp)
    
    def test_for_horizental_line1(self):
        """test for the normal line of a horizental line with the point
        being located on the line
        """

        line = shapes.Line(0, 2)
        point = shapes.Point(0, 2)
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        res = operations.normal(point, line)
        exp = shapes.Line.from_points(point1, point2)
        self.assertEqual(res, exp)
    
    def test_for_horizental_line2(self):
        """test for the normal line of a horizental line with the point
        not being located on the line
        """

        line = shapes.Line(0, 0)
        point = shapes.Point(0, -2)
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        res = operations.normal(point, line)
        exp = shapes.Line.from_points(point1, point2)
        self.assertEqual(res, exp)
    
    def test_for_line_with_arbitrary_slope(self):
        """test for the normal line of a given line with and arbitrarry
        slope
        """

        point = shapes.Point(-1, -1)
        line = shapes.Line(1, 0)
        res = shapes.Line(-1, -2)
        self.assertEqual(operations.normal(point, line), res)
    
    def test_for_point_outside_the_line(self):
        """testing for a line with arbitrary inclination and a point
        outside the line
        """

        point = shapes.Point(0, -1)
        line = shapes.Line(1, 0)
        res = shapes.Line(-1, -1)
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
        self.assertEqual(operations.intersection_length(line, rec), 1)
    
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
        self.assertEqual(operations.intersection_length(line, rec), 2)
    
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

    def test_for_line_and_circle1(self):
        """the first test for intersection length of a given line and a
        given circle with the line being located inside the circle
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 0.5)
        line = shapes.LineSegment(end1, end2)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.intersection_length(line, circle), 0.5)
    
    def test_for_line_and_circle2(self):
        """the second test for intersection length of a given line and
        a given circle with the line segment being located inside the
        circle but with one of its ends touching the circle's perimeter
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1)
        line = shapes.LineSegment(end1, end2)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.intersection_length(line, circle), 1)
    
    def test_for_line_and_circle3(self):
        """the third test for intersection length of a given line and a
        given circle with the line passing through the circle
        """

        end1 = shapes.Point(0, -2)
        end2 = shapes.Point(0, 2)
        line = shapes.LineSegment(end1, end2)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.intersection_length(line, circle), 2)
    
    def test_for_line_and_circle4(self):
        """the fourth test for intersection length of a given line and
        a given circle with the line simply intersecting the circle and
        with the larger part being located inside the circle
        """
        
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 1.5)
        line = shapes.LineSegment(end1, end2)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.intersection_length(line, circle), 1)
    
    def test_for_line_and_circle5(self):
        """the fifth test for intersection length of a given line and a
        given circle with them simply intersecting each other and the
        larger part of the line being outside the circle
        """

        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(0, 4)
        line = shapes.LineSegment(end1, end2)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.intersection_length(line, circle), 1)
    
    def test_for_line_and_circle6(self):
        """the sixth test for intersection length of a line andd a
        circle with one of line's ends simply touching the circle's
        perimeter
        """

        end1 = shapes.Point(0, 2)
        end2 = shapes.Point(0, 1)
        line = shapes.LineSegment(end1, end2)
        circle = shapes.Circle(shapes.Point(0, 0), 2)
        self.assertEqual(operations.intersection_length(line, circle), 0)
    

class TestAngleInBetween(unittest.TestCase):
    """test cases for the 'angle_in_between' function in the
    'two_dimensional_operations' module
    """

    def test_for_parallel_lines1(self):
        """the first test for angle in between two parallel lines with
        them being horizental
        """

        line1 = shapes.Line(0, 0)
        line2 = shapes.Line(0, 1)
        self.assertEqual(operations.angle_in_between(line1, line2), 0)
    
    def test_for_parallel_lines2(self):
        """the second test for angle in between two parallel lines with
        them being vertical
        """

        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        line1 = shapes.Line.from_points(point1, point2)
        point3 = shapes.Point(1, 0)
        point4 = shapes.Point(1, 1)
        line2 = shapes.Line.from_points(point3, point4)
        self.assertEqual(operations.angle_in_between(line1, line2), 0)
    
    def test_for_parallel_lines3(self):
        """the third test for two lines which are parallel but
        constructed in different ways
        """

        line1 = shapes.Line(1, 0)
        end1 = shapes.Point(0, 0)
        end2 = shapes.Point(-1, -1)
        line2 = shapes.LineSegment(end1, end2)
        self.assertEqual(operations.angle_in_between(line1, line2), 0)
        
    
    def test_for_orthogonal_lines1(self):
        """the first test for two orthogonal lines which are located
        both within the first quarter of the trigonomic circle
        """

        line1 = shapes.Line(0, 0)
        point1 = shapes.Point(0, 0)
        point2 = shapes.Point(0, 1)
        line2 = shapes.Line.from_points(point1, point2)
        res = (np.math.pi / 2)
        self.assertEqual(operations.angle_in_between(line1, line2), res)
    
    def test_for_orthogonal_lines2(self):
        """the second test for two orthogonal lines in a way that their
        bisector is a vertical line
        """

        line1 = shapes.Line(1, 0)
        line2 = shapes.Line(-1, 0)
        res = (np.math.pi / 2)
        self.assertEqual(operations.angle_in_between(line1, line2), res)
    
    def test_for_arbitrary_slopes1(self):
        """the first test for finding the angle in between two line segments
        with arbitrary slopes both located in the third quarter of the
        trigonometric circle
        """

        end1 = shapes.Point(-1, -1)
        end2 = shapes.Point(-2, -2)
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(-1, 0)
        end4 = shapes.Point(0, np.sqrt(3))
        line2 = shapes.LineSegment(end3, end4)
        res = operations.angle_in_between(line1, line2)
        exp = np.math.pi / 12
        self.assertAlmostEqual(res, exp)

    def test_for_arbitrary_slopes2(self):
        """the second test for two line segments that one of them is
        located at the first quarter and the other at the second quarter
        of the trigonomical circle
        """
        
        end1 = shapes.Point(2, 1)
        end2 = shapes.Point(1, 1 + np.sqrt(3))
        line1 = shapes.LineSegment(end1, end2)
        end3 = shapes.Point(-1, 0)
        end4 = shapes.Point(0, np.sqrt(3))
        line2 = shapes.LineSegment(end3, end4)
        res = operations.angle_in_between(line1, line2)
        exp = np.math.pi / 3
        self.assertAlmostEqual(res, exp)



class TestStandardizedInclination(unittest.TestCase):
    """test cases for the 'standardized_inclination' function from the
    'two_dimensional_operations' module
    """

    def test_for_a_standard_angle(self):
        """testing for an angle that is between 0 and pi radians
        """

        inc = np.math.pi/2
        self.assertEqual(operations.standardized_inclination(inc), inc)
    
    def test_for_angle_equal_to_pi(self):
        """testing for an angle equal to pi radians
        """

        inc = np.math.pi
        self.assertEqual(operations.standardized_inclination(inc), 0)
    
    def test_for_angle_between_pi_and_2pi(self):
        """testing for an angle between pi and 2*pi radians
        """

        inc = 3 * np.math.pi / 2
        res = np.math.pi / 2
        self.assertEqual(operations.standardized_inclination(inc), res)
    
    def test_for_angle_equal_to_2pi(self):
        """testing for an angle equal to 2*pi radians
        """

        inc = 2* np.math.pi
        res = 0
        self.assertEqual(operations.standardized_inclination(inc), res)
    
    def test_for_angle_more_than_2pi(self):
        """testing for an angle more than 2*pi radians
        """

        inc = 5 * np.math.pi / 2
        res = np.math.pi / 2
        self.assertEqual(operations.standardized_inclination(inc), res)


class TestIntersectionArea(unittest.TestCase):
    """test cases for 'intersection_area' method
    """
    
    def test_rectangles_being_apart(self):
        """testing the 'intersection_area' function where the two given
        rectangles are fully apart
        """
        
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(1, 0)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(0, 1)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(10, 0)
        v6 = shapes.Point(11, 0)
        v7 = shapes.Point(11, 1)
        v8 = shapes.Point(10, 1)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection_area(rec1, rec2), 0)

    def test_ractangle_inside_the_other(self):
        """testing the 'intersection_are' function where the first
        given rectangle is located fully inside the second one
        """

        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(1, 0)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(0, 1)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-10, -10)
        v6 = shapes.Point(10, -10)
        v7 = shapes.Point(10, 10)
        v8 = shapes.Point(-10, 10)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection_area(rec1, rec2), 1)

    def test_rectangles_intersect_on_the_corner(self):
        """testing the 'intersection_area' method where the two given
        rectangles are intersecting each other on two different edges
        on the corner of each other
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(1, 0)
        v3 = shapes.Point(1, 2)
        v4 = shapes.Point(-1, 2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(0, -5)
        v6 = shapes.Point(5, -5)
        v7 = shapes.Point(5, 1)
        v8 = shapes.Point(0, 1)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection_area(rec1, rec2), 1)

    def test_rectangles_with_overlapping_edges1(self):
        """testing the 'intersection_area' method where the two given
        rectangles having one overlapping edge but with no common area
        """
        
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(1, 0)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(0, 1)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(-1, -5)
        v6 = shapes.Point(0, -5)
        v7 = shapes.Point(0, 5)
        v8 = shapes.Point(-1, 5)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection_area(rec1, rec2), 0)
    
    def test_rectangles_with_overlapping_edges2(self):
        """testing the 'intersection_area' method where the two given
        rectangles having one overlapping edge but and with the second
        one being inside the first one
        """
        
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(1, 0)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(0, 1)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(3, -5)
        v6 = shapes.Point(0, -5)
        v7 = shapes.Point(0, 5)
        v8 = shapes.Point(3, 5)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection_area(rec1, rec2), 1)
    
    def test_rectangles_intersect_on_one_edge(self):
        """testing the 'intersection_area' function where the two given
        rectangles intersect in two points on the same edge of the
        bigger rectangle
        """
        
        v1 = shapes.Point(-1, 0)
        v2 = shapes.Point(1, 0)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(-1, 1)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(3, -5)
        v6 = shapes.Point(0, -5)
        v7 = shapes.Point(0, 5)
        v8 = shapes.Point(3, 5)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection_area(rec1, rec2), 1)
    
    def test_rectangles_with_two_overlapping_edges(self):
        """testing the 'intersection_area' function where the first
        given rectangle is located inside the second one and two of its
        edges overlaps with that rectangle
        """

        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(1, 0)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(0, 1)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(3, -5)
        v6 = shapes.Point(0, -5)
        v7 = shapes.Point(0, 1)
        v8 = shapes.Point(3, 1)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection_area(rec1, rec2), 1)
    
    def test_rectangles_overlapping_parallel_edges(self):
        """testing the 'intersection_area' function where the given
        rectangles have their parallel edges overlapping each other
        """
        
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(1, 0)
        v3 = shapes.Point(1, 1)
        v4 = shapes.Point(0, 1)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(3, 0)
        v6 = shapes.Point(-1, 0)
        v7 = shapes.Point(-1, 1)
        v8 = shapes.Point(3, 1)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection_area(rec1, rec2), 1)
    
    def test_rectangles_overlapping_one_edge_and_intersecting(self):
        """testing the 'intersection_area' function where the given
        rectangles overlap each other on one edge and intersect each
        other in one other point
        """
        
        v1 = shapes.Point(0, 0)
        v2 = shapes.Point(1, 0)
        v3 = shapes.Point(1, 2)
        v4 = shapes.Point(0, 2)
        rec1 = shapes.Rectangle(v1, v2, v3, v4)
        v5 = shapes.Point(3, -2)
        v6 = shapes.Point(0, -2)
        v7 = shapes.Point(0, 1)
        v8 = shapes.Point(3, 1)
        rec2 = shapes.Rectangle(v5, v6, v7, v8)
        self.assertEqual(operations.intersection_area(rec1, rec2), 1)


if __name__ == '__main__':
    unittest.main()