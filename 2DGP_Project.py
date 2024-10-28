from pico2d import *

from background import Background
from ground import Ground
from kobby import Kobby


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
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

open_canvas()

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()