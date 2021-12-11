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
    def test_clay_clay_contact(
        self,
        base_kaolinite_particle,
        intersecting_kaolinite_with_kaolinite,
        quartz_dict, kaolinite_dict
    ):
        container = Container(
        100000, 100000, [quartz_dict, kaolinite_dict], 'tt', 0.01, {}
        )
        container.particles = [
            base_kaolinite_particle, intersecting_kaolinite_with_kaolinite
        ]
        container.update_mechanical_boxes()
        container.update_mechanical_contacts_dictionary()
        assert intersecting_kaolinite_with_kaolinite in container.mechanical_contacts[base_kaolinite_particle]
        assert base_kaolinite_particle in container.mechanical_contacts[intersecting_kaolinite_with_kaolinite]
    
    def test_sand_sand_contact(
        self,
        base_quartz_particle,
        intersecting_quartz_with_quartz,
        quartz_dict, kaolinite_dict
    ):
        container = Container(
        100000, 100000, [quartz_dict, kaolinite_dict], 'tt', 0.01, {}
        )
        container.particles = [
            base_quartz_particle, intersecting_quartz_with_quartz
        ]
        container.update_mechanical_boxes()
        container.update_mechanical_contacts_dictionary()
        assert intersecting_quartz_with_quartz in container.mechanical_contacts[base_quartz_particle]
        assert base_quartz_particle in container.mechanical_contacts[intersecting_quartz_with_quartz]
    
    def test_sand_clay_contact(
        self,
        base_quartz_particle,
        intersecting_kaolinite_with_quartz,
        quartz_dict, kaolinite_dict
    ):
        container = Container(
        100000, 100000, [quartz_dict, kaolinite_dict], 'tt', 0.01, {}
        )
        container.particles = [
            base_quartz_particle, intersecting_kaolinite_with_quartz
        ]
        container.update_mechanical_boxes()
        container.update_mechanical_contacts_dictionary()
        assert intersecting_kaolinite_with_quartz in container.mechanical_contacts[base_quartz_particle]
        assert base_quartz_particle in container.mechanical_contacts[intersecting_kaolinite_with_quartz]
