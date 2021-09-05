"""module that contains tools to illustrate simulations
"""


import sys
import subprocess
import os
os.system('')
import pygame

clay_color = (196, 69, 69)
sand_color = (75, 204, 112)
container_color = (163, 250, 255)
wall_color = (28, 30, 31)
background_color = (86, 96, 97)

pygame.display.set_mode(1000, 1000) #fix sizes
pygame.draw.line(color = clay_color, start_pos = (100, 100), end_pos = (500, 500), width = 1)
