import pygame
import sys
import pygame_menu as pm
from src.game import game_loop

global user_name

def main_menu(screen):
    from src.options import options_menu
    menu_background = pygame.image.load("texture/menu/background2.png")
    menu_background = pygame.transform.scale(menu_background, (1920, 1080))

    custom_theme = pm.Theme(
        background_color=(0, 0, 0, 0),
        title=False,
        widget_offset=(0, 700),
        widget_margin=(0, 10),
        widget_font_color=(255, 165, 0),
    )
    menu = pm.Menu('', 1920, 1080, theme=custom_theme, center_content=False)

    def start_game():
        menu_running = False
        game_loop(screen, 2)
    menu.add.button('Play', start_game)
    menu.add.button('Options', lambda: options_menu(screen))
    menu.add.button('Quit', pm.events.EXIT, screen)
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
        screen.blit(menu_background, (0, 0))
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)
        pygame.display.flip()
