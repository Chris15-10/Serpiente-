import pygame
from arcade_machine_sdk import BASE_WIDTH, BASE_HEIGHT


class Interface:

    def __init__(self):
        pygame.font.init()

        self.block = 32
        self.big_font = pygame.font.SysFont("arial", 80)
        self.medium_font = pygame.font.SysFont("arial", 45)
        self.small_font = pygame.font.SysFont("arial", 30)

    def draw_grid(self, surface):

        grid_color = (35, 35, 35)

        for x in range(0, BASE_WIDTH, self.block):
            pygame.draw.line(surface, grid_color, (x, 0), (x, BASE_HEIGHT))

        for y in range(0, BASE_HEIGHT, self.block):
            pygame.draw.line(surface, grid_color, (0, y), (BASE_WIDTH, y))

    def draw_menu(self, surface, selected_option, options):

        title = self.big_font.render("Juego de la Serpiente", True, (0, 255, 150))
        surface.blit(title, (BASE_WIDTH // 2 - title.get_width() // 2, 180))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected_option else (200, 200, 200)
            text = self.medium_font.render(option, True, color)
            surface.blit(text,
                         (BASE_WIDTH // 2 - text.get_width() // 2, 350 + i * 80))

    def draw_game_over(self, surface, score, highscore, difficulty):

        title = self.big_font.render("Game Over", True, (255, 50, 50))
        surface.blit(title,
                     (BASE_WIDTH // 2 - title.get_width() // 2, 220))

        score_text = self.medium_font.render(f"Puntuaje: {score}", True, (255, 255, 255))
        surface.blit(score_text,
                     (BASE_WIDTH // 2 - score_text.get_width() // 2, 330))

        highscore_text = self.medium_font.render(f"Record Maximo: {highscore}", True, (0, 255, 150))
        surface.blit(highscore_text,
                     (BASE_WIDTH // 2 - highscore_text.get_width() // 2, 380))

        difficulty_text = self.medium_font.render(f"Modo: {difficulty}", True, (180, 180, 180))
        surface.blit(difficulty_text,
                     (BASE_WIDTH // 2 - difficulty_text.get_width() // 2, 430))