from typing import Iterable

from pydem.container.container_base import ContainerBase
from pydem.particle import ParticleBase, Wall


class ContainerBuilder:
    def __init__(self, container_class: ContainerBase) -> None:
        self._container_class = container_class

    def build_container(self) -> ContainerBase:
        return self._container_class()

    def _generate_particles(self) -> Iterable[ParticleBase]:
        pass

    def _generate_walls(self) -> Iterable[Wall]:
        pass
