from src.menu import *

#Create Window

pygame.init()
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Worms Math")
main_menu(screen)
pygame.quit()
