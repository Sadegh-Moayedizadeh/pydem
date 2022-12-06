from pydem.geometry.shape import Point


def test_points_with_same_coordinates_should_be_equal() -> None:
    # Arrange
    first_point = Point(0, 0)
    second_point = Point(0, 0)

    # Act, Assert
    assert first_point == second_point


def test_points_without_same_coordinates_should_not_be_equal() -> None:
    # Arrange
    first_point = Point(0, 0)
    second_point = Point(1, 1)

    # Act, Assert
    assert first_point != second_point


def test_point_should_have_area_equal_to_zero() -> None:
    # Arrange
    point = Point(0, 0)

    # Act, Assert
    assert point.area == 0
