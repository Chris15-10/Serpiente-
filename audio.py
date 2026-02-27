import pygame
from pathlib import Path


class AudioManager:

    def __init__(self):

        self.BASE_DIR = Path(__file__).resolve().parent
        self.ASSETS_DIR = self.BASE_DIR / "assets"

        pygame.mixer.init()

        pygame.mixer.music.load(str(self.ASSETS_DIR / "menu_music.wav"))
        pygame.mixer.music.set_volume(0.4)

        self.eat_sound = pygame.mixer.Sound(str(self.ASSETS_DIR / "eat.wav"))
        self.eat_sound.set_volume(0.4)

    def play_menu_music(self):
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_eat(self):
        self.eat_sound.play()