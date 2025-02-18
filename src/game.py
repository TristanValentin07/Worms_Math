import sys
import pygame
from src.map_loader import *
from src.player import *
from src.weapon import *

class DestructibleBlock:
    def __init__(self, material, width, height, x, y):
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image = pygame.image.load(material).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.surface.blit(self.image, (0, 0))      
        self.mask = pygame.mask.from_surface(self.surface)

    def draw(self, screen):
        screen.blit(self.surface, self.rect.topleft)

    def destroy_area(self, center, radius):
        local_center = (center[0] - self.rect.x, center[1] - self.rect.y)
        pygame.draw.circle(self.surface, (0, 0, 0, 0), local_center, radius)
        self.mask = pygame.mask.from_surface(self.surface)
        if self.mask.count() == 0:  
            self.rect = pygame.Rect(self.rect.x, self.rect.y, 0, 0)

def game_loop(screen, num_players):
    from src.menu import main_menu
    import time

    game_background = pygame.image.load("texture/game/game_background.jpeg").convert_alpha()
    game_background = pygame.transform.scale(game_background, (1920, 1080))

    player_manager = PlayerManager(num_players, "texture/game/player_img.png")
    all_players = player_manager.players

    map_file = "map/map.txt"
    map_data = load_map(map_file)

    maps = []
    for block_data in map_data:
        maps.append(
            DestructibleBlock(
                block_data["material"],
                block_data["width"],
                block_data["height"],
                block_data["x"],
                block_data["y"]
            )
        )
    from src.weapon import RocketWeapon
    rocket_weapon = RocketWeapon()
    if all_players:
        rocket_weapon.attach_to_player(all_players[0])

    clock = pygame.time.Clock()

    game_running = True
    while game_running:
        dt_ms = clock.tick(60)
        dt = dt_ms / 16.666

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu(screen)
                if event.key == pygame.K_t:
                    rocket_weapon.selected = False
                    rocket_weapon.show_deselect = False
                    player_manager.switch_turn()
                    new_player = player_manager.get_current_player()
                    rocket_weapon.attach_to_player(new_player)

            rocket_weapon.handle_event(event, maps, all_players)

        current_player = player_manager.get_current_player()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            current_player.move("left", maps)
        if keys[pygame.K_d]:
            current_player.move("right", maps)
        if keys[pygame.K_SPACE]:
            current_player.jump()

        current_player.apply_gravity(maps)
        rocket_weapon.update(dt, maps, all_players, maps)

        screen.blit(game_background, (0, 0))
        player_manager.draw_players(screen)
        for block in maps:
            block.draw(screen)
        rocket_weapon.draw_ui(screen)
        rocket_weapon.draw_projectiles(screen)
        pygame.display.update()
