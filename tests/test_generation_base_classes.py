"""Testing the base classes used in generation packaage
"""

from generation.base_classes import Montmorillonite, Quartz
import unittest


class TestGenerals(unittest.TestCase):

    instance = Montmorillonite(x=0, y=0, inclination=0, thickness=2, length=100)

    def test_particle_number(self):
        n1 = instance.num
        new_instance1 = Montmorillonite(
            x=100, y=100, inclination=0, thickness=2, length=100
        )
        n2 = new_instance1.num
        del new_instance
        new_instance2 = Montmorillonite(
            x=100, y=100, inclination=0, thickness=2, length=100
        )
        n3 = new_instance2.num
        self.assertEqual(n2, n3)

    def test_box_num(self):
        pass


class TestMontmorillonite(unittest.TestCase):
    def test_thickness_bounds(self):
        pass

    def test_length_bounds(self):
        pass

    def test_mass(self):
        pass


class TestQuartz(unittest.TestCase):
    def test_diameter_bounds(self):
        pass

    def test_mass(self):
        pass


if __name__ == "__main__":
    unittest.main()
