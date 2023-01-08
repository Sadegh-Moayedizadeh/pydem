from __future__ import annotations

from itertools import chain
from typing import Dict, Iterable, Mapping

from pydem.particle import ParticleBase
from pydem.container.cell import Cell


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
        cell = self._find_cell_containing_particles_center(particle)
        cell.add_particle(particle)

    def find_candidate_contacting_particles(
        self,
        particle: ParticleBase
    ) -> Iterable[ParticleBase]:
        main_cell = self._find_cell_containing_particles_center(particle)
        adjacent_cells = self._find_adjacent_cells(main_cell)
        valid_cells = [main_cell] + list(filter(
            lambda c: bool(particle.intersection(c)),
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

    def _find_cell_containing_particles_center(
        self, particle: ParticleBase
    ) -> Cell:
        return next(filter(
            lambda c: c.is_coordinates_inside(
                particle.center_x, particle.center_y),
            self._cells
        ))

    def _find_adjacent_cells(self, cell: Cell) -> Iterable[Cell]:
        return filter(
            lambda other_cell: cell.is_adjacent(other_cell),
            self._cells
        )
