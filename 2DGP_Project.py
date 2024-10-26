from pico2d import *


class Kobby:
    def __init__(self):
        self.x,self.y = 0, 80
        self.frame = 0
        self.count = 0
        self.timer = 0
        self.dir = 0
        self.last_dir = 0
        self.action = 0   #atcion 1:찌그러진, 2:점프 3: 하늘날수 있는
        self.mode = 0 #mode 0: 기본 1: 마법사 2: 검사 3: 얼음 4: 불꽃
        self.image=load_image('nomal_kobby_sheet.png')
        self.image2=load_image('magic_kobby_sheet.png')
        self.image3=load_image('sword_kobby_sheet.png')
        self.image4=load_image('ice_kobby_sheet.png')
        self.image5=load_image('fire_kobby_sheet.png')

    def update(self):
        if self.timer != 0:
            self.timer += 0.05
            if self.timer >= 0.5:
                self.timer = 0

        if self.dir == 0:
            self.count = (self.count + 1) % 50
            if self.count == 49 and self.frame == 0:
                self.frame = (self.frame + 1) % 2
            elif self.frame == 1:
                self.frame = (self.frame + 1) % 2
        elif self.dir == 1 and self.action == 0:
            self.frame = (self.frame + 1) % 10
            self.x += self.dir * 5
        elif self.dir > 1 and self.action == 0:
            self.frame = (self.frame + 1) % 8
            self.x += self.dir * 5
        elif self.dir == -1 and self.action == 0:
            self.frame = (self.frame + 1) % 10
            self.x += self.dir * 5
        elif self.dir < -1 and self.action == 0:
            self.frame = (self.frame + 1) % 8
            self.x += self.dir * 5


    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.frame = 0
                self.last_dir = 0
                if self.timer == 0 and self.action == 0:
                    if self.dir == -2:
                        self.dir = 0
                    else:
                        self.dir += 1
                        self.timer = 0.05
                elif self.timer < 0.26:
                    self.dir += 2
                else:
                    self.dir += 1
            elif event.key == SDLK_LEFT:
                self.frame = 0
                self.last_dir = 1
                if self.timer == 0 and self.action == 0:
                    if self.dir == 2:
                        self.dir = 0
                    else:
                        self.dir -= 1
                        self.timer = 0.05
                elif self.timer < 0.26:
                    self.dir -= 2
                else:
                    self.dir -= 1
            elif event.key == SDLK_UP:
                self.frame = 0
                self.action = 3 # 하늘 나는 풍선
            elif event.key == SDLK_DOWN:
                self.frame = 0
                self.action = 1 # 찌그러진
            elif event.key == SDLK_k:
                self.frame = 0
                self.action = 2 # 점프
            elif event.key == SDLK_1:
                self.mode = (self.mode + 1) % 5
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.dir = 0
                self.frame = 0
            elif event.key == SDLK_LEFT:
                self.dir = 0
                self.frame = 0
            elif event.key == SDLK_DOWN:
                self.action = 0
                self.frame = 0
            elif event.key == SDLK_UP:
                self.action = 0
                self.frame = 0

    def draw(self):
        if self.action == 0:
            if self.dir > 0:
                if self.dir > 1:
                    if self.mode == 0:
                        self.image.clip_draw(25 * self.frame, 25, 25, 25, self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_draw(25 * self.frame, 35, 25, 25, self.x, self.y, 50, 50)
                    elif self.mode == 2:
                        pass
                    elif self.mode == 3:
                        pass
                    elif self.mode == 4:
                        pass
                else:
                    if self.mode == 0:
                        self.image.clip_draw(25 * self.frame, 50, 25, 25, self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_draw(25 * self.frame, 60, 25, 25, self.x, self.y, 50, 50)
                    elif self.mode == 2:
                        pass
                    elif self.mode == 3:
                        pass
                    elif self.mode == 4:
                        pass
            elif self.dir < 0:
                if self.dir < -1:
                    if self.mode == 0:
                        self.image.clip_composite_draw(25 * self.frame, 25, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_composite_draw(25 * self.frame, 35, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                    elif self.mode == 2:
                        pass
                    elif self.mode == 3:
                        pass
                    elif self.mode == 4:
                        pass
                else:
                    if self.mode == 0:
                        self.image.clip_composite_draw(25 * self.frame, 50, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_composite_draw(25 * self.frame, 60, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                    elif self.mode == 2:
                        pass
                    elif self.mode == 3:
                        pass
                    elif self.mode == 4:
                        pass
            else:
                if self.last_dir == 0:
                    if self.mode == 0:
                        self.image.clip_draw(25 * self.frame, 100, 25, 25, self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_draw(25 * self.frame, 110, 25, 25, self.x, self.y, 50, 50)
                    elif self.mode == 2:
                        pass
                    elif self.mode == 3:
                        pass
                    elif self.mode == 4:
                        pass
                elif self.last_dir == 1:
                    if self.mode == 0:
                        self.image.clip_composite_draw(25 * self.frame, 100, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_composite_draw(25 * self.frame, 110, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                    elif self.mode == 2:
                        pass
                    elif self.mode == 3:
                        pass
                    elif self.mode == 4:
                        pass
        elif self.action == 1:
            if self.last_dir == 0:
                if self.mode == 0:
                    self.image.clip_draw(25 * self.frame, 75, 25, 25, self.x, self.y, 50, 50)
                elif self.mode == 1:
                    self.image2.clip_draw(25 * self.frame, 85, 25, 25, self.x, self.y, 50, 50)
                elif self.mode == 2:
                    pass
                elif self.mode == 3:
                    pass
                elif self.mode == 4:
                    pass
            if self.last_dir == 1:
                if self.mode == 0:
                    self.image.clip_composite_draw(25 * self.frame, 75, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                elif self.mode == 1:
                    self.image2.clip_composite_draw(25 * self.frame, 85, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                elif self.mode == 2:
                    pass
                elif self.mode == 3:
                    pass
                elif self.mode == 4:
                    pass
        elif self.action == 2:
            pass
        elif self.action == 3:
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

    def update(self):
        pass

    def draw(self):
        self.image.draw(750,100,1500,200)

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