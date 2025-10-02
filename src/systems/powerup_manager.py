import pygame as pg
import random
from entities.powerup import Powerup


class PowerupManager:
    def __init__(
        self,
        min_delay=3000,
        max_delay=10000,
        lifetime=8000,
        life_min_delay=20000,
        life_max_delay=40000,
        life_lifetime=10000,
    ):
        # Settings per type
        self.settings = {
            "score": {
                "min_delay": min_delay,
                "max_delay": max_delay,
                "lifetime": lifetime,
                "next_spawn": pg.time.get_ticks()
                + random.randint(min_delay, max_delay),
                "active": None,
            },
            "life": {
                "min_delay": life_min_delay,
                "max_delay": life_max_delay,
                "lifetime": life_lifetime,
                "next_spawn": pg.time.get_ticks()
                + random.randint(life_min_delay, life_max_delay),
                "active": None,
            },
        }

        # Use a single Sprite Group for all active powerups
        self.group = pg.sprite.Group()

    def update(self):
        """Call this every frame"""
        now = pg.time.get_ticks()

        for ptype, setting in self.settings.items():
            # --- Spawn new powerup if none active ---
            if setting["active"] is None and now >= setting["next_spawn"]:
                if ptype == "score":
                    powerup = Powerup(
                        rank=random.choice(
                            [Powerup.RANK_1, Powerup.RANK_2, Powerup.RANK_3]
                        ),
                        type=Powerup.TYPE_SCORE,
                    )
                elif ptype == "life":
                    powerup = Powerup(type=Powerup.TYPE_LIFE)
                else:
                    continue

                setting["active"] = {"object": powerup, "spawn_time": now}
                self.group.add(powerup)  # Add to the Sprite group

            # --- Expire powerup after lifetime ---
            if setting["active"] is not None:
                if now - setting["active"]["spawn_time"] >= setting["lifetime"]:
                    powerup = setting["active"]["object"]
                    self.group.remove(powerup)
                    self._reset_timer(ptype)

        # --- Update all sprites ---
        self.group.update()

    def draw(self, surface):
        """Draw all active powerups"""
        self.group.draw(surface)

    def pickup(self, powerup):
        """Handles any powerup pickup; returns its type"""
        for ptype, setting in self.settings.items():
            if setting["active"] and setting["active"]["object"] == powerup:
                self.group.remove(powerup)
                self._reset_timer(ptype)
                return ptype

    def _reset_timer(self, ptype):
        setting = self.settings[ptype]
        setting["active"] = None
        setting["next_spawn"] = pg.time.get_ticks() + random.randint(
            setting["min_delay"], setting["max_delay"]
        )
