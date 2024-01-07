from __future__ import annotations

from abc import ABC, abstractproperty
from typing import Iterable

from sympy.geometry import intersection
from sympy.geometry.entity import GeometryEntity


class Geometric(ABC):
    @abstractproperty
    def geometrical_shape(self) -> GeometryEntity:
        pass

    def intersection(self, other: Geometric) -> Iterable[GeometryEntity]:
        return intersection(self.geometrical_shape, other.geometrical_shape)

    def has_intersection_with(self, other: Geometric) -> bool:
        return bool(self.intersection(other))
