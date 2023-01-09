from typing import Iterable, Type

from pydem.container.container_base import ContainerBase
from pydem.container.mesh import Mesh
from pydem.particle import ParticleBase, Wall


class ContainerBuilder:
    def __init__(
        self,
        container_class: Type[ContainerBase],
        particle_class: Type[ParticleBase],
        container_length: float,
        container_height: float,
        number_of_particels: int
    ) -> None:
        self._container_class = container_class
        self._particle_class = particle_class
        self._container_length = container_length
        self._container_height = container_height
        self._number_of_particels = number_of_particels

    def build(self) -> ContainerBase:
        mesh = self._generate_mesh()
        particles = self._generate_particles(mesh)
        walls = self._generate_walls()
        return self._container_class(mesh, particles, walls)

    def _generate_particles(self, mesh: Mesh) -> Iterable[ParticleBase]:
        pass

    def _generate_walls(self) -> Iterable[Wall]:
        pass

    def _generate_mesh(self) -> Mesh:
        return Mesh(self._container_length, self._container_height)
