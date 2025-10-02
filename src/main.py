import pygame as pg
import sys
import math
import random

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, GAME_TITLE

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


def main():

    # Initialize pygame
    pg.init()

    # Create the screen
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption(GAME_TITLE)
    bg = load_bg()
    bg = pg.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    Powerup.load_images()
    UI.load_bg_image()
    Asteroid.load_images()

    # Create Clock to manage frame rate
    clock = pg.time.Clock()
    spawn_manager = SpawnManager()

    # Entity Intances
    ship = Ship(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    level_manager = LevelManager(spawn_manager, ship)
    powerup_manager = PowerupManager()
    asteroids = pg.sprite.Group(spawn_manager.spawn_asteroids(count=2))
    bullets = pg.sprite.Group()
    points = []

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
                    bullets.add(ship.shoot(pg.mouse.get_pos()))

        # ---Input + Updates---
        keys = pg.key.get_pressed()
        ship.handle_input(keys)

        # Update Ship
        ship.update()

        # Update Bullets
        bullets.update()

        # Update Asteroids
        asteroids.update()

        # Update Powerups
        powerup_manager.update()

        # Update Point Icons
        for point in points[:]:
            point.update()
            if not point.is_alive():
                points.remove(point)

        # Check Bullet-Asteroid Collision

        hits = pg.sprite.groupcollide(
            bullets, asteroids, True, True, collided=pg.sprite.collide_mask
        )

        for bullet, asteroid_list in hits.items():
            for asteroid in asteroid_list:
                # Update score
                ui.update_score(asteroid.rank, bullet.powerup_rank)

                # Split asteroid into smaller ones
                new_asteroids = asteroid.split()
                asteroids.add(new_asteroids)

                # Spawn floating score text/points
                new_point = Point(
                    amount=asteroid.rank,
                    spawn_point=asteroid,
                    powerup_rank=bullet.powerup_rank,
                )
                points.append(new_point)

        # Check Ship-Asteroid Collision
        if ship.invincibility_timer == 0:
            ship_hit = pg.sprite.spritecollide(
                ship, asteroids, False, collided=pg.sprite.collide_mask
            )

            if ship_hit:
                ship.take_hit()

                if ship.lives <= 0:
                    print("Game Over!")
                    running = False

        pickups = pg.sprite.spritecollide(ship, powerup_manager.group, dokill=True)
        for powerup in pickups:
            powerup_manager.pickup(powerup)
            ship.activate_powerup(powerup)

        # Check Level Status
        level_manager.check_status(asteroids=asteroids)

        # ---Draw---

        # Draw Background
        screen.blit(bg, (0, 0))

        # Draw Ship
        ship.draw(screen)

        # Draw Bullets
        bullets.draw(screen)

        # Draw Asteroids
        asteroids.draw(screen)

        # Draw Point Icons
        for point in points:
            point.draw(screen)

        # Draw Powerups
        powerup_manager.draw(screen)

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
