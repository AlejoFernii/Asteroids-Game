import pygame as pg
import sys
import math
import random

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK

from entities.ship import Ship
from entities.bullet import Bullet
from entities.asteroid import Asteroid
from entities.points import Point
from entities.powerup import Powerup

from systems.ui import UI
from systems.collision import ship_asteroid_collision, bullet_asteroid_collision
from systems.spawn_manager import SpawnManager
from systems.powerup_manager import PowerupManager
from systems.level_manager import LevelManager

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

    Powerup.load_images()

    # Create Clock to manage frame rate
    clock = pg.time.Clock()

    spawn_manager = SpawnManager()
    powerup_manager = PowerupManager()

    # Entity Intances
    ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroids = spawn_manager.spawn_asteroids(count=2)
    bullets = []
    points = []
    powerups = []

    level_manager = LevelManager(spawn_manager, ship)
    ui = UI(level_manager)
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
        for point in points[:]:
            point.update()
            if not point.is_alive():
                points.remove(point)

        # Update Powerups
        powerup_manager.update(powerups)

        # Check Bullet-Asteroid Collision
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if bullet_asteroid_collision(bullet, asteroid):
                    bullets.remove(bullet)

                    ui.update_score(asteroid.rank, bullet.powerup_rank)

                    new_asteroids = asteroid.split()
                    new_point = Point(
                        amount=asteroid.rank,
                        spawn_point=asteroid,
                        powerup_rank=bullet.powerup_rank,
                    )
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
        for powerup in powerups[:]:
            powerup.update()
            if ship.rect.colliderect(powerup.rect):
                powerup_manager.pickup(powerup, powerups)
                ship.activate_powerup(powerup.rank)

        # Check Level Status

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

        # Draw Powerups
        for powerup in powerups:
            powerup.draw(screen)

        # Draw UI HUD
        ui.draw(screen, ship)

        level_manager.check_status(asteroids=asteroids)
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
