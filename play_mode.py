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
    global stage1_monster_1
    global stage1_monster_2
    global stage1_monster_3
    global stage1_monster_4
    global stage1_monster_5
    global stage1_monster_6
    global portal

    # 잔디
    ground1_grass = Ground(1)
    game_world.add_object(ground1_grass, 1)

    # 몬스터
    stage1_monster_1 = Monster(0, 500, 90, 2, 1)
    game_world.add_object(stage1_monster_1, 1)
    game_world.add_collision_pair('kobby:monster', None,stage1_monster_1)
    game_world.add_collision_pair('air:monster', None, stage1_monster_1)
    game_world.add_collision_pair('kobby:food', None, stage1_monster_1)

    stage1_monster_2 = Monster(7, 790, 90, 0.5, 1)
    game_world.add_object(stage1_monster_2, 1)
    game_world.add_collision_pair('kobby:monster', None,stage1_monster_2)
    game_world.add_collision_pair('air:monster', None, stage1_monster_2)
    game_world.add_collision_pair('kobby:food', None, stage1_monster_2)

    stage1_monster_3 = Monster(0, 1400, 90, 1, 1)
    game_world.add_object(stage1_monster_3, 1)
    game_world.add_collision_pair('kobby:monster', None,stage1_monster_3)
    game_world.add_collision_pair('air:monster', None, stage1_monster_3)
    game_world.add_collision_pair('kobby:food', None, stage1_monster_3)

    stage1_monster_4 = Monster(2, 1900, 90, 1.5, 1)
    game_world.add_object(stage1_monster_4, 1)
    game_world.add_collision_pair('kobby:monster', None,stage1_monster_4)
    game_world.add_collision_pair('air:monster', None, stage1_monster_4)
    game_world.add_collision_pair('kobby:food', None, stage1_monster_4)

    stage1_monster_5 = Monster(6, 2360, 120, 0.7, 1)
    game_world.add_object(stage1_monster_5, 1)
    game_world.add_collision_pair('kobby:monster', None,stage1_monster_5)
    game_world.add_collision_pair('air:monster', None, stage1_monster_5)
    game_world.add_collision_pair('kobby:food', None, stage1_monster_5)

    stage1_monster_6 = Monster(3, 2700, 90, 0.7, 1)
    game_world.add_object(stage1_monster_6, 1)
    game_world.add_collision_pair('kobby:monster', None,stage1_monster_6)
    game_world.add_collision_pair('air:monster', None, stage1_monster_6)
    game_world.add_collision_pair('kobby:food', None, stage1_monster_6)

    # 포탈
    portal = Portal(2935, 190, 0)
    game_world.add_object(portal, 1)
    game_world.add_collision_pair('kobby:portal', None, portal)

def setting_stage2():
    #remove_object(portal)
    #remove_object(stage1_monster_1)
    #remove_object(stage1_monster_2)
    #remove_object(stage1_monster_3)
    #remove_object(stage1_monster_4)
    #remove_object(stage1_monster_5)
    #remove_object(stage1_monster_6)
    #remove_object(ground1_grass)

    global portal2
    global stage2_monster_1
    global stage2_monster_2
    global stage2_monster_3
    global stage2_monster_4
    global stage2_monster_5
    global stage2_monster_6

    stage2_monster_1 = Monster(1, 200, 600, 0.8, 2)
    game_world.add_object(stage2_monster_1, 1)
    game_world.add_collision_pair('kobby:monster', None, stage2_monster_1)
    game_world.add_collision_pair('air:monster', None, stage2_monster_1)
    game_world.add_collision_pair('kobby:food', None, stage2_monster_1)

    stage2_monster_2 = Monster(3, 600, 400, 1.5, 2)
    game_world.add_object(stage2_monster_2, 1)
    game_world.add_collision_pair('kobby:monster', None, stage2_monster_2)
    game_world.add_collision_pair('air:monster', None, stage2_monster_2)
    game_world.add_collision_pair('kobby:food', None, stage2_monster_2)

    stage2_monster_3 = Monster(5, 900, 650, 0.8, 2)
    game_world.add_object(stage2_monster_3, 1)
    game_world.add_collision_pair('kobby:monster', None, stage2_monster_3)
    game_world.add_collision_pair('air:monster', None, stage2_monster_3)
    game_world.add_collision_pair('kobby:food', None, stage2_monster_3)

    stage2_monster_4 = Monster(4, 1200, 650, 2.5, 2)
    game_world.add_object(stage2_monster_4, 1)
    game_world.add_collision_pair('kobby:monster', None, stage2_monster_4)
    game_world.add_collision_pair('air:monster', None, stage2_monster_4)
    game_world.add_collision_pair('kobby:food', None, stage2_monster_4)

    stage2_monster_5 = Monster(2, 2100, 600, 2.5, 2)
    game_world.add_object(stage2_monster_5, 1)
    game_world.add_collision_pair('kobby:monster', None, stage2_monster_5)
    game_world.add_collision_pair('air:monster', None, stage2_monster_5)
    game_world.add_collision_pair('kobby:food', None, stage2_monster_5)

    stage2_monster_6 = Monster(6, 2500, 250, 3, 2)
    game_world.add_object(stage2_monster_6, 1)
    game_world.add_collision_pair('kobby:monster', None, stage2_monster_6)
    game_world.add_collision_pair('air:monster', None, stage2_monster_6)
    game_world.add_collision_pair('kobby:food', None, stage2_monster_6)

    portal2 = Portal(2945, 310, 0)
    game_world.add_object(portal2, 1)
    game_world.add_collision_pair('kobby:portal', None, portal2)

