import pygame
import sys
import pygame_menu as pm
from src.game import game_loop

global user_name

def main_menu(screen):
    #import local
    from src.options import options_menu
    # Import background
    menu_background = pygame.image.load("texture/menu/background.png")
    menu_background = pygame.transform.scale(menu_background, (1920, 1080))

    # Create a custom theme with transparent background
    custom_theme = pm.Theme(
        background_color=(0, 0, 0, 0),  # Fully transparent
        title=False,
        widget_offset=(0, 700),
        widget_margin=(0, 10),
        widget_font_color=(255, 165, 0),
    )

    # Create the menu
    screen_width, screen_height = screen.get_size()
    menu = pm.Menu(
        title='',
        width=screen_width,
        height=screen_height,
        theme=custom_theme,
        center_content=False
    )

    def start_game():
        game_loop(screen)  # Start the game loop

    # Add buttons to the menu
    menu.add.button('Play', start_game)
    menu.add.button('Options', lambda: options_menu(screen))
    menu.add.button('Quit', pm.events.EXIT, screen)

    # Main menu loop
    menu.mainloop(screen, bgfun=lambda: screen.blit(menu_background, (0, 0)))
