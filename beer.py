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
            self.initial_velocity_x = 1  # 초기 속도 (왼쪽에서 오른쪽으로)
            self.initial_velocity_y = 10
        else:
            self.initial_velocity_x = -1  # 초기 속도 (오른쪽에서 왼쪽으로)
            self.initial_velocity_y = 10

    def draw(self):
        self.image.rotate_draw(radians(self.angle), self.x, self.y, 300, 100)
        draw_rectangle(self.x - 25, self.y - 25, self.x + 25, self.y + 25)  # 바운딩 박스를 그립니다. (크기는 50x50)

    def update(self):
        gravity = 0.1  # 중력 가속도를 0으로 설정하여 직선 운동으로 변경
        angle_radians = radians(self.angle)

        self.x += self.initial_velocity_x * cos(angle_radians) * self.time
        self.y += self.initial_velocity_y * sin(angle_radians) * self.time - gravity * (self.time ** 2)

        self.time += 0.1  # 시간 증가

    def is_clicked(self, mx, my):
        distance_x = abs(self.x - mx)
        distance_y = abs(self.y - my)

        return distance_x <= 75 and distance_y <= 50