global portal3

def setting_stage3():
    #remove_object(portal2)
    #remove_object(stage2_monster_1)
    #remove_object(stage2_monster_2)
    #remove_object(stage2_monster_3)
    #remove_object(stage2_monster_4)
    #remove_object(stage2_monster_5)
    #remove_object(stage2_monster_6)

    server.ground1.catch = 0

    global portal3
    global stage3_monster_1
    global stage3_monster_2
    global stage3_monster_3
    global stage3_monster_4
    global stage3_monster_5
    global stage3_monster_6
    global stage3_monster_7
    global stage3_monster_8

    stage3_monster_1 = Monster(0, 200, 200, 2, 3)
    game_world.add_object(stage3_monster_1, 1)
    game_world.add_collision_pair('kobby:monster', None, stage3_monster_1)
    game_world.add_collision_pair('air:monster', None, stage3_monster_1)
    game_world.add_collision_pair('kobby:food', None, stage3_monster_1)

    stage3_monster_2 = Monster(3, 500, 200, 2, 3)
    game_world.add_object(stage3_monster_2, 1)
    game_world.add_collision_pair('kobby:monster', None, stage3_monster_2)
    game_world.add_collision_pair('air:monster', None, stage3_monster_2)
    game_world.add_collision_pair('kobby:food', None, stage3_monster_2)

    stage3_monster_3 = Monster(5, 800, 200, 2, 3)
    game_world.add_object(stage3_monster_3, 1)
    game_world.add_collision_pair('kobby:monster', None, stage3_monster_3)
    game_world.add_collision_pair('air:monster', None, stage3_monster_3)
    game_world.add_collision_pair('kobby:food', None, stage3_monster_3)

    stage3_monster_4 = Monster(6, 1100, 200, 2, 3)
    game_world.add_object(stage3_monster_4, 1)
    game_world.add_collision_pair('kobby:monster', None, stage3_monster_4)
    game_world.add_collision_pair('air:monster', None, stage3_monster_4)
    game_world.add_collision_pair('kobby:food', None, stage3_monster_4)

    stage3_monster_5 = Monster(1, 1500, 200, 2, 3)
    game_world.add_object(stage3_monster_5, 1)
    game_world.add_collision_pair('kobby:monster', None, stage3_monster_5)
    game_world.add_collision_pair('air:monster', None, stage3_monster_5)
    game_world.add_collision_pair('kobby:food', None, stage3_monster_5)

    stage3_monster_6 = Monster(4, 1900, 200, 2, 3)
    game_world.add_object(stage3_monster_6, 1)
    game_world.add_collision_pair('kobby:monster', None, stage3_monster_6)
    game_world.add_collision_pair('air:monster', None, stage3_monster_6)
    game_world.add_collision_pair('kobby:food', None, stage3_monster_6)

    stage3_monster_7 = Monster(2, 2300, 200, 2, 3)
    game_world.add_object(stage3_monster_7, 1)
    game_world.add_collision_pair('kobby:monster', None, stage3_monster_7)
    game_world.add_collision_pair('air:monster', None, stage3_monster_7)
    game_world.add_collision_pair('kobby:food', None, stage3_monster_7)

    stage3_monster_8 = Monster(7, 2700, 200, 2, 3)
    game_world.add_object(stage3_monster_8, 1)
    game_world.add_collision_pair('kobby:monster', None, stage3_monster_8)
    game_world.add_collision_pair('air:monster', None, stage3_monster_8)
    game_world.add_collision_pair('kobby:food', None, stage3_monster_8)

    portal3 = Portal(1500, 140, 1)

def setting_boss():
    remove_object(portal3)


def init():
    server.kobby = Kobby()
    game_world.add_object(server.kobby, 1)
    game_world.add_collision_pair('kobby:monster', server.kobby, None)
    game_world.add_collision_pair('kobby:portal', server.kobby, None)
    game_world.add_collision_pair('kobby:air', None, server.kobby)

    server.background1 = Background(3)
    game_world.add_object(server.background1, 0)
    server.kobby.stage = 3
    server.ground1 = Ground(0, 3)
    game_world.add_object(server.ground1, 0)

    # 스테이지 1 셋팅
    setting_stage3()

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