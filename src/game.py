import sys
import pygame

def game_loop(screen):
    width, height = screen.get_size()

    game_background = pygame.image.load("texture/game/game_background.jpeg")
    game_background = pygame.transform.scale(game_background, (1280, 720))

    # Game loop
    game_running = True
    while game_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(game_background, (0, 0))
        pygame.display.update()


