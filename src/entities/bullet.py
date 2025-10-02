# bullet.py
import math
import pygame as pg
from settings import (
    BULLET_LIFETIME,
    BULLET_SPEED,
    WHITE,
    RED,
    DEEP_SKY_BLUE,
    BLUE,
    GREEN,
    YELLOW,
    VIOLET,
    INDIGO,
    ORANGE,
)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, angle, is_powerup=False, powerup_rank=1):
        super().__init__()

        # Movement setup
        rad = math.radians(angle)
        self.velocity_x = math.cos(rad) * BULLET_SPEED
        self.velocity_y = -math.sin(rad) * BULLET_SPEED

        self.lifetime = BULLET_LIFETIME
        self.radius = 3

        # Position & rect
        self.image = pg.Surface((self.radius * 2, self.radius * 2), pg.SRCALPHA)
        self.color = WHITE
        pg.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))

        # Optional pixel-perfect collisions
        self.mask = pg.mask.from_surface(self.image)

        # Powerup state
        self.is_powerup = is_powerup
        self.powerup_rank = powerup_rank

        # Color cycling (only used if powerup bullet)
        self.color_switch_delay = 50  # ms
        self.last_color_switch = pg.time.get_ticks()
        self.color_index = 0
        self.bullet_colors = [
            RED,
            DEEP_SKY_BLUE,
            BLUE,
            GREEN,
            YELLOW,
            VIOLET,
            INDIGO,
            ORANGE,
        ]

    def update(self):
        # Movement
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.lifetime -= 1

        # Kill if out of time
        if self.lifetime <= 0:
            self.kill()

        # Color cycling for powerup bullets
        if self.is_powerup:
            now = pg.time.get_ticks()
            if now - self.last_color_switch >= self.color_switch_delay:
                self.last_color_switch = now
                self.color_index = (self.color_index + 1) % len(self.bullet_colors)
                self.color = self.bullet_colors[self.color_index]

                # Update image to reflect color change
                self.image.fill((0, 0, 0, 0))  # clear surface
                pg.draw.circle(
                    self.image, self.color, (self.radius, self.radius), self.radius
                )
                self.mask = pg.mask.from_surface(self.image)
