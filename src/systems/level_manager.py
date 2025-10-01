import pygame as pg

from .spawn_manager import SpawnManager


class LevelManager:

    INIT_ASTEROID_COUNT = 3

    def __init__(self, spawn_manger, ship):
        self.level = 1
        self.asteroids_to_spawn = self.INIT_ASTEROID_COUNT
        self.spawn_manager = spawn_manger
        self.ship = ship

    def new_level(self, asteroids):

        self.ship.game_start()
        self.ship.lives += 1
        new_asteroids = self.spawn_manager.spawn_asteroids(
            count=(self.asteroids_to_spawn)
        )
        asteroids.extend(new_asteroids)

    def check_status(self, asteroids):
        if len(asteroids) == 0:
            self.level += 1
            self.asteroids_to_spawn += 1
            self.new_level(asteroids)
        # print(f"Level : {self.level}, Asteroids: {self.asteroids_to_spawn}")
