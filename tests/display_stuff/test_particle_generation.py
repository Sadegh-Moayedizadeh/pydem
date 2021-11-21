import pytest
from generation.base_classes import Container
from display.illustration import IllustrationMPL


def test_particle_generation_only_clay(kaolinite_dict, quartz_dict):
    container = Container(
        100000, 100000, [quartz_dict], 'tt', 0.01, {}
    )
    container.generate_particles()
    ill = IllustrationMPL(container, title='only clay')
    ill.display()
    assert True
