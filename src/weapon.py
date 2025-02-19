import math
import pygame

class RocketProjectile:
    def __init__(self, x, y, angle, speed=10, gravity=0.4):
        self.x = float(x)
        self.y = float(y)
        self.angle = angle
        self.speed = speed
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.exploded = False
        self.explosion_radius = 30
        self.gravity = gravity

    def update(self, dt, blocks, players):
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        proj_rect = pygame.Rect(int(self.x), int(self.y), 5, 5)
        mask_rocket = pygame.mask.from_surface(pygame.Surface((5, 5)))
        for block in blocks:
            if proj_rect.colliderect(block.rect):
                offset_x = proj_rect.x - block.rect.x
                offset_y = proj_rect.y - block.rect.y
                overlap = block.mask.overlap(mask_rocket, (offset_x, offset_y))
                if overlap:
                    self.explode(players)
                    self.exploded = True
                    break

    def explode(self, players):
        for p in players:
            dx = p.x - self.x
            dy = p.y - self.y
            dist = math.hypot(dx, dy)
            if dist < self.explosion_radius:
                if hasattr(p, 'health'):
                    p.health -= 20

                force = max(0, self.explosion_radius - dist)
                angle = math.atan2(dy, dx)
                knock_x = math.cos(angle) * force
                knock_y = math.sin(angle) * force * 0.5

                p.x += knock_x
                p.y += knock_y
                if hasattr(p, 'hitbox'):
                    p.hitbox.x = int(p.x)
                    p.hitbox.y = int(p.y)

    def draw(self, screen):
        if not self.exploded:
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 10)


class RocketWeapon:
    def __init__(self):
        self.selected = False
        self.projectiles = []
        self.button_rect = pygame.Rect(20, 20, 100, 40)
        self.deselect_rect = pygame.Rect(20, 70, 100, 40)
        self.show_deselect = False
        self.player_ref = None

    def attach_to_player(self, player):
        self.player_ref = player

    def handle_event(self, event, blocks, players):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.button_rect.collidepoint(mouse_pos):
                self.selected = True
                self.show_deselect = True

            if self.show_deselect and self.deselect_rect.collidepoint(mouse_pos):
                self.selected = False
                self.show_deselect = False

            if self.selected and event.button == 1:
                self.shoot(blocks, players, 0)
            
            elif event.button == 1:
                self.shoot(blocks, players)

    def shoot(self, blocks, players, gravity=0.4):
        if not self.player_ref:
            return
        mx, my = pygame.mouse.get_pos()
        px = self.player_ref.x
        py = self.player_ref.y

        angle = math.atan2((my - py), (mx - px))
        speed =15
        rocket = RocketProjectile(px, py, angle, speed, gravity)
        self.projectiles.append(rocket)

    def update(self, dt, blocks, players, maps):
        for rocket in self.projectiles[:]:
            if rocket.exploded:
                rx, ry = int(rocket.x), int(rocket.y)
                self.projectiles.remove(rocket)
                for block in maps:
                    if block.rect.collidepoint(rx, ry):
                        block.destroy_area((rx, ry), radius=50)
            else:
                rocket.update(dt, blocks, players)


    def draw_ui(self, screen):
        self.button_rect = pygame.Rect(120, 50, 150, 60)
        self.deselect_rect = pygame.Rect(120, 120, 150, 60)

        color = (255, 0, 0) if self.selected else (200, 200, 200)
        pygame.draw.rect(screen, color, self.button_rect)

        font = pygame.font.SysFont(None, 24)
        text = font.render("Roquette", True, (0, 0, 0))
        screen.blit(text, (self.button_rect.x + 10, self.button_rect.y + 20))

        if self.show_deselect:
            pygame.draw.rect(screen, (200, 200, 200), self.deselect_rect)
            dtext = font.render("Deselect", True, (0, 0, 0))
            screen.blit(dtext, (self.deselect_rect.x + 10, self.deselect_rect.y + 20))


    def draw_projectiles(self, screen):
        for rocket in self.projectiles:
            rocket.draw(screen)
        if self.selected and self.player_ref:
            mx, my = pygame.mouse.get_pos()
            px = self.player_ref.x
            py = self.player_ref.y
            pygame.draw.line(screen, (255, 0, 0), (int(px), int(py)), (mx, my), 2)