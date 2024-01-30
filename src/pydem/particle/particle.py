from abc import ABC, abstractproperty, abstractmethod
from pydem.geometry import Geometric


class Particle(Geometric):
    @abstractmethod
    def __init__(self, center_x: float, center_y: float, size: float) -> None:
        pass

    @abstractproperty
    def center_x(self) -> float:
        pass

    @abstractproperty
    def center_y(self) -> float:
        pass

    @abstractproperty
    def size(self) -> float:
        pass
