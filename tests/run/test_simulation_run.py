from simulations.simulations import Simulation
from generation.container import Container


def test_run_simulation(kaolinite_dict, quartz_dict):
    container = Container(
        100000, 100000, [quartz_dict], 'tt', 0.01, {}
    )
    simulation = Simulation(container)
    simulation.set_up()
    print(simulation.container.mechanical_boxes)
    print(simulation.container.chemical_boxes)
    assert True
    simulation.run()
    assert True
