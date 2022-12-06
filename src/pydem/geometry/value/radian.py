from __future__ import annotations

from math import pi


class Radian:
    def __init__(self, value: float) -> None:
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    def __add__(self, other: Radian) -> Radian:
        return Radian((self._value + other.value) % (2 * pi))

    def __sub__(self, other: Radian) -> Radian:
        return Radian((self._value - other.value) % (2 * pi))

    def __eq__(self, other: Radian) -> bool:
        return self._value == other.value
