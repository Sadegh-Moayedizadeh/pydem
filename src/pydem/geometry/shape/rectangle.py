from __future__ import annotations

from typing import Dict

from pydem.geometry.shape.shape_base import ShapeBase


class Rectangle(ShapeBase):
    def __init__(
        self,
        lower_left_corner_x: float,
        lower_left_corner_y: float,
        upper_right_corner_x: float,
        upper_right_corner_y: float
    ) -> None:
        self._lower_left_corner_x = lower_left_corner_x
        self._lower_left_corner_y = lower_left_corner_y
        self._upper_right_corner_x = upper_right_corner_x
        self._upper_right_corner_y = upper_right_corner_y

    @property
    def center_x(self) -> float:
        return (self._lower_left_corner_x + self._upper_right_corner_x) / 2

    @property
    def center_y(self) -> float:
        return (self._lower_left_corner_y + self._upper_right_corner_y) / 2

    @property
    def area(self) -> float:
        return abs(self._upper_right_corner_x - self._lower_left_corner_x) * \
            abs(self._upper_right_corner_y - self._lower_left_corner_y)

    def __deepcopy__(self, memo: Dict[int, object]) -> Rectangle:
        return Rectangle(
            self._lower_left_corner_x,
            self._lower_left_corner_y,
            self._upper_right_corner_x,
            self._upper_right_corner_y
        )

    def __eq__(self, other: Rectangle) -> bool:
        return self._lower_left_corner_x == other._lower_left_corner_x and \
            self._lower_left_corner_y == other._lower_left_corner_y and \
            self._upper_right_corner_x == other._upper_right_corner_x and \
            self._upper_right_corner_y == other._upper_right_corner_y
