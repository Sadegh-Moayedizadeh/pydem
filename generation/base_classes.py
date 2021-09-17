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

import sys
import multiprocessing
import random
import numpy as np
from collections import defaultdict
from typing import Tuple, List, Dict, Set, Type, Any, Union
from generation.exceptions import SizeOutOfBound
from functools import lru_cache
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations


def time_cache(method):
    cached_res = None
    last_time = None
    def wrapper(self):
        if (last_time is None) or (self.time != last_time):
            res = method(self)
            cached_res = res
            last_time = self.time
            return res
        else:
            return cached_res
    return wrapper


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
    
    def __init__(self, *args, **kwargs) -> None:
        """initializing the Particle instance

        Args (*required while instantiating):
            x (float): x coordinate of the particle in nanometers
            y (float): y coordinate of the particle in nanometers
            inclination (float): the inclination of the particle in 
                radians, ranges from '0' to '2*pi'
        
        Args (*not required; will be appointed by the class):
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

        self.x = kwargs['x']
        self.y = kwargs['y']
        self.inclination = operations.standardized_inclination(kwargs['inclination'])
        self.velocity = (0, 0, 0)
        self.force = (0, 0, 0)
        self.acceleration = (0, 0, 0)
        if 'is_segment' in kwargs.keys() and kwargs['is_segment']:
            self.num = Particle.last_num - 1
        else:
            self.num = Particle.last_num
            Particle.last_num += 1
        if 'hierarchy' in kwargs.keys():
            self.hierarchy = kwargs['hierarchy']
        else:
            self.hierarchy = None

    # def __new__(cls, name: str, bases: Tuple, attrs: Dict) -> None:
    #     cls.last_num += 1
    #     super().__new__(cls, name, bases, attrs)
    
    def __del__(self) -> None:
        Particle.last_num -= 1
    
    def __hash__(self) -> int:
        return int(self.num**2 + self.x**2 + self.y**2)
    
    def __eq__(self, other: Any) -> bool:
        if (
            isinstance(other, self.__class__)
            and other.__hash__ == self.__hash__ 
            and other.num == self.num):
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
        self.shape.move(delta_x, delta_y, delta_theta)


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
            is_segment (bool): specifies if the particle to be created
                is a segment of another particle or not; while
                instantiation it should be set to false; defaults to
                False
        
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
        
        if not 'is_segment' in kwargs.keys():
            kwargs['is_segment'] = False
        self.is_segment = kwargs['is_segment']
        try:
            if kwargs['thickness'] < self.width_bounds[0]:
                raise RuntimeError('the given thickness is lower than expected')
            elif kwargs['thickness'] > self.width_bounds[1]:
                raise RuntimeError('the given thickness is higher than expected')
            elif kwargs['length'] < self.length_bounds[0] and not self.is_segment:
                raise RuntimeError('the given length is lower than expected')
            elif kwargs['length'] > self.length_bounds[1] and not self.is_segment:
                raise RuntimeError('the given length is higher than expected')
        except AttributeError:
            pass
        self.thickness = kwargs.pop('thickness')
        self.length = kwargs.pop('length')
        super().__init__(*args, **kwargs)
        if not kwargs['is_segment']:
            self.segments: List = self.segmentalize()
    
    @property
    def shape(self):
        """the realistic 2D shape of the clay particle as a rectangle
        """
        
        return shapes.Rectangle.from_midline(self.midline, self.thickness/2)

    @property
    def midline(self):
        """the long line that represents the clay particle without a thickness
        """
        
        return shapes.LineSegment.from_point_and_inclination(self.midpoint, self.inclination, self.length)

    @property
    def midpoint(self):
        """the point at the middle of the particle
        """
        
        return shapes.Point(self.x, self.y)
    
    def segmentalize(self) -> List:
        """segmentalize the coresponding clay particles into 3 equal
        segments
        """
        
        particle_number = self.num
        size = self.length/3
        res = []
        for i, midpoint in enumerate(self.midline.navigator(1/6)):
            if i % 2 == 1:
                attrs = {k : v for k, v in self.__dict__.items()}
                attrs['x'] = midpoint.x
                attrs['y'] = midpoint.y
                attrs['length'] = size
                attrs['is_segment'] = True
                new_particle = self.__class__(**attrs)
                new_particle.num = particle_number
                res.append(new_particle)
        return res
    
    def reassemble_segments(self):
        """reassembles the segments of the particle
        """
        
        pass
    
    def move(self, delta_x: float = 0, delta_y: float = 0, delta_theta: float = 0):
        """moves the Clay particle by the given derivetives

        Args:
            delta_x (float, optional): the amount of particle's movement
                in the x coordinate; Defaults to 0.
            delta_y (float, optional): the amount of particle's movement
                in the y coordinate; Defaults to 0.
            delta_theta (float, optional): the amount of particle's
                roatation; Defaults to 0.
        """
        
        self.x += delta_x
        self.y += delta_y
        self.inclination = operations.standardized_inclination(self.inclination + delta_theta)
        self.shape.move(delta_x = delta_x, delta_y = delta_y, delta_theta = delta_theta)
        self.midline.move(delta_x = delta_x, delta_y = delta_y, delta_theta = delta_theta)
        self.midpoint.move(delta_x = delta_x, delta_y = delta_y)
    
    def __del__(self):
        if not self.is_segment:
            Particle.last_num -= 1

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
       
        try:
            if kwargs['length'] < self.diameter_bounds[0]:
                raise RuntimeError('the given diameter is lower than expected')
            elif kwargs['length'] > self.diameter_bounds[1]:
                raise RuntimeError('the given diameter is higher than expected')
        except AttributeError:
            pass
        self.length = kwargs.pop('length')
        x, y = kwargs['x'], kwargs['y']
        kwargs['inclination'] = 0
        self.shape = shapes.Circle(shapes.Point(x, y), self.length)
        super().__init__(*args, **kwargs)
    
    def move(self, delta_x: float = 0, delta_y: float = 0, delta_theta: float = 0):
        """moves the Sand particle by the given derivetives

        Args:
            delta_x (float, optional): the amount of particle's movement
                in the x coordinate; Defaults to 0.
            delta_y (float, optional): the amount of particle's movement
                in the y coordinate; Defaults to 0.
            delta_theta (float, optional): the amount of particle's
                roatation; Defaults to 0.
        """
        
        self.x += delta_x
        self.y += delta_y
        self.shape.move(delta_x, delta_y)


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
    
    length_bounds: Tuple[int, int] = (1000, 12000) # in nanometer; may change
    width_bounds: Tuple[int, int] = (1, 3) # in nanometer; may change
    cec: float = 5 # according to M.Khabazian and A.Mirghasemi, 2018
    ssa: float = 20 # in square meters per gram; ///
    hamaker_constant: float = 1e-19 # in Joule; ///
    boltzman_constant: float = 1.38e-23 # in Joule; ///
    young_modulus: float = 2e-8 # in Newton per square nanometer; ///
    shear_modulus: float = 8e-9 # in Newton per square nanometer; ///
    surface_tension: float = 0.075 # in Newton per meter; ///
    normal_stiffness: float = 3e-6 # in Newton per nanometer; ///
    shear_stiffness: float = 1.2e-6 # in Newton per nanometer; ///
    density: float = 2.7e-33 # in Newton second per nanometer to the power of four; ///
    formula: str = 'Al2Si2O5(OH)4' # according to 'sciencedirect.com/topics/chemical-engineering/kaolinite'
    
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
        
        super().__init__(*args, **kwargs)
    
    def __repr__(self) -> str:
        name = f'Kaolinite:: number {self.num}'
        return name if not self.is_segment else name + '-S' 


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

    diameter_bounds: Tuple[int, int] = (0, 1000000)
    normal_contact_stiffness: float = 2
    shear_contact_stiffness: float = 2
    density: float = 2.65e-33
    friction_ceofficient: float = 0.5
    formula: str = 'SiO2'
    
    def __init__(self, *args, **kwargs):
        """initialize the montmorillonite particle

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
        
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f'Quartz:: number {self.num}'


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
    width_bounds: Tuple[int, int] = (1, 3)
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
    width_bounds: Tuple[int, int] = (1, 3)
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
            length (float): the length of the wall
        """
        
        if 'is_fixed' not in kwargs.keys():
            kwargs['is_fixed'] = True
        self.is_fixed = kwargs.pop('is_fixed')
        if kwargs['length'] <= 0:
            raise RuntimeError(
                'the given length for the wall should be a positive number'
                )
        self.length = kwargs.pop('length')
        super().__init__(*args, **kwargs)
    
    @property
    def shape(self):
        """the geometrical shape of the Wall instance which is a line
        segment
        """
        
        return shapes.LineSegment.from_point_and_inclination(
            shapes.Point(self.x, self.y), self.inclination, self.length)
    
    @classmethod
    def from_ends(cls,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        is_fixed: bool = True,
    ) -> 'Wall':
        """alternative constructor to create a Wall instance from end
        points
        
        Args:
            x1 (float): the x coordinate of the wall's first end
            y1 (float): the y coordinate of the wall's first end
            x2 (float): the x coordinate of the wall's second end
            y2 (float): the y coordinate of the wall's second end
            is_fixed (bool): whether or not the wall is going to be
                motionless in the model
        
        Returns:
            Type[Wall]: the Wall instance
        """
        
        length = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        x =  (x1 + x2) / 2
        y = (y1 + y2) / 2
        if x1 == x2:
            inclination = np.math.pi / 2
        else:
            inclination = np.arctan((y2 - y1) / (x2 - x1))
        return Wall(x = x, y = y, inclination = inclination, length = length, is_fixed = is_fixed)
    
    def move(self, delta_x: float = 0, delta_y: float = 0, delta_theta: float = 0):
        """moves the wall with the given derivetives
        """

        self.x += delta_x
        self.y += delta_y
        self.inclination = operations.standardized_inclination(self.inclination + delta_theta)
    
    def __repr__(self):
        """string representation of the Wall object
        """
        return  f"Wall[inclination: {self.inclination}; center: ({self.x}, {self.y}); is_fixed: {self.is_fixed}]"

    def __eq__(self, other):
        if (
            isinstance(other, Wall)
            and abs(self.x - other.x) < 1e-10
            and abs(self.y - other.y) < 1e-10
            and abs(self.inclination - other.inclination) < 1e-10
            and self.is_fixed == other.is_fixed
        ):
            return True
        return False
    
    def __hash__(self) -> int:
        return int(self.x**2 + self.y**2)


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
    temprature: int = 293 # in Kelvin; According to M.Khabazian and A.Mirghasemi, 2018
    gravitational_acceleration = 9.81
    
    def __init__(
        self,
        length: float,
        width: float,
        particles_info: List[Dict],
        simulation_type: str,
        time_step: float,
        fluid_characteristics: Dict
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
        
        #miscellaneous stuff
        if not simulation_type.upper() in self.valid_simulation_types:
            raise RuntimeError(
                'invalid input for the simulation type; should be either of "TT", "DS", or "SS"'
                )
        self.simulation_type = simulation_type.upper()
        self.time_step = time_step
        self.time = 0
        self.fluid_characteristics = fluid_characteristics #do some validations here later
        
        #stuff about container's geometry
        if length <= 0 or width <= 0:
            raise RuntimeError(
                'the given length and width of the container should be a positive number'
                )
        self.length = length
        self.width = width
        self.walls: List = self.setup_walls()
        
        #stuff about particles
        if not (self._validate_info(particles_info) is True):
            message = self._validate_info(particles_info)
            raise RuntimeError(
                'invalid input for particles_info; ' + message
                )
        particles_info = sorted(
            particles_info, key = lambda x: x['size_upper_bound'], reverse = True
            )
        self.particles_info = particles_info
        self.number_of_groups: int = len(particles_info)
        self.number_of_clay_groups = len([di for di in self.particles_info if di['type'] != 'quartz'])
        self.particles: List = []
        
        #stuff about contacts
        self.mechanical_contacts: Type[defaultdict] = defaultdict(list)
        self.chemical_contacts: Type[defaultdict] = defaultdict(list)
        self.wall_contacts: List = []
        self.box_width, self.box_length = self._make_boxes()
        self.number_of_rows: List = [self.width // w for w in self.box_width]
        self.number_of_columns: List = [self.length // l for l in self.box_length]
        self.mechanical_boxes: List[Dict] = [defaultdict(list) for i in range(self.number_of_groups)]
        self.chemical_boxes: Dict = defaultdict(list)
        
        #stuff about generation phase
        big_box_numbers = [i for i in range(self.number_of_rows[0] * self.number_of_columns[0])]
        random.shuffle(big_box_numbers)
        self.generation_boxes = {k:0 for k in big_box_numbers}

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
            return "the given input should be a list"
        for d in info:
            if not isinstance(d, dict):
                return "the items of the list should be dictionaries"
            for att in essential_attributes:
                if not att in d.keys():
                    return "some of the essential attributes of the particle info are missing"
            if not d['type'] in valid_types:
                return "the given particle type is invalid"
            if d['size_lower_bound'] > d['size_upper_bound']:
                return "the given lower bound should be smaller than the upper bound"
            if d['size_lower_bound'] < 0 or d['size_upper_bound'] < 0 or d['quantity'] < 0:
                return "the given values for lower and upper bound and quantity should be positive numbers"
            if d['size_upper_bound'] > self.length or d['size_upper_bound'] > self.width:
                return "the given upper bound for particle size should be smaller than container's dimensions"
        return True
    
    def setup_walls(self) -> List[Type[Wall]]:
        """sets up the boundaries of the container as the Wall instances
        
        Returns:
            List[Type[Wall]]: Wall instances as the boundaries of the container
        """
        
        if self.simulation_type == 'TT':
            wall1 = Wall.from_ends(
                x1 = 0, y1 = 0, x2 = 0, y2 = self.width, is_fixed = True
                )
            wall2 = Wall.from_ends(
                x1 = 0, y1 = self.width, x2 = self.length, y2 = self.width, is_fixed = False
                )
            wall3 = Wall.from_ends(
                x1 = self.length, y1 = self.width, x2 = self.length, y2 = 0, is_fixed = True
                )
            wall4 = Wall.from_ends(
                x1 = self.length, y1 = 0, x2 = 0, y2 = 0, is_fixed = True
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
            length.append(d['size_upper_bound'])
            width.append(d['size_upper_bound'])
            while (reference_width % width[-1] != 0):
                width[-1] += 1
            while (reference_length % length[-1] != 0):
                length[-1] += 1
        for w in width:
            if self.width // w <= 2:
                raise RuntimeError(
                    'the given dimensions and sizes are not suitable to generate a proper grid system'
                    )
        for l in length:
            if self.length // l <= 2:
                raise RuntimeError(
                    'the given dimensions and sizes are not suitable to generate a proper grid system'
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
                self.box_width[h]
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
            if self.particles_info[i]['type'] == 'kaolinite':
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
                self.box_width[index]
                )
            for box in self.touching_boxes(particle.midline.circumcircle, index, nb):
                res[box].append(particle)
        self.chemical_boxes = res
    
    def generate_particles(self) -> None:
        """generate the list of particles in-place regarding the given
        particles_info array of the Container class
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
        
        particle_type = self.type_reference[self.particles_info[index]['type']]
        trials = 0
        while True:
            if trials > 50:
                raise RuntimeError('the container is too dense')
            x, y, inc = self.generate_random_location()
            new_particle = particle_type(
                x = x,
                y = y,
                length = random.uniform(
                    self.particles_info[index]['size_lower_bound'],
                    self.particles_info[index]['size_upper_bound'],
                    ),
                thickness = 2,
                inclination = inc,
                hierarchy = index
            )
            if (
                self.single_particle_mechanical_contact_check(new_particle)
                or self.particle_wall_contact_check(new_particle.shape)
            ):
                del new_particle
                trials += 1
            else:
                self.particles.append(new_particle)
                h = new_particle.hierarchy
                nb = new_particle.box_num(
                    self.number_of_columns[h], self.box_length[h], self.box_width[h]
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
            v1 = shapes.Point(circle.center.x - circle.radius, circle.center.y - circle.radius)
            v2 = shapes.Point(circle.center.x + circle.radius, circle.center.y - circle.radius)
            v3 = shapes.Point(circle.center.x + circle.radius, circle.center.y + circle.radius)
            v4 = shapes.Point(circle.center.x - circle.radius, circle.center.y + circle.radius)
            shape = shapes.Rectangle(v1, v2, v3, v4)
        nb = particle.box_num(self.number_of_columns[0], self.box_length[0], self.box_width[0])
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
        self.generation_boxes = {k:v for k, v in sorted(li, key = lambda x: x[1])}
    
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
    
    def particle_wall_contact_check(
        self,
        particle_shape
        ) -> bool:
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
        particle: Union[Type[Kaolinite], Type[Montmorillonite], Type[Quartz], Type[Illite]],
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
        for i in range(0, h+1):
            nb = particle.box_num(
                self.number_of_columns[i],
                self.box_length[i],
                self.box_width[i]
                )
            for box in self.touching_boxes(particle.shape, i, nb):
                for particle2 in self.mechanical_boxes[i][box]:
                    if (
                        operations.intersection(particle.shape, particle2.shape)
                        or operations.is_inside(particle.shape, particle2.shape)
                        or operations.is_inside(particle2.shape, particle.shape)
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
            for i in range(0, h+1):
                nb = particle.box_num(
                    self.number_of_columns[i],
                    self.box_length[i],
                    self.box_width[i]
                )
                for box in self.touching_boxes(particle.shape, i, nb):
                    for particle2 in self.mechanical_boxes[i][box]:
                        if (
                            (
                                operations.intersection(particle.shape, particle2.shape)
                                or operations.is_inside(particle.shape, particle2.shape)
                                or operations.is_inside(particle2.shape, particle.shape)
                            )
                            and particle2 != particle
                        ):
                            if not (particle2 in res[particle]):
                                res[particle].append(particle2)
                            if not (particle in res[particle2]):
                                res[particle2].append(particle)
        self.mechanical_contacts = res
    
    def update_chemical_contacts_dictionary(self) -> None:
        """updates the 'self.chemical_contacts' dictionary
        """
        
        res = defaultdict(list)
        for i in range(len(self.particles_info)):
            if self.particles_info[i]['type'] == 'kaolinite':
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
                self.box_width[index]
                )
            for box in self.touching_boxes(particle.midline.circumcircle, index, nb):
                for particle2 in self.chemical_boxes[box]:
                    if (
                        (operations.intersection(particle.midline.circumcircle, particle2.midline.circumcircle)
                        or operations.is_inside(particle.midline.circumcircle, particle2.midline.circumcircle)
                        or operations.is_inside(particle2.midline.circumcircle, particle.midline.circumcircle))
                        and particle != particle2
                        and not(particle2 in res[particle])
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
            #lower wall
            for box in range(0, nc, 1):
                for particle in self.mechanical_boxes[i][box]:
                    if(
                        particle.hierarchy == i
                        and operations.intersection(particle.shape, self.walls[3].shape)
                        and not (particle in res)
                        ):
                        res.append(particle)
            #left wall
            for box in range(0, nc*nr, nc):
                for particle in self.mechanical_boxes[i][box]:
                    if(
                        particle.hierarchy == i
                        and operations.intersection(particle.shape, self.walls[0].shape)
                        and not (particle in res)
                        ):
                        res.append(particle)
            #upper wall
            for box in range(nc*(nr-1), nc*nr, 1):
                for particle in self.mechanical_boxes[i][box]:
                    if(
                        particle.hierarchy == i
                        and operations.intersection(particle.shape, self.walls[1].shape)
                        and not (particle in res)
                        ):
                        res.append(particle)
            #right wall
            for box in range(nc-1, nc*nr, nc):
                for particle in self.mechanical_boxes[i][box]:
                    if(
                        particle.hierarchy == i
                        and operations.intersection(particle.shape, self.walls[2].shape)
                        and not (particle in res)
                        ):
                        res.append(particle)
        self.wall_contacts = res
    
    def touching_boxes(
        self,
        particle_shape: Type[Union[shapes.LineSegment, shapes.Rectangle, shapes.Circle]],
        index: int,
        nb: int
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
                (row * self.box_width[index])
                )
            corner2 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                (row * self.box_width[index])
                )
            corner4 = shapes.Point(
                (column * self.box_length[index]),
                ((row - 1) * self.box_width[index])
                )
            corner3 = shapes.Point(
                ((column + 1) * self.box_length[index]),
                ((row - 1) * self.box_width[index])
                )
            box = shapes.Rectangle(corner1, corner2, corner3, corner4)
            if operations.intersection(particle_shape, box):
                res.append(nb - self.number_of_columns[index])

        # upper box
        if row < (self.number_of_rows[index] - 1):
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
            if operations.intersection(particle_shape, box):
                res.append(nb + self.number_of_columns[index])

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
            if operations.intersection(particle_shape, box):
                res.append(nb - 1)

        # right box
        if column < (self.number_of_columns[index] - 1):
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
            if operations.intersection(particle_shape, box):
                res.append(nb + 1)

        # upper left box
        if row < (self.number_of_rows[index] - 1) and column > 0:
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
            if operations.intersection(particle_shape, box):
                res.append(nb + self.number_of_columns[index] - 1)

        # upper right box
        if row < (self.number_of_rows[index] - 1) and column < (self.number_of_columns[index] - 1):
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
            if operations.intersection(particle_shape, box):
                res.append(nb + self.number_of_columns[index] + 1)

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
            if operations.intersection(particle_shape, box):
                res.append(nb - self.number_of_columns[index] - 1)

        # lower right box
        if row > 0 and column < (self.number_of_columns[index] - 1):
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
            if operations.intersection(particle_shape, box):
                res.append(nb - self.number_of_columns[index] + 1)
        res.append(nb)
        return res
    
    def setup(self):
        """sets up the container; actions takes here are generating
        particles according the given info, generating the walls and
        setting up the boundary conditions and performing a relaxation
        phase
        """
        
        pass
    
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
        
        if self.simulation_type == 'TT':
            for wall in self.walls:
                if not wall.is_fixed:
                    wall.move(delta_y = displacement)
    
    def add_particle_wall_contact_forces(self):
        """updates the force vector of any particle that is in contact
        with a boundary wall
        """
        
        self.update_wall_contacts_list()
        for particla in self.wall_contacts:
            for wall in self.walls:
                pass
    
    def add_mechanical_forces(self, particle):
        """calculates machanical forces acting on the given particle
        and adds them to the particle's force vector components; the
        cases of mechanical forces between particle of the same type,
        particles of different types, forces between particles
        and boundaries are not covered here
        """
        
        pass
    
    def add_ddl_forces(self, particle):
        """calculates ddl forces acting on the given particle and adds
        them to the particle's force vector components
        """
        
        pass

    def add_vdv_forces(self, partice):
        """calculates the van der valse forces acting on the given
        particle and adds them to the particle's force vector components
        """

        pass
    
    def add_gravitational_forces(self, particle):
        """calculates the gravitational forces acting on the given
        particle and adds them to its force vector components
        """
        
        particle.force[1] += particle.mass * self.gravitational_acceleration
    
    def update_particle_forces(self, particle):
        """updates the particle's force vector
        """

        if isinstance(particle, Clay):
            self.add_mechanical_forces(particle)
            self.add_vdv_forces(particle)
            self.add_ddl_forces(particle)
        elif isinstance(particle, Sand):
            self.add_mechanical_forces(particle)
            self.add_gravitational_forces(particle)
    
    def update_locations(self, strain_rate):
        """updates the boundary conditions and perform a relaxation
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
    
    @property
    def void_ratio(self):
        """calculates the void ratio of the whole container
        """

        pass