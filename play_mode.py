from pico2d import *
import game_framework

import game_world
import monster
import server
from background import Background
from ground import Ground
from kobby import Kobby
from monster import Monster
from potal import Portal

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

def setting_stage1():
    server.background1 = Background()
    game_world.add_object(server.background1, 0)

    server.ground1 = Ground(0, 1)
    game_world.add_object(server.ground1, 0)

    server.ground1_grass = Ground(1)
    game_world.add_object(server.ground1_grass, 1)

    server.monster = Monster(7)
    game_world.add_object(server.monster, 1)
    game_world.add_collision_pair('kobby:monster', None, server.monster)
    game_world.add_collision_pair('air:monster', None, server.monster)

    potal = Portal(2935, 190, 0)
    game_world.add_object(potal, 1)
    game_world.add_collision_pair('kobby:portal', None, potal)

def setting_stage2():
    pass

def init():
    global ground1
    global background1
    global kobby
    global ground1_grass
    global monster
    global potal

    server.kobby = Kobby()
    game_world.add_object(server.kobby, 1)
    game_world.add_collision_pair('kobby:monster', server.kobby, None)
    game_world.add_collision_pair('kobby:portal', server.kobby, None)


    # 스테이지 1 셋팅
    setting_stage1()


def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass