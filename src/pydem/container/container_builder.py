from typing import Iterable, Type

from pydem.container.container_base import ContainerBase
from pydem.container.mesh import Mesh
from pydem.particle import ParticleBase, Wall

import random


class ContainerBuilder:
    def __init__(
        self,
        container_class: Type[ContainerBase],
        particle_class: Type[ParticleBase],
        container_length: float,
        container_height: float,
        number_of_particels: int,
        particle_size_upper_bound: int,
        particle_size_lower_bound: int,
    ) -> None:
        self._container_class = container_class
        self._particle_class = particle_class
        self._container_length = container_length
        self._container_height = container_height
        self._number_of_particels = number_of_particels
        self._particle_size_upper_bound = particle_size_upper_bound
        self._particle_size_lower_bound = particle_size_lower_bound

    def build(self) -> ContainerBase:
        mesh = self._generate_mesh()
        particles = self._generate_particles(mesh)
        walls = self._generate_walls()
        return self._container_class(mesh, particles, walls)

    def _generate_particles(self, mesh: Mesh) -> Iterable[ParticleBase]:
        result = []

        number_of_generated_particles = 0
        while number_of_generated_particles < self._number_of_particels:
            size = round(random.uniform(self._particle_size_lower_bound, self._particle_size_upper_bound), 2)
            center_x = round(random.uniform(0, self._container_length), 2)
            center_y = round(random.uniform(0, self._container_height), 2)
            new_particle = self._particle_class(center_x, center_y, size)
            # TODO: check if it has intersection with other particles.
            result.append(new_particle)

        return result

    def _generate_walls(self) -> Iterable[Wall]:
        pass

    def _generate_mesh(self) -> Mesh:
        return Mesh(self._container_length, self._container_height)
