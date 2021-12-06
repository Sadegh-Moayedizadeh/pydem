from generation.container import Container


def test_kaolinite_kaolinite_force(
    base_kaolinite_particle,
    intersecting_kaolinite_with_kaolinite,
    kaolinite_dict,
    quartz_dict,
):
    container = Container(
        100000, 100000, [quartz_dict, kaolinite_dict], 'tt', 0.01, {}
    )
    container.particles.extend([
        base_kaolinite_particle,
        intersecting_kaolinite_with_kaolinite,
    ])
    container.update_mechanical_boxes()
    container.update_mechanical_contacts_dictionary()
    forces = container.mechanical_contact_forces(base_kaolinite_particle)
    print('/////////////////////////')
    print(forces)
    assert True
