from pydem.container import Mesh


def test_generated_cells_should_fit_the_whole_mesh() -> None:
    # Arrange
    mesh = Mesh(length=100, height=100, min_cell_size=13)

    # Act
    cells = mesh.cells
    a_cell = cells[0]

    # Assert
    assert a_cell.length == 20
    assert a_cell.height == 20


def test_generated_cells_number_should_add_up_to_the_mesh_sizes() -> None:
    # Arrange
    mesh = Mesh(length=100, height=100, min_cell_size=13)

    # Act
    cells = mesh.cells

    # Assert
    assert len(cells) == 25
