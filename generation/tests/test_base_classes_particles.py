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
    is their parent class
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
    """test cases for the Clay class from the base_classes module
    """

    pass