from generation.base_classes import Kaolinite, Quartz, Container
from simulations.simulations import Simulation
from display import charts


quartz_sand1 = {
    'type': 'quartz',
    'size_upper_bound': 10000,
    'size_lower_bound': 8000,
    'quantity': 35
}
quartz_sand2 = {
    'type': 'quartz',
    'size_upper_bound': 10000,
    'size_lower_bound': 8000,
    'quantity': 35
}
kaolinite_clay1 = {
    'type': 'kaolinite',
    'size_upper_bound': 3000,
    'size_lower_bound': 1000,
    'quantity': 500
}
kaolinite_clay2 = {
    'type': 'kaolinite',
    'size_upper_bound': 3000,
    'size_lower_bound': 1000,
    'quantity': 500
}
kaolinite_clay3 = {
    'type': 'kaolinite',
    'size_upper_bound': 3000,
    'size_lower_bound': 1000,
    'quantity': 500
}
kaolinite_clay4 = {
    'type': 'kaolinite',
    'size_upper_bound': 3000,
    'size_lower_bound': 1000,
    'quantity': 500
}

def main():
    container = base_classes.Container(
        length = 100000,
        width = 100000,
        particles_info = [quartz_sand1, quartz_sand2, kaolinite_clay1, kaolinite_clay2, kaolinite_clay3, kaolinite_clay4],
        time_step = 0.01,
        simulation_type = 'tt',
        fluid_characteristics = None
    )
    simulation = Simulation(container)
    simulation.set_up()
    simulation.run()
    #export charts from simulation


if __name__ == '__main__':
    main()