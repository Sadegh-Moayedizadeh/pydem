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


def test_add_particles_should_add_it_to_the_cell_that_contains_its_centers_coordinates() -> None:  # noqa: E501
    # Arrange
    mesh = Mesh(length=100, height=100, min_cell_size=13)
    particle = Quartz(1, 1, 1)
    print(particle.center_x)

    # Act
    mesh.add_particles(particle)
    containing_cells = list(filter(
        lambda cell: cell.is_coordinates_inside(1, 1),
        mesh.cells
    ))

    # Assert
    assert len(containing_cells) == 1
    assert particle in next(iter(containing_cells)).particles


def test_find_candidate_contacting_particle_should_return_every_particle_inside_intersecting_cells() -> None:  # noqa: E501
    # Arrange
    mesh = Mesh(length=100, height=100, min_cell_size=13)

    cell_length = next(iter(mesh.cells)).length
    cell_height = next(iter(mesh.cells)).height
    first_particle = Quartz(10, 10, 20)
    second_particle = Quartz(1 + cell_length, 1, 1)
    third_particle = Quartz(1, 1 + cell_height, 1)
    fourth_particle = Quartz(1 + 2 * cell_length, 1, 1)

    # Act
    mesh.add_particles(
        first_particle, second_particle, third_particle, fourth_particle)
    candidate_contacting_particles = mesh.find_candidate_contacting_particles(
        first_particle)

    # Assert
    assert set(candidate_contacting_particles) == \
        {second_particle, third_particle}
