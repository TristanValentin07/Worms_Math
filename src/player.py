import pygame

class Player:
    def __init__(self, x, y, sprite_sheet, scale_factor=0.3):
        self.x = float(x)
        self.y = float(y)
        self.scale_factor = scale_factor
        self.sprites = self.load_sprite_sheet(sprite_sheet, 1, 1)
        self.current_sprite = 0
        self.health = 100
        self.velocity_y = 0
        self.on_ground = False

        sprite_width = self.sprites[0].get_width()
        sprite_height = self.sprites[0].get_height()
        hitbox_width = int(sprite_width * 1)
        hitbox_height = int(sprite_height * 1)

        self.hitbox = pygame.Rect(self.x + (sprite_width - hitbox_width) // 2, 
                                  self.y + (sprite_height - hitbox_height) // 2, 
                                  hitbox_width, 
                                  hitbox_height)

    def jump(self):
        if self.on_ground:
            self.velocity_y = -12.0
            self.on_ground = False


    def load_sprite_sheet(self, sheet, columns, rows):
        sheet_width, sheet_height = sheet.get_size()
        sprite_width = sheet_width // columns
        sprite_height = sheet_height // rows
        sprites = []

        for row in range(rows):
            for col in range(columns):
                rect = pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)
                image = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA).convert_alpha()
                image.blit(sheet, (0, 0), rect)
                new_size = (int(sprite_width * self.scale_factor), int(sprite_height * self.scale_factor))
                image = pygame.transform.scale(image, new_size)
                sprites.append(image)
        return sprites

    def apply_gravity(self, blocks):
        gravity_up = 0.5
        gravity_down = 3

        if self.velocity_y >= 0:
            self.velocity_y = min(self.velocity_y + gravity_down, 5)
        else:
            self.velocity_y = min(self.velocity_y + gravity_up, 5)
        new_y = self.y + self.velocity_y
        test_hitbox = pygame.Rect(self.hitbox.x, int(new_y), self.hitbox.width, self.hitbox.height)
        if self.collides_with_any_block(test_hitbox, blocks):
            if self.velocity_y > 0:
                self.on_ground = True
                self.velocity_y = 0
            else:
                self.velocity_y = 0
        else:
            self.y = new_y
            self.hitbox.y = int(new_y)
            self.on_ground = False



    def collides_with_any_block(self, test_hitbox, blocks):
        mask_player = pygame.mask.from_surface(self.sprites[self.current_sprite])

        for block in blocks:
            if test_hitbox.colliderect(block.rect) and block.mask.count() > 0:
                offset_x = test_hitbox.x - block.rect.x
                offset_y = test_hitbox.y - block.rect.y
                overlap = block.mask.overlap(mask_player, (offset_x, offset_y))
                if overlap:
                    return True
        return False

    def move(self, direction, blocks):
        speed = 5
        if direction == "left":
            self.move_horizontally(-speed, blocks)
        elif direction == "right":
            self.move_horizontally(speed, blocks)


    def move_horizontally(self, dx, blocks):
        steps = abs(dx)
        step_direction = 1 if dx > 0 else -1

        for _ in range(steps):
            test_x = self.x + step_direction
            test_hitbox = pygame.Rect(test_x, self.y, self.hitbox.width, self.hitbox.height)
            if self.collides_with_any_block(test_hitbox, blocks):
                return
            else:
                self.x = test_x
                self.hitbox.x = self.x

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 2)

class PlayerManager:
    def __init__(self, num_players, sprite_sheet_path):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.players = self.create_players(num_players)
        self.current_player_index = 0

    def create_players(self, num_players):
        return [Player(100 + i * 150, 400, self.sprite_sheet) for i in range(num_players)]

    def switch_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_current_player(self):
        return self.players[self.current_player_index]

    def draw_players(self, screen):
        for i, player in enumerate(self.players):
            if i == self.current_player_index:
                pygame.draw.circle(screen, (255, 0, 0), (player.x + 25, player.y - 10), 10)  # Indicateur du joueur actif
            screen.blit(player.sprites[player.current_sprite], (player.x, player.y))
            player.draw_hitbox(screen)