"""test cases for all the base classes for particles
"""

import unittest
import numpy as np
from typing import Type, Union, Any
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations
from generation import base_classes
import sys
import logging


class TestParticle(unittest.TestCase):
    """test cases for the Particle class in base_classes module; the
    methods 'move', 'mass', and 'moment_of_inertia' will be tested
    under test classes for other particle types as the Particle class
    is their parent class; other stuff that are tested here will also
    be tested for the child classes
    """

    def test_ascending_particle_number(self):
        """testing if the particle number increases correctly by
        instantiating new ones
        """

        particle1 = base_classes.Particle(x = 0, y = 0, inclination = 0)
        particle2 = base_classes.Particle(x = 1, y = 1, inclination = 0)
        self.assertEqual(particle1.num + 1, particle2.num)

    def test_descending_particle_number(self):
        """testing if the 'last_num' class attribute decreases by
        deleting a particle and a new instance gets its number
        correctly
        """

        particle1 = base_classes.Particle(x = 0, y = 0, inclination = 0)
        particle2 = base_classes.Particle(x = 1, y = 1, inclination = 0)
        del particle2
        self.assertEqual(base_classes.Particle.last_num, particle1.num+1)
        particle3 = base_classes.Particle(x = 1, y = 1, inclination = 0)
        self.assertEqual(particle1.num + 1, particle3.num)

    def test_hashable(self):
        """testing if a generated particle is hashable or not
        """

        particle = base_classes.Particle(x = 0, y = 0, inclination = 0)
        s = {particle}
        self.assertTrue(s)

    def test_equality_condition(self):
        """testing the equality condition of a particle instance; a
        particle should only be equal to itself
        """

        particle1 = base_classes.Particle(x = 0, y = 0, inclination = 0)
        particle2 = base_classes.Particle(x = 0, y = 0, inclination = 0)
        self.assertNotEqual(particle1, particle2)

    def test_box_num(self):
        """testing if a the 'box_num' method of a Particle instance
        generates the correct box number given its required arguments
        """

        particle = base_classes.Particle(x = 55, y = 58, inclination = 0)
        bn = particle.box_num(nc = 100, box_length = 10, box_width = 10)
        self.assertEqual(bn, 505)  


