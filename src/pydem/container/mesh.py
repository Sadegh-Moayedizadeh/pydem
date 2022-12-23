from typing import Mapping, Iterable, List

from pydem.particle import ParticleBase
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
    def cells(self) -> Mapping[int: Rectangle]:
        def __init__(self) -> None:
            self.id = 0


class Cell:
    def __init__(
        self,
        id: int,
        length: float,
        height: float,
        lower_left_corner_x: float,
        lower_left_corner_y: float
    ) -> None:
        self._id = id
        self._particles: List[ParticleBase] = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def particles(self) -> Iterable[ParticleBase]:
        return self._particles

    def add_particle(self, particle: ParticleBase) -> None:
        self._particles.append(particle)


# # client
# x = random.uniform(0, length)
# y = random.uniform(0, height)
# size = random.uniform(min_size, max_size)
# new_particel = Particle(x, y, size)
# cell = mesh.get_cell_containing_coordicates()
# adjacent_cells = mesh.find_adjacent_cells(cell)
# cells = adjacent_cells + [cell]
# if any(
#         new_particel.intersection(other_particle)
#         for other_particle in chain.from_iterable(...)):
#     del new_particel
# else:
#     cell.add_particle(new_particel)
#     count += 1
