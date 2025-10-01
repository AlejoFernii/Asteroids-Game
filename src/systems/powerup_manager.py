import pygame as pg
import random
from entities.powerup import Powerup


class PowerupManager:
    def __init__(self, min_delay=3000, max_delay=10000, lifetime=8000):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.lifetime = lifetime

        self.active_powerup = None
        self.next_spawn_time = pg.time.get_ticks() + random.randint(
            min_delay, max_delay
        )

    def update(self, powerups):
        now = pg.time.get_ticks()

        # If no active powerup, check if it’s time to spawn one
        if self.active_powerup is None and now >= self.next_spawn_time:
            powerup = Powerup(
                rank=random.choice([Powerup.RANK_1, Powerup.RANK_2, Powerup.RANK_3])
            )
            self.active_powerup = {"object": powerup, "spawn_time": now}
            powerups.append(powerup)

        # If there is an active powerup, check its lifetime
        if self.active_powerup is not None:
            if now - self.active_powerup["spawn_time"] >= self.lifetime:
                # Expire the powerup
                if self.active_powerup["object"] in powerups:
                    powerups.remove(self.active_powerup["object"])
                self._reset_timer()

    def pickup(self, powerup, powerups):
        """Call this when the player collides with a powerup."""
        if self.active_powerup and self.active_powerup["object"] == powerup:
            if powerup in powerups:
                powerups.remove(powerup)
            self._reset_timer()

    def _reset_timer(self):
        self.active_powerup = None
        self.next_spawn_time = pg.time.get_ticks() + random.randint(
            self.min_delay, self.max_delay
        )