class TestClay(unittest.TestCase):
    """test cases for the Clay class from the base_classes module; some
    of the methods and attribute assignings that happen in the parent
    class 'Particle' will also be tested to see if they work here;
    these kind of tests might not be repeated for similar classes, so
    if any changes to the source code takes place those should also be
    taken care of; mehtods tested here will also be tested in at least
    one of the classes that inherit from it
    """

    def test_ascending_particle_number(self):
        """testing if the particle number thing works in this class too
        in the ascending manner; it should be correctly inherited from
        the parent class 'Particle'
        """
        
        particle1 = base_classes.Clay(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 1, length = 100,
            )
        particle2 = base_classes.Clay(
            x = 1, y = 1, inclination = np.math.pi/4, thickness = 1, length = 100,
            )
        self.assertEqual(particle1.num + 1, particle2.num)

    def test_descending_particle_number(self):
        """testing if the particle number thing works in this class too
        in the descending manner; it should be correctly inherited from
        the parent class 'Particle'
        """
        
        particle1 = base_classes.Clay(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 1, length = 100,
            )
        particle2 = base_classes.Clay(
            x = 1, y = 1, inclination = np.math.pi/4, thickness = 1, length = 100,
            )
        del particle2
        self.assertEqual(base_classes.Particle.last_num, particle1.num+1)
        particle3 = base_classes.Clay(
            x = 1, y = 1, inclination = np.math.pi/4, thickness = 1, length = 100,
            )
        self.assertEqual(particle1.num + 1, particle3.num)
    
    def test_hashable(self):
        """testing if the particle being hashable works here too; it is
        inherited from the parent class 'Particle'
        """

        particle = base_classes.Clay(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 1, length = 100,
            )
        s = {particle}
        self.assertTrue(s)

    def test_equality_condition(self):
        """testing if the equality condition works here to; it is
        inherited from the parent class 'Particle'
        """

        particle1 = base_classes.Clay(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 1, length = 100,
            )
        particle2 = base_classes.Clay(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 1, length = 100,
            )
        self.assertNotEqual(particle1, particle2)

    def test_box_num(self):
        """testing if the box_number method works here too; it is
        inherited from the parent class 'Particle'
        """

        particle = base_classes.Clay(
            x = 501, y = 74, inclination = np.math.pi/4, thickness = 1, length = 100,
            )
        bn = particle.box_num(nc = 100, box_length = 10, box_width = 10)
        self.assertEqual(bn, 750)

    def test_standardizing_inclination1(self):
        """testing if a non-standard given inclination becomes standard
        """

        particle = base_classes.Clay(
            x = 501, y = 74, inclination = 3*np.math.pi/2, thickness = 1, length = 100,
            )
        self.assertEqual(particle.inclination, np.math.pi/2)
    
    def test_standardizing_inclination2(self):
        """testing if a non-standard given inclination becomes standard
        with a negative inclination given
        """

        particle = base_classes.Clay(
            x = 501, y = 74, inclination = -1*np.math.pi/6, thickness = 1, length = 100,
            )
        self.assertAlmostEqual(particle.inclination, 5*np.math.pi/6)

    def test_attribute_assigning(self):
        """testing if all the attributes that a Clay instance should
        contain are present here; this also includes all the attributes
        and properties of the parent class 'Particle'
        """

        particle = base_classes.Clay(
            x = 501, y = 74, inclination = -1*np.math.pi/6, thickness = 1, length = 100,
            )
        self.assertEqual(particle.x, 501)
        self.assertEqual(particle.y, 74)
        self.assertAlmostEqual(particle.inclination, 5*np.math.pi/6)
        self.assertEqual(particle.thickness, 1)
        self.assertEqual(particle.length, 100)
        self.assertFalse(particle.is_segment)
        self.assertTrue(particle.midline)
        self.assertTrue(particle.midpoint)
        self.assertTrue(particle.segments)

    def test_midpoint(self):
        """testing if the midpoint attribute of the Clay instance is
        created correctly
        """

        particle = base_classes.Clay(
            x = 501, y = 74, inclination = -1*np.math.pi/6, thickness = 1, length = 100,
            )
        self.assertEqual(particle.midpoint, shapes.Point(501, 74))

    def test_midline(self):
        """testing if the midline attribute of the Clay instance is
        created correctly
        """

        particle = base_classes.Clay(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 1, length = 20*np.sqrt(2),
            )
        line = shapes.LineSegment(shapes.Point(-10, -10), shapes.Point(10, 10))
    
    def test_shape(self):
        """testing if the 'shape' attribute of the Clay instance is
        created correctly
        """

        particle = base_classes.Clay(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 20*np.sqrt(2), length = 20*np.sqrt(2),
            )
        v1 = shapes.Point(-20, 0)
        v2 = shapes.Point(0, -20)
        v3 = shapes.Point(20, 0)
        v4 = shapes.Point(0, 20)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(particle.shape, rec)

    def test_segmentalize(self):
        """testing if the 'segments' attribute of the Clay instance is
        created correctly using the 'segmentalize' method of the class;
        it should generate three segments which all have the same 'num'
        attribute; also testing if the next created particle comes with
        a correct 'num' attribute
        """

        particle = base_classes.Clay(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 1, length = 6*np.sqrt(2),
            )
        self.assertEqual(len(particle.segments), 3)
        for seg in particle.segments:
            self.assertTrue(seg.is_segment)
        self.assertEqual(particle.segments[1].midpoint, shapes.Point(0, 0))
        self.assertEqual(particle.segments[0].length, 2*np.sqrt(2))
        self.assertEqual(particle.segments[2].midline, shapes.LineSegment(shapes.Point(1, 1), shapes.Point(3, 3)))
        

