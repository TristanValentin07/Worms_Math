import sys
import pygame
import pygame_menu as pm
from src.menu import main_menu

def options_menu(screen):
    width, height = screen.get_size()
    options = pm.Menu('Options', width, height, theme=pm.themes.THEME_DARK)

    options.add.button('Back', lambda: main_menu(screen))

    option_running = True
    while option_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    option_running = False

        if options.is_enabled():
            options.update(events)
            options.draw(screen)

        pygame.display.update()
