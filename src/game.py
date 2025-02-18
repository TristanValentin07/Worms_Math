import sys
import pygame
from src.map_loader import load_map  # Import the map loader function


class DestructibleBlock:
    def __init__(self, material, width, height, x, y, destructible=True):

        # Create a surface for the block
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Surface with transparency
        self.image = pygame.image.load(material).convert_alpha()  # Load the texture
        self.image = pygame.transform.scale(self.image, (width, height))  # Resize the texture
        self.rect = pygame.Rect(x, y, width, height)  # Position and dimensions
        self.surface.blit(self.image, (0, 0))  # Draw the texture on the surface
        self.destructible = destructible  # Whether the block can be destroyed
        self.destroyed = False # Track if the block is destroyed

    def draw(self, screen):
        if not self.destroyed:
            screen.blit(self.surface, self.rect.topleft)

    def destroy_area(self, center, radius):
        if not self.destructible : # Skip destruction if not destructible
            return

        #Convert center to local coordinates (relative to the block)
        local_center = (center[0] - self.rect.x, center[1] - self.rect.y)

        # Draw a transparent circle to simulate destruction
        pygame.draw.circle(self.surface, (0, 0, 0, 0), local_center, radius)


def game_loop(screen):
    # Local import to avoid circular dependencies
    from src.menu import main_menu

    # Load the background
    game_background = pygame.image.load("texture/game/game_background.jpeg").convert_alpha()
    game_background = pygame.transform.scale(game_background, (1920, 1080))

    # Load the map
    map_file = "map/map.txt"
    map_data = load_map(map_file)

    # Create destructible blocks from the map data
    maps = []
    for block_data in map_data:
        block = DestructibleBlock(
            block_data["material"],
            block_data["width"],
            block_data["height"],
            block_data["x"],
            block_data["y"],
            destructible=block_data["destructible"] # Pass the flag
        )
        maps.append(block)

    # Game loop
    game_running = True
    while game_running:
        # Handle events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Destroy a block on mouse click
                mouse_pos = pygame.mouse.get_pos()
                for block in maps:
                    if block.rect.collidepoint(mouse_pos) and block.destructible:  # Check if the click is on a block
                        block.destroy_area(mouse_pos, radius=50)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Return to the main menu
                    game_running = False
                    main_menu(screen)

        # Draw the background
        screen.blit(game_background, (0, 0))

        # Draw the blocks
        for block in maps:
            block.draw(screen)

        # Update the display
        pygame.display.update()