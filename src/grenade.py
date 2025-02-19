import math
import pygame

class GrenadeProjectile:
    def __init__(self, x, y, angle, speed=10):
        self.x = float(x)
        self.y = float(y)
        self.angle = angle
        self.speed = speed
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed

        self.exploded = False
        self.explosion_radius = 50

        self.bounce_factor = 0.6
        self.timer = 3 * 1000
        self.start_time = pygame.time.get_ticks()

    def update(self, dt, blocks, players):
        if pygame.time.get_ticks() - self.start_time >= self.timer:
            self.explode(players)
            self.exploded = True
            return

        gravity = 0.5

        sub_steps = 5
        step_dt = dt / sub_steps

        for _ in range(sub_steps):
            self.vy += gravity * step_dt

            self.x += self.vx * step_dt
            self.y += self.vy * step_dt

            grenade_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(grenade_surf, (255, 255, 255), (5, 5), 4)
            grenade_mask = pygame.mask.from_surface(grenade_surf)

            proj_rect = pygame.Rect(int(self.x), int(self.y), 10, 10)

            for block in blocks:
                if proj_rect.colliderect(block.rect):
                    offset_x = proj_rect.x - block.rect.x
                    offset_y = proj_rect.y - block.rect.y

                    overlap = block.mask.overlap(grenade_mask, (offset_x, offset_y))
                    if overlap:
                        if abs(self.vy) > 1:
                            self.vy = -self.vy * self.bounce_factor
                        else:
                            self.vy = 0
                        self.vx *= 0.8
                        self.y = block.rect.top - 10
                        break

    def explode(self, players):
        for p in players:
            dx = p.x - self.x
            dy = p.y - self.y
            dist = math.hypot(dx, dy)
            if dist < self.explosion_radius:
                if hasattr(p, 'health'):
                    p.health -= 30

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
            pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), 8)


class GrenadeWeapon:
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
                self.throw_grenade(blocks, players)

    def throw_grenade(self, blocks, players):
        if not self.player_ref:
            return
        mx, my = pygame.mouse.get_pos()
        px = self.player_ref.x
        py = self.player_ref.y

        angle = math.atan2((my - py), (mx - px))
        speed = 12
        grenade = GrenadeProjectile(px, py, angle, speed)
        self.projectiles.append(grenade)

    def update(self, dt, blocks, players, maps):
        for grenade in self.projectiles[:]:
            if grenade.exploded:
                rx, ry = int(grenade.x), int(grenade.y)
                for block in maps:
                    if block.rect.collidepoint(rx, ry):
                        block.destroy_area((rx, ry), radius=50)
                        print("Grenade => Sol creusé !")
                self.projectiles.remove(grenade)
            else:
                grenade.update(dt, blocks, players)

    def draw_ui(self, screen):
        self.button_rect = pygame.Rect(500, 50, 150, 60)
        self.deselect_rect = pygame.Rect(500, 120, 150, 60)

        color = (0, 255, 0) if self.selected else (200, 200, 200)
        pygame.draw.rect(screen, color, self.button_rect)

        font = pygame.font.SysFont(None, 24)
        text = font.render("Grenade", True, (0, 0, 0))
        screen.blit(text, (self.button_rect.x + 10, self.button_rect.y + 20))

        if self.show_deselect:
            pygame.draw.rect(screen, (200, 200, 200), self.deselect_rect)
            dtext = font.render("Deselect", True, (0, 0, 0))
            screen.blit(dtext, (self.deselect_rect.x + 10, self.deselect_rect.y + 20))

    def draw_projectiles(self, screen):
        for grenade in self.projectiles:
            grenade.draw(screen)

        if self.selected and self.player_ref:
            mx, my = pygame.mouse.get_pos()
            px = self.player_ref.x
            py = self.player_ref.y
            pygame.draw.line(screen, (0, 255, 0), (int(px), int(py)), (mx, my), 2)
