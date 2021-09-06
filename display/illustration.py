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


class Illustration(object):
    """class to illustrate the DEM simulation
    """
    
    clay_color = (196, 69, 69)
    sand_color = (75, 204, 112)
    container_color = (163, 250, 255)
    wall_color = (28, 30, 31)
    background_color = (86, 96, 97)
    
    def __init__(self, container):
        """initializes the illustration instace
        """
        
        self.container = container
    
    def set_shapes(self, screen):
        """sets up the shapes to be displayed
        """
        
        for wall in container.walls:
            pygame.draw.line(
                screen,
                self.wall_color,
                (wall.shape.end1.x, wall.shape.end1.y),
                (wall.shape.end2.x, wall.shape.end2.y),
                width = 5,
            )
        for particle in self.container.particles:
            if isinstance(particle, base_classes.Clay):
                pygame.draw.line(
                    screen,
                    self.clay_color,
                    (particle.midline.end1.x, particle.midline.end1.y),
                    (particle.midline.end2.x, particle.midline.end2.y),
                    particle.thickness,
                    )
            elif isinstance(particle, base_classes.Sand):
                pygame.draw.circle(
                    screen,
                    self.sand_color,
                    (particle.center.x, particle.center.y),
                    paritcle.radius
                )
    
    def display(self):
        """displays the illustraion
        """
        
        pygame.init()
        screen = pygame.display.set_mode((1500, 1500)) #fix sizes
        screen.fill(self.background_color)
        container_surface = pygame.Surface([1000, 1000])
        container_surface.fill(self.container_color)
        screen.blit(container_surface, (250, 250))
        
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
                pygame.display.flip()


ill = Illustration(0)
ill.display()