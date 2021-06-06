from generation import base_classes
from simulations import simulations
from display import charts, illustration

particles_info = [
    {'type': 'kaolinite', 'size_upper_bound': 200, 'size_lower_bound': 120, 'quantity': 500},
    {'type': 'quartz', 'size_upper_bound': 1200, 'size_lower_bound': 1000, 'quantity': 80},
    ]
container = base_classes.Container(
    length = 4000,
    width = 4000,
    particles_info = particles_info
)
container.generate()

# run the simulation with appropriate parameters
# sim = simulations.Triaxial(container, params)
# sim.run()

# connect charts and illustrations with the running simulation