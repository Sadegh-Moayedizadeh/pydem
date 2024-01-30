from abc import ABC, abstractmethod
from typing import Iterable

from pydem.container.mesh import Mesh
from pydem.particle import Particle, Wall


class ContainerBase(ABC):
    @abstractmethod
    def __init__(
        self, mesh: Mesh, particles: Iterable[Particle], walls: Iterable[Wall]
    ) -> None:
        pass
