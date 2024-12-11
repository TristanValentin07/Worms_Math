import pygame
import sys
import pygame_menu as pm
from src.game import game_loop

global user_name

def main_menu(screen):
    # Window Settings
    width, height = screen.get_size()

    # Import background
    menu_background = pygame.image.load("texture/menu/background.png")
    menu_background = pygame.transform.scale(menu_background, (1280, 720))

    # Create a custom theme with transparent background
    custom_theme = pm.Theme(
        background_color=(0, 0, 0, 0),  # Fully transparent
        title=False,
        widget_offset=(0, 400),
        widget_margin=(0, 10),
        widget_font_color=(255, 165, 0),
    )

    # Create the menu
    menu = pm.Menu('', width, height, theme=custom_theme, center_content=False)

    def start_game():
        menu_running = False
        game_loop(screen)  # Démarre la boucle de jeu

    # Add buttons to the menu
    menu.add.button('Play', start_game)
    menu.add.button('Options', pm.events.NONE, screen)
    menu.add.button('Quit', pm.events.EXIT, screen)

    # Menu loop
    menu_running = True

    while menu_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Draw the background first
        screen.blit(menu_background, (0, 0))

        # Draw the menu (buttons on top of the background)
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        # Update the display
        pygame.display.flip()
