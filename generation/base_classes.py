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

import multiprocessing
import random
import numpy as np
from collections import defaultdict
from typing import Tuple, List, Dict, Set, Type, Any, Union
from generation.exceptions import SizeOutOfBound
from functools import lru_cache
from geometry import two_dimensional_entities as shapes
from geometry import two_dimentional_operations as operations

class Particle(object):
    """Base class to create soil particles
    
    Methods
        box_num: calculates the number of box corresponding to 
            the particle, used in contact detection
        mass: caculates the mass of the Particle object using its
            density and its geometric shape
        moment_of_inertia: calculates the moment of inertia of the
            Particle instance
        move: relocates the Particle instance with the given differences
            in x and y coordinate and the amount of rotation it 
            experiences
    
    Class Attributes:
        last_num (int): the number to keep track of the last number
            associated to a particle
    """

    last_num: int = 0
    
    def __init__(
        self,
        x: float,
        y: float,
        inclination: float,
        hierarchy: int,
        velocity: Tuple[float, float, float] = (0, 0, 0),
        force: Tuple[float, float, float] = (0, 0, 0),
        num: int = 0,
        ) -> None:
        """initializing the Particle instance

        Args:
            x (float): x coordinate of the particle in nanometers
            y (float): y coordinate of the particle in nanometers
            inclination (float): the inclination of the particle in 
                radians, ranges from '0' to '2*pi'
            velocity (Tuple, optional): the velocity of the particle in 
                respect to x coordinate, and y coordinate in nanometers
                per second, and the rotational velocity in radians per
                second respectively. Defaults to (0, 0, 0).
            force (Tuple, optional): forces acting on the particle,
                with the first two elements being the force in x axis
                and the force in y axis respectively in Newtons, and
                the third element being the moment acting on the
                particle in Newton-metre. Defaults to (0, 0, 0).
            num (int): number of the particle
            hierarchy (int): the hierarchy of particle in the container
                due to its size in comparison to the size of other
                particles
        """
        
        self.x = x
        self.y = y
        self.inclination = inclination
        self.velocity = velocity
        self.force = force
        self.num = self.last_num
        self.hierarchy = hierarchy

    def __new__(cls, name: str, bases: Tuple, attrs: Dict) -> None:
        cls.last_num += 1
        super().__new__(cls, name, bases, attrs)
    
    def __del__(self) -> None:
        self.last_num -= 1
        super().__del__(self)
    
    def __hash__(self) -> int:
        return self.num
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__) and other.__hash__ == self.__hash__:
            return True
        return False

    @property
    def mass(self) -> float:
        """calculate the mass of the particel

        Returns:
            float: the mass of the particle in Newtons
        """

        return (self.shape.area) * (self.density)
    
    @property
    def moment_of_inertia(self) -> float:
        pass
    
    def box_num(self, nc: int, box_length: int, box_width: int) -> int:
        """calculate the number of box corresponding to the particle,
        used in contact detection

        Args:
            nc (int): number of columns used in meshing the container
            box_length (int): length of each box in the mesh
            box_width (int): width of each box in the mesh

        Returns:
            int: the number of box corresponing to the particle
        """
        
        return int(self.x / box_length) + int(self.y / box_width) * (nc)
    
    def move(self, delta_x: float, delta_y: float, delta_theta: float) -> None:
        """relocate the particle with the given displacements

        Args:
            delta_x (float): displacement in the x coordinate
            delta_y (float): displacement in the y coordinate
            delta_theta (float): angle of rotation in radians
        """
        
        self.x += delta_x
        self.y += delta_y
        self.inclination += delta_theta
        self.shape.move(delta_x, delta_y)
        self.shape.rotate(delta_theta)


