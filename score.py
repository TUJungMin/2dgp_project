from pico2d import *

import random


class Score:
    def __init__(self):
        self.score = 0
        self.font = load_font('ENCR10B.TTF', 30)
        self.combo = 0


    def draw(self):
        self.font.draw(500, 650, f'score: {self.score}', (255, 255, 0))
        self.font.draw(1000, 600, f'combo: {self.combo}', (255, 0, 0))

    def initial(self):
        self.score = 0
        self.combo = 0

