from __future__ import annotations

from itertools import chain
from typing import Dict, Iterable, List, Mapping

from sympy import Polygon

from pydem.particle import ParticleBase


class Mesh:
    def __init__(
        self,
        length: float,
        height: float,
        min_cell_size: float
    ) -> None:
        self._length = length
        self._height = height
        self._min_cell_size = min_cell_size
        self._cells: Dict[int, Cell] = {}

        self._generate_cells()

    @property
    def cells(self) -> Mapping[int, Cell]:
        return self._cells

    def add_particle(self, particle: ParticleBase) -> None:
        cell = self._find_cell_containing_particle(particle)
        cell.add_particle(particle)

    def find_candidate_contacting_particles(
        self,
        particle: ParticleBase
    ) -> Iterable[ParticleBase]:
        main_cell = self._find_cell_containing_particle(particle)
        adjacent_cells = self._find_adjacent_cells(main_cell)
        valid_cells = [main_cell] + list(filter(
            lambda c: particle.intersection(c),
            adjacent_cells
        ))
        return chain.from_iterable(map(lambda c: c.particles, valid_cells))

    def _generate_cells(self) -> None:
        cell_length = self._calculate_next_divisor_without_remainder(
            self._length,
            self._min_cell_size
        )
        cell_height = self._calculate_next_divisor_without_remainder(
            self._height,
            self._min_cell_size
        )
        id = 0
        lower_left_corner_x, lower_left_corner_y = 0, 0
        while lower_left_corner_x < self._length:
            while lower_left_corner_y < self._height:
                cell = Cell(
                    cell_length,
                    cell_height,
                    lower_left_corner_x,
                    lower_left_corner_y
                )
                self._cells[id] = cell
                lower_left_corner_y += cell_height
                id += 1
            lower_left_corner_x += cell_length
            lower_left_corner_y = 0

    def _calculate_next_divisor_without_remainder(
        self,
        number: int,
        divisor: int
    ) -> int:
        if number % divisor == 0:
            return divisor
        while divisor <= number // 2:
            if number % divisor == 0:
                return divisor
            divisor += 1
        return number

    def _find_cell_containing_particle(self, particle: ParticleBase) -> Cell:
        pass

    def _find_adjacent_cells(self, cell: Cell) -> Iterable[Cell]:
        pass


class Cell:
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

        self._shape = Polygon(
            (lower_left_corner_x, lower_left_corner_y),
            (lower_left_corner_x + length, lower_left_corner_y),
            (lower_left_corner_x + length, lower_left_corner_y + height),
            (lower_left_corner_x, lower_left_corner_y + height)
        )

        self._particles: List[ParticleBase] = []

    @property
    def length(self) -> int:
        return self._length

    @property
    def height(self) -> int:
        return self._height

    @property
    def particles(self) -> Iterable[ParticleBase]:
        return self._particles

    def add_particle(self, particle: ParticleBase) -> None:
        self._particles.append(particle)

    def remove_particle(self, particle: ParticleBase) -> None:
        self._particles.remove(particle)
