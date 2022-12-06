from __future__ import annotations

from typing import Dict

from pydem.geometry.shape.base_shape import BaseShape


class Point(BaseShape):
    def __init__(self, center_x: float, center_y: float) -> None:
        self._center_x = center_x
        self._center_y = center_y

    @property
    def center_x(self) -> float:
        return self._center_x

    @property
    def center_y(self) -> float:
        return self._center_y

    @property
    def area(self) -> float:
        return 0

    def __deepcopy__(self, memo: Dict[int, object]) -> Point:
        return Point(self._center_x, self._center_y)

    def __eq__(self, other: Point) -> bool:
        return self._center_x == other.center_x \
            and self._center_y == other.center_y
