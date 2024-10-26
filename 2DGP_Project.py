from pico2d import *


open_canvas()
background = load_image('background1.png')
character = load_image('sword_kobby_sheet.png')


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

class Ground:
    def __init__(self):
        pass
    def draw(self):
        pass
    def update(self):
        pass

class Monster:
    def __init__(self):
        pass
    def update(self):
        pass
    def handle_event(self, event):
        pass
    def draw(self):
        pass


def handle_events():
    global running, dir, dir2

    global x
    global left, up
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir += 1
                left = False
                up = False
            elif event.key == SDLK_LEFT:
                dir -= 1
                left = True
                up = False
            elif event.key == SDLK_DOWN:
                dir2 -= 1
                left = False
                up = True
            elif event.key == SDLK_UP:
                dir2 += 1
                left = True
                up = True
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir -= 1
            elif event.key == SDLK_LEFT:
                dir += 1
            elif event.key == SDLK_DOWN:
                dir2 += 1
            elif event.key == SDLK_UP:
                dir2 -= 1


running = True
x = 800 // 2
y = 600 // 2
frame = 0
dir = 0
dir2 = 0

left = False
up = False

while running:
    clear_canvas()
    background.draw(750,300,1500,600)
    if left == True and up == False:
        character.clip_draw(frame * 32, 80, 32, 40, x, y, 48, 60)
    elif left == False and up == False:
        character.clip_draw(frame * 32, 80, 32, 40, x, y, 48, 60)
    elif left == False and up == True:
        character.clip_draw(frame * 32, 80, 32, 40, x, y, 48, 60)
    elif left == True and up == True:
        character.clip_draw(frame * 32, 80, 32, 40, x, y, 48, 60)
    update_canvas()
    handle_events()
    frame = (frame + 1) % 11
    if dir > 0:
        if x < 800:
            x += dir * 5
    elif dir < 0:
        if x > 0:
            x += dir * 5
    if dir2 > 0:
        if y < 600:
            y += dir2 * 5
    elif dir2 < 0:
        if y > 0:
            y += dir2 * 5
    delay(0.05)

close_canvas()