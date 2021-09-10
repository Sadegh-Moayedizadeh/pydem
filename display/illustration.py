"""module that contains tools to illustrate simulations
"""


import sys
import os
import pygame
from geometry import two_dimensional_entities as shapes
from geometry import two_dimensional_operations as operations
from generation import base_classes
import numpy as np
from typing import Type, Union, Tuple, List, Set, Dict, Any
import pathlib


class IllustrationPG(object):
    """class to illustrate the DEM simulation using the "pygame"
    libarary package
    """
    
    clay_color = (161, 93, 93)
    sand_color = (75, 204, 112)
    container_color = (163, 250, 255)
    wall_color = (28, 30, 31)
    background_color = (86, 96, 97)
    
    def __init__(self, container):
        """initializes the illustration instace
        """
        
        self.container = container
    
    def _convert_x(self, x: float) -> float:
        """converts the given x coordinate to a value that fits into
        the illustrated container
        """

        return (0.025) * (self.container.length) + (x) * (0.1)
    
    def _convert_y(self, y: float) -> float:
        """converts the given y coordinate to a value that fits into
        the illustrated container
        """

        return ((0.025) * (self.container.width)) + ((0.15) * (self.container.width) - (y) * (0.1))
    
    def set_shapes(self, screen):
        """sets up the shapes to be displayed
        """
        
        for wall in self.container.walls:
            pygame.draw.line(
                screen,
                self.wall_color,
                (self._convert_x(wall.shape.end1.x), self._convert_y(wall.shape.end1.y)),
                (self._convert_x(wall.shape.end2.x), self._convert_y(wall.shape.end2.y)),
                width = 5,
            )
        for particle in self.container.particles:
            if isinstance(particle, base_classes.Clay):
                pygame.draw.line(
                    screen,
                    self.clay_color,
                    (self._convert_x(particle.midline.end1.x), self._convert_y(particle.midline.end1.y)),
                    (self._convert_x(particle.midline.end2.x), self._convert_y(particle.midline.end2.y)),
                    particle.thickness,
                    )
            elif isinstance(particle, base_classes.Sand):
                pygame.draw.circle(
                    screen,
                    self.sand_color,
                    (self._convert_x(particle.center.x), self._convert_y(particle.center.y)),
                    paritcle.radius * 0.1
                )
    
    def display(self):
        """displays the illustraion
        """
        
        pygame.init()
        screen = pygame.display.set_mode((int(0.15*self.container.length), int(0.15*self.container.width))) #fix sizes
        screen.fill(self.background_color)
        container_surface = pygame.Surface([self.container.length//10, self.container.width//10])
        container_surface.fill(self.container_color)
        screen.blit(container_surface, (int(0.025*self.container.length), int(0.025*self.container.width)))
        
        pygame.display.set_caption('2D DEM simulation of tiaxial test on sand-clay mixtures')
        # font = pygame.font.Font('CrimsonText-Regular.ttf', 32)
        # text = font.render('GeeksForGeeks', True, self.sand_color, self.sand_color)
        # textRect = text.get_rect()
        # textRect.center = (750, 100)
        # image = pygame.image.load('ut_logo.png')
        
        self.set_shapes(screen)
        done = False
        while done is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True


class IllustrationMPL(object):
    """class to illustrate the DEM simulation using the "matplotlib"
    libarary package
    """
    
    def __init__(self, container):
        """initialize the illustration instance
        """
        
        self.container = container
    
    def _convert_x(self):
        """converts the x coordinate of the given entity in a way that
        fits into the container illustration created by this class
        """

        pass

    def _convert_y(self):
        """converts the x coordinate of the given entity in a way that
        fits into the container illustration created by this class
        """
        
        pass
    
    def set_shapes(self):
        """sets up the shapes of the all the particles and boundaries
        in the model
        """
        
        pass
    
    def display(self):
        """displays the illustration of the DEM model
        """

        pass