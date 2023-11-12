from pico2d import load_image

class Map:
    def __init__(self):
        self.image = load_image('map.jpg')

    def draw(self):
        self.image.draw(600, 300)  # 적절한 위치로 조절
        # 추가적인 그리기 로직이 있다면 여기에 추가

    def update(self):
        # 추가적인 업데이트 로직이 있다면 여기에 추가
        pass