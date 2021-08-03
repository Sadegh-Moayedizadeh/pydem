"""test cases for all the base classes for particles
"""

from generation import base_classes
import unittest
import numpy as np
from typing import Type, Union, Any
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations


class TestParticle(unittest.TestCase):
    """test cases for the Particle class in base_classes module
    """

    def test_particle_number(self):
        pass