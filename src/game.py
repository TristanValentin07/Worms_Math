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


class PlayerManager:
    # Configuration des contrôles partagée entre les joueurs
    CONTROLS = {
        'left': pygame.K_q,
        'right': pygame.K_d,
        'jump': pygame.K_z
    }
    
    # Couleurs prédéfinies pour les joueurs
    COLORS = [
        (255, 0, 0),    # Rouge
        (0, 255, 0),    # Vert
        (0, 0, 255),    # Bleu
        (255, 255, 0),  # Jaune
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
    ]
    
    def __init__(self, num_players):
        self.players = []
        screen_width = 1920  # Largeur de l'écran
        
        # Création des joueurs avec espacement régulier
        for i in range(num_players):
            x_pos = (screen_width / (num_players + 1)) * (i + 1)
            color = self.COLORS[i % len(self.COLORS)]
            self.players.append(Player(x_pos, 300, color, self.CONTROLS))
            
        self.current_player_index = 0
        self.last_switch = time.time()
        self.turn_duration = 10
        
    def get_current_player(self):
        return self.players[self.current_player_index]
    
        return self.players
    def get_list_of_players(self):
        
    def update_turn(self):
        current_time = time.time()
        time_left = self.turn_duration - (current_time - self.last_switch)
        if time_left <= 0:
        
            self.last_switch = current_time
            
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return time_left
    def draw_players(self, screen):
        
        for player in self.players:
            player.draw(screen)
class Player:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = color
        self.velocity_y = 0
        self.is_jumping = False
        self.controls = controls
        self.base_speed = 150
        self.jump_force = -400
        self.gravity = 1200

    def move(self, blocks, dt):
        keys = pygame.key.get_pressed()
        
            self.rect.x -= self.base_speed * dt
        if keys[self.controls['left']]:
        if keys[self.controls['right']]:
            self.rect.x += self.base_speed * dt
            
        if keys[self.controls['jump']] and not self.is_jumping:
            self.velocity_y = self.jump_force
            self.is_jumping = True

    def gravityAndCollision(self, blocks, dt):
        self.velocity_y += self.gravity * dt
        self.rect.y += self.velocity_y * dt

        for block in blocks:
            if block.rect.colliderect(self.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = block.rect.top
                    self.velocity_y = 0
                    self.is_jumping = False
                elif self.velocity_y < 0:
                    self.rect.top = block.rect.bottom
                    self.velocity_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

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
    # Initialiser le gestionnaire de joueurs
    player_manager = PlayerManager(NUM_PLAYERS)
    font = pygame.font.Font(None, 36)
    game_running = True
    while game_running:
        # Handle events
        dt = clock.tick(60) / 1000.0
        
        time_left = player_manager.update_turn()
        current_player = player_manager.get_current_player()
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