import pygame
from src.menu import *

#Initialize Pygame
pygame.init()

#Configure the window
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Worms Math")

#Call the main menu
main_menu(screen)
