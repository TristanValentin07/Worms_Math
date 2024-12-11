import sys
import pygame
from src.map_loader import *

class DestructibleBlock:
    def __init__(self, material, width, height, x, y):
        #Init block
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Surface propre au bloc
        self.image = pygame.image.load(material).convert_alpha()         # Charger le matériau
        self.image = pygame.transform.scale(self.image, (width, height)) # Redimensionner l'image
        self.rect = pygame.Rect(x, y, width, height)                     # Position et dimensions
        self.surface.blit(self.image, (0, 0))                            # Dessiner l'image sur la surface

    def draw(self, screen):
        #Affichage block
        screen.blit(self.surface, self.rect.topleft)

    def destroy_area(self, center, radius):
        #Destroy block
        local_center = (center[0] - self.rect.x, center[1] - self.rect.y)  # Coordonner par rapport au bloc
        pygame.draw.circle(self.surface, (0, 0, 0, 0), local_center, radius)

def game_loop(screen):
    # Charger l'arrière-plan
    game_background = pygame.image.load("texture/game/game_background.jpeg").convert_alpha()
    game_background = pygame.transform.scale(game_background, (1280, 720))

    # Charger la carte
    map_file = "map/map.txt"
    map_data = load_map(map_file)

    # Créer des blocs destructibles
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

    # Game loop
    game_running = True
    while game_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Clic pour détruire une zone
                mouse_pos = pygame.mouse.get_pos()
                for block in maps:
                    if block.rect.collidepoint(mouse_pos):  # Vérifier si le clic est sur un bloc
                        block.destroy_area(mouse_pos, radius=50)

        # Dessiner l'arrière-plan
        screen.blit(game_background, (0, 0))

        # Dessiner les blocs
        for block in maps:
            block.draw(screen)

        # Mettre à jour l'écran
        pygame.display.update()
