"""A module containing all the base classes upon which to build all
the elements used in the model

Classes
    Particle: the base class for all the soil particles to inherit from 
    Sand: the base class for sand particles
    Clay: the base class for clay particles
    Kaolinite: the class to create kaolinite particles
    Montmorillonite: the class to create montmorillonite particles
    Quartz: the class to create quartz particles
    Illite: the class to create illite particles
    Wall: the class to creat walls as boundaries to the model
    Container: the class to create container objects which hold all the
        stuff to run simulations upon
"""

import logging
import pdb
import random
from collections import defaultdict
from typing import Dict, List, Tuple, Type, Union

import numpy as np
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations

from generation.particles import (
    Clay,
    Illite,
    Kaolinite,
    Montmorillonite,
    Quartz,
    Sand,
    Wall,
)

logging.getLogger().setLevel(logging.INFO)


class Container(object):
    """create the container in which the simulation for different tests
    takes place

    Class Attributes:
        type_reference (Dict): dictionary used to relate the given
            particle type in string to its corresponding class

    Methods:
        _validate_info: validate the given particle_info array to
            initialize the container
        _make_boxes: calculate the length and width for boxes in
            different particle size hierarchies
        generate: generate all the particle with the given information
            on their type, size and quantity in the particle_info array
        _add_particle: adds one particle to the self.particles array
        _single_particle_contact_check: checks wether if the given
            particle is in contact with any other particle; in the
            generation phase returns True if it hits only one particle
            while in the middle of the simulation updates the
            self.contacts array with all the contacting particles
        update_contact_list: clears and refills the self.cantacts array
            and also self.boxes dictionary
        touching_boxes: calculates the boxes in touch with the given
            particle in a specific size hierarchy and returns the number
            of those boxes in an array
    """

    type_reference = {
        "kaolinite": Kaolinite,
        "montmorillonite": Montmorillonite,
        "illite": Illite,
        "quartz": Quartz,
    }
    valid_simulation_types = ["TT", "DS", "SS"]
    temprature: int = (
        293  # in Kelvin; According to M.Khabazian and A.Mirghasemi, 2018
    )
    gravitational_acceleration = 9.81
    clay_clay_contact_stiffness = 1
    sand_clay_contact_stiffness = 1
    sand_sand_contact_stiffness = 1
    sand_wall_contact_stiffness = 1
    clay_wall_contact_stiffness = 1
    strain_rate = 1

    def __init__(
        self,
        length: float,
        width: float,
        particles_info: List[Dict],
        simulation_type: str,
        time_step: float,
        fluid_characteristics: Dict,
    ) -> None:
        """initialize the Container instance

        Args:
            length (float): the length of the container instance
            width (float): the width of the container instance
            particles_info (List[Dict]): the information associated to the
                particles to be generated in the container in an array
                in which every element is a dictionary in which the
                keys "type, size_upper_bound, size_lower_bound, and
                quantity" have to be present;
            simulation_type (str): the type of simulation to be run on
                the container; it should be either of these options:
                    TT: for triaxial test
                    DS: for direct shear test
                    SS: for simple shear test

        Other Attributes:
            number_of_groups (int): the number of categories of
                particles which is basically the length of the given
                particles_info array
            contacts (Type[defaultdict]): a dictionary in which keys
                are the generated particles in the container and values
                are lists that hold tuples in which the first element
                is the particle in contact with the key particle and
                the second element is itself a tuple containing the
                geometrical entities representing the location of the
                contact
            particles (List): an array containing all the particles in
                the container
            boxes (Dict): a dictionary in which each key represents a
                size hierarchy and holds a dictionary with the number
                of boxes in the corresponding hierarchy as keys and a
                list containing the particles in touch with that box
            box_width (List): an array containing the whith of boxes in
                the corresponding size hierarchy
            box_length (List): an array containing the legth of boxes in
                the corresponding size hierarchy
            nr (List): an array containing the number of rows in each
                corresponding size hierarchy
            nc (List): an array containing the number of columns in each
                corresponding size hierarchy

        Raises:
            RuntimeError: when the given particles_info array is invalid
        """

        # miscellaneous stuff
        if not simulation_type.upper() in self.valid_simulation_types:
            raise RuntimeError(
                'invalid input for the simulation type; should be either of "TT", "DS", or "SS"'
            )
        self.simulation_type = simulation_type.upper()
        self.time_step = time_step
        self.time = 0
        self.fluid_characteristics = (
            fluid_characteristics  # do some validations here later
        )

        # stuff about container's geometry
        if length <= 0 or width <= 0:
            raise RuntimeError(
                "the given length and width of the container should be a positive number"
            )
        self.length = length
        self.width = width
        self.walls: List = self.setup_walls()

        # stuff about particles
        if not (self._validate_info(particles_info) is True):
            message = self._validate_info(particles_info)
            raise RuntimeError("invalid input for particles_info; " + message)
        particles_info = sorted(
            particles_info, key=lambda x: x["size_upper_bound"], reverse=True
        )
        self.particles_info = particles_info
        self.number_of_groups: int = len(particles_info)
        self.number_of_clay_groups = len(
            [di for di in self.particles_info if di["type"] != "quartz"]
        )
        self.particles: List = []

        # stuff about contacts
        self.mechanical_contacts: Type[defaultdict] = defaultdict(list)
        self.chemical_contacts: Type[defaultdict] = defaultdict(list)
        self.wall_contacts: List = []
        self.box_width, self.box_length = self._make_boxes()
        self.number_of_rows: List = [self.width // w for w in self.box_width]
        self.number_of_columns: List = [
            self.length // l for l in self.box_length
        ]
        self.mechanical_boxes: List[Dict] = [
            defaultdict(list) for i in range(self.number_of_groups)
        ]
        self.chemical_boxes: Dict = defaultdict(list)

        # stuff about generation phase
        big_box_numbers = [
            i
            for i in range(self.number_of_rows[0] * self.number_of_columns[0])
        ]
        random.shuffle(big_box_numbers)
        self.generation_boxes = {k: 0 for k in big_box_numbers}

    def _validate_info(self, info: List[Dict]) -> bool:
        """validate the array passed in as the particles info

        Args:
            info (list): the particles_info array passed in when
                instantiating

        Returns:
            (bool): True or False indicating the validity of the passed
                in particles_info array
        """

        essential_attributes = [
            "type",
            "size_upper_bound",
            "size_lower_bound",
            "quantity",
        ]
        valid_types = list(self.type_reference.keys())
        if not isinstance(info, list):
            return "the given input should be a list"
        for d in info:
            if not isinstance(d, dict):
                return "the items of the list should be dictionaries"
            for att in essential_attributes:
                if not att in d.keys():
                    return "some of the essential attributes of the particle info are missing"
            if not d["type"] in valid_types:
                return "the given particle type is invalid"
            if d["size_lower_bound"] > d["size_upper_bound"]:
                return "the given lower bound should be smaller than the upper bound"
            if (
                d["size_lower_bound"] < 0
                or d["size_upper_bound"] < 0
                or d["quantity"] < 0
            ):
                return "the given values for lower and upper bound and quantity should be positive numbers"
            if (
                d["size_upper_bound"] > self.length
                or d["size_upper_bound"] > self.width
            ):
                return "the given upper bound for particle size should be smaller than container's dimensions"
        return True

    def setup_walls(self) -> List[Type[Wall]]:
        """sets up the boundaries of the container as the Wall instances

        Returns:
            List[Type[Wall]]: Wall instances as the boundaries of the container
        """

        if self.simulation_type == "TT":
            wall1 = Wall.from_ends(
                x1=0, y1=0, x2=0, y2=self.width, is_fixed=True
            )
            wall2 = Wall.from_ends(
                x1=0,
                y1=self.width,
                x2=self.length,
                y2=self.width,
                is_fixed=False,
            )
            wall3 = Wall.from_ends(
                x1=self.length,
                y1=self.width,
                x2=self.length,
                y2=0,
                is_fixed=True,
            )
            wall4 = Wall.from_ends(
                x1=self.length, y1=0, x2=0, y2=0, is_fixed=True
            )
            return [wall1, wall2, wall3, wall4]

    def _make_boxes(self) -> Tuple[List, List]:
        """calculate the width and length for the boxes corresponding
        to each particle size range (a.k.a hierarchy)

        Returns:
            list: list containing appropriate width and length for
                boxes in each particle size range
        """

        length, width = [], []
        reference_width, reference_length = self.width, self.length
        for i, d in enumerate(self.particles_info):
            if i != 0:
                reference_width, reference_length = width[-1], length[-1]
            length.append(d["size_upper_bound"])
            width.append(d["size_upper_bound"])
            while reference_width % width[-1] != 0:
                width[-1] += 1
            while reference_length % length[-1] != 0:
                length[-1] += 1
        for w in width:
            if self.width // w <= 2:
                raise RuntimeError(
                    "the given dimensions and sizes are not suitable to generate a proper grid system"
                )
        for l in length:
            if self.length // l <= 2:
                raise RuntimeError(
                    "the given dimensions and sizes are not suitable to generate a proper grid system"
                )
        return width, length

    def update_mechanical_boxes(self):
        """updates the 'self.mechanical_boxes' attribute; this is
        usually done after each update in particles' position
        """

        res = [defaultdict(list) for _ in range(self.number_of_groups)]
        for particle in self.particles:
            h = particle.hierarchy
            nb = particle.box_num(
                self.number_of_columns[h],
                self.box_length[h],
                self.box_width[h],
            )
            for box in self.touching_boxes(particle.shape, h, nb):
                res[h][box].append(particle)
        self.mechanical_boxes = res

    def update_chemical_boxes(self):
        """updates the 'self.chemical_boxes' attribute; this is
        usually done after each update in particles' position
        """

        res = defaultdict(list)
        for i in range(len(self.particles_info)):
            if self.particles_info[i]["type"] == "kaolinite":
                index = i
                break
        else:
            return
        for particle in self.particles:
            if not isinstance(particle, Clay):
                continue
            nb = particle.box_num(
                self.number_of_columns[index],
                self.box_length[index],
                self.box_width[index],
            )
            for box in self.touching_boxes(
                particle.midline.circumcircle, index, nb
            ):
                res[box].append(particle)
        self.chemical_boxes = res

    def generate_particles(self) -> None:
        """generate the list of particles in-place regarding the given
        particles_info array of the Container class
        """

        total_quantity = sum(d["quantity"] for d in self.particles_info)
        index = 0
        while len(self.particles) < total_quantity:
            self._add_particle(index)
            if len(self.particles) == sum(
                self.particles_info[i]["quantity"] for i in range(index + 1)
            ):
                index += 1

    def _add_particle(self, index: int) -> None:
        """private method to add one new particle to the self.particles
        array

        Args:
            index (int): the index which points to the appropriate set
                of particles in the self.particles_info array

        Raises:
            RuntimeError: raises when the container is too dense and
                generation of a new particle sounds impossible
        """

        particle_type = self.type_reference[self.particles_info[index]["type"]]
        trials = 0
        while True:
            if trials > 100:
                raise RuntimeError("the container is too dense")
            # x, y, inc = self.generate_random_location()
            x = random.uniform(0, self.length)
            y = random.uniform(0, self.width)
            inc = random.uniform(0, np.math.pi)
            new_particle = particle_type(
                x=x,
                y=y,
                length=random.uniform(
                    self.particles_info[index]["size_lower_bound"],
                    self.particles_info[index]["size_upper_bound"],
                ),
                thickness=2,
                inclination=inc,
                hierarchy=index,
            )
            if self.single_particle_mechanical_contact_check(
                new_particle
            ) or self.particle_wall_contact_check(new_particle.shape):
                del new_particle
                trials += 1
            else:
                self.particles.append(new_particle)
                h = new_particle.hierarchy
                nb = new_particle.box_num(
                    self.number_of_columns[h],
                    self.box_length[h],
                    self.box_width[h],
                )
                for box in self.touching_boxes(new_particle.shape, h, nb):
                    self.mechanical_boxes[index][box].append(new_particle)
                self.reduce_generation_chance(new_particle)
                return

    def reduce_generation_chance(self, particle):
        """reduces the generation chance of a new particle inside boxes
        in which the given particle is located by changing the values
        of the 'generation_boxes' dictionary and then sorting that
        dictionary
        """

        if isinstance(particle, Clay):
            shape = shapes.Rectangle.from_diagonal(particle.midline)
        elif isinstance(particle, Sand):
            circle = particle.shape
            v1 = shapes.Point(
                circle.center.x - circle.radius,
                circle.center.y - circle.radius,
            )
            v2 = shapes.Point(
                circle.center.x + circle.radius,
                circle.center.y - circle.radius,
            )
            v3 = shapes.Point(
                circle.center.x + circle.radius,
                circle.center.y + circle.radius,
            )
            v4 = shapes.Point(
                circle.center.x - circle.radius,
                circle.center.y + circle.radius,
            )
            shape = shapes.Rectangle(v1, v2, v3, v4)
        nb = particle.box_num(
            self.number_of_columns[0], self.box_length[0], self.box_width[0]
        )
        for box in self.touching_boxes(shape, 0, nb):
            x0 = (box % self.number_of_columns[0]) * self.box_length[0]
            y0 = (box // self.number_of_columns[0]) * self.box_width[0]
            v1 = shapes.Point(x0, y0)
            v2 = shapes.Point(x0 + self.box_length[0], y0)
            v3 = shapes.Point(x0 + self.box_length[0], y0 + self.box_width[0])
            v4 = shapes.Point(x0, y0 + self.box_width[0])
            rec = shapes.Rectangle(v1, v2, v3, v4)
            ratio = (operations.intersection_area(shape, rec)) / (rec.area)
            self.generation_boxes[box] += ratio
        li = list(self.generation_boxes.items())
        self.generation_boxes = {
            k: v for k, v in sorted(li, key=lambda x: x[1])
        }

    def generate_random_location(self):
        """generates random values for 'x' and 'y' coordinates and the
        inclination of a new particle based on the 'generation_boxes'
        dictionary
        """

        box = list(self.generation_boxes.keys())[0]
        x0 = (box % self.number_of_columns[0]) * self.box_length[0]
        y0 = (box // self.number_of_columns[0]) * self.box_width[0]
        x1 = x0 + self.box_length[0]
        y1 = y0 + self.box_width[0]
        x = random.uniform(x0, x1)
        y = random.uniform(y0, y1)
        inc = random.uniform(0, np.math.pi)
        return x, y, inc

    def particle_wall_contact_check(self, particle_shape) -> bool:
        """checks if the given particle is in contact with any of the
        boundary walls; it is only used in generation phase, so the
        additional distance of the particles from the wall in this
        phase is also considered here

        Args:
            particle (Type[Union[Kaolinite, Montmorillonite, Quartz, Illite]]):
                the given particle
            hierarchy (int): the hierarchy of the given particle according
                to its size

        Returns:
            bool: True or False indicating the contacting situation between
                the given particle and any of the boundaries
        """

        for wall in self.walls:
            if operations.intersection(particle_shape, wall.shape):
                return True
        return False

    def single_particle_mechanical_contact_check(
        self,
        particle: Union[
            Type[Kaolinite], Type[Montmorillonite], Type[Quartz], Type[Illite]
        ],
    ) -> bool:
        """checking if the given particle is in contact with any other
            particle; it only returns True or False; the aim here is
            not to quantify the contact; this method only checks
            contacts with particles with the same or lower hierarchy
            since in the generation phase bigger particles are produced
            first

        Args:
            particle: the given particle to check if it's in contact
                with any other particle

        Returns:
            bool: True of False indicating the contacting situation of
                the given particle
        """

        h = particle.hierarchy
        for i in range(0, h + 1):
            nb = particle.box_num(
                self.number_of_columns[i],
                self.box_length[i],
                self.box_width[i],
            )
            for box in self.touching_boxes(particle.shape, i, nb):
                for particle2 in self.mechanical_boxes[i][box]:
                    if (
                        operations.intersection(
                            particle.shape, particle2.shape
                        )
                        or operations.is_inside(
                            particle.shape, particle2.shape
                        )
                        or operations.is_inside(
                            particle2.shape, particle.shape
                        )
                    ):
                        if particle.num != particle2.num:
                            return True
        return False

    def update_mechanical_contacts_dictionary(self) -> None:
        """updates the 'self.mechanical_contacts' dictionary; note that
        the "mechanical_boxes" and "mechanical_boxes_reversed" arrays
        should be updated before calling this method
        """

        res = defaultdict(list)
        for particle in self.particles:
            h = particle.hierarchy
            for i in range(0, h + 1):
                nb = particle.box_num(
                    self.number_of_columns[i],
                    self.box_length[i],
                    self.box_width[i],
                )
                for box in self.touching_boxes(particle.shape, i, nb):
                    for particle2 in self.mechanical_boxes[i][box]:
                        if (
                            operations.intersection(
                                particle.shape, particle2.shape
                            )
                            or operations.is_inside(
                                particle.shape, particle2.shape
                            )
                            or operations.is_inside(
                                particle2.shape, particle.shape
                            )
                        ) and particle2 != particle:
                            if not (particle2 in res[particle]):
                                res[particle].append(particle2)
                            if not (particle in res[particle2]):
                                res[particle2].append(particle)
        self.mechanical_contacts = res

    def update_chemical_contacts_dictionary(self) -> None:
        """updates the 'self.chemical_contacts' dictionary"""

        res = defaultdict(list)
        for i in range(len(self.particles_info)):
            if self.particles_info[i]["type"] == "kaolinite":
                index = i
                break
        else:
            return
        for particle in self.particles:
            if not isinstance(particle, Clay):
                continue
            nb = particle.box_num(
                self.number_of_columns[index],
                self.box_length[index],
                self.box_width[index],
            )
            for box in self.touching_boxes(
                particle.midline.circumcircle, index, nb
            ):
                for particle2 in self.chemical_boxes[box]:
                    if (
                        (
                            operations.intersection(
                                particle.midline.circumcircle,
                                particle2.midline.circumcircle,
                            )
                            or operations.is_inside(
                                particle.midline.circumcircle,
                                particle2.midline.circumcircle,
                            )
                            or operations.is_inside(
                                particle2.midline.circumcircle,
                                particle.midline.circumcircle,
                            )
                        )
                        and particle != particle2
                        and not (particle2 in res[particle])
                    ):
                        res[particle].append(particle2)
        self.chemical_contacts = res

    def update_wall_contacts_list(self):
        """updates the 'self.wall_contacts' list; note that the
        "mechanical_boxes" should be already updated
        """

        res = []
        for i in range(self.number_of_groups):
            nc = self.number_of_columns[i]
            nr = self.number_of_rows[i]
            # lower wall
            for box in range(0, nc, 1):
                for particle in self.mechanical_boxes[i][box]:
                    if (
                        particle.hierarchy == i
                        and operations.intersection(
                            particle.shape, self.walls[3].shape
                        )
                        and not (particle in res)
                    ):
                        res.append(particle)
            # left wall
            for box in range(0, nc * nr, nc):
                for particle in self.mechanical_boxes[i][box]:
                    if (
                        particle.hierarchy == i
                        and operations.intersection(
                            particle.shape, self.walls[0].shape
                        )
                        and not (particle in res)
                    ):
                        res.append(particle)
            # upper wall
            for box in range(nc * (nr - 1), nc * nr, 1):
                for particle in self.mechanical_boxes[i][box]:
                    if (
                        particle.hierarchy == i
                        and operations.intersection(
                            particle.shape, self.walls[1].shape
                        )
                        and not (particle in res)
                    ):
                        res.append(particle)
            # right wall
            for box in range(nc - 1, nc * nr, nc):
                for particle in self.mechanical_boxes[i][box]:
                    if (
                        particle.hierarchy == i
                        and operations.intersection(
                            particle.shape, self.walls[2].shape
                        )
                        and not (particle in res)
                    ):
                        res.append(particle)
        self.wall_contacts = res

    def touching_boxes(
        self,
        particle_shape: Type[
            Union[shapes.LineSegment, shapes.Rectangle, shapes.Circle]
        ],
        index: int,
        nb: int,
    ) -> List:
        """finds the boxes in touch with the given particle in the
        specified size hierarchy

        Args:
            particle (Particle): the particle for which to calculate
                the boxes in contact with
            index (int): the size hieratchy
            nb (int): number of the box inside which the particle's
                center is located

        Returns:
            list: an array containing the number of boxes in touch
                with the given particle in the specified hierarchy
        """

        res = []
        row = nb // self.number_of_columns[index]
        column = nb % self.number_of_rows[index]

        # lower box
        if row > 0:
            corner1 = shapes.Point(
                (column * self.box_length[index]),
                (row * self.box_width[index]),
            )
            corner2 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                (row * self.box_width[index]),
            )
            corner4 = shapes.Point(
                (column * self.box_length[index]),
                ((row - 1) * self.box_width[index]),
            )
            corner3 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row - 1) * self.box_width[index]),
            )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle_shape, box):
                res.append(nb - self.number_of_columns[index])

        # upper box
        if row < (self.number_of_rows[index] - 1):
            corner1 = shapes.Point(
                (column * self.box_length[index]),
                ((row + 1) * self.box_width[index]),
            )
            corner2 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row + 1) * self.box_width[index]),
            )
            corner3 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row + 2) * self.box_width[index]),
            )
            corner4 = shapes.Point(
                (column * self.box_length[index]),
                ((row + 2) * self.box_width[index]),
            )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle_shape, box):
                res.append(nb + self.number_of_columns[index])

        # left box
        if column > 0:
            corner1 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                (row * self.box_width[index]),
            )
            corner2 = shapes.Point(
                (column * self.box_length[index]),
                (row * self.box_width[index]),
            )
            corner3 = shapes.Point(
                (column * self.box_length[index]),
                ((row + 1) * self.box_width[index]),
            )
            corner4 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                ((row + 1) * self.box_width[index]),
            )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle_shape, box):
                res.append(nb - 1)

        # right box
        if column < (self.number_of_columns[index] - 1):
            corner1 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                (row * self.box_width[index]),
            )
            corner2 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                (row * self.box_width[index]),
            )
            corner3 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                ((row + 1) * self.box_width[index]),
            )
            corner4 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row + 1) * self.box_width[index]),
            )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle_shape, box):
                res.append(nb + 1)

        # upper left box
        if row < (self.number_of_rows[index] - 1) and column > 0:
            corner1 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                ((row + 1) * self.box_width[index]),
            )
            corner2 = shapes.Point(
                (column * self.box_length[index]),
                ((row + 1) * self.box_width[index]),
            )
            corner3 = shapes.Point(
                (column * self.box_length[index]),
                ((row + 2) * self.box_width[index]),
            )
            corner4 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                ((row + 2) * self.box_width[index]),
            )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle_shape, box):
                res.append(nb + self.number_of_columns[index] - 1)

        # upper right box
        if row < (self.number_of_rows[index] - 1) and column < (
            self.number_of_columns[index] - 1
        ):
            corner1 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row + 1) * self.box_width[index]),
            )
            corner2 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                ((row + 1) * self.box_width[index]),
            )
            corner3 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                ((row + 2) * self.box_width[index]),
            )
            corner4 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row + 2) * self.box_width[index]),
            )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle_shape, box):
                res.append(nb + self.number_of_columns[index] + 1)

        # lower left box
        if column > 0 and row > 0:
            corner1 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                ((row - 1) * self.box_width[index]),
            )
            corner2 = shapes.Point(
                (column * self.box_length[index]),
                ((row - 1) * self.box_width[index]),
            )
            corner3 = shapes.Point(
                (column * self.box_length[index]),
                (row * self.box_width[index]),
            )
            corner4 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                (row * self.box_width[index]),
            )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle_shape, box):
                res.append(nb - self.number_of_columns[index] - 1)

        # lower right box
        if row > 0 and column < (self.number_of_columns[index] - 1):
            corner1 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row - 1) * self.box_width[index]),
            )
            corner2 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                ((row - 1) * self.box_width[index]),
            )
            corner3 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                (row * self.box_width[index]),
            )
            corner4 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                (row * self.box_width[index]),
            )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle_shape, box):
                res.append(nb - self.number_of_columns[index] + 1)
        res.append(nb)
        return res

    def update_boundary_conditions(self, displacement: float) -> None:
        """updates the boundary conditions of the container object
        given the amount of displacement needs to be taken by the
        moving boundaries; the particle-wall contact forces will
        also be calculated here

        Args:
            displacement (float): the amount of displacement needs to
                be taken by the moving boundaries; for triaxial test
                (TT) it will be the delta_y movement of the upper
                boundary in nanometers, in direct shear test it will be
                the delta_x movement of the upper part of the container
                in nanometers, and in simple shear test it will be the
                delta_theta rotation of the left and right walls in
                radian
        """

        if self.simulation_type == "TT":
            for wall in self.walls:
                if not wall.is_fixed:
                    wall.move(delta_y=displacement)
        # do this for other simulation types too

    def wall_contact_forces(self, particle):
        """updates the force vector of any particle that is in contact
        with a boundary wall
        """

        if not (particle in self.wall_contacts):
            return (0, 0, 0)
        if isinstance(particle, Sand):
            res = [0, 0, 0]
            for wall in self.walls:
                inter = operations.intersection(particle.shape, wall.shape)
                if isinstance(inter, tuple):
                    line = shapes.LineSegment(*inter)
                    a1 = (
                        (line.length)
                        * (operations.distance(particle.shape.center, line))
                        * 0.5
                    )
                    angle = operations.angle_in_between(
                        shapes.LineSegment(inter[0], particle.shape.center),
                        shapes.LineSegment(inter[1], particle.shape.center),
                    )
                    a2 = (angle / (2 * np.math.pi)) * (particle.shape.area)
                    area = a2 - a1
                    F = area * (self.sand_wall_contact_stiffness)
                    if (
                        operations.standardized_inclination(wall.inclination)
                        == 0
                    ):
                        res[1] += F
                    else:
                        res[0] += F
            return tuple(res)
        if isinstance(particle, Clay):
            res = [0, 0, 0]
            for wall in self.walls:
                if intersection(particle.midline, wall.shape):
                    delta = operations.intersection_length(
                        particle.midline, wall.shape
                    )
                    F = delta * (self.clay_wall_contact_stiffness)
                    fx = F * np.cos(particle.midline.inclination)
                    fy = F * np.sin(particle.midline.inclination)
                    res[0] += fx
                    res[1] += fy
            return tuple(res)

    def mechanical_contact_forces(self, particle):
        """calculates machanical forces acting on the given particle
        and adds them to the particle's force vector components; the
        cases of mechanical forces between particle of the same type,
        particles of different types, forces between particles
        and boundaries are not covered here
        """

        # do sth about alignment of forces
        forces = [0, 0, 0]
        for particle2 in self.mechanical_contacts[particle]:
            if isinstance(particle, Sand) and isinstance(particle2, Clay):
                delta = operations.intersection_length(
                    particle2.midline, particle.shape
                )
                intersection_point = operations.intersection(
                    particle2.midline, particle.shape
                )
                radius_line = shapes.LineSegment(
                    intersection_point, particle.shape.center
                )
                theta = operations.angle_in_between(
                    particle2.midline, radius_line
                )
                gama = particle2.midline.inclination
                fn = (
                    (delta)
                    * (np.sin(theta))
                    * (self.sand_clay_contact_stiffness)
                )
                m = (fn) * (particle.shape.radius)
                fx = delta * np.cos(gama)
                fy = delta * np.sin(gama)
                forces = [forces[0] + fx, forces[1] + fy, forces[2] + m]
            elif isinstance(particle, Sand) and isinstance(particle2, Sand):
                area = operations.intersection_area(
                    particle.shape, particle2.shape
                )
                f = (area) * (self.clay_clay_contact_stiffness)
                intersection_points = operations.intersection(
                    particle.shape, particle2.shape
                )
                intersection_midline = shapes.LineSegment(
                    intersection_points[0], intersection_points[1]
                )
                gama = operations.standardized_inclination(
                    intersection_midline.inclination
                )
                fx = f * (np.cos(gama))
                fy = f * (np.sin(gama))
                m = 0  # doesn't really matter with circular shape
                forces = [forces[0] + fx, forces[1] + fy, forces[2] + m]
            elif isinstance(particle, Clay) and isinstance(particle2, Clay):
                delta = operations.intersection_length(
                    particle2.midline, particle.midline
                )
                F = delta * (self.clay_clay_contact_stiffness)
                fx = F * (np.cos(particle2.midline.inclination))
                fy = F * (np.sin(particle2.midline.inclination))
                r = operations.distance(
                    particle.midline.center,
                    operations.intersection(
                        particle2.midline, particle.midline
                    ),
                )
                theta = operations.angle_in_between(
                    particle2.midline, particle.midline
                )
                m = r * F * np.sin(theta)
                forces = [forces[0] + fx, forces[1] + fy, forces[2] + m]
            elif isinstance(particle, Clay) and isinstance(particle2, Sand):
                delta = operations.intersection_length(
                    particle.midline, particle2.shape
                )
                F = delta * (self.sand_clay_contact_stiffness)
                line = shapes.LineSegment(
                    particle2.shape.center,
                    operations.intersection(particle.midline, particle2.shape),
                )
                fx = F * np.cos(line.inclination)
                fy = F * np.sin(line.inclination)
                theta = operations.angle_in_between(particle.midline, line)
                r = operations.distance(
                    particle.midline.center,
                    operations.intersection(particle.midline, particle2.shape),
                )
                m = r * F * np.sin(theta)
                forces = [forces[0] + fx, forces[1] + fy, forces[2] + m]
        return forces

    def ddl_repulsion_forces(self, particle):
        """calculates ddl forces acting on the given particle and adds
        them to the particle's force vector components

        Args:
            particle (Particle): the particle to calculate the
                diffuse double layer forces acting upon
        """

        if not isinstance(particle, Clay):
            return (0, 0, 0)

        # constant parameters
        k = particle.Boltzman_constant
        t = self.temprature
        v = self.fluid_characteristics["cation_valance"]
        e = 1.38e23  # charge of an electron in J/K
        n = self.fluid_characteristics["cation_concentration"]
        epsilon = self.fluid_characteristics["dielectric_constant"]
        phi = particle.electric_potential

        # calculate 'D', 'd', and 'L' for each particle pair and calculating
        # the ddl for acitng on 'particle' for each one
        for particle2 in self.chemical_contacts[particle]:
            line1 = particle.midline.infinite()
            line2 = particle2.midline.infinite()
            bisec = operations.bisector(line1, line2)
            norm1 = operations.normal(particle.midline.end1, bisec)
            norm2 = operations.normal(particle.midline.end2, bisec)
            norm3 = operations.normal(particle2.midline.end1, bisec)
            norm4 = operations.normal(particle2.midline.end2, bisec)
            vertices = []
            for norm in [norm1, norm2, norm3, norm4]:
                if operations.intersection(
                    norm, particle.midline
                ) and operations.intersection(norm, particle2.midline):
                    vertices.append(
                        operations.intersection(norm, particle.midline)
                    )
                    vertices.append(
                        operations.intersection(norm, particle2.midline)
                    )
                    if len(vertices) == 4:
                        break
            vertices[2], vertices[3] = vertices[3], vertices[2]
            pol = shapes.Polygon(*vertices)

            # fixing ddl area for midiary particles
            for particle3 in self.chemical_contacts[particle]:
                if (particle2 != particle3) and operations.intersection(
                    particle3, pol
                ):
                    pass
            D = min(
                edge.length
                for edge in pol.edges
                if not (
                    (operations.intersection(edge.end1, line1))
                    ^ (operations.intersection(edge.end2, line2))
                )
            )
            d = D
            for edge in pol:
                if operations.intersection(
                    edge.end1, line1
                ) and operations.intersection(edge.end2, line1):
                    L = edge.length
                    break

            # calculating the ddl force for the pair
            K = np.sqrt(
                (8 * np.math.pi * n * (v ** 2) * (e ** 2)) / (epsilon * k * t)
            )
            z = (v * e * phi) / (k * t)
            u = 4 * np.log(
                (np.exp(z / 4) + 1 + (np.exp(z / 4) - 1) * exp(-1 * K * d))
                / (np.exp(z / 4) + 1 - (np.exp(z / 4) - 1) * exp(-1 * K * d))
            )
            P = 2 * n * k * t * (np.cosh(u) - 1)
            bl = 0.001 * phi ** 2.9 + 1.2
            al = 0.007 * phi ** 3.1 + (7e-7) * phi ** 7.7 - 0.3
            bf = -0.725 * (phi ** (-0.85)) * np.log(L) + 2.3 - 0.18 * phi
            af = 0.005 * (L ** 2.5) * (phi ** (-0.6 * np.log(L) + 3.1))
            Il = 1 / (1 + al ** bl)
            If = 1 / (1 + af ** bf)
            F = If * (P * np.exp(-1 * K * D))
            I = 0.5 * (Il) * (L * np.cos(2 * gama))
            angle = operations.angle_in_between(norm1, line1)
            inc = operations.standardized_inclination(norm1.inclination)
            M = F * np.sin(angle) * I
            Fx = F * np.cos(inc)
            Fy = F * np.sin(inc)

            return (Fx, Fy, M)

    def vdw_forces(self, particle):
        """calculates the van der valse forces acting on the given
        particle and adds them to the particle's force vector components

        Args:
            particle (Particle): the particle to calculate the
                van der waals forces acting upon
        """

        if not isinstance(particle, Clay):
            return (0, 0, 0)

        # calculating the vdv force for each pair
        for particle2 in self.chemical_contacts[particle]:
            A = particle.hammaker_constant
            W = particle.thickness
            c = 49.363  # in nanometer
            gama = 0.5 * operations.angle_in_between(
                particle.midline, particle2.midline
            )
            d1, d2 = 1, 1  # in nanometer
            L2 = particle2.length
            D = operations.distance(particle.midline, particle2.midline)
            x1 = D
            x2 = D + d1
            x3 = D + d1 + L2 * np.sin(0.5 * gama)
            x4 = D + L2 * np.sin(0.5 * gama)
            x5 = D + d1 + d2 * np.sin(0.5 * gama)
            x6 = D + d2 * np.sin(0.5 * gama)
            x7 = D + d2 * np.sin(0.5 * gama) + L2 * np.sin(0.5 * gama)
            x8 = D + d1 + d2 * np.sin(0.5 * gama) + L2 * np.sin(0.5 * gama)
            X = [x1, x2, x3, x4, x5, x6, x7, x8]
            F = (
                (A * W)
                / (6 * (np.math.pi) * (np.sin(2 * gama)))
                * sum(
                    ((-1) ** i)
                    * (
                        4 / (c * x)
                        - 1 / (x ** 2)
                        - (12 * ((x + c) ** 2) / (c ** 4))
                        * np.log((x + c) / x)
                    )
                    for i, x in enumerate(X)
                )
            )

            # adding the force to the particle in the proper alignment
            line1 = particle.midline.infinite()
            line2 = particle2.midline.infinite()
            bisec = operations.bisector(line1, line2)
            norm1 = operations.normal(particle.midline.end1, bisec)
            inc = operations.standardized_inclination(norm1.inclination)
            Fx = F * np.cos(inc)
            Fy = F * np.sin(inc)

            return (Fx, Fy, 0)

    def gravitational_forces(self, particle):
        """calculates the gravitational forces acting on the given
        particle and adds them to its force vector components

        Args:
            particle (Particle): the particle to calculate the
                gravitational forces acting upon
        """

        if not isinstance(particle, Sand):
            return (0, 0, 0)
        return (particle.mass * self.gravitational_acceleration, 0, 0)

    def update_particle_forces(self, particle):
        """updates the particle's force vector"""

        F1 = self.wall_contact_forces(particle)
        F2 = self.mechanical_contact_forces(
            particle
        )  # returns None, fix it !!!!!!
        F3 = self.ddl_repulsion_forces(particle)
        F4 = self.vdw_forces(particle)
        F5 = self.gravitational_forces(particle)
        particle.forces = tuple(
            [
                particle.forces[i] + F1[i] + F2[i] + F3[i] + F4[i] + F5[i]
                for i in range(3)
            ]
        )
        return

    def update_velocity(self, particle):
        """updates the velocity attribute for the given particle"""

        D1 = 0  # incomplete
        D2 = 0  # incomplete
        alpha = self.angular_damping_proportion_coefficient
        omega = self.angular_damping_resonance_coefficient
        Vx = (
            particle.velocity[0] * (1 - alpha * (self.time_step) / 2)
            + ((particle.forces[0] + D1) / (particle.mass)) * (self.time_step)
        ) / (1 + (alpha * (self.time_step)) / 2)
        Vy = (
            particle.velocity[1] * (1 - alpha * (self.time_step) / 2)
            + ((particle.forces[1] + D2) / (particle.mass)) * (self.time_step)
        ) / (1 + (alpha * (self.time_step)) / 2)
        Vm = (
            particle.velocity[2] * (1 - omega * alpha * (self.time_step) / 2)
            + ((particle.forces[2]) / (particle.moment_of_inertia))
            * (self.time_step)
        ) / (1 + (omega * alpha * (self.time_step)) / 2)
        particle.velocity = (Vx, Vy, Vm)
        return

    def update_locations(self, particle):
        """updates the boundary conditions and perform a relaxation
        phase; the "update_velocity" method should be called beforehand
        """

        x = particle.x + particle.velocity[0] * self.time_step
        y = particle.y + particle.velocity[1] * self.time_step
        inc = particle.inclination + particle.velocity[2] * self.time_step
        inc = operations.standardized_inclination(inc)
        particle.x = x
        particle.y = y
        particle.inclination = inc
        return

    def update(self):
        """updates the container state"""

        self.update_chemical_boxes()
        self.update_mechanical_boxes()
        self.update_mechanical_contacts_dictionary()
        self.update_chemical_contacts_dictionary()
        self.update_wall_contacts_list()

        for particle in self.particles:
            self.update_particle_forces(particle)
        for particle in self.particles:
            self.update_velocity(particle)
            self.update_locations(particle)
            particle.forces = (0, 0, 0)
        self.time += self.time_step

    @property
    def overal_stress(self):
        """calculates the overal stress between the particles in the
        container
        """

        overal_force = sum(particle.force[1] for particle in self.particles)
        return (overal_force) / self.length

    @property
    def overal_strain(self):
        """calculated the overal strain in the container"""

        if self.simulation_type == "TT":
            return (self.width - self.moving_wall.y) / (self.width)
        # do this also for other simulation types
        return 0

    @property
    def void_ratio(self):
        """calculates the void ratio of the whole container"""

        particle_area = sum(particle.shape.area for particle in self.particles)
        container_area = self.length * self.moving_wall.y
        return (container_area - particle_area) / particle_area