class TestSand(unittest.TestCase):
    """test cases for the 'Sand' class from 'base_classes' module; the
    methods inherited from the parent class 'Particle' will also be
    tested here; mehtods tested here will also be tested in at least
    one of the classes that inherit from it
    """
    
    def test_ascending_particle_number(self):
        """testing if the particle number thing works in this class too
        in the ascending manner; it should be correctly inherited from
        the parent class 'Particle'
        """
        
        particle1 = base_classes.Sand(x = 0, y = 0, diameter = 10)
        particle2 = base_classes.Sand(x = 20, y = 0, diameter = 10)
        self.assertEqual(particle1.num + 1, particle2.num)

    def test_descending_particle_number(self):
        """testing if the particle number thing works in this class too
        in the descending manner; it should be correctly inherited from
        the parent class 'Particle'
        """
        
        particle1 = base_classes.Sand(x = 0, y = 0, diameter = 10)
        particle2 = base_classes.Sand(x = 20, y = 0, diameter = 10)
        del particle2
        self.assertEqual(particle1.num + 1, base_classes.Particle.last_num)
        particle3 = base_classes.Sand(x = 20, y = 0, diameter = 10)
        self.assertEqual(particle1.num + 1, particle3.num)
    
    def test_hashable(self):
        """testing if the particle being hashable works here too; it is
        inherited from the parent class 'Particle'
        """

        particle = base_classes.Sand(x = 0, y = 0, diameter = 10)
        s = {particle}
        self.assertTrue(s)

    def test_equality_condition(self):
        """testing if the equality condition works here to; it is
        inherited from the parent class 'Particle'
        """

        particle1 = base_classes.Sand(x = 0, y = 0, diameter = 10)
        particle2 = base_classes.Sand(x = 0, y = 0, diameter = 10)
        self.assertNotEqual(particle1, particle2)

    def test_box_num(self):
        """testing if the box_number method works here too; it is
        inherited from the parent class 'Particle'
        """

        particle = base_classes.Sand(x = 482, y = 376, diameter = 10)
        bn = particle.box_num(nc = 100, box_length = 10, box_width = 10)
        self.assertEqual(bn, 3748)
    
    def test_shape(self):
        """testing if the 'shape' attribute of the Sand instance is
        assigned correctly
        """

        particle = base_classes.Sand(x = 0, y = 0, diameter = 10)
        self.assertEqual(particle.shape, shapes.Circle(shapes.Point(0, 0), 10))
    
    def test_attribute_assigning(self):
        """testing if all the attributes that a Sand instance should
        contain are present here; this also includes all the attributes
        and properties of the parent class 'Particle'
        """

        particle = base_classes.Sand(x = 0, y = 0, diameter = 10)
        self.assertEqual(particle.x, 0)
        self.assertEqual(particle.y, 0)
        self.assertEqual(particle.diameter, 10)
        self.assertEqual(particle.shape, shapes.Circle(shapes.Point(0, 0), 10))
        self.assertEqual(particle.velocity, 0)
        self.assertEqual(particle.force, (0, 0, 0))
        self.assertEqual(particle.hierarchy, -1)

class TestQuartz(unittest.TestCase):
    """test cases for the Quartz class from 'base_classes' module; all
    the stuff inherited from the parent classes -'Sand' and 'Particle'-
    will also be tested here to see if they work correctly or not
    """

    def test_ascending_particle_number(self):
        """testing if the particle number thing works in this class too
        in the ascending manner; it should be correctly inherited from
        the parent class 'Particle'
        """
        
        particle1 = base_classes.Quartz(x = 0, y = 0, diameter = 10)
        particle2 = base_classes.Quartz(x = 0, y = 0, diameter = 10)
        self.assertEqual(particle1.num + 1, particle2.num)

    def test_descending_particle_number(self):
        """testing if the particle number thing works in this class too
        in the descending manner; it should be correctly inherited from
        the parent class 'Particle'
        """
        
        particle1 = base_classes.Quartz(x = 0, y = 0, diameter = 10)
        particle2 = base_classes.Quartz(x = 0, y = 0, diameter = 10)
        del particle2
        self.assertEqual(particle1.num+1, base_classes.Particle.last_num)
        particle3 = base_classes.Quartz(x = 0, y = 0, diameter = 10)
        self.assertEqual(particle1.num + 1, particle3.num)
    
    def test_hashable(self):
        """testing if the particle being hashable works here too; it is
        inherited from the parent class 'Particle'
        """

        particle = base_classes.Quartz(x = 0, y = 0, diameter = 10)
        s = {particle}
        self.assertTrue(s)

    def test_equality_condition(self):
        """testing if the equality condition works here to; it is
        inherited from the parent class 'Particle'
        """

        particle1 = base_classes.Quartz(x = 0, y = 0, diameter = 10)
        particle2 = base_classes.Quartz(x = 0, y = 0, diameter = 10)
        self.assertNotEqual(particle1, particle2)

    def test_box_num(self):
        """testing if the box_number method works here too; it is
        inherited from the parent class 'Particle'
        """

        particle = base_classes.Sand(x = 1, y = 1, diameter = 10)
        bn = particle.box_num(nc = 100, box_length = 10, box_width = 10)
        self.assertEqual(bn, 0)
    
    def test_diameter_validation(self):
        """testing if the invalid input for 'diameter' argument raises
        an error and valid ones goes alright; this behavior is
        inherited from the parent class 'Sand'
        """
        
        d = base_classes.Quartz.diameter_bounds[1]+1
        self.assertRaises(RuntimeError, base_classes.Quartz, x=0, y=0, diameter=d)
    
    def test_shape(self):
        """testing if the 'shape' attribute of the Sand instance is
        assigned correctly; this behavior is inherited from the parent
        class 'Sand'
        """

        particle = base_classes.Sand(x = 1, y = 1, diameter = 10)
        self.assertEqual(particle.shape, shapes.Circle(shapes.Point(1, 1), 10))
    
    def test_attribute_assigning(self):
        """testing if all the attributes that a Sand instance should
        contain are present here; this also includes all the attributes
        and properties of the parent classes 'Particle' and 'Sand'
        """

        particle = base_classes.Sand(x = 1, y = 1, diameter = 10)
        self.assertEqual(particle.x, 1)
        self.assertEqual(particle.y, 1)
        self.assertEqual(particle.diameter, 10)
        self.assertEqual(particle.shape, shapes.Circle(shapes.Point(1, 1), 10))
        self.assertEqual(particle.velocity, 0)
        self.assertEqual(particle.force, (0, 0, 0))
        self.assertEqual(particle.hierarchy, -1)
    
    def test_move(self):
        """testing if the Quartz instance moves correctly with the 
        given derivatives; this is inherited from the parent class
        'Particle'
        """

        particle = base_classes.Sand(x = 1, y = 1, diameter = 10)
        particle.move(delta_x = 2, delta_y = 2)
        self.assertEqual(particle.x, 3)
        self.assertEqual(particle.y, 3)
        self.assertEqual(particle.shape, shapes.Circle(shapes.Point(3, 3), 10))

    def test_mass(self):
        """testing if the Quartz instance returns a correct mass; this
        is inherited from the parent class 'Particle'
        """
        
        particle = base_classes.Quartz(x = 1, y = 1, diameter = 10)
        exp = base_classes.Quartz.density * (np.math.pi*10**2)/4
        self.assertAlmostEqual(particle.mass, exp)
    
    def test_moment_of_inertia(self):
        """testing if the Quartz instance returns a correct moment of
        inertia; this is inherited from the parent class 'Particle'
        """

        pass


