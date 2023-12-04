from pico2d import *
from math import radians, sin, cos, sqrt
import random

target_path = 'beer.png'  # 맥주병 이미지 파일 경로

class Beer:
    def __init__(self, x, y, direction, round):
        self.x = x
        self.y = y
        self.image = load_image(target_path)
        self.angle = 0  # 초기 회전 각도
        self.time = 0
        self.direction = direction
        self.round = round
        if self.direction == 1:
            self.initial_velocity_x = 7  # 초기 속도 (왼쪽에서 오른쪽으로)
        else:
            self.initial_velocity_x = -7 # 초기 속도 (오른쪽에서 왼쪽으로)

    def draw(self):

        self.image.rotate_draw(radians(self.angle), self.x, self.y, 300, 100)
        #draw_rectangle(self.x - 30, self.y - 50, self.x + 30, self.y + 50)  # 바운딩 박스를 그립니다. (크기는 50x50)

    def update(self):
        gravity = 0.1  # 중력 가속도를 0으로 설정하여 직선 운동으로 변경
        self.angle += 5 * self.round
        if self.angle > 360:
            self.angle = 0

        self.x += self.initial_velocity_x * self.round * 1.5



        self.time += 0.1  # 시간 증가

    def is_clicked(self, mx, my):
        half_width = 30  # 바운딩 박스의 가로 길이의 절반
        half_height = 50  # 바운딩 박스의 세로 길이의 절반

        if (self.x - half_width) <= mx <= (self.x + half_width) and (self.y - half_height) <= my <= (
                self.y + half_height):
            return True  # 바운딩 박스 내부를 클릭했을 경우
        else:
            return False  # 바운딩 박스 내부를 클릭하지 않았을 경우

