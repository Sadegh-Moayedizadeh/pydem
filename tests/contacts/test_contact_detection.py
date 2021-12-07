from geometry import two_dimensional_operations as operations
from generation.container import Container
import pytest


class TestIntersection:
    def test_clay_clay_intersection(
        self,
        base_kaolinite_particle,
        intersecting_kaolinite_with_kaolinite
    ):
        inter = operations.intersection(
            base_kaolinite_particle.midline,
            intersecting_kaolinite_with_kaolinite.midline,
        )
        assert inter
    
    def test_sand_sand_intersection(
        self,
        base_quartz_particle,
        intersecting_quartz_with_quartz
    ):
        inter = operations.intersection(
            base_quartz_particle.shape,
            intersecting_quartz_with_quartz.shape,
        )
        assert inter
    
    def test_sand_and_clay_intersection(
        self,
        base_quartz_particle,
        intersecting_kaolinite_with_quartz,
    ):
        inter = operations.intersection(
            base_quartz_particle.shape,
            intersecting_kaolinite_with_quartz.midline,
        )
        assert inter


class TestContactDetection:
    
    @pytest.fixture(scope='class')
    def container(self, quartz_dict, kaolinite_dict):
        c = Container(
        100000, 100000, [quartz_dict, kaolinite_dict], 'tt', 0.01, {}
        )
        return c

    def test_clay_clay_contact(
        self,
    ):
        pass
    
    def test_sand_sand_contact(
        self,
        base_quartz_particle,
        intersecting_quartz_with_quartz,
    ):
        pass
    
    def test_sand_clay_contact(
        self,
        base_quartz_particle,
        intersecting_kaolinite_with_quartz,
    ):
        pass
