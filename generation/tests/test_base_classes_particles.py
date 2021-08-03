"""test cases for all the base classes for particles
"""

from generation import base_classes
import unittest
import numpy as np
from typing import Type, Union, Any
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations


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

        pass

    def test_descending_particle_number(self):
        """testing if the 'last_num' class attribute decreases by
        deleting a particle and a new instance gets its number
        correctly
        """

        pass

    def test_hashable(self):
        """testing if a generated particle is hashable or not
        """

        pass

    def test_equality_condition(self):
        """testing the equality condition of a particle instance; a
        particle should only be equal to itself
        """

        pass

    def test_box_num(self):
        """testing if a the 'box_num' method of a Particle instance
        generates the correct box number given its required arguments
        """

        pass


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

    def test_box_num(self):
        """testing if the box_number method works here too; it is
        inherited from the parent class 'Particle'
        """

        pass

    def test_standardizing_inclination(self):
        """testing if a non-standard given inclination becomes standard
        """

        pass

    def test_attribute_assigning(self):
        """testing if all the attributes that a Clay instance should
        contain are present here; this also includes all the attributes
        and properties of the parent class 'Particle'
        """

        pass

    def test_midpoint(self):
        """testing if the midpoint attribute of the Clay instance is
        created correctly
        """

        pass

    def test_midline(self):
        """testing if the midline attribute of the Clay instance is
        created correctly
        """

        pass
    
    def test_shape(self):
        """testing if the 'shape' attribute of the Clay instance is
        created correctly
        """

        pass

    def test_segmentalize(self):
        """testing if the 'segments' attribute of the Clay instance is
        created correctly using the 'segmentalize' method of the class;
        it should generate three segments which all have the same 'num'
        attribute; also testing if the next created particle comes with
        a correct 'num' attribute
        """

        pass


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

    def test_box_num(self):
        """testing if the box_number method works here too; it is
        inherited from the parent class 'Particle'
        """

        pass
    
    def test_shape(self):
        """testing if the 'shape' attribute of the Sand instance is
        assigned correctly
        """

        pass
    
    def test_attribute_assigning(self):
        """testing if all the attributes that a Sand instance should
        contain are present here; this also includes all the attributes
        and properties of the parent class 'Particle'
        """

        pass

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

    def test_box_num(self):
        """testing if the box_number method works here too; it is
        inherited from the parent class 'Particle'
        """

        pass
    
    def test_diameter_validation(self):
        """testing if the invalid input for 'diameter' argument raises
        an error and valid ones goes alright; this behavior is
        inherited from the parent class 'Sand'
        """
        
        pass
    
    def test_shape(self):
        """testing if the 'shape' attribute of the Sand instance is
        assigned correctly; this behavior is inherited from the parent
        class 'Sand'
        """

        pass
    
    def test_attribute_assigning(self):
        """testing if all the attributes that a Sand instance should
        contain are present here; this also includes all the attributes
        and properties of the parent classes 'Particle' and 'Sand'
        """

        pass
    
    def test_move(self):
        """testing if the Quartz instance moves correctly with the 
        given derivatives; this is inherited from the parent class
        'Particle'
        """

        pass

    def test_mass(self):
        """testing if the Quartz instance returns a correct mass; this
        is inherited from the parent class 'Particle'
        """
        
        pass
    
    def test_moment_of_inertia(self):
        """testing if the Quartz instance returns a correct moment of
        inertia; this is inherited from the parent class 'Particle'
        """

        pass


class TestMontmorillonite(unittest.TestCase):
    """test cases for the Montmorillonite class from 'base_classes'
    module; it also includes tests for all the stuff inherited from
    parent classes 'Clay' and 'Particle'
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

    def test_box_num(self):
        """testing if the box_number method works here too; it is
        inherited from the parent class 'Particle'
        """

        pass
    
    def test_thickness_validation(self):
        """testing if an invalid given thickness raises an error and a
        valid given thickness goes alright
        """

        pass

    def test_length_validation(self):
        """testing if an invalid given length raises an error and a
        valid given thickness goes alright
        """

        pass

    def test_standardizing_inclination(self):
        """testing if a non-standard given inclination becomes standard
        """

        pass

    def test_attribute_assigning(self):
        """testing if all the attributes that a Montmorillonite instance
        should contain are present here; this also includes all the
        attributes and properties of the parent classes 'Particle' and
        'Clay'
        """

        pass

    def test_midpoint(self):
        """testing if the midpoint attribute of the Montmorillonite
        instance is created correctly
        """

        pass

    def test_midline(self):
        """testing if the midline attribute of the Montmorillonite
        instance is created correctly
        """

        pass
    
    def test_shape(self):
        """testing if the 'shape' attribute of the Montmorillonite
        instance is created correctly
        """

        pass

    def test_segmentalize(self):
        """testing if the 'segments' attribute of the Montmorillonite
        instance is created correctly using the 'segmentalize' method
        of the parent class 'Clay'; it should generate three segments
        which all have the same 'num' attribute and are all instances
        of 'Montmorillonite' class; also testing if the next created
        particle comes with a correct 'num' attribute regardless of its
        type
        """

        pass
    
    def test_move(self):
        """testing if the Montmorillonite instance moves correctly with
        the given derivatives; this is inherited from the parent class
        'Particle'
        """

        pass

    def test_mass(self):
        """testing if the Montmorillonite instance returns a correct
        mass; this is inherited from the parent class 'Particle'
        """
        
        pass
    
    def test_moment_of_inertia(self):
        """testing if the Montmorillonite instance returns a correct
        moment of inertia; this is inherited from the parent class
        'Particle'
        """

        pass