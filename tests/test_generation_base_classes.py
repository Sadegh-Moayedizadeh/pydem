import unittest
from generation.base_classes import Container, Kaolinite, Quartz
from display.illustration import IllustrationMPL
import logging

logging.getLogger().setLevel(logging.INFO)

class TestParticleGeneration(unittest.TestCase):
    
    def setUp(self):
        self.kaolinite_clay = {
        'type': 'kaolinite',
        'size_upper_bound': 3000,
        'size_lower_bound': 1000,
        'quantity': 20,
        }
        self.quartz_sand = {
            'type': 'quartz',
            'size_upper_bound': 10000,
            'size_lower_bound': 8000,
            'quantity': 2,
        }
        
    
    def test_sand_generation(self):
        container = Container(
            100000, 100000, [self.quartz_sand], 'tt', 0.01, {}
        )
        container.generate_particles()
        ill = IllustrationMPL(container, title='only sand')
        ill.display()

    def test_clay_generation(self):
        container = Container(
            100000, 100000, [self.kaolinite_clay], 'tt', 0.01, {}
        )
        container.generate_particles()
        ill = IllustrationMPL(container, title='only clay')
        ill.display()

    def test_sand_clay_generation(self):
        pass


if __name__ == '__main__':
    unittest.main()
