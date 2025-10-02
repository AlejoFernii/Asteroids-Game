import pygame as pg


def load_ship_image():
    return pg.image.load("assets/images/Ship.png").convert_alpha()


def load_asteroid_images():
    return {
        "large": pg.image.load("assets/images/Asteroid-Spawn.png").convert_alpha(),
        "medium": pg.image.load("assets/images/Asteroid-Large.png").convert_alpha(),
        "small": pg.image.load("assets/images/Asteroid-Med.png").convert_alpha(),
    }


def load_bg():
    return pg.image.load("assets/images/asteroids-bg.png").convert()


def load_powerups():
    return {
        "rank_1": pg.image.load("assets/images/powerup-1.png").convert_alpha(),
        "rank_2": pg.image.load("assets/images/powerup-2.png").convert_alpha(),
        "rank_3": pg.image.load("assets/images/powerup-3.png").convert_alpha(),
        "life": pg.image.load("assets/images/powerup-life.png").convert_alpha(),
    }
