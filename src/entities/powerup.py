import pygame as pg
import random
import math

from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from assets_loader import load_powerups


class Powerup(pg.sprite.Sprite):
    # Types
    TYPE_SCORE = "score"
    TYPE_SPEED = "speed"
    TYPE_INVINCIBLE = "invincible"
    TYPE_LIFE = "life"

    # Ranks (only meaningful for TYPE_SCORE)
    RANK_NONE = 1.0
    RANK_1 = 1.5
    RANK_2 = 2.0
    RANK_3 = 3.0

    IMAGES = None  # shared across all Powerups

    def __init__(self, x=None, y=None, size=20, rank=RANK_NONE, type=TYPE_SCORE):
        super().__init__()  # 👈 init the Sprite part

        # Position
        self.x = x if x is not None else random.randint(10, SCREEN_WIDTH - 10)
        self.y = y if y is not None else random.randint(10, SCREEN_HEIGHT - 10)
        self.size = size

        # Attributes
        self.rank = rank
        self.type = type
        self.lives = 1 if self.type == self.TYPE_LIFE else None
        self.lifetime = 480
        self.flash_interval = 10

        # Pick image based on type / rank
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

        # Every Sprite needs a rect
        if self.image:
            self.rect = self.image.get_rect(center=(self.x, self.y))
        else:
            self.image = pg.Surface((self.size, self.size))
            self.image.fill((200, 200, 200))  # fallback gray box
            self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        # Powerup floaty animation (right now just wiggles up/down)
        now = pg.time.get_ticks() / 200  # slow down time (adjust divisor)
        float_offset = math.sin(now) * 10  # amplitude of 5 pixels up/down
        self.rect.center = (self.x, self.y + float_offset)

        # Lifetime countdown
        self.lifetime -= 1

        # Blinking effect near the end
        if self.lifetime <= 120:
            if (self.lifetime // self.flash_interval) % 2 == 0:
                self.image.set_alpha(0)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def is_alive(self):
        return self.lifetime > 0

    @classmethod
    def load_images(cls):
        if cls.IMAGES is None:  # only load once
            cls.IMAGES = load_powerups()
