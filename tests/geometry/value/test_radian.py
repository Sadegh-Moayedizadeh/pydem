from math import pi

from pydem.geometry.value import Radian


def test_add_radian_with_sum_greater_than_2pi() -> None:
    # Arrange
    first_radian = Radian(1.5 * pi)
    second_radian = Radian(1.5 * pi)

    # Act
    sum_radian = first_radian + second_radian

    # Assert
    assert sum_radian.value == pi


def test_subtract_negative_radian() -> None:
    # Arrange
    first_radian = Radian(0)
    second_radian = Radian(0.5 * pi)

    # Act
    sub_radian = first_radian - second_radian

    # Assert
    assert sub_radian.value == 1.5 * pi


def test_eq() -> None:
    # Arrange
    first_radian = Radian(0)
    second_radian = Radian(0)

    # Act, Assert
    assert first_radian == second_radian
