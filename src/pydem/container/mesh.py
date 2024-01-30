from __future__ import annotations

from itertools import chain
from typing import Iterable, List

from pydem.container.cell import Cell
from pydem.particle import Particle


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
        self._cells: List[Cell] = []

        self._generate_cells()

    @property
    def cells(self) -> Iterable[Cell]:
        return self._cells

    def add_particles(self, *particles: Particle) -> None:
        for particle in particles:
            cell = self._find_cell_containing_particles_center(particle)
            cell.add_particle(particle)

    def find_candidate_contacting_particles(
        self,
        particle: Particle
    ) -> Iterable[Particle]:
        main_cell = self._find_cell_containing_particles_center(particle)
        adjacent_cells = self._find_adjacent_cells(main_cell)
        valid_cells = [main_cell] + list(filter(
            lambda c: bool(particle.intersection(c)),
            adjacent_cells
        ))
        return filter(
            lambda candidate_particle: candidate_particle is not particle,
            chain.from_iterable(map(lambda c: c.particles, valid_cells))
        )

    def refresh(self) -> None:
        # TODO: implement this method to refresh particles in cells
        pass

    def _generate_cells(self) -> None:
        cell_length = self._calculate_next_divisor_without_remainder(
            self._length,
            self._min_cell_size
        )
        cell_height = self._calculate_next_divisor_without_remainder(
            self._height,
            self._min_cell_size
        )
        lower_left_corner_x, lower_left_corner_y = 0, 0
        while lower_left_corner_x < self._length:
            while lower_left_corner_y < self._height:
                cell = Cell(
                    cell_length,
                    cell_height,
                    lower_left_corner_x,
                    lower_left_corner_y
                )
                self._cells.append(cell)
                lower_left_corner_y += cell_height
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
        self, particle: Particle
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
