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


if __name__ == '__main__':
    unittest.main()