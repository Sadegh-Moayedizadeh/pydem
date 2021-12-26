from typing import Any, Dict, List, Set, Tuple, Type, Union

import numpy as np
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations


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

        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.inclination = operations.standardized_inclination(
            kwargs["inclination"]
        )
        self.velocity = (0, 0, 0)
        self.forces = (0, 0, 0)
        self.acceleration = (0, 0, 0)
        if "is_segment" in kwargs.keys() and kwargs["is_segment"]:
            self.num = Particle.last_num - 1
        else:
            self.num = Particle.last_num
            Particle.last_num += 1
        if "hierarchy" in kwargs.keys():
            self.hierarchy = kwargs["hierarchy"]
        else:
            self.hierarchy = None

    # def __new__(cls, name: str, bases: Tuple, attrs: Dict) -> None:
    #     cls.last_num += 1
    #     super().__new__(cls, name, bases, attrs)

    def __del__(self) -> None:
        Particle.last_num -= 1

    def __hash__(self) -> int:
        return int(self.num ** 2 + self.x ** 2 + self.y ** 2)

    def __eq__(self, other: Any) -> bool:
        if (
            isinstance(other, self.__class__)
            and other.__hash__ == self.__hash__
            and other.num == self.num
        ):
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

        if not "is_segment" in kwargs.keys():
            kwargs["is_segment"] = False
        self.is_segment = kwargs["is_segment"]
        try:
            if kwargs["thickness"] < self.width_bounds[0]:
                raise RuntimeError(
                    "the given thickness is lower than expected"
                )
            elif kwargs["thickness"] > self.width_bounds[1]:
                raise RuntimeError(
                    "the given thickness is higher than expected"
                )
            elif (
                kwargs["length"] < self.length_bounds[0]
                and not self.is_segment
            ):
                raise RuntimeError("the given length is lower than expected")
            elif (
                kwargs["length"] > self.length_bounds[1]
                and not self.is_segment
            ):
                raise RuntimeError("the given length is higher than expected")
        except AttributeError:
            pass
        self.thickness = kwargs.pop("thickness")
        self.length = kwargs.pop("length")
        super().__init__(*args, **kwargs)
        if not kwargs["is_segment"]:
            self.segments: List = self.segmentalize()

    @property
    def shape(self):
        """the realistic 2D shape of the clay particle as a rectangle"""

        return self.midline

    @property
    def midline(self):
        """the long line that represents the clay particle without a thickness"""

        return shapes.LineSegment.from_point_and_inclination(
            self.midpoint, self.inclination, self.length
        )

    @property
    def midpoint(self):
        """the point at the middle of the particle"""

        return shapes.Point(self.x, self.y)

    def segmentalize(self) -> List:
        """segmentalize the coresponding clay particles into 3 equal
        segments
        """

        particle_number = self.num
        size = self.length / 3
        res = []
        for i, midpoint in enumerate(self.midline.navigator(1 / 6)):
            if i % 2 == 1:
                attrs = {k: v for k, v in self.__dict__.items()}
                attrs["x"] = midpoint.x
                attrs["y"] = midpoint.y
                attrs["length"] = size
                attrs["is_segment"] = True
                new_particle = self.__class__(**attrs)
                new_particle.num = particle_number
                res.append(new_particle)
        return res

    def reassemble_segments(self):
        """reassembles the segments of the particle"""

        pass

    def move(
        self, delta_x: float = 0, delta_y: float = 0, delta_theta: float = 0
    ):
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
        self.inclination = operations.standardized_inclination(
            self.inclination + delta_theta
        )
        self.shape.move(
            delta_x=delta_x, delta_y=delta_y, delta_theta=delta_theta
        )
        self.midline.move(
            delta_x=delta_x, delta_y=delta_y, delta_theta=delta_theta
        )
        self.midpoint.move(delta_x=delta_x, delta_y=delta_y)

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
            if kwargs["length"] < self.diameter_bounds[0]:
                raise RuntimeError("the given diameter is lower than expected")
            elif kwargs["length"] > self.diameter_bounds[1]:
                raise RuntimeError(
                    "the given diameter is higher than expected"
                )
        except AttributeError:
            pass
        self.length = kwargs.pop("length")
        x, y = kwargs["x"], kwargs["y"]
        kwargs["inclination"] = 0
        self.shape = shapes.Circle(shapes.Point(x, y), self.length)
        super().__init__(*args, **kwargs)

    def move(
        self, delta_x: float = 0, delta_y: float = 0, delta_theta: float = 0
    ):
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

    length_bounds: Tuple[int, int] = (1000, 12000)  # in nanometer; may change
    width_bounds: Tuple[int, int] = (1, 3)  # in nanometer; may change
    cec: float = 5  # according to M.Khabazian and A.Mirghasemi, 2018
    ssa: float = 20  # in square meters per gram; ///
    hamaker_constant: float = 1e-19  # in Joule; ///
    boltzman_constant: float = 1.38e-23  # in Joule; ///
    young_modulus: float = 2e-8  # in Newton per square nanometer; ///
    shear_modulus: float = 8e-9  # in Newton per square nanometer; ///
    surface_tension: float = 0.075  # in Newton per meter; ///
    normal_stiffness: float = 3e-6  # in Newton per nanometer; ///
    shear_stiffness: float = 1.2e-6  # in Newton per nanometer; ///
    density: float = (
        2.7e-33  # in Newton second per nanometer to the power of four; ///
    )
    formula: str = "Al2Si2O5(OH)4"  # according to 'sciencedirect.com/topics/chemical-engineering/kaolinite'

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
        name = f"Kaolinite:: number {self.num}"
        return name if not self.is_segment else name + "-S"


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
    formula: str = "SiO2"

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
        return f"Quartz:: number {self.num}"


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
    formula: str = "(Na,Ca)0.33(Al,Mg)2(Si4O10)(OH)2·nH2O"

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
        return f"Montmorillonite-{self.num}"


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
    formula: str = "(Na,Ca)0.33(Al,Mg)2(Si4O10)(OH)2·nH2O"

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

        kwargs["thickness"] = 2
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"Montmorillonite-{self.num}"


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

        if "is_fixed" not in kwargs.keys():
            kwargs["is_fixed"] = True
        self.is_fixed = kwargs.pop("is_fixed")
        if kwargs["length"] <= 0:
            raise RuntimeError(
                "the given length for the wall should be a positive number"
            )
        self.length = kwargs.pop("length")
        super().__init__(*args, **kwargs)

    @property
    def shape(self):
        """the geometrical shape of the Wall instance which is a line
        segment
        """

        return shapes.LineSegment.from_point_and_inclination(
            shapes.Point(self.x, self.y), self.inclination, self.length
        )

    @classmethod
    def from_ends(
        cls,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        is_fixed: bool = True,
    ) -> "Wall":
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

        length = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        if x1 == x2:
            inclination = np.math.pi / 2
        else:
            inclination = np.arctan((y2 - y1) / (x2 - x1))
        return Wall(
            x=x, y=y, inclination=inclination, length=length, is_fixed=is_fixed
        )

    def move(
        self, delta_x: float = 0, delta_y: float = 0, delta_theta: float = 0
    ):
        """moves the wall with the given derivetives"""

        self.x += delta_x
        self.y += delta_y
        self.inclination = operations.standardized_inclination(
            self.inclination + delta_theta
        )

    def __repr__(self):
        """string representation of the Wall object"""
        return f"Wall[inclination: {self.inclination}; center: ({self.x}, {self.y}); is_fixed: {self.is_fixed}]"

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
        return int(self.x ** 2 + self.y ** 2)
