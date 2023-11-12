from pico2d import *
from math import radians, sin, cos, sqrt
import random

target_path = 'beer.png'  # 맥주병 이미지 파일 경로

class Beer:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.image = load_image(target_path)
        self.angle = 0  # 초기 회전 각도
        self.time = 0
        self.direction = direction

        if self.direction == 1:
            self.initial_velocity = 1  # 초기 속도 (왼쪽에서 오른쪽으로)
        else:
            self.initial_velocity = -1  # 초기 속도 (오른쪽에서 왼쪽으로)

    def draw(self):
        self.image.rotate_draw(radians(self.angle), self.x, self.y, 300, 100)

    def update(self):
        gravity = 0  # 중력 가속도를 0으로 설정하여 직선 운동으로 변경
        angle_radians = radians(self.angle)

        self.x += self.initial_velocity * cos(angle_radians) * self.time
        self.y += self.initial_velocity * sin(angle_radians) * self.time - gravity * (self.time ** 2)

        self.time += 0.1  # 시간 증가

    def is_clicked(self, mx, my):
        distance = sqrt((self.x - mx) ** 2 + (self.y - my) ** 2)
        return distance <= 100
