from pico2d import *
import game_framework

import game_world
import monster
import server
from background import Background
from game_world import remove_object
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
    global ground1_grass
    global monster
    global portal

    ground1_grass = Ground(1)
    game_world.add_object(ground1_grass, 1)

    monster = Monster(7)
    game_world.add_object(monster, 1)
    game_world.add_collision_pair('kobby:monster', None,monster)
    game_world.add_collision_pair('air:monster', None, monster)

    portal = Portal(2935, 190, 0)
    game_world.add_object(portal, 1)
    game_world.add_collision_pair('kobby:portal', None, portal)

def setting_stage2():
    #remove_object(portal)
    #remove_object(monster)
    #remove_object(ground1_grass)

    global portal2

    portal2 = Portal(2935, 200, 0)
    game_world.add_object(portal2, 1)

    pass

def init():
    server.kobby = Kobby()
    game_world.add_object(server.kobby, 1)
    game_world.add_collision_pair('kobby:monster', server.kobby, None)
    game_world.add_collision_pair('kobby:portal', server.kobby, None)

    server.background1 = Background(2)
    game_world.add_object(server.background1, 0)
    server.kobby.stage = 2
    server.ground1 = Ground(0, 2)
    game_world.add_object(server.ground1, 0)

    # 스테이지 1 셋팅
    setting_stage2()

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