class Clay(Particle):
    """Base class to create different clay particles upon

    Parents:
        Particle: the base class to create soil particles
        
    Methods:
        segmentalize: to be defined
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """initialize clay attributes
        
        Args:
            thickness (float): thickness of the particle
            length (float): length of the particle
            x (float): x coordinate of the particle in nanometers
            y (float): y coordinate of the particle in nanometers
            inclination (float): the inclination of the particle in 
                radians, ranges from '0' to '2*pi'
        
        Other Attributes:
            midpoint (Type[shapes.Point]): shapes.Point instance
                denoting the center of the particle
            midline (Type[shapes.LineSegment]): shapes.LineSegment
                instance denoting the longer axis of the Clay particle
            shape (Type[shapes.Rectangle]): the geometric representation
                of the Clay instance
            segments (List): an array containing the segments of the
                Clay instance to be used to model the flexibility of the
                particle
        
        Exceptions:
            RuntimeError (Exception): raises when the given thickness
                and length are outside the bounds specified as the
                class private attributes
        """
        
        if kwargs['thickness'] < self.width_bounds[0]:
            raise RuntimeError('the given thickness is lower than expected')
        elif kwargs['thickness'] > self.width_bounds[1]:
            raise RuntimeError('the given thickness is higher than expected')
        elif kwargs['length'] < self.length_bounds[0]:
            raise RuntimeError('the given length is lower than expected')
        elif kwargs['length'] > self.length_bounds[1]:
            raise RuntimeError('the given length is higher than expected')
        
        self.thickness = kwargs.pop('thickness')
        self.length = kwargs.pop('length')
        self.midpoint: Type[shapes.Point] = shapes.Point(self.x, self.y)
        self.midline: Type[shapes.LineSegment] = shapes.LineSegment.from_point_and_inclination(
            self.midpoint, self.inclination, self.length
            )
        self.shape: Type[shapes.Rectangle] = shapes.Rectangle.from_midline(
            self.midline, self.thickness
            )
        self.segments: List = self.segmentalize()
        super().__init__(*args, *kwargs)
    
    def segmentalize(self) -> List:
        """segmentalize the coresponding clay particles into 3 equal
        segments
        """
        
        particle_number = self.num
        size = self.length/3
        res = []
        for i, midpoint in enumerate(self.midline.navigator(0.166)):
            if i % 2 == 1:
                attrs = self.__dict__
                attrs['x'] = midpoint.x
                attrs['y'] = midpoint.y
                attrs['length'] = size
                name = f'Particle {particle_number}-{i%2}'
                new_particle = type(name, self.__bases__, attrs)
                new_particle.num = particle_number
                res.append(new_particle)
        self.last_num -= 3
        self.segments = res


class Sand(Particle):
    """Base class to create different sand particles upon

    Parents:
        Particle: the base class to create soil particles
    """

    def __init__(self, *args, **kwargs):
        """initialize clay attributes
        
        Args:
            diameter (float): the diameter of the sand particle
            x (float): x coordinate of the particle in nanometers
            y (float): y coordinate of the particle in nanometers
            inclination (float): the inclination of the particle in 
                radians, ranges from '0' to '2*pi', this is left unused
                if the shape of the partice is circular
        
        Exceptions:
            SizeOutOfBound (Exception): raises when the given diameter
                is outside the bounds specified as the class private
                attributes
        """

        super().__init__(*args, *kwargs)        
        if kwargs['length'] < self.diameter_bounds[0]:
            raise SizeOutOfBound('the given diameter is lower than expected')
        elif kwargs['length'] > self.diameter_bounds[1]:
            raise SizeOutOfBound('the given diameter is higher than expected')
        
        self.diameter = kwargs.pop('length')
        x, y = kwargs['x'], kwargs['y']
        self.shape = shapes.Circle(x, y, self.diameter)
# shift the super up everywhere

class Kaolinite(Clay):
    """Class to create montmorillonite particels
    
    Parents:
        Clay: the base class to create different clay particles upon,
            it includes the common methods and attributes shared among
            the clay particles
        Particle: the base class to create soil particles upon, it
            contains all the methods and attributes common among all
            the soil particles
    
    Class Attributes:
        length_bounds (Tuple(int, int)): upper and lower boundaries
            of the length of kaolinite particles as the first and
            second elements of the tuple respectively
        width_bounds (Tuple(int, int)): upper and lower boundaries of
            the thickness of kaolinite particles as the first and
            second elements of the tuple respectively
        cec (float): cation exchange capacity of the kaolinite particle
        ssa (float): special surface area of the kaolinite particle
        hamaker_constant (float): a constant defined for a van der-
            waals body-body interaction in Jules
        boltzman_constant (float): the proportionality factor that 
            relates the average relative kinetic energy of particles
            with the thermodynamic temrature, in Jules
        young_modulus (float): the young modulus assiciated with
            kaolinite particls in Newtons per nanometers square
        density (float): the density of kaolinite particles in grams
            per nanometer
        maximum_stiffness_coefficient (float): maximum stiffness
            coefficient of the kaolinite particle
        formula (str): general formula for kaolinite particles
    """
    
    length_bounds: Tuple(int, int) = (4000, 12000)
    width_bounds: Tuple(int, int) = (1, 3) # to be modified
    cec: float = 5
    ssa: float = 20
    hamaker_constant: float = 1e-19
    boltzman_constant: float = 1.38e-23
    young_modulus: float = 2e-8
    density: float = 2.65e-33
    maximum_stiffness_coefficient: float = 1.5e-7 # to be modified
    formula: str = 'Al2Si2O5(OH)4'
    
    def __init__(self, *args, **kwargs):
        """initialize the montmorillonite particle

        Args:
            thickness (float): thickness of the particle
            length (float): length of the particle
            x (float): x coordinate of the particle in nanometers
            y (float): y coordinate of the particle in nanometers
            inclination (float): the inclination of the particle in 
                radians, ranges from '0' to '2*pi'
        Exceptions:
            SizeOutOfBound (Exception): raises when the given thickness
                and length are outside the bounds specified as the
                class private attributes
        """
        
        kwargs['thickness'] = 2
        super().__init__(*args, **kwargs)
    
    def __repr__(self) -> str:
        return f'Kaolinite-{self.num}'


class Quartz(Sand):
    """Class to create quartz particles

    Parents:
        Sand: the base class to create sand particels
        Particle: the base class to create soil particles
    
    Class Attributes:
        diameter_bounds (Tuple(int, int)): upper and lower boundaries
            for diameter of quartz particles
        normal_contact_stiffness (float): normal contact stiffness of
            quartz particles in Newtons per nanometer
        shear_contact_stiffness (float): shear contact stiffness of
            quartz particles in Newtons per nanometer
        density (float): the density of quartz particles in grams per 
            nanometer
        friction_coefficient (float): the friction coefficient of
            quartz particels
        formula (str): the general formula of the quartz particles
    """

    diameter_bounds: Tuple(int, int) = ()
    normal_contact_stiffness: float = 2
    shear_contact_stiffness: float = 2
    density: float = 2.65e-33
    friction_ceofficient: float = 0.5
    formula: str = 'SiO2'
    
    def __init__(self, *args, **kwargs):
        """initialize the montmorillonite particle

        Args:
            length (float): the diameter of the sand particle
            x (float): x coordinate of the particle in nanometers
            y (float): y coordinate of the particle in nanometers
            inclination (float): the inclination of the particle in 
                radians, ranges from '0' to '2*pi', this is left unused
                if the shape of the partice is circular
        
        Exceptions:
            SizeOutOfBound (Exception): raises when the given diameter
                is outside the bounds specified as the class private
                attributes
        """
        
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f'Quartz-{self.num}'


class Montmorillonite(Clay):
    """Class to create montmorillonite particels

    Parents:
        Clay: the base class to create different clay particles upon,
            it includes the common methods and attributes shared among
            the clay particles
        Particle: the base class to create soil particles upon, it
            contains all the methods and attributes common among all
            the soil particles
    
    Class Attributes:
        length_bounds (Tuple(int, int)): upper and lower boundaries
            of the length of montmorillonite particles as the first and
            second elements of the tuple respectively
        width_bounds (Tuple(int, int)): upper and lower boundaries of
            the thickness of montmorillonite particles as the first and
            second elements of the tuple respectively
        cec (float): cation exchange capacity of the montmorillonite
            particle
        ssa (float): special surface area of the montmorillonite
            particle
        hamaker_constant (float): a constant defined for a van der-
            waals body-body interaction in Jules
        boltzman_constant (float): the proportionality factor that 
            relates the average relative kinetic energy of particles
            with the thermodynamic temrature, in Jules
        young_modulus (float): the young modulus assiciated with
            montmorillonite particls in Newtons per nanometers square
        density (float): the density of montmorillonite particles
        maximum_stiffness_coefficient (float): maximum stiffness
            coefficient of the montmorillonite particle
        formula (str): general formula for montmorillonite particles
    """
    
    length_bounds: Tuple[int, int] = (80, 220)
    width_bounds: Tuple(int, int) = (1, 3)
    cec: float = 100
    ssa: float = 800
    hamaker_constant: float = 8.7e-21
    boltzman_constant: float = 1.38e-23
    young_modulus: float = 2e-8
    density: float = 2.35e-33
    maximum_stiffness_coefficient: float = 1.5e-7
    formula: str = '(Na,Ca)0.33(Al,Mg)2(Si4O10)(OH)2·nH2O'

    def __init__(self, *args, **kwargs) -> None:
        """initialize the montmorillonite particle

        Args:
            thickness (float): thickness of the particle
            length (float): length of the particle
            x (float): x coordinate of the particle in nanometers
            y (float): y coordinate of the particle in nanometers
            inclination (float): the inclination of the particle in 
                radians, ranges from '0' to '2*pi'
        Exceptions:
            SizeOutOfBound (Exception): raises when the given thickness
                and length are outside the bounds specified as the
                class private attributes
        """
        
        kwargs['thickness'] = 2
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f'Montmorillonite-{self.num}'


class Illite(Clay):
    """Class to create illite particels

    Parents:
        Clay: the base class to create different clay particles upon,
            it includes the common methods and attributes shared among
            the clay particles
        Particle: the base class to create soil particles upon, it
            contains all the methods and attributes common among all
            the soil particles
    
    Class Attributes:
        length_bounds (Tuple(int, int)): upper and lower boundaries
            of the length of illite particles as the first and
            second elements of the tuple respectively
        width_bounds (Tuple(int, int)): upper and lower boundaries of
            the thickness of illite particles as the first and
            second elements of the tuple respectively
        cec (float): cation exchange capacity of the illite particle
        ssa (float): special surface area of the illite particle
        hamaker_constant (float): a constant defined for a van der-
            waals body-body interaction in Jules
        boltzman_constant (float): the proportionality factor that 
            relates the average relative kinetic energy of particles
            with the thermodynamic temrature, in Jules
        young_modulus (float): the young modulus assiciated with
            montmorillonite particls in Newtons per nanometers square
        density (float): the density of illite particles
        maximum_stiffness_coefficient (float): maximum stiffness
            coefficient of the illite particle
        formula (str): general formula for illite particles
    """
    
    length_bounds: Tuple[int, int] = (80, 220)
    width_bounds: Tuple(int, int) = (1, 3)
    cec: float = 100
    ssa: float = 800
    hamaker_constant: float = 8.7e-21
    boltzman_constant: float = 1.38e-23
    young_modulus: float = 2e-8
    density: float = 2.35e-33
    maximum_stiffness_coefficient: float = 1.5e-7
    formula: str = '(Na,Ca)0.33(Al,Mg)2(Si4O10)(OH)2·nH2O'

    def __init__(self, *args, **kwargs) -> None:
        """initialize the illite particle

        Args:
            thickness (float): thickness of the particle
            length (float): length of the particle
            x (float): x coordinate of the particle in nanometers
            y (float): y coordinate of the particle in nanometers
            inclination (float): the inclination of the particle in 
                radians, ranges from '0' to '2*pi'
        Exceptions:
            SizeOutOfBound (Exception): raises when the given thickness
                and length are outside the bounds specified as the
                class private attributes
        """
        
        kwargs['thickness'] = 2
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f'Montmorillonite-{self.num}'


class Wall(Particle):
    """create walls to be used is boundaries of the model

    Parents:
        Particle: the base class upon which to build all the
            particles in the model
    """

    density: float = 0    
    stiffness: float = 0
    
    def __init__(self, *args, **kwargs):
        """initializing the Wall instance
        
        Args:
            x (float): x coordinate of the particle in nanometers
            y (float): y coordinate of the particle in nanometers
            inclination (float): the inclination of the particle in 
                radians, ranges from '0' to '2*pi'
            velocity (Tuple, optional): the velocity of the particle in 
                respect to x coordinate, and y coordinate in nanometers
                per second, and the rotational velocity in radians per
                second respectively; Defaults to (0, 0, 0).
            force (Tuple, optional): forces acting on the particle,
                with the first two elements being the force in x axis
                and the force in y axis respectively in Newtons, and
                the third element being the moment acting on the
                particle in Newton-metre; Defaults to (0, 0, 0).
            num (int): number of the particle
            is_fixed (bool): specifying if the wall is fixed or is able
                to relocate
        """
        
        self.is_fixed = kwargs.pop('is_fixed')
        super().__init__(*args, **kwargs)
        

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
        'kaolinite' : Kaolinite,
        'montmorillonite' : Montmorillonite,
        'illite' : Illite,
        'quartz' : Quartz,
        }
    valid_simulation_types = ['TT', 'DS', 'SS']
    
    def __init__(
        self,
        length: float,
        width: float,
        particles_info: list(dict),
        simulation_type: 'str',
        ) -> None:
        """initialize the Container instance

        Args:
            length (float): the length of the container instance
            width (float): the width of the container instance
            particles_info (list): the information assiciated to the
                particles to be generated in the container in and array
                in which every element is a dictionary in which the
                keys "type, size_upper_bound, size_lower_bound,
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
        
        if not simulation_type.upper() in self.valid_simulation_types:
            raise RuntimeError('invalid input for the simulation type')
        self.simulation_type = simulation_type
        self.length = length
        self.width = width
        if not self._validate_info(particles_info):
            raise RuntimeError('invalid input as particles_info')
        particles_info = sorted(particles_info, key = lambda x: x['size_upper_bound'], reverse = True)
        self.particles_info = particles_info
        self.number_of_groups: int = len(particles_info)
        self.contacts: Type[defaultdict] = defaultdict(set)
        self.particles: List = []
        self.boxes: Dict = {i : defaultdict(list) for i in range(self.number_of_groups)}
        self.box_width, self.box_length = self._make_boxes()
        self.nr: List = [self.width // w for w in self.box_width]
        self.nc: List = [self.length // l for l in self.box_length]
    
    def _validate_info(self, info: List[Dict]) -> bool:
        """validate the array passed in as the particles info

        Args:
            info (list): the particles_info array passed in when
                instantiating
        
        Returns:
            (bool): True or False indicating the validity of the passed
                in particles_info array
        """
        
        essential_attributes = ['type', 'size_upper_bound',
                                'size_lower_bound', 'quantity',]
        valid_types = list(self.type_reference.keys())
        if not isinstance(info, list):
            return False
        for d in info:
            if not isinstance(d, dict):
                return False
            for att in essential_attributes:
                if not att in d.keys():
                    return False
            if not d['type'] in valid_types:
                return False
            if d['size_lower_bound'] > d['size_upper_bound']:
                return False
            if d['size_lower_bound'] < 0 or d['size_upper_bound'] < 0 or d['quantity'] < 0:
                return False
        return True
    
    def _make_boxes(self) -> Tuple[List, List]:
        """calculate the width and length for the boxes corresponding
        to each particle size range (a.k.a hierarchy)

        Returns:
            list: list containing appropriate width and length for
                boxes in each particle size range
        """
        
        length, width = [], []
        for i, d in enumerate(self.particles_info):
            if i == 0:
                length.append(d['size_upper_bound'])
                width.append(d['size_upper_bound'])
                while (self.width % width[-1] != 0):
                    width[-1] += 1
                while (self.lenght % length != 0):
                    length[-1] += 1
            else:
                width.append(width[-1] * (d['size_upper_bound'] // width[-1]
                                          + ((d['size_upper_bound'] / width[-1]) % 1 != 0)))
                nr = self.width / width[-2]
                while nr % (width[-1] / width[-2]) != 0:
                    width[-1] += width[-2]
                length.append(length[-1] * (d['size_upper_bound'] // length[-1]
                                          + ((d['size_upper_bound'] / length[-1]) % 1 != 0)))
                nr = self.length / length[-2]
                while nr % (length[-1] / length[-2]) != 0:
                    length[-1] += length[-2]
        return width, length
    
    def generate(self) -> None:
        """generate the list of particles in-place regarding the given
        particles_info array to the Container class
        """
        
        total_quantity = sum(d['quantity'] for d in self.particles_info)
        index = 0
        while len(self.particles) < total_quantity:
            self._add_particle(index)
            if len(self.particles) == sum(self.particles_info[i]['quantity'] for i in range(index + 1)):
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
        
        particle_type = self.type_reference(self.particles_info[index]['type'])
        trials = 0
        while True:
            if trials > 50:
                raise RuntimeError('the container is too dense')
            new_particle = particle_type(
                x = random.uniform(0, self.length),
                y = random.uniform(0, self.width),
                length = random.uniform(
                    self.particles_info[index]['size_lower_bound'],
                    self.particles_info[index]['size_upper_bound'],
                    ),
                inclination = random.uniform(0, 2*np.pi),
                hierarchy = index
            )
            if self._single_particle_contact_check(new_particle):
                del new_particle
                trials += 1
            else:
                self.particles.append(new_particle)
                for index in range(new_particle.hierarchy, self.number_of_groups):
                    for box in self.touching_boxes(new_particle, index):
                        self.boxes[index][box].append(new_particle)
                return
    
    def _single_particle_contact_check(
        self,
        particle: Type[Union[Kaolinite, Montmorillonite, Quartz, Illite]],
        generation_phase: bool = True
        ) -> bool:
        """checking if the given particle is in contact with any other
            particle

        Args:
            particle: the given particle to check if it's in contact
                with any other particle
            generation_phase (bool): specifying if the container is in
                the generation phase or not

        Returns:
            bool: True of False indicating the contacting situation of
                the given particle
        """

        for box in self.touching_boxes(particle, particle.hierarchy):
            for particle2 in self.boxes[particle.hierarchy][box]:
                contact = operations.intersection(particle.shape, particle2.shape)
                if contact:
                    if particle.num != particle2.num:
                        if not generation_phase:
                            self.contacts[particle].add[(particle2, contact)]
                            self.contacts[particle2].add[(particle, contact)]
                        else:
                            return True
        if not generation_phase:
            return
        return False
        
    def update_contact_list(self) -> None:
        """recreating the self.contacts dictionary
        """
        
        self.boxes = {i : defaultdict(list) for i in range(self.number_of_groups)}
        self.contacts = defaultdict(set)
        self.particles = sorted(self.particles, key = lambda x: x.hierarchy)
        for particle in self.particles:
            self._single_particle_contact_check(particle, generation_phase = False)
    
    def touching_boxes(
        self,
        particle: Type[Union[Kaolinite, Montmorillonite, Quartz, Illite]],
        index: int
        ) -> List:
        """finds the boxes in touch with the given particle in the
        specified size hierarchy

        Args:
            particle (Particle): the particle for which to calculate
                the boxes in contact with            
            index (int): the size hieratchy

        Returns:
            list: an array containing the number of boxes in touch
                with the given particle in the specified hierarchy
        """
        
        res = []
        row = particle.nb // self.nc[index]
        column = particle.nb % self.nr[index]
        
        # lower box
        if row > 0:
            corner1 = shapes.Point(
                (column * self.box_length[index]),
                (row * self.box_width[index])
                )
            corner2 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                (row * self.box_width[index])
                )
            corner3 = shapes.Point(
                (column * self.box_length[index]),
                ((row - 1) * self.box_width[index])
                )
            corner4 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row - 1) * self.box_width[index])
                )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle.shape, box):
                res.append(particle.nb - self.nc[index])

        # upper box
        if row < (self.nr[index] - 1):
            corner1 = shapes.Point(
                (column * self.box_length[index]),
                ((row + 1) * self.box_width[index])
                )
            corner2 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row + 1) * self.box_width[index])
                )
            corner3 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row + 2) * self.box_width[index])
                )
            corner4 = shapes.Point(
                (column * self.box_length[index]), 
                ((row + 2) * self.box_width[index])
                )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle.shape, box):
                res.append(particle.nb + self.nc[index])

        # left box
        if column > 0:
            corner1 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                (row * self.box_width[index])
                )
            corner2 = shapes.Point(
                (column * self.box_length[index]),
                (row * self.box_width[index])
                )
            corner3 = shapes.Point(
                (column * self.box_length[index]),
                ((row + 1) * self.box_width[index])
                )
            corner4 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                ((row + 1) * self.box_width[index])
                )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle.shape, box):
                res.append(particle.nb - 1)

        # right box
        if column < (self.nc[index] - 1):
            corner1 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                (row * self.box_width[index])
                )
            corner2 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                (row * self.box_width[index])
                )
            corner3 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                ((row + 1) * self.box_width[index])
                )
            corner4 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row + 1) * self.box_width[index])
                )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle.shape, box):
                res.append(particle.nb + 1)

        # upper left box
        if row < (self.nr[index] - 1) and column > 0:
            corner1 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                ((row + 1) * self.box_width[index])
                )
            corner2 = shapes.Point(
                (column * self.box_length[index]),
                ((row + 1) * self.box_width[index])
                )
            corner3 = shapes.Point(
                (column * self.box_length[index]),
                ((row + 2) * self.box_width[index])
                )
            corner4 = shapes.Point(
                ((column  - 1) * self.box_length[index]),
                ((row + 2) * self.box_width[index])
                )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle.shape, box):
                res.append(particle.nb + self.nc[index] - 1)

        # upper right box
        if row < (self.nr[index] - 1) and column < (self.nc[index] - 1):
            corner1 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row + 1) * self.box_width[index])
                )
            corner2 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                ((row + 1) * self.box_width[index])
                )
            corner3 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                ((row + 2) * self.box_width[index])
                )
            corner4 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row + 2) * self.box_width[index])
                )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle.shape, box):
                res.append(particle.nb + self.nc[index] + 1)

        # lower left box
        if column > 0 and row > 0:
            corner1 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                ((row - 1) * self.box_width[index])
                )
            corner2 = shapes.Point(
                (column * self.box_length[index]),
                ((row - 1) * self.box_width[index])
                )
            corner3 = shapes.Point(
                (column * self.box_length[index]),
                (row * self.box_width[index])
                )
            corner4 = shapes.Point(
                ((column - 1) * self.box_length[index]),
                (row * self.box_width[index])
                )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle.shape, box):
                res.append(particle.nb - self.nc[index] - 1)

        # lower right box
        if row > 0 and column < (self.nc[index] - 1):
            corner1 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row - 1) * self.box_width[index])
                )
            corner2 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                ((row - 1) * self.box_width[index])
                )
            corner3 = shapes.Point(
                ((column + 2) * self.box_length[index]),
                (row * self.box_width[index])
                )
            corner4 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                (row * self.box_width[index])
                )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle.shape, box):
                res.append(particle.nb - self.nc[index] + 1)

        return res
    
    def setup(self):
        """sets up the container; actions takes here are generating
        particles according the given info, generating the walls and
        setting up the boundary conditions and performing a relaxation
        phase
        """
        
        pass

    @property
    def overal_stress(self):
        """calculates the overal stress between the particles in the
        container
        """
        
        pass

    @property
    def overal_strain(self):
        """calculated the overal strain in the container
        """
        
        if self.simulation_type == 'TT':
            return (self.width - self.moving_wall.y) / (self.width)
        # do this also for other simulation types
        return 0

    def update(self, strain_rate):
        """updates the boundary conditions and perform a relaxation
        phase
        """
        
        pass
    
    def calculate_forces(self):
        """calculates forces acting on each particle
        """
        
        pass