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


class Bullet:
    def __init__(self, x, y, angle, is_powerup=False, powerup_rank=1):
        self.x = x
        self.y = y
        rad = math.radians(angle)
        self.velocity_x = math.cos(rad) * BULLET_SPEED
        self.velocity_y = -math.sin(rad) * BULLET_SPEED

        self.lifetime = BULLET_LIFETIME
        self.radius = 3

        # Remember powerup state at creation
        self.is_powerup = is_powerup
        self.powerup_rank = powerup_rank

        # Color cycling
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
        self.color = WHITE

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifetime -= 1

        if self.is_powerup:
            now = pg.time.get_ticks()
            if now - self.last_color_switch >= self.color_switch_delay:
                self.last_color_switch = now
                self.color_index = (self.color_index + 1) % len(self.bullet_colors)
                self.color = self.bullet_colors[self.color_index]

    def is_alive(self):
        return self.lifetime > 0

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
