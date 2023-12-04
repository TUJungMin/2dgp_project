from pico2d import *
from beer import Beer
from cure import Cure
import random
from heart import Heart
from gamesound import Gunsound,Bottlesound,BGM
import time

WIDTH, HEIGHT = 1200, 700  # 화면 크기
map = 'map.jpg'  # 배경 사진 파일 경로
cursor_path = 'scope.png'  # 마우스 커서 이미지 파일 경로
start_screen = 'startsscreen.png'  # 마우스 커서 이미지 파일 경로
start,gameclear,gameover = 0,4,5
start_bgm = False
gameover_screen = 'gameover.png'
gameclear_screen = 'gameclear.png'
process = 0
round  = 1

x_pos, y_pos = 0, 0
beers = []  # 맥주병 객체들을 저장할 리스트
cures = []
beer_timer = 0
cure_timer = 0
beer_interval = 1  # 1초마다 맥주 생성
cure_interval = 1  #
#beer_count = [0,random.randint(10,15),random.randint(20,25),random.randint(25,30)]
beer_count = [0,1,2,3]
current_beercount = 0
current_curecount = 0

hearts = []  # 하트 객체들을 저장할 리스트
heart_size = 50  # 하트 크기
heart_padding = 10  # 하트 간격
heart_count = 3
collision = 0

def reset_world():
    global  background, cursor
    background = load_image(start_screen)
    cursor = load_image(cursor_path)
    hide_cursor()
    for i in range(heart_count):
        heart = Heart(WIDTH - (i + 1) * (heart_size + heart_padding), HEIGHT - heart_size, heart_size)
        hearts.append(heart)
def render_world(mx, my):
    global process, background,start_bgm


    if process == start:
        background = load_image(start_screen)
        if(start_bgm == False):
            bgm = BGM()
            start_bgm = True
    else:
        if process == gameover:
            background = load_image(gameover_screen)
        else:
            if process == gameclear:
                background = load_image(gameclear_screen)
            else:
                background = load_image(map)

    background.draw(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)

    if process != gameover:
        for beer in beers:
            beer.draw()
        for cure in cures:  # Cure 객체들 그리기
            cure.draw()

    # process가 1일 때, 화면 우측 상단에 하트 그리기
    if process != start and process != gameover:
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
                if process != gameover:  # 프로세스가 4가 아닐 때에만 실행
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

    if process == start and (450 <= mx <= 750) and (100 <= my <= 200):
        process = round

    else:
        clicked_beers = [beer for beer in beers if beer.is_clicked(mx, my)]
        clicked_cures = [cure for cure in cures if cure.is_clicked(mx, my)]
        if not clicked_beers and not clicked_cures and len(hearts) > 0:
            if process != start:
                hearts.pop()
                collision = 2
                if len(hearts) == 0:
                    process = gameover
        else:
            for clicked_beer in clicked_beers:
                beers.remove(clicked_beer)
                collision = 1

            for clicked_cure in clicked_cures:
                cures.remove(clicked_cure)
                collision = 3
                if len(hearts) < 5:
                    heart = Heart(WIDTH - (len(hearts) + 1) * (heart_size + heart_padding), HEIGHT - heart_size,
                                  heart_size)
                    hearts.append(heart)
            if process != gameclear:
                if len(beers) == 0 and current_beercount == beer_count[round]:  # 맥주가 모두 사라졌을 때
                    if process != gameover:  # 프로세스가 4가 아닐 때에만 실행
                        process += 1
                        if(round<3):
                            round += 1
                        current_beercount = 0
                        show_image_for_time('stage_clear.png', 2)



def generate_beer():
    global beer_timer, round, current_beercount
    if process != start and process != gameover and current_beercount < beer_count[round]:
        direction = random.choice([1, 2])
        if direction == 1:
            beers.append(Beer(-100, random.randint(400, HEIGHT), direction, round))
            current_beercount += 1
        else:
            beers.append(Beer(WIDTH + 100, random.randint(400, HEIGHT), direction, round))
            current_beercount += 1
        beer_timer = get_time()


def generate_cure_interval(round_number):
    if round_number == 1:
        return 100
    elif round_number == 2:
        return random.randint(5,10)
    elif round_number == 3:
        return random.randint(5,10)
    else:
        return 0

def generate_cure():
    global current_curecount, round, cure_timer,cure_interval
    cure_interval = generate_cure_interval(round)
    if process != start and process != gameover and current_curecount < beer_count[round]:
        if get_time() - cure_timer > cure_interval:
            direction = random.choice([1, 2])
            if direction == 1:
                cures.append(Cure(-100, random.randint(400, HEIGHT), direction, round))
                current_curecount += 1
            else:
                cures.append(Cure(WIDTH + 100, random.randint(400, HEIGHT), direction, round))
                current_curecount += 1
            cure_timer = get_time()

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

def restart():
    global  current_beercount, current_curecount,process,round, beers, cures
    reset_world()
    current_beercount = start
    current_curecount = start
    process = start
    round = 1
    beers = []
    cures = []

open_canvas(WIDTH, HEIGHT)
reset_world()

# game loop
running = True
mx, my = 0, 0
while running:

    clear_canvas()
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, HEIGHT - event.y - 1  # 마우스 위치 업데이트

    render_world(mx, my)

    # 2초마다 맥주 생성
    if(process != start):
        if get_time() - beer_timer > beer_interval:
            generate_beer()
        if get_time() - cure_timer > beer_interval:
            generate_cure()




    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN and process == gameover:
           restart()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx, my = event.x, HEIGHT - event.y - 1
            handle_mouse_events(mx, my)
            if(collision == 1):
                bottle_sound = Bottlesound()
            else:
                if(collision == 2):
                    gun_sound = Gunsound()  # Gunsound 객체 생성)
            collision = 0


    update_world()
    delay(0.01)

# finalization code
close_canvas()