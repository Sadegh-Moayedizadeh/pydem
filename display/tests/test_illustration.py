"""module containing test cases for the illustration module
"""


from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations
from generation import base_classes
from display import illustration
import os
import sys
import unittest
import numpy as np

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
    'quantity': 100
}
quartz_sand1 = {
    'type': 'quartz',
    'size_upper_bound': 10000,
    'size_lower_bound': 8000,
    'quantity': 25
}
container = base_classes.Container(
    length = 100000,
    width = 100000,
    particles_info = [quartz_sand1, kaolinite_clay2],
    time_step = 0.01,
    simulation_type = 'tt',
    fluid_characteristics = None
    )
particle1 = base_classes.Quartz(
    x = 5000, y = 5000, length = 10000, hierarchy = 0
)
particle2 = base_classes.Kaolinite(
    x = 53000, y = 53000, length = 5000, thickness = 2, inclination = -1*np.math.pi/4, hierarchy = 1
)
particle3 = base_classes.Kaolinite(
    x = 50000, y = 50000, length = 5000, thickness = 2, inclination = np.math.pi/4, hierarchy = 1
)
particle4 = base_classes.Kaolinite(
    x = 5000, y = 5000, length = 5000, thickness = 2, inclination = -1*np.math.pi/2, hierarchy = 1
)
container.particles.extend([particle2, particle3, particle4])
# container.generate_particles()
ill = illustration.IllustrationMPL(container)
ill.display()