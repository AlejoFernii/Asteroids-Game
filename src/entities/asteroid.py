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


class Asteroid:

    LARGE_RANK = 100
    MEDIUM_RANK = 250
    SMALL_RANK = 500

    def __init__(self, x=None, y=None, size=40, image=None, rank=100):
        self.x = x if x is not None else random.randint(0, SCREEN_WIDTH)
        self.y = y if y is not None else random.randint(0, SCREEN_HEIGHT)

        angle = random.uniform(0, 360)
        speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)

        self.velocity_x = math.cos(math.radians(angle)) * speed
        self.velocity_y = -math.sin(math.radians(angle)) * speed

        self.size = size
        self.alive = True
        self.image = image if image else load_asteroid_images()["large"]
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
                    image=load_asteroid_images()["medium"],
                    rank=self.choose_rank("medium"),
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
                    image=load_asteroid_images()["small"],
                    rank=self.choose_rank("small"),
                )
                for _ in range(ASTEROID_SPLIT_COUNT)
            ]
        else:
            return []

    def collides_with(self, ship):
        dx = self.x - ship.x
        dy = self.y - ship.y
        distance = math.hypot(dx, dy)

        return distance < self.size + ship.size

    def choose_rank(cls, rank="large"):
        if rank == "small":
            return cls.SMALL_RANK
        elif rank == "medium":
            return cls.MEDIUM_RANK
        else:
            return cls.LARGE_RANK
