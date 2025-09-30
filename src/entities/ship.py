import math
import pygame as pg
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SHIP_ACCELERATION,
    SHIP_FRICTION,
    SHIP_MAX_SPEED,
    SHIP_ROTATION_SPEED,
    WHITE,
)
from .bullet import Bullet
from assets_loader import load_ship_image


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.image = load_ship_image()
        self.rect = self.image.get_rect(center=(x, y))

        self.size = 20

        self.lives = 3
        self.invincibility_timer = 0
        self.flash_interval = 10

    def handle_input(self, keys):

        # Roate Left/Right
        # if keys[pg.K_LEFT] or keys[pg.K_a]:
        #     self.angle += SHIP_ROTATION_SPEED
        # if keys[pg.K_RIGHT] or keys[pg.K_d]:
        #     self.angle -= SHIP_ROTATION_SPEED

        # Ship Rotates Toward Mouse Cursor
        mouse_x, mouse_y = pg.mouse.get_pos()
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        self.angle = math.degrees(math.atan2(-dy, dx))

        # Thrust Forward
        if keys[pg.K_UP] or keys[pg.K_w]:
            rad = math.radians(self.angle)
            self.velocity_x += math.cos(rad) * SHIP_ACCELERATION
            self.velocity_y -= math.sin(rad) * SHIP_ACCELERATION
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            rad = math.radians(self.angle)
            self.velocity_x -= math.cos(rad) * SHIP_ACCELERATION
            self.velocity_y += math.sin(rad) * SHIP_ACCELERATION

    def update(self):

        # Apply Velocity
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Apply Friction
        self.velocity_x *= SHIP_FRICTION
        self.velocity_y *= SHIP_FRICTION

        # Cap Speed

        speed = math.hypot(self.velocity_x, self.velocity_y)
        if speed > SHIP_MAX_SPEED:
            scale = SHIP_MAX_SPEED / speed
            self.velocity_x *= scale
            self.velocity_y *= scale

        # Screen Warp

        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        # Flash ship when invincible
        if self.invincibility_timer > 0:
            # Skip drawing every few frames → blinking effect
            if (self.invincibility_timer // self.flash_interval) % 2 == 0:
                return  # Skip drawing this frame

        rad = math.radians(self.angle)
        tip = (self.x + math.cos(rad) * self.size, self.y - math.sin(rad) * self.size)

        left = (
            self.x + math.cos(rad + math.radians(140)) * self.size,
            self.y - math.sin(rad + math.radians(140)) * self.size,
        )

        right = (
            self.x + math.cos(rad - math.radians(140)) * self.size,
            self.y - math.sin(rad - math.radians(140)) * self.size,
        )

        # pg.draw.polygon(surface, WHITE, [tip, left, right], 1)
        rotated_image = pg.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, new_rect.topleft)

    def shoot(self, target_pos):

        mouse_x, mouse_y = target_pos

        # Compute angle from ship to mouse
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        angle = math.degrees(math.atan2(-dy, dx))

        rad = math.radians(angle)
        tip_x = self.x + math.cos(rad) * self.size
        tip_y = self.y - math.sin(rad) * self.size
        return Bullet(tip_x, tip_y, angle)

    def take_hit(self):
        if self.invincibility_timer == 0:
            self.lives -= 1
            self.invincibility_timer = 120
            print(f"Lives Left: {self.lives}")

    def game_start(self):
        self.invincibility_timer = 180
