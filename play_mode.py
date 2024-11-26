from pico2d import *
import game_framework

import game_world
import monster
import server
from background import Background
from ground import Ground
from kobby import Kobby
from monster import Monster

#from background import FixedBackground as Background

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
                server.kobby.handle_event(event)

def init():
    global ground1
    global background1
    global kobby
    global ground1_grass
    global monster

    running = True

    server.kobby = Kobby()
    game_world.add_object(server.kobby, 1)
    game_world.add_collision_pair('kobby:monster', server.kobby, None)

    server.background1 = Background()
    game_world.add_object(server.background1, 0)

    server.ground1 = Ground(0)
    game_world.add_object(server.ground1, 0)

    server.ground1_grass = Ground(1)
    game_world.add_object(server.ground1_grass, 1)

    server.monster = Monster(7)
    game_world.add_object(server.monster, 1)
    game_world.add_collision_pair('kobby:monster', None, server.monster)
    game_world.add_collision_pair('air:monster',None, server.monster)

def finish():
    game_world.clear()
    pass

def check_world():
    # 스테이지1 횡스크롤 재생
    #if server.kobby.x <= 400:
    #    server.kobby.screen_x = server.kobby.x
    #    server.background1.x = 1500
    #    server.ground1.x = 1500
    #    server.ground1_grass.x = 1500
    #    server.monster.screen_x = server.monster.x
    #elif server.kobby.x > 400 and server.kobby.x < 2600:
    #    server.kobby.screen_x = 400
    #    server.background1.x = 1500 - (server.kobby.x - 400)
    #    server.ground1.x = 1500 - (server.kobby.x - 400)
    #    server.ground1_grass.x = 1500 - (server.kobby.x - 400)
    #    server.monster.screen_x = server.monster.x - (server.kobby.x - 400)
    #elif server.kobby.x >= 2600:
    #    server.kobby.screen_x = server.kobby.x - 2200
    #    server.background1.x = -700
    #    server.ground1.x = -700
    #    server.ground1_grass.x = -700
    #    monster.screen_x = server.monster.x - 2200


    # 스테이지1 커비 땅 좌표
    #if server.kobby.x < 0:
    #    server.kobby.x = 0
    #    if server.kobby.y > server.ground1.y - 55:
    #        server.kobby.ground = False
    #        server.kobby.y -= server.kobby.gravity * game_framework.frame_time
    #    else:
    #        server.kobby.y = ground1.y - 55
    #        server.kobby.ground = True
    #elif ((server.kobby.x >= 0 and server.kobby.x < 600) or (server.kobby.x >= 760 and server.kobby.x < 1070) or
    #      (server.kobby.x >= 1140 and server.kobby.x < 1350)):
    #    if server.kobby.y > server.ground1.y - 55:
    #        server.kobby.ground = False
    #        server.kobby.y -= server.kobby.gravity * game_framework.frame_time
    #    else:
    #        server.kobby.y = server.ground1.y - 55
    #        server.kobby.ground = True
    #elif ((server.kobby.x >= 600 and server.kobby.x < 760) or (server.kobby.x >= 1070 and server.kobby.x < 1140) or
    #      (server.kobby.x >= 1350 and server.kobby.x < 1525) or (server.kobby.x > 1820 and server.kobby.x < 2280) or
    #      (server.kobby.x > 2420 and server.kobby.x < 3000)):
    #    if server.kobby.y > server.ground1.y - 25:
    #        server.kobby.ground = False
    #        server.kobby.y -= server.kobby.gravity * game_framework.frame_time
    #    elif server.kobby.y <= server.ground1.y - 25 and server.kobby.y > server.ground1.y - 35:
    #        server.kobby.y = server.ground1.y - 25
    #        server.kobby.ground = True
    #    else:
    #        if server.kobby.x < server.kobby.past_x:
    #            server.kobby.x = server.kobby.past_x + 10
    #        else:
    #            server.kobby.x = server.kobby.past_x - 10
    #        server.kobby.ground = True
    #        if ((server.kobby.x >= 601 and server.kobby.x < 759) or (server.kobby.x >= 1071 and server.kobby.x < 1139) or
    #                (server.kobby.x >= 1351 and server.kobby.x < 1524) or (server.kobby.x > 1821 and server.kobby.x < 2279) or
    #                (server.kobby.x > 2421 and server.kobby.x < 2999)):
    #            server.kobby.y = server.ground1.y - 25
    #elif ((server.kobby.x >= 1525 and server.kobby.x < 1640) or (server.kobby.x >= 2370 and server.kobby.x < 2420)):
    #    if server.kobby.y > server.ground1.y + 70:
    #        server.kobby.ground = False
    #        server.kobby.y -= server.kobby.gravity * game_framework.frame_time
    #    elif server.kobby.y <= server.ground1.y + 70 and server.kobby.y > server.ground1.y + 60:
    #        server.kobby.y = server.ground1.y + 70
    #        server.kobby.ground = True
    #    else:
    #        if server.kobby.x < server.kobby.past_x:
    #            server.kobby.x = server.kobby.past_x + 10
    #        else:
    #            server.kobby.x = server.kobby.past_x - 10
    #        server.kobby.ground = True
    #        if ((server.kobby.x >= 1526 and server.kobby.x < 1639) or (server.kobby.x >= 2371 and server.kobby.x < 2419)):
    #            server.kobby.y = server.ground1.y + 70
    #elif ((server.kobby.x >= 1640 and server.kobby.x <= 1820)):
    #    if server.kobby.y > server.ground1.y + 70 - ((server.kobby.x - 1640)*(1/2)):
    #        server.kobby.ground = False
    #        server.kobby.y -= server.kobby.gravity * game_framework.frame_time
    #    else:
    #        server.kobby.y = server.ground1.y + 70 - ((server.kobby.x - 1640)*(1/2))
    #        server.kobby.ground = True
    #elif ((server.kobby.x >= 2280 and server.kobby.x < 2370)):
    #    if server.kobby.y > server.ground1.y + 135:
    #        server.kobby.ground = False
    #       server.kobby.y -= server.kobby.gravity * game_framework.frame_time
    #    elif server.kobby.y <= server.ground1.y + 135 and server.kobby.y > server.ground1.y + 125:
    #        server.kobby.y = server.ground1.y + 135
    #        server.kobby.ground = True
    #    else:
    #        if server.kobby.x < server.kobby.past_x:
    #            server.kobby.x = server.kobby.past_x + 10
    #        else:
    #            server.kobby.x = server.kobby.past_x - 10
    #        server.kobby.ground = True
    #        if ((server.kobby.x >= 2281 and server.kobby.x < 2369)):
    #            server.kobby.y = server.ground1.y + 135
    #elif server.kobby.x >= 3000:
    #    server.kobby.x = 3000
    #    if server.kobby.y > server.ground1.y - 25:
    #        server.kobby.ground = False
    #        server.kobby.y -= server.kobby.gravity * game_framework.frame_time
    #    else:
    #        server.kobby.y = server.ground1.y - 25
    #        server.kobby.ground = True
    pass

def update():
    game_world.update()
    check_world()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass