from pytest import mark

from pydem.container import Cell


@mark.parametrize('x, y, cell, expected_result', [
    (0, 0, Cell(2, 2, -1, -1), True),  # fully inside
    (-1, -1, Cell(2, 2, -1, -1), True),  # on the corner
    (-1, 0, Cell(2, 2, -1, -1), True),  # on the side
    (-2, 0, Cell(2, 2, -1, -1), False),  # fully outsise
    (2, 0, Cell(2, 2, -1, -1), False)  # fully outside
])
def test_is_coordinates_inside(
    x: float, y: float, cell: Cell, expected_result: bool
) -> None:
    # Arrange(empty)
    # Act
    actual_result = cell.is_coordinates_inside(x, y)

    # Assert
    assert actual_result == expected_result


@mark.parametrize('first_cell, second_cell, expected_result', [
    (Cell(1, 1, 0, 0), Cell(1, 1, 1, 0), True),  # right side
    (Cell(1, 1, 0, 0), Cell(1, 1, 1, 1), True),  # upper right side
    (Cell(1, 1, 0, 0), Cell(1, 1, 0, 1), True),  # upper side
    (Cell(1, 1, 0, 0), Cell(1, 1, -1, 0), True),  # lower side
    (Cell(1, 1, 0, 0), Cell(1, 1, 0, -1), True),  # left side
    (Cell(1, 1, 0, 0), Cell(1, 1, -1, -1), True),  # lower left side
    (Cell(1, 1, 0, 0), Cell(1, 1, 1, -1), True),  # lower right side
    (Cell(1, 1, 0, 0), Cell(1, 1, -1, 1), True),  # upper left side
    (Cell(1, 1, 0, 0), Cell(1, 1, 10, 10), False),  # away from each other
])
def test_is_adjacent(
    first_cell: Cell, second_cell: Cell, expected_result: bool
) -> None:
    # Arrange (empty)
    # Act
    actual_result = first_cell.is_adjacent(second_cell)

    # Assert
    assert actual_result == expected_result
