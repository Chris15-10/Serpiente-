from pathlib import Path


class HighScoreManager:

    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        self.file_path = self.BASE_DIR / "highscore.txt"
        self.highscore = self.load()

    def load(self):
        try:
            with open(self.file_path, "r") as file:
                return int(file.read())
        except:
            return 0

    def save(self):
        with open(self.file_path, "w") as file:
            file.write(str(self.highscore))

    def update(self, score):
        if score > self.highscore:
            self.highscore = score
            self.save()