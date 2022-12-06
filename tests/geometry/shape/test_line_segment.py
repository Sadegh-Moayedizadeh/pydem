from pydem.geometry.shape import LineSegment
from pydem.geometry.value import Radian


def test_area_is_zero() -> None:
    # Arrange
    line_segment = LineSegment(0, 0, Radian(0), 1)

    # Act, Assert
    assert line_segment.area == 0


def test_len() -> None:
    # Arrange
    line_segment = LineSegment(0, 0, Radian(0), 1)

    # Act, Assert
    assert len(line_segment) == 1


def test_eq() -> None:
    # Arrange
    first_line_segment = LineSegment(0, 0, Radian(0), 1)
    second_line_segment = LineSegment(0, 0, Radian(0), 1)

    # Act, Assert
    assert first_line_segment == second_line_segment
