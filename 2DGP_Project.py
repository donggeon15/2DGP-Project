from pico2d import *


class Kobby:
    def __init__(self):
        self.x,self.y = 0, 100
        self.frame=0
        self.dir=0
        self.action=0
        self.mode=0
        self.image=load_image('nomal_kobby_sheet.png')

    def update(self):
        pass
    def handle_event(self, event):
        pass
    def draw(self):
        pass

class Background:
    def __init__(self):
        self.image = load_image('background1.png')

    def update(self):
        pass
    def draw(self):
        self.image.draw(750,300,1500,600)


class Ground:
    def __init__(self):
        self.image=load_image('ground1.png')
        self.x,self.y = 0,0

    def draw(self):
        self.image.draw(750,100,1500,200)

    def update(self):
        pass

class Monster:
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass


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