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
        'size_upper_bound': 3000,
        'size_lower_bound': 1000,
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
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')
    
    def test_length(self):
        """testing the validation of length parameter
        """

        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 0,
            width = 35000,
            simulation_type = 'ds',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'ds',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'DS')

    def test_width(self):
        """testing the validation of width parameter
        """
        
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 0,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')

    def test_particle_type(self):
        """testing the validation of 'type' parameter in the particle
        info parameter
        """
        
        info = {k:v for k,v in self.kaolinite_clay1.items()}
        info['type'] = 'bent'
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [info],
            fluid_characteristics = None
            )
        info['type'] = 'quartz'
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')

    def test_particle_info_data_type(self):
        """testing the validation of the data type of the particle_info
        array
        """
        
        info = {k:v for k,v in self.kaolinite_clay1.items()}
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = info,
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [info],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')

    def test_particle_essential_attributes(self):
        """testing the validation of particle_info array due to the
        essential attrirbutes that need to present in each dictionary
        """
        
        info = {k:v for k,v in self.kaolinite_clay1.items()}
        info.pop('type')
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [info],
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')

    def test_particle_size_bounds(self):
        """testing the validation of particle size bounds
        """
        
        info = {k:v for k,v in self.kaolinite_clay1.items()}
        info['size_upper_bound'] = 36000
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [info],
            fluid_characteristics = None
            )
        container = base_classes.Container(
            length = 35000,
            width = 35000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.simulation_type, 'TT')


class TestSimleSetups(unittest.TestCase):
    """test cases for simple setups and attribute settings that take
    place at the beginning of the simulation
    """
    
    def test_number_of_groups(self):
        """testing the 'number_of_groups' attribute of the Container
        class
        """
        
        pass

    def test_box_width(self):
        """testing the 'box_width' attribute if the Container class;
        """
        
        pass

    def test_box_length(self):
        """testing the 'box_length' attribute of the Container class
        """
        
        pass
    
    def test_make_boxes(self):
        """testing the 'make_boxes' method of the container class
        """
        
        pass

    def test_nr(self):
        """testing the 'nr' attribute of the Container class
        """
        
        pass

    def test_nc(self):
        """testing the 'nc' attribute of the container class
        """
        
        pass
    
    def test_setup_walls(self):
        """testing the 'setup_walls' method of the Container class
        """
        
        pass
    
    
class TestContacts(unittest.TestCase):
    """test cases for the contact detection operations for different
    types of contacts and particles
    """
    
    pass


class TestParticleGeneration(unittest.TestCase):
    """test cases to see if the particle generation phase in the
    container takes place flawlessly
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


if __name__ == '__main__':
    unittest.main()