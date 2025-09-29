import math


def circle_collision(obj1_x, obj1_y, obj1_radius, obj2_x, obj2_y, obj2_radius):
    dx = obj1_x - obj2_x
    dy = obj1_y - obj2_y
    distance = math.hypot(dx, dy)

    return distance < obj1_radius + obj2_radius


def bullet_asteroid_collision(bullet, asteroid):
    return circle_collision(
        bullet.x, bullet.y, bullet.radius, asteroid.x, asteroid.y, asteroid.size
    )


def ship_asteroid_collision(ship, asteroid):
    return circle_collision(
        ship.x, ship.y, ship.size, asteroid.x, asteroid.y, asteroid.size
    )
