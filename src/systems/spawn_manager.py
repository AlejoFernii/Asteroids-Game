import random

from entities.asteroid import Asteroid
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE

from assets_loader import load_asteroid_images


class SpawnManager:
    def __init__(self):
        self.asteroid_count = 5
        self.asteroid_images = load_asteroid_images()

    def spawn_asteroids(self, count=None):
        num = count if count else self.asteroid_count
        return [Asteroid() for _ in range(num)]

    def spawn_asteroid_at_position(self, x, y, size=40):
        return Asteroid(x, y, size)
