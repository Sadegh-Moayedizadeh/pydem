from typing import Mapping

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
    pass


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
