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
