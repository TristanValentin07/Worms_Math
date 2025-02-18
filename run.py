from src.menu import *

#Create Window

pygame.init()
width = 1920
height = 1080
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Worms Math")
main_menu(screen)
pygame.quit()
