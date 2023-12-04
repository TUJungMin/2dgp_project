from pico2d import *
from beer import Beer
from cure import Cure
import random
from heart import Heart
from gamesound import Gunsound,Bottlesound
import time

WIDTH, HEIGHT = 1200, 700  # 화면 크기
map = 'map.jpg'  # 배경 사진 파일 경로
cursor_path = 'scope.png'  # 마우스 커서 이미지 파일 경로
start = 'startsscreen.png'  # 마우스 커서 이미지 파일 경로
gameover = 'gameover.png'
process = 0
round  = 1

x_pos, y_pos = 0, 0
beers = []  # 맥주병 객체들을 저장할 리스트
cures = []
beer_timer = 0
beer_interval = 1  # 1초마다 맥주 생성
beer_count = [0,10,20,30]
current_beercount = 0
current_curecount = 0

hearts = []  # 하트 객체들을 저장할 리스트
heart_size = 50  # 하트 크기
heart_padding = 10  # 하트 간격
heart_count = 3
collision = 0

def reset_world():
    global process, background, cursor
    background = load_image(start)
    cursor = load_image(cursor_path)
    hide_cursor()
    for i in range(heart_count):
        heart = Heart(WIDTH - (i + 1) * (heart_size + heart_padding), HEIGHT - heart_size, heart_size)
        hearts.append(heart)
def render_world(mx, my):
    global process, background
    clear_canvas()

    if process == 0:
        background = load_image(start)
    else:
        if process == 4:
            background = load_image(gameover)
        else:
            background = load_image(map)

    background.draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    if process != 4:
        for beer in beers:
            beer.draw()
        for cure in cures:  # Cure 객체들 그리기
            cure.draw()

    # process가 1일 때, 화면 우측 상단에 하트 그리기
    if process != 0 and process != 4:
        for heart in hearts:
            heart.draw(1)

    cursor.draw(mx, my, 100, 50)
    update_canvas()
def update_world():
    global beers,process,round,current_beercount,cures
    for beer in beers:
        beer.update()
        if beer.x < -100 or beer.x > WIDTH + 100:
            beers.remove(beer)
    for cure in cures:
        cure.update()
        if cure.x < -100 or cure.x > WIDTH + 100:
            cures.remove(cure)
            if len(beers) == 0:  # 맥주가 모두 사라졌을 때
                if process != 4:  # 프로세스가 4가 아닐 때에만 실행
                    process += 1
                    round += 1
                    current_beercount = 0
                    show_image_for_time('stage_clear.png', 2)

def show_image_for_time(image_path, duration):
    start_time = time.time()
    image = load_image(image_path)

    while time.time() - start_time < duration:

        image.draw(WIDTH // 2, HEIGHT // 2,600,500)
        update_canvas()
        delay(0.01)
def handle_mouse_events(mx, my):
    global process, hearts, current_beercount,round,collision

    if process == 0 and (450 <= mx <= 750) and (100 <= my <= 200):
        process = 1
        #reset_world()
    else:
        clicked_beers = [beer for beer in beers if beer.is_clicked(mx, my)]
        if not clicked_beers and len(hearts) > 0:  # 맥주와 충돌하지 않았고, 하트가 남아있을 때만
            if process !=0:
                hearts.pop()  # 하트를 제거
                if len(hearts) == 0:  # 하트가 모두 사라졌을 때
                    process = 4
        else:

            for clicked_beer in clicked_beers:
                beers.remove(clicked_beer)
                collision = 1

            if len(beers) == 0:  # 맥주가 모두 사라졌을 때
                if process != 4:  # 프로세스가 4가 아닐 때에만 실행
                    process += 1
                    round += 1
                    current_beercount = 0
                    show_image_for_time('stage_clear.png', 2)

def generate_beer():
    global beer_timer, round, current_beercount
    if process != 0 and process != 4 and current_beercount < beer_count[round]:
        direction = random.choice([1, 2])
        if direction == 1:
            beers.append(Beer(-100, random.randint(400, HEIGHT), direction, round))
            current_beercount += 1
        else:
            beers.append(Beer(WIDTH + 100, random.randint(400, HEIGHT), direction, round))
            current_beercount += 1
        beer_timer = get_time()


def generate_cure():
    global current_curecount, round,beer_timer
    if process != 0 and process != 4 and current_curecount < beer_count[round]:
        direction = random.choice([1, 2])
        if direction == 1:
            cures.append(Cure(-100, random.randint(400, HEIGHT), direction, round))
            current_curecount += 1
        else:
            cures.append(Cure(WIDTH + 100, random.randint(400, HEIGHT), direction, round))
            current_curecount += 1

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
            generate_cure()

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
            if(collision == 1):
                bottle_sound = Bottlesound()
            else:
                if(collision == 2):
                    gun_sound = Gunsound()  # Gunsound 객체 생성)
            collision = 0

    delay(0.01)

# finalization code
close_canvas()