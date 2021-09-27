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
# from display import illustraion


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


class TestSimpleSetups(unittest.TestCase):
    """test cases for simple setups and attribute settings that take
    place at the beginning of the simulation
    """
    
    kaolinite_clay1 = {
        'type': 'kaolinite',
        'size_upper_bound': 2000,
        'size_lower_bound': 1000,
        'quantity': 500
    }
    kaolinite_clay2 = {
        'type': 'kaolinite',
        'size_upper_bound': 3000,
        'size_lower_bound': 2000,
        'quantity': 500
    }
    quartz_sand1 = {
        'type': 'quartz',
        'size_upper_bound': 10000,
        'size_lower_bound': 8000,
        'quantity': 50
    }
    
    def test_number_of_groups(self):
        """testing the 'number_of_groups' attribute of the Container
        class
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay1, self.kaolinite_clay2, self.quartz_sand1],
            fluid_characteristics = None
        )
        self.assertEqual(container.number_of_groups, 3)

    def test_box_length_and_width1(self):
        """testing the 'box_length' and 'box_width' attribute of the
        Container class with one grop of particles given
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1],
            fluid_characteristics = None
        )
        self.assertEqual(container.box_length, [10000])
        self.assertEqual(container.box_width, [10000])
        
    def test_box_length_and_width2(self):
        """testing the 'box_length' and 'box_width' attribute of the
        Container class with one grop of particles given and the upper
        bound size for the given particle is a number that the container
        dimensions are not divisible by it
        """
        
        kaolinite = {k:v for k,v in self.kaolinite_clay2.items()}
        kaolinite['size_upper_bound'] = 2700
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [kaolinite],
            fluid_characteristics = None
        )
        self.assertEqual(len(container.box_length), 1)
        self.assertEqual(container.box_length, [3125])
        self.assertEqual(len(container.box_width), 1)
        self.assertEqual(container.box_width, [3125])
    
    def test_box_length_and_width3(self):
        """testing the 'box_length' and 'box_width' attribute of the
        Container class with one grop of particles given and the given
        length and width for the container not being proper numbers so
        the generated boxes become 
        """
        
        self.assertRaises(
            RuntimeError,
            base_classes.Container,
            length = 100001,
            width = 100001,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1],
            fluid_characteristics = None
            )
    
    def test_box_length_and_width4(self):
        """testing the 'box_length' and 'box_width' attribute of the
        Container class with two grop of particles given
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(len(container.box_length), 2)
        self.assertEqual(container.box_length, [10000, 2000])
        self.assertEqual(len(container.box_width), 2)
        self.assertEqual(container.box_width, [10000, 2000])
    
    def test_box_length_and_width5(self):
        """testing the 'box_length' and 'box_width' attribute of the
        Container class with three grop of particles given
        """
    
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1, self.kaolinite_clay2],
            fluid_characteristics = None
        )
        self.assertEqual(len(container.box_length), 3)
        self.assertEqual(container.box_length, [10000, 5000, 2500])
        self.assertEqual(len(container.box_width), 3)
        self.assertEqual(container.box_width, [10000, 5000, 2500])

    def test_nr_nc1(self):
        """testing the 'nr' and 'nc' attribute of the Container class
        for one group of particles given
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1],
            fluid_characteristics = None
        )
        self.assertEqual(container.number_of_rows, [10])
        self.assertEqual(container.number_of_columns, [10])
    
    def test_nr_nc2(self):
        """testing the 'nr' and 'nc' attribute of the Container class
        for two group of particles given
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.number_of_rows, [10, 50])
        self.assertEqual(container.number_of_columns, [10, 50])
    
    def test_nr_nc3(self):
        """testing the 'nr' and 'nc' attribute of the Container class
        for three group of particles given
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.kaolinite_clay2, self.quartz_sand1, self.kaolinite_clay1],
            fluid_characteristics = None
        )
        self.assertEqual(container.number_of_rows, [10, 20, 40])
        self.assertEqual(container.number_of_columns, [10, 20, 40])
    
    def test_setup_walls1(self):
        """testing the 'setup_walls' method of the Container class with
        the 'simulation_type' parameter being "tt"
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 100000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1],
            fluid_characteristics = None
        )
        wall1 = base_classes.Wall(
            x = 0, y = 50000, inclination = np.math.pi/2, is_fixed = True, length = 100000)
        wall2 = base_classes.Wall(
            x = 50000, y = 100000, inclination = 0, is_fixed = False, length = 100000)
        wall3 = base_classes.Wall(
            x = 100000, y = 50000, inclination = np.math.pi/2, is_fixed = True, length = 100000)
        wall4 = base_classes.Wall(
            x = 50000, y = 0, inclination = 0, is_fixed = True, length = 100000)
        exp = [wall1, wall2, wall3, wall4]
        res = container.walls
        self.assertEqual(set(res), set(exp))
    
    def test_setup_walls2(self):
        """testing the 'setup_walls' method of the Container class with
        the 'simulation_type' parameter being "tt" and the length and
        width of the cotainer being different from each other
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 80000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1],
            fluid_characteristics = None
        )
        wall1 = base_classes.Wall(
            x = 0, y = 40000, inclination = np.math.pi/2, is_fixed = True, length = 80000)
        wall2 = base_classes.Wall(
            x = 50000, y = 80000, inclination = 0, is_fixed = False, length = 100000)
        wall3 = base_classes.Wall(
            x = 100000, y = 40000, inclination = np.math.pi/2, is_fixed = True, length = 80000)
        wall4 = base_classes.Wall(
            x = 50000, y = 0, inclination = 0, is_fixed = True, length = 100000)
        walls = [wall1, wall2, wall3, wall4]
        self.assertEqual(set(container.walls), set(walls))
    
    def test_number_of_clay_groups(self):
        """testing the 'number_of_clay_groups' attribute of the
        Container class
        """
        
        container = base_classes.Container(
            length = 100000,
            width = 80000,
            simulation_type = 'tt',
            time_step = 1.8e-13,
            particles_info = [self.quartz_sand1, self.kaolinite_clay1, self.kaolinite_clay2],
            fluid_characteristics = None
        )
        self.assertEqual(container.number_of_clay_groups, 2)
        

