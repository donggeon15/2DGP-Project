from pico2d import *
import game_framework

import game_world
from background import Background
from ground import Ground
from kobby import Kobby

#Grass Action Speed
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
                kobby.handle_event(event)

def init():
    global ground1
    global background1
    global kobby
    global ground1_grass

    running = True

    kobby = Kobby()
    game_world.add_object(kobby, 1)

    background1 = Background()
    game_world.add_object(background1, 0)

    ground1 = Ground(0)
    game_world.add_object(ground1, 0)

    ground1_grass = Ground(1)
    game_world.add_object(ground1_grass, 1)

def finish():
    game_world.clear()
    pass

def check_world():
    # 스테이지1 횡스크롤 재생
    if kobby.x <= 400:
        kobby.screen_x = kobby.x
        background1.x = 1500
        ground1.x = 1500
        ground1_grass.x = 1500
    elif kobby.x > 400 and kobby.x < 2600:
        kobby.screen_x = 400
        background1.x = 1500 - (kobby.x - 400)
        ground1.x = 1500 - (kobby.x - 400)
        ground1_grass.x = 1500 - (kobby.x - 400)
    elif kobby.x >= 2600:
        kobby.screen_x = kobby.x - 2200
        background1.x = -700
        ground1.x = -700
        ground1_grass.x = -700

    # 스테이지1 잔디 좌표
    if ((kobby.x > 315 and kobby.x < 515 and kobby.ground == True) or
            (kobby.x > 1550 and kobby.x < 1640 and kobby.ground == True) or
            (kobby.x > 2425 and kobby.x < 2640 and kobby.ground == True)):
        ground1_grass.frame = (ground1_grass.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    # 스테이지1 커비 땅 좌표
    if kobby.x < 0:
        kobby.x = 0
        if kobby.y > ground1.y - 55:
            kobby.ground = False
            kobby.y -= kobby.gravity * game_framework.frame_time
        else:
            kobby.y = ground1.y - 55
            kobby.ground = True
    elif ((kobby.x >= 0 and kobby.x < 600) or (kobby.x >= 760 and kobby.x < 1070) or
          (kobby.x >= 1140 and kobby.x < 1350)):
        if kobby.y > ground1.y - 55:
            kobby.ground = False
            kobby.y -= kobby.gravity * game_framework.frame_time
        else:
            kobby.y = ground1.y - 55
            kobby.ground = True
    elif ((kobby.x >= 600 and kobby.x < 760) or (kobby.x >= 1070 and kobby.x < 1140) or
          (kobby.x >= 1350 and kobby.x < 1525) or (kobby.x > 1820 and kobby.x < 2280) or
          (kobby.x > 2420 and kobby.x < 3000)):
        if kobby.y > ground1.y - 25:
            kobby.ground = False
            kobby.y -= kobby.gravity * game_framework.frame_time
        elif kobby.y <= ground1.y - 25 and kobby.y > ground1.y - 35:
            kobby.y = ground1.y - 25
            kobby.ground = True
        else:
            if kobby.x < kobby.past_x:
                kobby.x = kobby.past_x + 10
            else:
                kobby.x = kobby.past_x - 10
            kobby.ground = True
            if ((kobby.x >= 601 and kobby.x < 759) or (kobby.x >= 1071 and kobby.x < 1139) or
                    (kobby.x >= 1351 and kobby.x < 1524) or (kobby.x > 1821 and kobby.x < 2279) or
                    (kobby.x > 2421 and kobby.x < 2999)):
                kobby.y = ground1.y - 25
    elif ((kobby.x >= 1525 and kobby.x < 1640) or (kobby.x >= 2370 and kobby.x < 2420)):
        if kobby.y > ground1.y + 70:
            kobby.ground = False
            kobby.y -= kobby.gravity * game_framework.frame_time
        elif kobby.y <= ground1.y + 70 and kobby.y > ground1.y + 60:
            kobby.y = ground1.y + 70
            kobby.ground = True
        else:
            if kobby.x < kobby.past_x:
                kobby.x = kobby.past_x + 10
            else:
                kobby.x = kobby.past_x - 10
            kobby.ground = True
            if ((kobby.x >= 1526 and kobby.x < 1639) or (kobby.x >= 2371 and kobby.x < 2419)):
                kobby.y = ground1.y + 70
    elif ((kobby.x >= 1640 and kobby.x <= 1820)):
        if kobby.y > ground1.y + 70 - ((kobby.x - 1640)*(1/2)):
            kobby.ground = False
            kobby.y -= kobby.gravity * game_framework.frame_time
        else:
            kobby.y = ground1.y + 70 - ((kobby.x - 1640)*(1/2))
            kobby.ground = True
    elif ((kobby.x >= 2280 and kobby.x < 2370)):
        if kobby.y > ground1.y + 135:
            kobby.ground = False
            kobby.y -= kobby.gravity * game_framework.frame_time
        elif kobby.y <= ground1.y + 135 and kobby.y > ground1.y + 125:
            kobby.y = ground1.y + 135
            kobby.ground = True
        else:
            if kobby.x < kobby.past_x:
                kobby.x = kobby.past_x + 10
            else:
                kobby.x = kobby.past_x - 10
            kobby.ground = True
            if ((kobby.x >= 2281 and kobby.x < 2369)):
                kobby.y = ground1.y + 135
    elif kobby.x >= 3000:
        kobby.x = 3000
        if kobby.y > ground1.y - 25:
            kobby.ground = False
            kobby.y -= kobby.gravity * game_framework.frame_time
        else:
            kobby.y = ground1.y - 25
            kobby.ground = True

def update():
    game_world.update()
    check_world()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass