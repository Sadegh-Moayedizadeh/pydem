from typing import Iterable

from pydem.geometry.shape import Rectangle


class Mesh:
    def __init__(
        self,
        length: float,
        height: float,
        max_cell_size: float,
        min_cell_size: float
    ) -> None:
        self._length = length
        self._height = height
        self._max_cell_size = max_cell_size
        self._min_cell_size = min_cell_size

    @property
    def cells(self) -> Iterable[Rectangle]:
        pass