class TestContacts(unittest.TestCase):
    """test cases for mechanical contact detection operations for
    different types of particles; contact lists for contacting
    particles with walls are also tested; stuff like tolerance and
    having multiple particle size hierarchies have been considered
    while writing these test cases; also test cases included for
    chemical contact detection since its process is similar to
    mechanical contacts
    """
    
    #particle info dictionaries used in test cases in this class
    kaolinite_clay1 = {
        'type': 'kaolinite',
        'size_upper_bound': 2000,
        'size_lower_bound': 1000,
        'quantity': 500
    }
    kaolinite_clay2 = {
        'type': 'kaolinite',
        'size_upper_bound': 3000,
        'size_lower_bound': 2000,
        'quantity': 500
    }
    quartz_sand1 = {
        'type': 'quartz',
        'size_upper_bound': 10000,
        'size_lower_bound': 8000,
        'quantity': 50
    }
    
    #quatrz particles to be appended to the container for test cases
    quartz1 = base_classes.Quartz(
        x = 10000, y = 10000, length = 8500, hierarchy = 0
    ) #touches 4 boxes, intersects with kaolinite2_6 and kaolinite1_5
    quartz2 = base_classes.Quartz(
        x = 50000, y = 10000, length = 9000, hierarchy = 0
    ) #touches 4 boxes, intersects with kaolinite2_5
    quartz3 = base_classes.Quartz(
        x = 30000, y = 25000, length = 9000, hierarchy = 0
    ) #touches 2 boxes, doesn't have any intersections
    quartz4 = base_classes.Quartz(
        x = 60000, y = 40000, length = 9000, hierarchy = 0
    ) #touches 4 boxes, doesn't have any intersections
    quartz5 = base_classes.Quartz(
        x = 30000, y = 50000, length = 8500, hierarchy = 0
    ) #touches 4 boxes, intersects with quartz15
    quartz6 = base_classes.Quartz(
        x = 82000, y = 1000, length = 8500, hierarchy = 0
    ) #intersects with the lower wall and touches two boxes
    quartz7 = base_classes.Quartz(
        x = 20000, y = 60000, length = 8500, hierarchy = 0
    ) #touches 4 boxes, intersects with quartz8 and quartz9
    quartz8 = base_classes.Quartz(
        x = 25000, y = 65000, length = 8500, hierarchy = 0
    ) #touches one box, intersects with quartz7
    quartz9 = base_classes.Quartz(
        x = 15000, y = 65000, length = 8500, hierarchy = 0
    ) #touches one box, intersects with quartz7
    quartz10 = base_classes.Quartz(
        x = 80000, y = 50000, length = 8500, hierarchy = 0
    ) #touches 4 boxes, wraps around quartz11
    quartz11 = base_classes.Quartz(
        x = 80000, y = 50000, length = 8100, hierarchy = 0
    ) #touches 4 boxes, located inside quartz10
    quartz12 = base_classes.Quartz(
        x = 75000, y = 30000, length = 8500, hierarchy = 0
    ) #touches two boxes, kaolinite2_2 is located completely inside this particle
    quartz13 = base_classes.Quartz(
        x = 55000, y = 55000, length = 8500, hierarchy = 0
    ) #touches only one box, intersects with kaolinite2_1
    quartz14 = base_classes.Quartz(
        x = 40000, y = 40000, length = 8500, hierarchy = 0
    ) #touches 4 boxes, kaolinite1_1 is located completely inside this particle
    quartz15 = base_classes.Quartz(
        x = 25000, y = 45000, length = 8500, hierarchy = 0
    ) #touches only one box, intersects with quartz5
    quartz16 = base_classes.Quartz(
        x = 0, y = 35000, length = 8500, hierarchy = 0
    ) #touches only one box, intersects with the left wall
    
    #first group of kaolinite particles to be appended to the container for test cases
    kaolinite1_1 = base_classes.Kaolinite(
        x = 38000, y = 38000, length = 1500, thickness = 2, inclination = np.math.pi/4, hierarchy = 2
    ) #located completely inside quartz14
    kaolinite1_2 = base_classes.Kaolinite(
        x = 45000, y = 45000, length = 1500, thickness = 2, inclination = np.math.pi/4, hierarchy = 2
    ) #intersects with kaolinite3
    kaolinite1_3 = base_classes.Kaolinite(
        x = 45000, y = 45000, length = 1500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 2
    ) #intersects with kaolinite2
    kaolinite1_4 = base_classes.Kaolinite(
        x = 21000, y = 0, length = 1500, thickness = 2, inclination = np.math.pi/4, hierarchy = 2
    ) #intersects with the lower wall
    kaolinite1_5 = base_classes.Kaolinite(
        x = 8000, y = 8000, length = 1500, thickness = 2, inclination = np.math.pi/4, hierarchy = 2
    ) #intersects with quartz1 and kaolinite2_7
    kaolinite1_6 = base_classes.Kaolinite(
        x = 25000, y = 15000, length = 1500, thickness = 2, inclination = np.math.pi/4, hierarchy = 2
    ) #intersects with kaolinite2_8
    kaolinite1_7 = base_classes.Kaolinite(
        x = 33000, y = 48000, length = 1500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 2
    ) #intersects with quartz5
    
    #second group of kaolinite particles to be appended to the container for test cases
    kaolinite2_1 = base_classes.Kaolinite(
        x = 53000, y = 53000, length = 2500, thickness = 2, inclination = np.math.pi/4, hierarchy = 1
    ) #intersects with quartz13
    kaolinite2_2 = base_classes.Kaolinite(
        x = 75000, y = 30000, length = 2500, thickness = 2, inclination = 0, hierarchy = 1
    ) #is located fully inside quartz12
    kaolinite2_3 = base_classes.Kaolinite(
        x = 35000, y = 15000, length = 2500, thickness = 2, inclination = np.math.pi/4, hierarchy = 1
    ) #intersects with kaolinite2_4
    kaolinite2_4 = base_classes.Kaolinite(
        x = 35000, y = 15000, length = 2500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
    ) #intersects with kaolinite2_3
    kaolinite2_5 = base_classes.Kaolinite(
        x = 47500, y = 7500, length = 2500, thickness = 2, inclination = np.math.pi/4, hierarchy = 1
    ) #intersects with quartz2
    kaolinite2_6 = base_classes.Kaolinite(
        x = 12000, y = 8000, length = 2500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
    ) #intersects with quartz1
    kaolinite2_7 = base_classes.Kaolinite(
        x = 7550, y = 7550, length = 2500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
    ) #intersects with kaolinite1_5
    kaolinite2_8 = base_classes.Kaolinite(
        x = 25050, y = 15050, length = 2500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
    ) #intersects with kaolinite1_6
    kaolinite2_9 = base_classes.Kaolinite(
        x = 99999, y = 15050, length = 2500, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
    ) #intersects with the right wall
    
    #container instance to run the tests on
    container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [kaolinite_clay1, kaolinite_clay2, quartz_sand1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
    )
    container.particles.extend([
        quartz1, quartz2, quartz3, quartz4, quartz5,
        quartz6, quartz7, quartz8, quartz8, quartz9,
        quartz10, quartz11, quartz12, quartz13, quartz14,
        quartz15, kaolinite1_1, kaolinite1_2, kaolinite1_3,
        kaolinite1_4, kaolinite1_5, kaolinite1_6, kaolinite1_7,
        kaolinite2_1, kaolinite2_2, kaolinite2_3, kaolinite2_4,
        kaolinite2_5, kaolinite2_6, kaolinite2_7, kaolinite2_8
    ])
    
    
    def test_touching_boxes1(self):
        """testing the "touching_boxes" method of the Container class
        given an instance of the Line class as its 'particle_shape'
        parameter
        """
        
        end1 = shapes.Point(17000, 27000)
        end2 = shapes.Point(14500, 21000)
        line = shapes.LineSegment(end1, end2)
        exp = [103, 82, 83]
        res = self.container.touching_boxes(particle_shape = line, index = 1, nb = 83)
        self.assertEqual(set(res), set(exp))
    
    def test_touching_boxes2(self):
        """testing the "touching_boxes" method of the Container class
        given an instance of the Circle class as its 'particle_shape'
        parameter
        """
        
        circle = shapes.Circle(shapes.Point(80000, 51000), 8000)
        exp = [47, 48, 57, 58]
        res = self.container.touching_boxes(circle, 0, 57)
        self.assertEqual(set(res), set(exp))
    
    def test_touching_boxes3(self):
        """testing the "touching_boxes" method of the Container class
        given an instance of the Rectangle class as its 'particle_shape'
        parameter
        """
        
        v1 = shapes.Point(99500, 2499)
        v2 = shapes.Point(99500, 2501)
        v3 = shapes.Point(100500, 2501)
        v4 = shapes.Point(100500, 2499)
        rec = shapes.Rectangle(v1, v2, v3, v4)
        exp = [39, 79]
        res = self.container.touching_boxes(rec, 2, 39)
        self.assertEqual(set(res), set(exp))
    
    def test_update_mechanical_boxes1(self):
        """testing the "update_mechanical_boxes" method of the Container
        class appending some particles to the "particles" attribute of
        the container instance, while instantiated given only one
        particle group
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend([
            self.quartz7, self.quartz8, self.quartz9
        ])
        container.update_mechanical_boxes()
        self.assertEqual(len(container.mechanical_boxes), 1)
        self.assertEqual(container.mechanical_boxes[0][51], [self.quartz7])
        self.assertEqual(container.mechanical_boxes[0][61], [self.quartz7, self.quartz9])
        self.assertEqual(container.mechanical_boxes[0][62], [self.quartz7, self.quartz8])
    
    def test_update_mechanical_boxes2(self):
        """testing the "update_mechanical_boxes" method of the Container
        class appending some particles to the "particles" attribute of
        the container instance, while instantiated given two particle
        groups
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend([
            self.quartz1, self.kaolinite2_6
        ])
        container.update_mechanical_boxes()
        self.assertEqual(len(container.mechanical_boxes), 2)
        self.assertEqual(container.mechanical_boxes[0][0], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[0][11], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[1][204], [])
        self.assertEqual(container.mechanical_boxes[1][155], [self.kaolinite2_6])
    
    def test_update_mechanical_boxes3(self):
        """testing the "update_mechanical_boxes" method of the Container
        class appending some particles to the "particles" attribute of
        the container instance, while instantiated given two particle
        groups but with different sizes than the previous test
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend([
            self.quartz1, self.kaolinite2_6
        ])
        container.update_mechanical_boxes()
        self.assertEqual(len(container.mechanical_boxes), 2)
        self.assertEqual(container.mechanical_boxes[0][0], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[0][10], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[1][42], [])
        self.assertEqual(container.mechanical_boxes[1][22], [self.kaolinite2_6])
    
    def test_update_mechanical_boxes4(self):
        """testing the "update_mechanical_boxes" method of the Container
        class appending some particles to the "particles" attribute of
        the container instance, while instantiated given three particle
        groups
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay1, self.kaolinite_clay2],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend([
            self.quartz1, self.kaolinite2_7, self.kaolinite1_5
        ])
        container.update_mechanical_boxes()
        self.assertEqual(len(container.mechanical_boxes), 3)
        self.assertEqual(container.mechanical_boxes[0][11], [self.quartz1])
        self.assertEqual(container.mechanical_boxes[1][41], [])
        self.assertEqual(container.mechanical_boxes[1][21], [self.kaolinite2_7])
        self.assertEqual(
            container.mechanical_boxes[2][123], [self.kaolinite1_5]
            )
        
    
    def test_single_particle_mechanical_contact_check1(self):
        """testing the "single_particle_mechanical_contact_check"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given only one particle group
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.quartz7,
                self.quartz8,
                self.quartz12,
                self.quartz10,
                self.quartz11,
            ]
        )
        container.update_mechanical_boxes()
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.quartz7))
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.quartz8))
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.quartz10))
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.quartz11))
        self.assertFalse(
            container.single_particle_mechanical_contact_check(self.quartz12))
    
    def test_single_particle_mechanical_contact_check2(self):
        """testing the "single_particle_mechanical_contact_check"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given two particle groups
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.quartz2,
                self.kaolinite2_5,
                self.quartz13,
                self.quartz12,
                self.kaolinite2_2,
                self.quartz7,
                self.quartz8,
                self.kaolinite2_8
            ]
        )
        container.update_mechanical_boxes()
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.kaolinite2_5)
        )
        self.assertFalse(
            container.single_particle_mechanical_contact_check(self.quartz13)
        )
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.kaolinite2_2)
        )
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.quartz7)
        )
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.quartz8)
        )
        self.assertFalse(
            container.single_particle_mechanical_contact_check(self.kaolinite2_8)
        )
    
    def test_single_particle_mechanical_contact_check3(self):
        """testing the "single_particle_mechanical_contact_check"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given three particle groups
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2, self.kaolinite_clay1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.kaolinite2_8,
                self.kaolinite1_6,
                self.kaolinite2_4,
                self.kaolinite2_3,
                self.quartz1,
                self.kaolinite2_7,
                self.kaolinite1_5,
                self.quartz10,
                self.quartz11,
                self.quartz3,
                self.kaolinite1_3,
                self.quartz14,
                self.kaolinite1_1
            ]
        )
        container.update_mechanical_boxes()
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.kaolinite1_6)
        )
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.kaolinite2_4)
        )
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.kaolinite2_3)
        )
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.kaolinite2_7)
        )
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.kaolinite1_5)
        )
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.quartz10)
        )
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.quartz11)
        )
        self.assertFalse(
            container.single_particle_mechanical_contact_check(self.quartz3)
        )
        self.assertFalse(
            container.single_particle_mechanical_contact_check(self.kaolinite1_3)
        )
        self.assertTrue(
            container.single_particle_mechanical_contact_check(self.kaolinite1_1)
        )
    
    def test_update_mechanical_contacts_dictionary1(self):
        """testing the "update_mechanical_contacts_dictionary"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given only one particle group
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.quartz7,
                self.quartz8,
                self.quartz9,
                self.quartz12,
            ]
        )
        container.update_mechanical_boxes()
        container.update_mechanical_contacts_dictionary()
        self.assertEqual(container.mechanical_contacts[self.quartz7], [self.quartz9, self.quartz8])
        self.assertEqual(container.mechanical_contacts[self.quartz8], [self.quartz7])
        self.assertEqual(container.mechanical_contacts[self.quartz9], [self.quartz7])
        self.assertEqual(container.mechanical_contacts[self.quartz12], [])
    
    def test_update_mechanical_contacts_dictionary2(self):
        """testing the "update_mechanical_contacts_dictionary"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given two particle groups
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.quartz2,
                self.kaolinite2_5,
                self.quartz12,
                self.kaolinite2_2,
                self.quartz7,
                self.kaolinite2_8
            ]
        )
        container.update_mechanical_boxes()
        container.update_mechanical_contacts_dictionary()
        self.assertEqual(container.mechanical_contacts[self.quartz2], [self.kaolinite2_5])
        self.assertEqual(container.mechanical_contacts[self.kaolinite2_5], [self.quartz2])
        self.assertEqual(container.mechanical_contacts[self.quartz12], [self.kaolinite2_2])
        self.assertEqual(container.mechanical_contacts[self.kaolinite2_2], [self.quartz12])
        self.assertEqual(container.mechanical_contacts[self.quartz7], [])
        self.assertEqual(container.mechanical_contacts[self.kaolinite2_8], [])
    
    def test_update_mechanical_contacts_dictionary3(self):
        """testing the "update_mechanical_contacts_dictionary"
        method of the Container class appending some particles to the
        "particles" attribute of the container instance, while
        instantiated given three particle groups
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2, self.kaolinite_clay1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.kaolinite2_8,
                self.kaolinite1_6,
                self.kaolinite2_4,
                self.kaolinite2_3,
                self.quartz1,
                self.kaolinite2_7,
                self.kaolinite1_5,
                self.quartz10,
                self.quartz11,
                self.quartz3,
                self.quartz5,
                self.quartz15,
                self.kaolinite1_7
            ]
        )
        container.update_mechanical_boxes()
        container.update_mechanical_contacts_dictionary()
        self.assertEqual(container.mechanical_contacts[self.kaolinite2_8], [self.kaolinite1_6])
        self.assertEqual(container.mechanical_contacts[self.kaolinite1_6], [self.kaolinite2_8])
        self.assertEqual(container.mechanical_contacts[self.kaolinite2_4], [self.kaolinite2_3])
        self.assertEqual(container.mechanical_contacts[self.kaolinite1_5], [self.quartz1, self.kaolinite2_7])
        self.assertEqual(container.mechanical_contacts[self.quartz10], [self.quartz11])
        self.assertEqual(container.mechanical_contacts[self.quartz11], [self.quartz10])
        self.assertEqual(container.mechanical_contacts[self.quartz5], [self.quartz15, self.kaolinite1_7])
    
    def test_particle_wall_contact_check(self):
        """testing the "particle_wall_contact_check" method of the
        Container class
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2, self.kaolinite_clay1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        line = shapes.LineSegment(shapes.Point(0, 0), shapes.Point(0, 100000))
        self.assertTrue(container.particle_wall_contact_check(self.quartz6.shape))
        self.assertTrue(container.particle_wall_contact_check(self.quartz16.shape))
        self.assertFalse(container.particle_wall_contact_check(self.quartz1.shape))
        self.assertTrue(container.particle_wall_contact_check(self.kaolinite1_4.shape))
        self.assertFalse(container.particle_wall_contact_check(self.kaolinite1_2.shape))
    
    def test_update_wall_contacts_list1(self):
        """testing the "update_wall_contacts_list" method of the
        Container class appending some particles to the "particles"
        attribute of the container instance, while instantiated given
        only one particle group
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.quartz6,
                self.quartz16,
                self.quartz1,
                self.quartz2,
            ]
        )
        container.update_mechanical_boxes()
        container.update_wall_contacts_list()
        self.assertEqual(container.wall_contacts, [self.quartz6, self.quartz16])
    
    def test_update_wall_contacts_list2(self):
        """testing the "update_wall_contacts_list" method of the
        Container class appending some particles to the "particles"
        attribute of the container instance, while instantiated given
        two particle groups
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.quartz6,
                self.quartz16,
                self.quartz1,
                self.quartz2,
                self.kaolinite2_9,
                self.kaolinite2_1,
            ]
        )
        container.update_mechanical_boxes()
        container.update_wall_contacts_list()
        self.assertEqual(container.wall_contacts, [self.quartz6, self.quartz16, self.kaolinite2_9])
    
    def test_update_wall_contacts_list3(self):
        """testing the "update_wall_contacts_list" method of the
        Container class appending some particles to the "particles"
        attribute of the container instance, while instantiated given
        three particle groups
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2, self.kaolinite_clay1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.quartz6,
                self.quartz16,
                self.quartz1,
                self.quartz2,
                self.kaolinite2_9,
                self.kaolinite2_1,
                self.kaolinite1_4,
                self.kaolinite1_1
            ]
        )
        container.update_mechanical_boxes()
        container.update_wall_contacts_list()
        self.assertEqual(
            container.wall_contacts, [self.quartz6, self.quartz16, self.kaolinite2_9, self.kaolinite1_4]
            )

    def test_update_chemical_boxes(self):
        """testing the 'update_chemical_boxes' method of the Container
        class
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2, self.kaolinite_clay1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.quartz6,
                self.quartz16,
                self.kaolinite2_8,
                self.kaolinite1_6,
                self.kaolinite1_4,
                self.kaolinite1_1
            ]
        )
        container.update_chemical_boxes()
    
    def test_update_chemical_contacts_dictionary(self):
        """testing the  'update_chemical_contacts_dictionary' method of
        the Container class
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2, self.kaolinite_clay1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.particles.extend(
            [
                self.quartz6,
                self.quartz16,
                self.kaolinite2_8,
                self.kaolinite1_6,
                self.kaolinite1_4,
                self.kaolinite1_1
            ]
        )
        container.update_chemical_boxes()
        container.update_chemical_contacts_dictionary()
        self.assertEqual(container.chemical_contacts[self.kaolinite2_8], [self.kaolinite1_6])
        

