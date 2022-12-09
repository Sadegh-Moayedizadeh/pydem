from __future__ import annotations

from typing import Dict

from pydem.geometry.shape.shape_base import ShapeBase
from pydem.geometry.value import Radian


class LineSegment(ShapeBase):
    def __init__(
        self,
        center_x: float,
        center_y: float,
        inclination: Radian,
        length: float
    ) -> None:
        self._center_x = center_x
        self._center_y = center_y
        self._inclination = inclination
        self._length = length

    @property
    def center_x(self) -> float:
        return self._center_x

    @property
    def center_y(self) -> float:
        return self._center_y

    @property
    def inclination(self) -> Radian:
        return self._inclination

    @property
    def length(self) -> float:
        return self._length

    @property
    def area(self) -> float:
        return 0

    def __deepcopy__(self, memo: Dict[int, object]) -> LineSegment:
        return LineSegment(self._center_x, self._center_y)

    def __len__(self) -> float:
        return self._length

    def __eq__(self, other: LineSegment) -> bool:
        return (
            self._center_x == other.center_x and
            self._center_y == other.center_y and
            self._inclination == other.inclination and
            self._length == other.length
        )