class TestKaolinite(unittest.TestCase):
    """test cases for the Montmorillonite class from 'base_classes'
    module; it also includes tests for all the stuff inherited from
    parent classes 'Clay' and 'Particle'
    """

    def test_ascending_particle_number(self):
        """testing if the particle number thing works in this class too
        in the ascending manner; it should be correctly inherited from
        the parent class 'Particle'
        """
        
        particle1 = base_classes.Kaolinite(
            x = 0, y = 0, length = 5000, thickness = 2, inclination = np.math.pi/4,
            )
        particle2 = base_classes.Kaolinite(
            x = 10, y = 10, length = 5000, thickness = 2, inclination = np.math.pi/4,
            )
        self.assertEqual(particle1.num + 1, particle2.num)

    def test_descending_particle_number(self):
        """testing if the particle number thing works in this class too
        in the descending manner; it should be correctly inherited from
        the parent class 'Particle'
        """
        
        particle1 = base_classes.Kaolinite(
            x = 0, y = 0, length = 5000, thickness = 2, inclination = np.math.pi/4,
            )
        particle2 = base_classes.Kaolinite(
            x = 10, y = 10, length = 5000, thickness = 2, inclination = np.math.pi/4,
            )
        del particle2
        self.assertEqual(particle1.num + 1, base_classes.Kaolinite.last_num)
        particle3 = base_classes.Kaolinite(
            x = 10, y = 10, length = 5000, thickness = 2, inclination = np.math.pi/4,
            )
        self.assertEqual(particle1.num + 1, particle3.num)
    
    def test_hashable(self):
        """testing if the particle being hashable works here too; it is
        inherited from the parent class 'Particle'
        """

        particle = base_classes.Kaolinite(
            x = 0, y = 0, length = 5000, thickness = 2, inclination = np.math.pi/4,
            )
        s = {particle}
        self.assertTrue(s)

    def test_equality_condition(self):
        """testing if the equality condition works here to; it is
        inherited from the parent class 'Particle'
        """

        particle1 = base_classes.Kaolinite(
            x = 0, y = 0, length = 5000, thickness = 2, inclination = np.math.pi/4,
            )
        particle2 = base_classes.Kaolinite(
            x = 0, y = 0, length = 5000, thickness = 2, inclination = np.math.pi/4,
            )
        self.assertNotEqual(particle1, particle2)

    def test_box_num(self):
        """testing if the box_number method works here too; it is
        inherited from the parent class 'Particle'
        """

        particle = base_classes.Kaolinite(
            x = 6023, y = 5634, length = 5000, thickness = 2, inclination = np.math.pi/4,
            )
        bn = particle.box_num(nc = 100, box_length = 10, box_width = 10)
        self.assertEqual(bn, 56902)
        
    
    def test_thickness_validation(self):
        """testing if an invalid given thickness raises an error and a
        valid given thickness goes alright
        """

        lower = base_classes.Kaolinite.width_bounds[0]-0.5
        higher = base_classes.Kaolinite.width_bounds[1]+0.5
        self.assertRaises(
            RuntimeError,
            base_classes.Kaolinite,
            x = 6023, y = 5634, length = 5000, thickness = lower, inclination = np.math.pi/4
            )
        self.assertRaises(
            RuntimeError,
            base_classes.Kaolinite,
            x = 6023, y = 5634, length = 5000, thickness = higher, inclination = np.math.pi/4
            )

    def test_length_validation(self):
        """testing if an invalid given length raises an error and a
        valid given thickness goes alright
        """

        lower = base_classes.Kaolinite.length_bounds[0]-0.5
        higher = base_classes.Kaolinite.length_bounds[1]+0.5
        self.assertRaises(
            RuntimeError,
            base_classes.Kaolinite,
            x = 6023, y = 5634, length = lower, thickness = 2, inclination = np.math.pi/4
            )
        self.assertRaises(
            RuntimeError,
            base_classes.Kaolinite,
            x = 6023, y = 5634, length = higher, thickness = 2, inclination = np.math.pi/4
            )

    def test_standardizing_inclination(self):
        """testing if a non-standard given inclination becomes standard
        """

        particle = base_classes.Kaolinite(
            x = 501, y = 74, inclination = -3*np.math.pi/4, thickness = 1, length = 10000,
            )
        self.assertEqual(particle.inclination, np.math.pi/4)

    def test_attribute_assigning(self):
        """testing if all the attributes that a Montmorillonite instance
        should contain are present here; this also includes all the
        attributes and properties of the parent classes 'Particle' and
        'Clay'
        """

        particle = base_classes.Kaolinite(
            x = 501, y = 74, inclination = -3*np.math.pi/4, thickness = 2, length = 10000,
            )
        self.assertEqual(particle.x, 501)
        self.assertEqual(particle.y, 74)
        self.assertAlmostEqual(particle.inclination, np.math.pi/4)
        self.assertEqual(particle.thickness, 2)
        self.assertEqual(particle.length, 10000)
        self.assertFalse(particle.is_segment)
        self.assertTrue(particle.midline)
        self.assertTrue(particle.midpoint)
        self.assertTrue(particle.segments)


    def test_midpoint(self):
        """testing if the midpoint attribute of the Montmorillonite
        instance is created correctly
        """

        particle = base_classes.Kaolinite(
            x = 500, y = 70, inclination = -3*np.math.pi/4, thickness = 2, length = 10000,
            )
        self.assertEqual(particle.midpoint, shapes.Point(500, 70))

    def test_midline(self):
        """testing if the midline attribute of the Montmorillonite
        instance is created correctly
        """

        particle = base_classes.Kaolinite(
            x = 500, y = 70, inclination = -3*np.math.pi/4, thickness = 2, length = 10000,
            )
        end1 = shapes.Point(500 - 2500*np.sqrt(2), 70 - 2500*np.sqrt(2))
        end2 = shapes.Point(500 + 2500*np.sqrt(2), 70 + 2500*np.sqrt(2))
        exp = shapes.LineSegment(end1, end2)
        self.assertEqual(particle.midline, exp)
    
    def test_shape(self):
        """testing if the 'shape' attribute of the Montmorillonite
        instance is created correctly
        """

        particle = base_classes.Kaolinite(
            x = 100, y = 100, inclination = np.math.pi/2, thickness = 2, length = 10000,
            )
        v1 = shapes.Point(101, 5100)
        v2 = shapes.Point(99, 5100)
        v3 = shapes.Point(99, -4900)
        v4 = shapes.Point(101, -4900)
        exp = shapes.Rectangle(v1, v2, v3, v4)
        self.assertEqual(particle.shape, exp)

    def test_segmentalize(self):
        """testing if the 'segments' attribute of the Montmorillonite
        instance is created correctly using the 'segmentalize' method
        of the parent class 'Clay'; it should generate three segments
        which all have the same 'num' attribute and are all instances
        of 'Montmorillonite' class; also testing if the next created
        particle comes with a correct 'num' attribute regardless of its
        type
        """

        particle = base_classes.Kaolinite(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 1, length = 6000*np.sqrt(2),
            )
        self.assertEqual(len(particle.segments), 3)
        for seg in particle.segments:
            self.assertTrue(seg.is_segment)
        self.assertEqual(particle.segments[1].midpoint, shapes.Point(0, 0))
        self.assertAlmostEqual(particle.segments[0].length, 2000*np.sqrt(2))
        self.assertEqual(particle.segments[2].midline, shapes.LineSegment(
            shapes.Point(1000, 1000), shapes.Point(3000, 3000)))
    
    def test_move(self):
        """testing if the Montmorillonite instance moves correctly with
        the given derivatives; this is inherited from the parent class
        'Particle'
        """

        particle = base_classes.Kaolinite(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 2, length = 6000*np.sqrt(2),
            )
        particle.move(delta_x = 1000, delta_y = 1000, delta_theta = np.math.pi/4)
        self.assertEqual(particle.x, 1000)
        self.assertEqual(particle.y, 1000)
        self.assertEqual(particle.inclination, np.math.pi/2)
        self.assertEqual(particle.midpoint, shapes.Point(1000, 1000))
        self.assertEqual(particle.midline, shapes.LineSegment(
            shapes.Point(1000, 1000 + 3000*np.sqrt(2)), shapes.Point(1000, 1000 - 3000*np.sqrt(2))))
        v1 = shapes.Point(1001, 1000 + 3000*np.sqrt(2))
        v2 = shapes.Point(999, 1000 + 3000*np.sqrt(2))
        v3 = shapes.Point(999, 1000 - 3000*np.sqrt(2))
        v4 = shapes.Point(1001, 1000 - 3000*np.sqrt(2))
        self.assertEqual(particle.shape, shapes.Rectangle(v1, v2, v3, v4))

    def test_mass(self):
        """testing if the Montmorillonite instance returns a correct
        mass; this is inherited from the parent class 'Particle'
        """
        
        particle = base_classes.Kaolinite(
            x = 0, y = 0, inclination = np.math.pi/4, thickness = 2, length = 6000*np.sqrt(2),
            )
        exp = base_classes.Kaolinite.density * 2 * 6000*np.sqrt(2)
        self.assertAlmostEqual(particle.mass, exp)

    
    def test_moment_of_inertia(self):
        """testing if the Montmorillonite instance returns a correct
        moment of inertia; this is inherited from the parent class
        'Particle'
        """

        pass


