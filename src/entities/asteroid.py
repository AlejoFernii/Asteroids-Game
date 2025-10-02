import math
import random
import pygame as pg

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASTEROID_MAX_SPEED,
    ASTEROID_MIN_SPEED,
    ASTEROID_SPLIT_COUNT,
    WHITE,
)

from assets_loader import load_asteroid_images


class Asteroid(pg.sprite.Sprite):

    LARGE_RANK = 100
    MEDIUM_RANK = 250
    SMALL_RANK = 500

    IMAGES = None

    def __init__(self, x=None, y=None, size=40, image=None, rank=100):
        super().__init__()

        self.x = x if x is not None else random.randint(0, SCREEN_WIDTH)
        self.y = y if y is not None else random.randint(0, SCREEN_HEIGHT)

        angle = random.uniform(0, 360)
        speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)

        self.velocity_x = math.cos(math.radians(angle)) * speed
        self.velocity_y = -math.sin(math.radians(angle)) * speed

        self.size = size
        self.alive = True
        self.image = image if image else self.IMAGES["large"]
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.rank = rank if rank else self.choose_rank()

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Warp Screen
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = SCREEN_HEIGHT
        elif self.y > SCREEN_HEIGHT:
            self.y = 0

        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        # pg.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size, 1)
        surface.blit(self.image, self.rect.topleft)

    def split(self):
        # Only split if Asteroid is large enough
        if self.size > 25:
            new_size = self.size // 2
            return [
                Asteroid(
                    self.x,
                    self.y,
                    new_size,
                    image=self.IMAGES["medium"],
                    rank=self.MEDIUM_RANK,
                )
                for _ in range(ASTEROID_SPLIT_COUNT)
            ]
        elif self.size > 15 and self.size < 25:
            new_size = self.size // 2
            return [
                Asteroid(
                    self.x,
                    self.y,
                    new_size,
                    image=self.IMAGES["small"],
                    rank=self.SMALL_RANK,
                )
                for _ in range(ASTEROID_SPLIT_COUNT)
            ]
        else:
            return []

    @classmethod
    def load_images(cls):
        if cls.IMAGES == None:
            cls.IMAGES = load_asteroid_images()
