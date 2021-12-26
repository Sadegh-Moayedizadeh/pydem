from generation.container import Container
from geometry.two_dimensional_operations import (
    intersection_area,
    intersection_length,
)


class TestParticleOverlap:
    def test_clay_clay(
        self,
        base_kaolinite_particle,
        intersecting_kaolinite_with_kaolinite,
    ):
        length = intersection_length(
            base_kaolinite_particle.shape,
            intersecting_kaolinite_with_kaolinite.shape,
        )
        expected_result = 500
        assert length == expected_result

    def test_sand_clay(
        self,
        base_quartz_particle,
        intersecting_kaolinite_with_quartz,
    ):
        length = intersection_length(
            intersecting_kaolinite_with_quartz.shape,
            base_quartz_particle.shape,
        )
        expected_result = 500
        assert length == expected_result

    def test_sand_sand(
        self,
        base_quartz_particle,
        intersecting_quartz_with_quartz,
    ):
        area = intersection_area(
            base_quartz_particle.shape,
            intersecting_quartz_with_quartz.shape,
        )
        expected_result = 37482287.27931191
        assert abs(area - expected_result) < 1e-10


class TestForceCalculation:
    def test_clay_clay(
        self,
        base_kaolinite_particle,
        intersecting_kaolinite_with_kaolinite,
        quartz_dict,
        kaolinite_dict,
    ):
        container = Container(
            100000, 100000, [quartz_dict, kaolinite_dict], "tt", 0.01, {}
        )
        container.particles = [
            base_kaolinite_particle,
            intersecting_kaolinite_with_kaolinite,
        ]
        container.update_mechanical_boxes()
        container.update_mechanical_contacts_dictionary()
        forces_on_base_particle = container.mechanical_contact_forces(
            base_kaolinite_particle
        )
        forces_on_other_particle = container.mechanical_contact_forces(
            intersecting_kaolinite_with_kaolinite
        )
        assert forces_on_base_particle
        assert forces_on_other_particle

    def test_sand_clay(
        self,
        base_quartz_particle,
        intersecting_kaolinite_with_quartz,
        quartz_dict,
        kaolinite_dict,
    ):
        container = Container(
            100000, 100000, [quartz_dict, kaolinite_dict], "tt", 0.01, {}
        )
        container.particles = [
            base_quartz_particle,
            intersecting_kaolinite_with_quartz,
        ]
        container.update_mechanical_boxes()
        container.update_mechanical_contacts_dictionary()
        forces_on_quartz_particle = container.mechanical_contact_forces(
            base_quartz_particle
        )
        forces_on_koalinite_particle = container.mechanical_contact_forces(
            intersecting_kaolinite_with_quartz
        )
        assert forces_on_quartz_particle
        assert forces_on_koalinite_particle

    def test_sand_sand(
        self,
        base_quartz_particle,
        intersecting_quartz_with_quartz,
        quartz_dict,
        kaolinite_dict,
    ):
        container = Container(
            100000, 100000, [quartz_dict, kaolinite_dict], "tt", 0.01, {}
        )
        container.particles = [
            base_quartz_particle,
            intersecting_quartz_with_quartz,
        ]
        container.update_mechanical_boxes()
        container.update_mechanical_contacts_dictionary()
        forces_on_base_quartz_particle = container.mechanical_contact_forces(
            base_quartz_particle
        )
        forces_on_other_particle = container.mechanical_contact_forces(
            intersecting_quartz_with_quartz
        )
        assert forces_on_other_particle
        assert forces_on_base_quartz_particle
