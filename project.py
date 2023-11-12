from pico2d import *
from map import Map
WIDTH, HEIGHT = 1200, 600  # 원하는 화면 크기
# Game object class here

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            # 'boy.handle_event(event)' 대신에 적절한 처리 로직 추가
            pass

def reset_world():
    global running, world, boy

    running = True
    world = []

    open_canvas(WIDTH, HEIGHT)  # 화면 크기 설정

    background = Map()
    world.append(background)

    # 추가적인 game object를 생성하고 world에 추가
    # 예: boy = Boy()와 같은 코드를 이곳에 추가
    # world.append(boy)

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas()
reset_world()

# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

# finalization code
close_canvas()