class TestParticleGeneration(unittest.TestCase):
    """test cases to see if the particle generation phase in the
    container takes place flawlessly
    """
    
    #particle info dictionaries used in test cases in this class
    kaolinite_clay1 = {
        'type': 'kaolinite',
        'size_upper_bound': 2000,
        'size_lower_bound': 1000,
        'quantity': 500
    }
    kaolinite_clay2 = {
        'type': 'kaolinite',
        'size_upper_bound': 3000,
        'size_lower_bound': 2000,
        'quantity': 500
    }
    quartz_sand1 = {
        'type': 'quartz',
        'size_upper_bound': 10000,
        'size_lower_bound': 8000,
        'quantity': 35
    }
    
    def test_reduce_generation_chance(self):
        """testing the 'reduce_generation_chance' method of the
        Container class
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1, self.kaolinite_clay2, self.kaolinite_clay1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        particle1 = base_classes.Quartz(
            x = 5000, y = 5000, length = 10000, hierarchy = 0
        )
        particle2 = base_classes.Quartz(
            x = 20000, y = 30000, length = 10000, hierarchy = 0
        )
        particle3 = base_classes.Kaolinite(
            x = 10000, y = 20000, length = 2000*np.sqrt(2), thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
        )
        container.reduce_generation_chance(particle1)
        container.reduce_generation_chance(particle2)
        container.reduce_generation_chance(particle3)
        self.assertEqual(container.generation_boxes[0], 1)
        self.assertEqual(container.generation_boxes[10], 0.01)
        self.assertEqual(container.generation_boxes[21], 0.26)
        self.assertEqual(container.generation_boxes[31], 0.25)
        self.assertEqual(container.generation_boxes[32], 0.25)
        self.assertEqual(list(container.generation_boxes.keys())[-1], 0)
        self.assertEqual(list(container.generation_boxes.keys())[-2], 21)
    
    def test_no_contacts1(self):
        """testing particle generation given one group of particles
        making sure that no particle is in contact with any other
        particle or the wall
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.generate_particles()
        container.update_mechanical_boxes()
        container.update_wall_contacts_list()
        container.update_mechanical_contacts_dictionary()
        self.assertEqual(len(container.mechanical_contacts.keys()), 0)

    def test_no_contacts2(self):
        """testing particle generation given two groups of particles
        making sure that no particle is in contact with any other
        particle or the wall
        """
        
        qs = {k:v for k,v in self.quartz_sand1.items()}
        kc = {k:v for k,v in self.kaolinite_clay1.items()}
        qs['quantity'] = 30
        kc['quantity'] = 100
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [qs, kc],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.generate_particles()
        container.update_mechanical_boxes()
        container.update_wall_contacts_list()
        container.update_mechanical_contacts_dictionary()
        self.assertEqual(len(container.mechanical_contacts.keys()), 0)
    
    def test_no_contacts3(self):
        """testing particle generation given three groups of particles
        making sure that no particle is in contact with any other
        particle or the wall
        """
        
        qs = {k:v for k,v in self.quartz_sand1.items()}
        kc1 = {k:v for k,v in self.kaolinite_clay1.items()}
        kc2 = {k:v for k,v in self.kaolinite_clay2.items()}
        qs['quantity'] = 30
        kc1['quantity'] = 80
        kc2['quantity'] = 80
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [qs, kc1, kc2],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.generate_particles()
        container.update_mechanical_boxes()
        container.update_wall_contacts_list()
        container.update_mechanical_contacts_dictionary()
        self.assertEqual(len(container.mechanical_contacts.keys()), 0)
    
    def test_homogenity1(self):
        """testing particle generation making sure that the generated
        particles are distributed in the container homogenously given
        one group of particles
        """

        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.generate_particles()
        container.update_mechanical_boxes()
        container.update_wall_contacts_list()
        container.update_mechanical_contacts_dictionary()
        pass
    
    def test_homogenity2(self):
        """testing particle generation making sure that the generated
        particles are distributed in the container homogenously given
        two groups of particles
        """

        qs = {k:v for k,v in self.quartz_sand1.items()}
        kc = {k:v for k,v in self.kaolinite_clay1.items()}
        qs['quantity'] = 30
        kc['quantity'] = 100
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [qs, kc],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.generate_particles()
        container.update_mechanical_boxes()
        container.update_wall_contacts_list()
        container.update_mechanical_contacts_dictionary()
        pass
    
    def test_homogenity3(self):
        """testing particle generation making sure that the generated
        particles are distributed in the container homogenously given
        three groups of particles
        """

        qs = {k:v for k,v in self.quartz_sand1.items()}
        kc1 = {k:v for k,v in self.kaolinite_clay1.items()}
        kc2 = {k:v for k,v in self.kaolinite_clay2.items()}
        qs['quantity'] = 30
        kc1['quantity'] = 80
        kc2['quantity'] = 80
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [qs, kc1, kc2],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.generate_particles()
        container.update_mechanical_boxes()
        container.update_wall_contacts_list()
        container.update_mechanical_contacts_dictionary()
        pass
    
    def test_quantity1(self):
        """testing if the 'generate_particles' method of the container
        class generates the right number of particles given one group
        of particles
        """
        
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [self.quartz_sand1],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.generate_particles()
        self.assertEqual(len(container.particles), 35)
    
    def test_quantity2(self):
        """testing if the 'generate_particles' method of the container
        class generates the right amount of particles overal and also
        regarding each particle type given two particle groups
        """
        
        qs = {k:v for k,v in self.quartz_sand1.items()}
        kc = {k:v for k,v in self.kaolinite_clay1.items()}
        qs['quantity'] = 30
        kc['quantity'] = 100
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [qs, kc],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.generate_particles()
        self.assertEqual(len(container.particles), 130)
        c = sum(isinstance(particle, base_classes.Clay) for particle in container.particles)
        s = sum(isinstance(particle, base_classes.Sand) for particle in container.particles)
        self.assertEqual(c, 100)
        self.assertEqual(s, 30)
    
    def test_dummy(self):
        qs = {k:v for k,v in self.quartz_sand1.items()}
        kc = {k:v for k,v in self.kaolinite_clay1.items()}
        qs['quantity'] = 30
        kc['quantity'] = 20
        container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [kc],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
        )
        container.generate_particles()
        for particle in container.particles:
            sys.stdout.write(str(particle.midpoint) + '\n')

    def test_void_ratio1(self):
        """testing particle generation making sure that a certain void
        ratio is achieved in the container given one group of particels
        """

        pass
    
    def test_void_ratio2(self):
        """testing particle generation making sure that a certain void
        ratio is achieved in the container given two groups of
        particels
        """

        pass
    
    def test_void_ratio3(self):
        """testing particle generation making sure that a certain void
        ratio is achieved in the container given three groups of
        particels
        """

        pass    


