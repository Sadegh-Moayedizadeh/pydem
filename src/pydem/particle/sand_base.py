from sympy import Circle
from sympy.geometry.entity import GeometryEntity

from pydem.geometry import Geometric
from pydem.particle.particle_base import ParticleBase


class SandBase(ParticleBase, Geometric):
    def __init__(self, center_x: float, center_y: float, size: float) -> None:
        self._center_x = center_x
        self._center_y = center_y
        self._radius = size
        self._geometrical_shape = Circle((center_x, center_y), size)

    @property
    def center_x(self) -> float:
        return self._center_x

    @property
    def center_y(self) -> float:
        return self._center_y

    @property
    def size(self) -> float:
        return self._radius

    @property
    def geometrical_shape(self) -> GeometryEntity:
        return self._geometrical_shape

    def move(self, delta_x: float, delta_y: float) -> None:
        self._center_x += delta_x
        self._center_y += delta_y
        self._geometrical_shape = Circle(
            (self._center_x, self._center_y), self._radius)
