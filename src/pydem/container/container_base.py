from abc import ABC, abstractmethod

from typing import Iterable

from pydem.particle import ParticleBase, Wall
from pydem.container.mesh import Mesh


class ContainerBase(ABC):
    @abstractmethod
    def __init__(
        self, mesh: Mesh, particles: Iterable[ParticleBase], walls: Iterable[Wall]
    ) -> None:
        pass
