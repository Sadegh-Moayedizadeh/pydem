from typing import Iterable

from pydem.geometry.shape import Rectangle


class Mesh:
    def __init__(self, length: float, height: float) -> None:
        self._length = length
        self._height = height

    @property
    def cells(self) -> Iterable[Rectangle]:
        pass
