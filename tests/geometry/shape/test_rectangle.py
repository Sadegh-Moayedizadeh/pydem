from pydem.geometry.shape import Rectangle


def test_center_x() -> None:
    # Arrange
    rectangle = Rectangle(0, 0, 1, 1)

    # Act
    actual_center_x = rectangle.center_x

    # Assert
    assert actual_center_x == 0.5


def test_center_y() -> None:
    # Arrange
    rectangle = Rectangle(0, 0, 1, 1)

    # Act
    actual_center_y = rectangle.center_y

    # Assert
    assert actual_center_y == 0.5


def test_eq() -> None:
    # Arrange
    first_rectangle = Rectangle(0, 0, 1, 1)
    second_rectangle = Rectangle(0, 0, 1, 1)

    # Act, Assert
    assert first_rectangle == second_rectangle


def test_area() -> None:
    # Arrange
    rectangle = Rectangle(0, 0, 1, 1)

    # Act
    actual_area = rectangle.area

    # Assert
    assert actual_area == 1


def test_area_should_be_independent_of_order_of_inputs_to_rectangle_constructor() -> None:  # noqa: E501
    # Arrange
    rectangle = Rectangle(1, 1, 0, 0)

    # Act
    actula_area = rectangle.area

    # Assert
    assert actula_area == 1
