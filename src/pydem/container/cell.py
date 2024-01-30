from __future__ import annotations

from typing import Iterable, List

from sympy.geometry import Polygon
from sympy.geometry.entity import GeometryEntity

from pydem.geometry import Geometric
from pydem.particle import Particle


class Cell(Geometric):
    def __init__(
        self,
        length: int,
        height: int,
        lower_left_corner_x: float,
        lower_left_corner_y: float
    ) -> None:
        self._length = length
        self._height = height
        self._lower_left_corner_x = lower_left_corner_x
        self._lower_left_corner_y = lower_left_corner_y

        self._geometrical_shape = Polygon(
            (lower_left_corner_x, lower_left_corner_y),
            (lower_left_corner_x + length, lower_left_corner_y),
            (lower_left_corner_x + length, lower_left_corner_y + height),
            (lower_left_corner_x, lower_left_corner_y + height)
        )

        self._particles: List[Particle] = []

    @property
    def length(self) -> int:
        return self._length

    @property
    def height(self) -> int:
        return self._height

    @property
    def geometrical_shape(self) -> GeometryEntity:
        return self._geometrical_shape

    @property
    def particles(self) -> Iterable[Particle]:
        return self._particles

    def add_particle(self, particle: Particle) -> None:
        self._particles.append(particle)

    def remove_particle(self, particle: Particle) -> None:
        self._particles.remove(particle)

    def is_coordinates_inside(
        self, x_coordinate: float, y_coordinate: float
    ) -> bool:
        return x_coordinate >= self._lower_left_corner_x \
            and x_coordinate <= self._lower_left_corner_x + self._length \
            and y_coordinate >= self._lower_left_corner_y \
            and y_coordinate <= self._lower_left_corner_y + self._height

    def is_adjacent(self, other: Cell) -> bool:
        return (
            self._lower_left_corner_x ==
            other._lower_left_corner_x + other._length
            and self._lower_left_corner_y ==
            other._lower_left_corner_y
        ) or (
            self._lower_left_corner_x ==
            other._lower_left_corner_x + other._length
            and self._lower_left_corner_y ==
            other._lower_left_corner_y + other._height
        ) or (
            self._lower_left_corner_x ==
            other._lower_left_corner_x + other._length
            and self._lower_left_corner_y ==
            other._lower_left_corner_y - other._height
        ) or (
            self._lower_left_corner_x == other._lower_left_corner_x
            and self._lower_left_corner_y ==
            other._lower_left_corner_y + other._height
        ) or (
            self._lower_left_corner_x == other._lower_left_corner_x
            and self._lower_left_corner_y ==
            other._lower_left_corner_y - other._height
        ) or (
            self._lower_left_corner_x ==
            other._lower_left_corner_x - other._length
            and self._lower_left_corner_y ==
            other._lower_left_corner_y - other.height
        ) or (
            self._lower_left_corner_x ==
            other._lower_left_corner_x - other._length
            and self._lower_left_corner_y ==
            other._lower_left_corner_y
        ) or (
            self._lower_left_corner_x ==
            other._lower_left_corner_x - other._length
            and self._lower_left_corner_y ==
            other._lower_left_corner_y + other.height
        )
