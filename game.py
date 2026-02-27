import pygame
import random
from arcade_machine_sdk import BASE_WIDTH, BASE_HEIGHT, GameBase
from interface import Interface
from audio import AudioManager
from highscore import HighScoreManager


class SnakeGame(GameBase):

    def __init__(self, metadata):
        super().__init__(metadata)

        self.block = 32

        self.interface = Interface()
        self.audio = AudioManager()
        self.highscore_manager = HighScoreManager()

        self.menu_options = ["Facil", "Dificil"]
        self.selected_option = 0

    def start(self, surface):
        super().start(surface)
        self.reset()
        self.audio.play_menu_music()
    
    def stop(self):
        super().stop()
        self.audio.stop_music()

    def reset(self):
        self.snake = [(BASE_WIDTH // 2, BASE_HEIGHT // 2)]
        self.direction = "STOP"
        self.food = self.generate_food()
        self.score = 0
        self.state = "MENU"
        self.difficulty = None
        self.move_timer = 0
        self._running = True

    def start_game(self):

        self.audio.stop_music()

        if self.selected_option == 0:
            self.difficulty = "Facil"
            self.speed = 8
            self.speed_increment = 0.5
        else:
            self.difficulty = "Dificil"
            self.speed = 14
            self.speed_increment = 1.2

        self.state = "PLAYING"

    def generate_food(self):
        return (
            random.randrange(0, BASE_WIDTH, self.block),
            random.randrange(0, BASE_HEIGHT, self.block)
        )

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if self.state == "MENU":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.start_game()

                elif self.state == "PLAYING":
                    if event.key in (pygame.K_UP, pygame.K_w) and self.direction != "DOWN":
                        self.direction = "UP"
                    if event.key in (pygame.K_DOWN, pygame.K_s) and self.direction != "UP":
                        self.direction = "DOWN"
                    if event.key in (pygame.K_LEFT, pygame.K_a) and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    if event.key in (pygame.K_RIGHT, pygame.K_d) and self.direction != "LEFT":
                        self.direction = "RIGHT"

                elif self.state == "GAME_OVER":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.reset()
                        self.audio.play_menu_music()

    # SDK USA dt
    def update(self, dt):

        if self.state != "PLAYING" or self.direction == "STOP":
            return

        self.move_timer += dt

        if self.move_timer < 1 / self.speed:
            return

        self.move_timer = 0

        x, y = self.snake[0]

        if self.direction == "UP":
            y -= self.block
        if self.direction == "DOWN":
            y += self.block
        if self.direction == "LEFT":
            x -= self.block
        if self.direction == "RIGHT":
            x += self.block

        new_head = (x, y)
        self.snake.insert(0, new_head)

        if x < 0 or x >= BASE_WIDTH or y < 0 or y >= BASE_HEIGHT:
            self.highscore_manager.update(self.score)
            self.state = "GAME_OVER"

        if new_head == self.food:
            self.food = self.generate_food()
            self.score += 10
            self.speed += self.speed_increment
            self.audio.play_eat()
        else:
            self.snake.pop()

        if new_head in self.snake[1:]:
            self.highscore_manager.update(self.score)
            self.state = "GAME_OVER"

    def render(self):

        surface = self.surface
        surface.fill((15, 15, 15))
        self.interface.draw_grid(surface)

        if self.state == "MENU":
            self.interface.draw_menu(surface,
                                    self.selected_option,
                                    self.menu_options)

        elif self.state == "PLAYING":
            # Draw food
            pygame.draw.rect(surface, (255, 50, 50),
                             (self.food[0], self.food[1], self.block, self.block))
            
            # Draw snake
            for i, segment in enumerate(self.snake):
                color = (0, 255, 100) if i == 0 else (0, 200, 80)
                pygame.draw.rect(surface, color,
                                 (segment[0], segment[1], self.block, self.block))
            
            # Draw score
            score_text = self.interface.small_font.render(f"Puntuaje: {self.score}", True, (255, 255, 255))
            surface.blit(score_text, (10, 10))

        elif self.state == "GAME_OVER":
            self.interface.draw_game_over(
                surface,
                self.score,
                self.highscore_manager.highscore,
                self.difficulty
            )