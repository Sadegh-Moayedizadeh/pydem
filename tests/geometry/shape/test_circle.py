from math import pi

from pydem.geometry.shape import Circle


def test_area() -> None:
    # Arrange
    circle = Circle(0, 0, 1)

    # Act, Assert
    assert circle.area == 2 * pi


def test_eq() -> None:
    # Arrange
    first_circle = Circle(0, 0, 1)
    second_circle = Circle(0, 0, 1)

    # Act, Assert
    assert first_circle == second_circle
