import pygame
from arcade_machine_sdk import GameMeta
from game import SnakeGame

if not pygame.get_init():
    pygame.init()

game_meta = (
    GameMeta()
    .with_title("Juego de la Serpiente")
    .with_description("Juego Clasico de la Serpiente")
    .with_release_date("2026-02-27")
    .with_tags(["arcade", "snake", "retro"])
    .with_group_number(7)
    .with_authors(["Hemberth Garcia", "Eduardo Diaz"])
)

game = SnakeGame(game_meta)

if __name__ == "__main__":
    game.run_independently()