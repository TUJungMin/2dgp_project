from pico2d import *
from beer import Beer
import random

WIDTH, HEIGHT = 1200, 700  # 화면 크기
map = 'map.jpg'  # 배경 사진 파일 경로
cursor_path = 'scope.png'  # 마우스 커서 이미지 파일 경로
start = 'startsscreen.png'  # 마우스 커서 이미지 파일 경로
process = 0
round  = 1

x_pos, y_pos = 0, 0
beers = []  # 맥주병 객체들을 저장할 리스트
beer_timer = 0
beer_interval = 1  # 1초마다 맥주 생성
world = []
def reset_world():
    global process,background, cursor
    background = load_image(start)
    cursor = load_image(cursor_path)
    hide_cursor()

def render_world(mx, my):
    global process, background
    clear_canvas()

    if process == 0:
        background = load_image(start)
    else:
        background = load_image(map)

    background.draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
    cursor.draw(mx, my, 100, 50)

    for beer in beers:
        beer.draw()

    update_canvas()

def update_world():
    global beers
    for beer in beers:
        beer.update()

def handle_mouse_events(mx, my):
    global process
    if process == 0 and (450 <= mx <= 750) and (100 <= my <= 200):
        process = 1
        #reset_world()
    else:
        clicked_beers = [beer for beer in beers if beer.is_clicked(mx, my)]
        for clicked_beer in clicked_beers:
            beers.remove(clicked_beer)

MAX_BEER_COUNT = 10  # 최대 맥주 객체 개수

def generate_beer():
    global beer_timer, round
    if process == 1 and len(beers) < MAX_BEER_COUNT:  # process가 1이고 맥주 개수가 최대 개수보다 작을 때만 생성
        direction = random.choice([1, 2])
        if direction == 1:
            beers.append(Beer(-100, random.randint(400, HEIGHT), direction, round))
        else:
            beers.append(Beer(WIDTH + 100, random.randint(400, HEIGHT), direction, round))
        beer_timer = get_time()


def get_mouse_pos():
    global x_pos, y_pos
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

    # 2초마다 맥주 생성
    if(process != 0):
        if get_time() - beer_timer > beer_interval:
            generate_beer()

    update_world()

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            # 왼쪽 마우스 버튼 클릭 시 맥주병 제거
            mx, my = get_mouse_pos()
            handle_mouse_events(mx, my)

    delay(0.01)

# finalization code
close_canvas()