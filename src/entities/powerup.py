import pygame as pg
import random

from settings import SCREEN_HEIGHT, SCREEN_WIDTH

from assets_loader import load_powerups


class Powerup:
    # Types
    TYPE_SCORE = "score"
    TYPE_SPEED = "speed"
    TYPE_INVINCIBLE = "invincible"

    # Ranks (only meaningful for TYPE_SCORE)
    RANK_NONE = 1.0
    RANK_1 = 1.5
    RANK_2 = 2.0
    RANK_3 = 3.0

    IMAGES = None

    def __init__(self, x=None, y=None, size=20, rank=RANK_NONE, type=TYPE_SCORE):
        self.x = x if x is not None else random.randint(0, SCREEN_WIDTH)
        self.y = y if y is not None else random.randint(0, SCREEN_HEIGHT)
        self.size = size
        self.rank = rank
        self.type = type
        self.lifetime = 480
        self.flash_interval = 10

        # Pick image based on rank (for score powerups)
        rank_map = {
            self.RANK_1: self.IMAGES["rank_1"],
            self.RANK_2: self.IMAGES["rank_2"],
            self.RANK_3: self.IMAGES["rank_3"],
        }
        self.image = (
            rank_map.get(self.rank, None)
            if self.type == self.TYPE_SCORE
            else self.IMAGES.get(self.type)
        )

        self.rect = (
            self.image.get_rect(center=(self.x, self.y))
            if self.image
            else pg.Rect(self.x, self.y, self.size, self.size)
        )

    def update(self):
        self.y += 2
        self.y -= 2

        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime <= 120:
            if (self.lifetime // self.flash_interval) % 2 == 0:
                return
        surface.blit(self.image, self.rect.topleft)

    def is_alive(self):
        return self.lifetime > 0

    @classmethod
    def load_images(cls):
        if cls.IMAGES is None:  # only load once
            cls.IMAGES = load_powerups()
