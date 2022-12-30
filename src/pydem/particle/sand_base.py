from pydem.particle.particle_base import ParticleBase
from sympy import Circle


class SandBase(ParticleBase):
    def __init__(self) -> None:
        ParticleBase.__init__(self)
        self._shape = Circle()
