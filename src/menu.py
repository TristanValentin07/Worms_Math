import pygame
import sys
import pygame_menu as pm

global user_name

def main_menu(screen):

    #Windows Settings
    width, height = screen.get_size()
    menu = pm.Menu('Worms_Math', width, height, theme=pm.themes.THEME_DARK)

    #State variable
    menu_running = True

    #Buttons
    menu.add.button('Quit', pm.events.EXIT, screen)


    #Menu loop
    while menu_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Update screen infos
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        #Update Frames
        pygame.display.update()
