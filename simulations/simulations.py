"""contains the Simulation class that runs the DEM simulation
"""


class Simulation(object):
    
    def __init__(self, container):    
        self.container = container
    
    def set_up(self):
        self.container.generate_particles()
        self.container.update_mechanical_boxes()
        self.container.update_chemical_boxes()
    
    def run(self):
        while True:
            self.update_boundary_conditions()
            is_relaxed = False
            while not is_relaxed:
                self.container.update()
    