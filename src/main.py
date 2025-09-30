import pygame as pg
import sys
import math

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK

from entities.ship import Ship
from entities.bullet import Bullet
from entities.asteroid import Asteroid
from entities.points import Point

from systems.ui import UI
from systems.collision import ship_asteroid_collision, bullet_asteroid_collision
from systems.spawn_manager import SpawnManager

from assets_loader import load_bg

GAME_TITLE = "Asteroids Clone"


def main():

    # Initialize pygame
    pg.init()

    # Create the screen
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption(GAME_TITLE)
    bg = load_bg()
    bg = pg.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create Clock to manage frame rate
    clock = pg.time.Clock()

    spawn_manager = SpawnManager()

    # Entity Intances
    ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    bullets = []
    asteroids = spawn_manager.spawn_asteroids()
    points = []

    ui = UI()
    # score = 0
    start_game = False

    # Start Menu Loop
    while not start_game:
        ui.draw_start_menu(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    start_game = True

    # Game Loop
    running = True
    ship.game_start()
    while running:

        # ---Event handeling---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bullets.append(ship.shoot(pg.mouse.get_pos()))

        # ---Input + Updates---
        keys = pg.key.get_pressed()
        ship.handle_input(keys)

        # Update Ship
        ship.update()

        # Update Bullets
        for bullet in bullets[:]:
            bullet.update()
            if not bullet.is_alive():
                bullets.remove(bullet)

        # Update Asteroids
        for asteroid in asteroids:
            asteroid.update()

        # Update Point Icons
        for point in points:
            point.update()

        # Check Bullet-Asteroid Collision
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if bullet_asteroid_collision(bullet, asteroid):
                    bullets.remove(bullet)

                    ui.update_score(asteroid.rank)

                    new_asteroids = asteroid.split()
                    new_point = Point(amount=asteroid.rank, spawn_point=asteroid)
                    points.append(new_point)

                    asteroids.remove(asteroid)
                    asteroids.extend(new_asteroids)

                    break

        # Check Ship-Asteroid Collision
        for asteroid in asteroids:
            if ship.invincibility_timer == 0 and ship_asteroid_collision(
                ship, asteroid
            ):
                ship.take_hit()
                if ship.lives <= 0:

                    print("Game Over!")
                    running = False
                break

        # ---Draw---

        # Draw Background
        screen.blit(bg, (0, 0))

        # Draw Ship
        ship.draw(screen)

        # Draw Bullets
        for bullet in bullets:
            bullet.draw(screen)

        # Draw Asteroids
        for asteroid in asteroids:
            asteroid.draw(screen)

        # Draw Point Icons
        for point in points:
            point.draw(screen)

        # Draw UI HUD
        ui.draw(screen, ship)

        pg.display.flip()
        clock.tick(FPS)
        # End of Game Loop

    game_over = True
    while game_over:
        ui.draw_game_over(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    main()
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()


if __name__ == "__main__":
    main()
