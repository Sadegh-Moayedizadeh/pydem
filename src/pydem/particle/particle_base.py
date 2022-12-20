from abc import ABC, abstractproperty


class ParticleBase(ABC):
    @abstractproperty
    def center_x(self) -> float:
        pass

    @abstractproperty
    def center_y(self) -> float:
        pass
