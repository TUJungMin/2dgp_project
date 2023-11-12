from pico2d import *

WIDTH, HEIGHT = 1200, 700  # 화면 크기
background_path = 'map.jpg'  # 배경 사진 파일 경로
cursor_path = 'scope.png'  # 마우스 커서 이미지 파일 경로
x_pos,y_pos = 0,0
def reset_world():
    global background, cursor
    background = load_image(background_path)
    cursor = load_image(cursor_path)


def render_world(mx, my):
    clear_canvas()
    background.draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
    cursor.draw(mx, my, 100, 50)  # 마우스 위치에 따라 커서 그리기
    update_canvas()

def get_mouse_pos():
    global x_pos,y_pos
    x, y = x_pos, y_pos
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEMOTION:
            x, y = event.x, HEIGHT - event.y - 1  # Y 좌표는 화면의 반전된 값으로 처리
            x_pos, y_pos = x, y
            break  # 마우스 이벤트를 하나만 처리하고 나머지 이벤트는 무시

    return x, y

open_canvas(WIDTH, HEIGHT)
reset_world()

# game loop
running = True

while running:
    mx, my = get_mouse_pos()  # 마우스의 현재 위치 얻기
    render_world(mx, my)
    delay(0.01)

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False

# finalization code
close_canvas()