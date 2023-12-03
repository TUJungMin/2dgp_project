
from pico2d import *


class Gunsound:
    def __init__(self):
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.bgm = load_wav('gunsound.wav')
        self.bgm.set_volume(15)
        self.bgm.play(1)


class Bottlesound:
    def __init__(self):
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.bgm = load_wav('bottle_break.wav')
        self.bgm.set_volume(10)
        self.bgm.play(1)

