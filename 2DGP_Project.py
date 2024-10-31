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
    if kobby.x <= 400:
        kobby.screen_x = kobby.x
        background1.x = 750
        ground1.x = 750
    elif kobby.x > 400 and kobby.x < 1100:
        kobby.screen_x = 400
        background1.x = 750 - (kobby.x - 400)
        ground1.x = 750 - (kobby.x - 400)
    elif kobby.x >= 1100:
        kobby.screen_x = kobby.x - 700
        background1.x = 50
        ground1.x = 50



    if kobby.y > ground1.y - 15:
        kobby.y -= 9.8


open_canvas()

reset_world()

while running:
    handle_events()
    update_world()
    check_world()
    render_world()
    delay(0.04)

close_canvas()