class TestForces(unittest.TestCase):
    """test cases for calculation of all sorts of forces acting on an
    arbitrary particle
    """
    
    #define some particles here
    
    def test_mechanical_contact_forces1(self):
        """testing the calculation of mechanical forces acting on the
        given particle where there are two clay particles overlapping
        each other
        """
        
        pass

    def test_mechanical_contact_forces2(self):
        """testing the calculation of mechanical forces acting on the
        given particle where there are two sand particles in contact
        with each other
        """
        
        pass

    def test_mechanical_contact_forces3(self):
        """testing the calculation of mechanical forces acting on the
        given clay particle contacting with a sand particle
        """
        
        pass
    
    def test_mechanical_contact_forces4(self):
        """testing the calculation of mechanical forces acting on the
        given sand particle contacting with a clay particle
        """
        
        pass
    
    def test_mechanical_contact_forces5(self):
        """testing the calculation of mechanical forces acting on the
        given clay particle in contact with two other clay particles
        """
        
        pass
    
    def test_mechanical_contact_forces6(self):
        """testing the calculation of mechanical forces acting on the
        given clay particle in contact with one clay and one sand
        particle
        """
        
        pass
    
    def test_wall_contact_forces1(self):
        """testing the calculation of wall contact forces acting on a
        clay particle
        """
        
        pass
    
    def test_wall_contact_forces2(self):
        """testing the calculation of wall contact forces acting on a
        sand particle
        """
        
        pass
    
    def test_wall_contact_forces3(self):
        """testing the calculation of wall contact forces acting on a
        sand particle in contact with two walls in the corner
        """
        
        pass
    
    def test_vdw_forces(self):
        """testing the calculation of van der waals forces acting on a
        given clay particle; since the geometrical conditions don't
        really matter in this case this one test seems to be enough
        """
        
        pass
    
    def test_ddl_repulsion_forces1(self):
        """testing the calculation of ddl repultion forces acting on
        a given clay particle where the second particle is not located
        in front of the first one but it's pretty close
        """
        
        pass
    
    def test_ddl_repulsion_forces2(self):
        """testing the calculation of ddl repultion forces acting on
        a given clay particle where the second particle's alignment is
        in a way that its extension is orthogonal to the first particle
        """
        
        pass
    
    def test_ddl_repulsion_forces3(self):
        """testing the calculation of ddl repultion forces acting on
        a given clay particle where there are two other particles in
        chemical contact with the first one but with non-intersecting
        areas of repulsion
        """
        
        pass
    
    def test_ddl_repulsion_forces4(self):
        """testing the calculation of ddl repultion forces acting on
        a given clay particle where the other particle is intersecting
        the first one
        """
        
        pass
    
    def test_ddl_repulsion_forces5(self):
        """testing the calculation of ddl repultion forces acting on
        a given clay particle where there is a mediary particle in a
        way that it only intersects the perimeter of the repulsion area
        from the outside
        """
        
        pass
    
    def test_ddl_repulsion_forces6(self):
        """testing the calculation of ddl repultion forces acting on
        a given clay particle where there is a mediary particle that
        fully intersects with the area of repulsion of the other pair
        """
        
        pass
    
    def test_ddl_repulsion_forces7(self):
        """testing the calculation of ddl repultion forces acting on
        a given clay particle where there is a mediary particle that 
        intersects with both the area of repulsion and one of the
        particles
        """
        
        pass
    
    def test_ddl_repulsion_forces8(self):
        """testing the calculation of ddl repultion forces acting on
        a given clay particle where there is a mediary particle that
        intersects with one of the other particles and one of the
        edges of the repulsion area at the same time
        """
        
        pass
    
    def test_ddl_repulsion_forces9(self):
        """testing the calculation of ddl repultion forces acting on
        a given clay particle where there is a mediary particle located
        fully inside the area of repulsion
        """
        
        pass
    
    def test_ddl_repulsion_forces10(self):
        """testing the calculation of ddl repultion forces acting on
        a given clay particle where there is a mediary particle that
        passes through the area of repulsion in a way that the other
        two particles are no longer facing each other
        """
        
        pass


class TestUpdateLocations(unittest.TestCase):
    """test cases to see if the container and particle's conditions are
    updated correctly after a relaxation phase
    """
    
    pass


if __name__ == '__main__':
    unittest.main()