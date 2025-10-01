import pygame as pg

from settings import DEEP_SKY_BLUE, WHITE, POINTS_LIFETIME


class Point:
    def __init__(self, spawn_point, amount=100, is_powerup=False, powerup_rank=1):
        self.x = spawn_point.x
        self.y = spawn_point.y
        self.amount = amount
        self.rect = spawn_point.rect
        self.font = pg.font.SysFont(None, 36)
        self.lifetime = POINTS_LIFETIME
        self.is_powerup = is_powerup
        self.powerup_rank = powerup_rank

    def update(self):
        self.rect.y -= 5
        self.lifetime -= 1

    def draw(self, surface):

        point_text = self.font.render(
            f"+{self.amount * self.powerup_rank:,.0f}", True, DEEP_SKY_BLUE
        )
        surface.blit(point_text, self.rect)
        # pg.display.flip()

    def is_alive(self):
        return self.lifetime > 0
