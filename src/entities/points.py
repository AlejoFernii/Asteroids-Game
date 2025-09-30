import pygame as pg

from settings import DEEP_SKY_BLUE, WHITE


class Point:
    def __init__(self, spawn_point, amount=100):
        self.x = spawn_point.x
        self.y = spawn_point.y
        self.amount = amount
        self.rect = spawn_point.rect
        self.font = pg.font.SysFont(None, 36)

    def update(self):
        self.rect.y -= 5

    def draw(self, surface):

        point_text = self.font.render(f"+{self.amount}", True, DEEP_SKY_BLUE)
        surface.blit(point_text, self.rect)
        # pg.display.flip()