class TestWall(unittest.TestCase):
    """test cases for Wall class from 'base_classes' module; some of
    the stuff that it inherits from its parent class 'Particle' will
    also be tested again in here to see if it inherits them correctly
    """

    def test_ascending_particle_number(self):
        """testing if the particle number thing works in this class too
        in the ascending manner; it should be correctly inherited from
        the parent class 'Particle'
        """
        
        pass

    def test_descending_particle_number(self):
        """testing if the particle number thing works in this class too
        in the descending manner; it should be correctly inherited from
        the parent class 'Particle'
        """
        
        pass
    
    def test_hashable(self):
        """testing if the particle being hashable works here too; it is
        inherited from the parent class 'Particle'
        """

        pass

    def test_equality_condition(self):
        """testing if the equality condition works here to; it is
        inherited from the parent class 'Particle'
        """

        pass
    
    def test_move(self):
        """testing if the Wall instance moves correctly with the given
        derivatives; this is inherited from the parent class 'Particle'
        """

        pass

    def test_mass(self):
        """testing if the Wall instance returns a correct mass; this is
        inherited from the parent class 'Particle'
        """
        
        pass
    
    def test_moment_of_inertia(self):
        """testing if the Wall instance returns a correct moment of
        inertia; this is inherited from the parent class 'Particle'
        """

        pass
    
    def test_length_validation(self):
        """testing if it raises an error with a non-positive given
        length 
        """

        pass

    def test_shape(self):
        """testing if the 'shape' attribute is assigned correctly
        """

        pass

    def test_attribute_assigning(self):
        """testing if all the attributes are assigned correctly; this
        includes those of the parent class 'Particle'
        """

        pass

    def test_frorm_ends(self):
        """testing the classmethod 'from_ends'
        """

        pass


if __name__ == '__main__':
    unittest.main()