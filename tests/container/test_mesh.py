from pydem.container import Mesh
from pydem.particle import Quartz


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


def test_add_particle_should_add_it_to_the_cell_that_contains_its_centers_coordinates() -> None:  # noqa: E501
    # Arrange
    mesh = Mesh(length=100, height=100, min_cell_size=13)
    particle = Quartz(1, 1, 1)
    print(particle.center_x)

    # Act
    mesh.add_particle(particle)
    containing_cells = list(filter(
        lambda cell: cell.is_coordinates_inside(1, 1),
        mesh.cells
    ))

    # Assert
    assert len(containing_cells) == 1
    assert particle in next(iter(containing_cells)).particles
