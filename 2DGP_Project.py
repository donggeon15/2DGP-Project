from pico2d import *

from background import Background
from ground import Ground
from kobby import Kobby
from state_machine import*

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            if event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
                kobby.handle_event(event)


def reset_world():
    global running
    global world
    global ground1
    global background1
    global kobby

    running = True
    world= [ ]

    background1 = Background()
    world.append(background1)

    ground1 = Ground()
    world.append(ground1)

    kobby = Kobby()
    world.append(kobby)


def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

def check_world():
    # 스테이지1 횡스크롤 재생
    if kobby.x <= 400:
        kobby.screen_x = kobby.x
        background1.x = 1500
        ground1.x = 1500
    elif kobby.x > 400 and kobby.x < 2600:
        kobby.screen_x = 400
        background1.x = 1500 - (kobby.x - 400)
        ground1.x = 1500 - (kobby.x - 400)
    elif kobby.x >= 2600:
        kobby.screen_x = kobby.x - 2200
        background1.x = -700
        ground1.x = -700
    # 스테이지1 잔디 좌표
    if ((kobby.x > 315 and kobby.x < 515 and kobby.ground == True) or
            (kobby.x > 1550 and kobby.x < 1640 and kobby.ground == True) or
            (kobby.x > 2425 and kobby.x < 2640 and kobby.ground == True)):
        ground1.frame = (ground1.frame + 1) % 4
    # 스테이지1 커비 땅 좌표
    if kobby.x < 0:
        kobby.x = 0
    elif ((kobby.x >= 0 and kobby.x < 600) or (kobby.x >= 760 and kobby.x < 1070) or
          (kobby.x >= 1140 and kobby.x < 1350)):
        if kobby.y > ground1.y - 55:
            kobby.ground = False
            kobby.y -= kobby.gravity
        else:
            kobby.y = ground1.y - 55
            kobby.ground = True

    elif (kobby.x >= 600 and kobby.x < 760) or (kobby.x >= 1070 and kobby.x < 1140):
        if kobby.y > ground1.y - 25:
            kobby.ground = False
            kobby.y -= kobby.gravity
        elif kobby.y <= ground1.y - 25 and kobby.y > ground1.y - 35:
            kobby.y = ground1.y - 25
            kobby.ground = True
        else:
            kobby.x = kobby.past_x
            kobby.ground = True



open_canvas()

reset_world()

while running:
    handle_events()
    update_world()
    check_world()
    render_world()
    #print(kobby.x)
    print(kobby.y)
    #print(kobby.past_x)
    delay(0.04)

close_canvas()