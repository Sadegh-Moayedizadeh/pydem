from __future__ import annotations

from math import pi
from typing import Dict

from pydem.geometry.shape.shape_base import ShapeBase


class Circle(ShapeBase):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        radius: float
    ) -> None:
        self._center_x = center_x
        self._center_y = center_y
        self._radius = radius

    @property
    def center_x(self) -> float:
        return self._center_x

    @property
    def center_y(self) -> float:
        return self._center_y

    @property
    def radius(self) -> float:
        return self._radius

    @property
    def area(self) -> float:
        return 2 * pi * self._radius

    def __deepcopy__(self, memo: Dict[int, object]) -> Circle:
        return Circle(self._center_x, self._center_y, self._radius)

    def __eq__(self, other: Circle) -> bool:
        return (
            self._center_x == other.center_x and
            self._center_y == other.center_y and
            self._radius == other.radius
        )
