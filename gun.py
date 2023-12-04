from pico2d import *
import time

from math import radians, sin, cos, sqrt
import random

target_path = 'gun.png'  # 맥주병 이미지 파일 경로

class Gun:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image(target_path)
        self.frame = 0
        self.bullet = 6
        self.reloading = False
        self.reload_start_time = 0

    def reload(self):
        self.bullet = 0
        self.reloading = True
        self.reload_start_time = time.time()
        self.bgm = load_wav('reload.wav')
        self.bgm.set_volume(20)
        self.bgm.play(1)

    def update(self):
        if self.reloading and time.time() - self.reload_start_time > 1:
            self.bullet = 6
            self.reloading = False

    def draw(self):
        if self.bullet ==6:
            self.image.clip_draw(166, 0, 166, 166, self.x, self.y)

        if self.bullet ==5:
            self.image.clip_draw(332, 166, 166, 166, self.x, self.y)

        if self.bullet ==4:
            self.image.clip_draw(166, 166, 166, 166, self.x, self.y)

        if self.bullet ==3:
            self.image.clip_draw(0, 166, 166, 166, self.x, self.y)

        if self.bullet ==2:
            self.image.clip_draw(332, 332, 166, 166, self.x, self.y)

        if self.bullet ==1:
            self.image.clip_draw(166, 332, 166, 166, self.x, self.y)

        if self.bullet ==0:
            self.image.clip_draw(0, 332, 166, 166, self.x, self.y)

        if self.bullet == 0 and not self.reloading:
            self.reload()

    def shoot(self):
        if self.bullet == 0:
            return False
        else:
            return True

        #2048 * 2048







