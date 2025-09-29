import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK


class UI:
    def __init__(self):
        self.font = pg.font.SysFont(None, 36)
        self.large_font = pg.font.SysFont(None, 72)

    def draw(self, surface, ship, score):
        # Draw Lives
        lives_text = self.font.render(f"Lives: {ship.lives}", True, WHITE)
        surface.blit(lives_text, (10, 10))

        score_text = self.font.render(f"Score: {score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH - 150, 10))

    def draw_start_menu(self, surface):
        surface.fill(BLACK)
        title_text = self.large_font.render("Asteroids Clone", True, WHITE)
        prompt_text = self.font.render("Press Enter to Start", True, WHITE)

        # Center Title
        surface.blit(
            title_text,
            ((SCREEN_WIDTH - title_text.get_width()) // 2, SCREEN_HEIGHT // 3),
        )
        surface.blit(
            prompt_text,
            ((SCREEN_WIDTH - prompt_text.get_width()) // 2, SCREEN_HEIGHT // 2),
        )
        pg.display.flip()

    def draw_game_over(self, surface, score):
        surface.fill(BLACK)
        game_over_text = self.large_font.render("GAME OVER", True, WHITE)
        score_text = self.font.render(f"Final Score: {score}", True, WHITE)
        prompt_text = self.font.render(
            "Press ENTER to Restart or ESC to Quit", True, WHITE
        )

        surface.blit(
            game_over_text,
            ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 4),
        )
        surface.blit(
            score_text,
            ((SCREEN_WIDTH - score_text.get_width()) // 2, SCREEN_HEIGHT // 2),
        )
        surface.blit(
            prompt_text,
            ((SCREEN_WIDTH - prompt_text.get_width()) // 2, SCREEN_HEIGHT // 1.5),
        )

        pg.display.flip()
