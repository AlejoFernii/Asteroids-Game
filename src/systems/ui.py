import pygame as pg
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK

from assets_loader import load_bg


class UI:
    BG = None

    def __init__(self, level_manager):
        self.font = pg.font.SysFont(None, 36)
        self.large_font = pg.font.SysFont(None, 72)
        self.score = 0
        self.level_manager = level_manager
        # Create Overlay
        self.overlay = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.set_alpha(150)
        self.overlay.fill(BLACK)

    def update_score(self, rank, powerup_rank):
        self.score += rank * powerup_rank

    def draw(self, surface, ship):
        # Draw Lives
        lives_text = self.font.render(f"Lives: {ship.lives}", True, WHITE)
        surface.blit(lives_text, (10, 10))

        score_text = self.font.render(f"Score: {self.score:,.0f}", True, WHITE)
        surface.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, 10))

        level_text = self.font.render(f"Level: {self.level_manager.level}", True, WHITE)
        surface.blit(level_text, ((SCREEN_WIDTH - level_text.get_width()) - 10, 10))

    def draw_start_menu(self, surface):
        surface.blit(self.BG, (0, 0))
        surface.blit(self.overlay, (0, 0))

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

    def draw_game_over(self, surface):
        surface.blit(self.BG, (0, 0))
        surface.blit(self.overlay, (0, 0))

        game_over_text = self.large_font.render("GAME OVER", True, WHITE)
        score_text = self.font.render(f"Final Score: {self.score:,.0f}", True, WHITE)
        prompt_text = self.font.render(
            "Press ENTER to Restart or ESC to Quit", True, WHITE
        )
        level_text = self.font.render(
            f"Highest Level: {self.level_manager.level}", True, WHITE
        )

        surface.blit(
            game_over_text,
            ((SCREEN_WIDTH - game_over_text.get_width()) // 2, SCREEN_HEIGHT // 4),
        )
        surface.blit(
            level_text,
            ((SCREEN_WIDTH - level_text.get_width()) // 2, SCREEN_HEIGHT // 2.5),
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

    @classmethod
    def load_bg_image(cls):
        if cls.BG is None:  # only load once
            cls.BG = load_bg()
