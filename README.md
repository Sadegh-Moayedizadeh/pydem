# Pydem

## Preface
``Pydem`` aims to run discrete elements method (DEM) simulations on a granular
mass. You have to create a ``Container`` to hold the particle providing
arguments such as information regarding the particles, size and type of
container. You can also create a custom container inheriting from
``ContainerBase`` and even give it your own set of particles. The program
gradually applies forces to the mass and updates particles location to a point
that everything is stable and sound.

After a full session of DEM simulation you can see the generated reports such
as force-displacement, tension-shear, etc. You can also implement your own
reporter by inheriting from the ``ReporterBase`` class.

## Installation
You can install ``Pydem`` simple by running this command:

```console
$ pip install pydem
```

## Quick Start
[to be completed]