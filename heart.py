from pico2d import *
class Heart:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.image = load_image('heart.png')  # 하트 이미지 파일 경로

    def draw(self, count):
        for i in range(count):
            self.image.draw(self.x - i * (self.size + 5), self.y, self.size, self.size)