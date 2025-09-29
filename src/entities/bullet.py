import math
import pygame as pg
from settings import BULLET_LIFETIME, BULLET_SPEED, WHITE, DEEP_SKY_BLUE


class Bullet:
    def __init__(self, x, y, angle):

        # Position
        self.x = x
        self.y = y

        # Direction
        rad = math.radians(angle)
        self.velocity_x = math.cos(rad) * BULLET_SPEED
        self.velocity_y = -math.sin(rad) * BULLET_SPEED

        # Liftime Counter

        self.lifetime = BULLET_LIFETIME

        # Size

        self.radius = 3

    def update(self):

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.lifetime -= 1

    def is_alive(self):
        return self.lifetime > 0

    def draw(self, surface):
        pg.draw.circle(surface, DEEP_SKY_BLUE, (int(self.x), int(self.y)), self.radius)
