
from pico2d import *


target_path = 'beer.png'  # 맥주병 이미지 파일 경로
class Beer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image(target_path)

    def draw(self):
        self.image.draw(self.x, self.y, 200, 100)
