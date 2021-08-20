"""test cases for all the functionalities of the Container class in
base_classes module
"""


from generation import base_classes
import unittest
import numpy as np
from typing import Type, Union, Any
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations
import sys


class TestValidations(unittest.TestCase):
    """test cases for validations that need to take place while
    initializing the container
    """

    kaolinite_clay1 = {
        'type': 'kaolinite',
        'size_upper_bound': 1000,
        'size_lower_bound': 3000,
        'quantity': 1000
    }
    
    def test_simulation_type(self):
        """testing the validation of simulation type
        """
        
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 35000,
            simulation_type = 'tf',
            time_step = 1.8e-13,
            partice_info = self.kaolinite_clay1
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            partice_info = [self.kaolinite_clay1]
        )
        self.assertEqual(container.simulation_type, 'TT')
    
    def test_length(self):
        """testing the validation of length parameter
        """

        pass

    def test_width(self):
        """testing the validation of width parameter
        """
        
        pass

    def test_particle_type(self):
        """testing the validation of 'type' parameter in the particle
        info parameter
        """
        
        pass

    def test_particle_info_data_type(self):
        """testing the validation of the data type of the particle_info
        array
        """
        
        pass

    def test_particle_essential_attributes(self):
        """testing the validation of particle_info array due to the
        essential attrirbutes that need to present in each dictionary
        """
        
        pass

    def test_particle_size_bounds(self):
        """testing the validation of particle size bounds
        """
        
        pass


class TestSimleSetups(unittest.TestCase):
    """test cases for simple setups and attribute settings that take
    place at the beginning of the simulation
    """
    
    pass


class TestParticleGeneration(unittest.TestCase):
    """test cases to see if the particle generation phase in the
    container takes place flawlessly
    """
    
    pass


class TestContacts(unittest.TestCase):
    """test cases for the contact detection operations for different
    types of contacts and particles
    """
    
    pass


class TestForces(unittest.TestCase):
    """test cases for the stuff that are related to particle forces
    """
    
    pass


class TestUpdates(unittest.TestCase):
    """test cases to see if the container and particle's conditions are
    updated correctly after a relaxation phase
    """
    
    pass