from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_k, SDLK_1, SDL_KEYUP


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
            if self.mode == 4:
                self.frame = (self.frame + 1) % 4
                if self.count == 49:
                    self.frame += 4
                elif self.frame > 3:
                    self.frame -= 4
            else:
                if self.count == 49 and self.frame == 0:
                    self.frame = (self.frame + 1) % 2
                elif self.frame == 1:
                    self.frame = (self.frame + 1) % 2
        elif self.dir == 1 and self.action == 0:
            if self.mode == 1:
                self.frame = (self.frame + 1) % 12
            elif self.mode == 2:
                self.frame = (self.frame + 1) % 11
            elif self.mode == 4:
                self.frame = (self.frame + 1) % 20
            else:
                self.frame = (self.frame + 1) % 10
            self.x += self.dir * 5
        elif self.dir > 1 and self.action == 0:
            self.frame = (self.frame + 1) % 8
            self.x += self.dir * 5
        elif self.dir == -1 and self.action == 0:
            if self.mode == 1:
                self.frame = (self.frame + 1) % 12
            elif self.mode == 2:
                self.frame = (self.frame + 1) % 11
            elif self.mode == 4:
                self.frame = (self.frame + 1) % 20
            else:
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
                self.frame = 0
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
                        self.image2.clip_draw(25 * self.frame, 35, 25, 25, self.x - 2, self.y + 2, 50, 50)
                    elif self.mode == 2:
                        self.image3.clip_draw(32 * self.frame, 40, 32, 40, self.x - 7, self.y + 17, 64, 80)
                    elif self.mode == 3:
                        self.image4.clip_draw(25 * self.frame, 28, 25, 28, self.x, self.y + 5, 50, 56)
                    elif self.mode == 4:
                        self.image5.clip_draw(40 * self.frame, 40, 40, 32, self.x, self.y + 5, 80, 64)
                else:
                    if self.mode == 0:
                        self.image.clip_draw(25 * self.frame, 50, 25, 25, self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_draw(25 * self.frame, 60, 25, 25, self.x - 2, self.y + 2, 50, 50)
                    elif self.mode == 2:
                        self.image3.clip_draw(32 * self.frame, 80, 32, 40, self.x - 7, self.y + 17, 64, 80)
                    elif self.mode == 3:
                        self.image4.clip_draw(25 * self.frame, 56, 25, 28, self.x, self.y + 5, 50, 56)
                    elif self.mode == 4:
                        self.image5.clip_draw(25 * self.frame, 72, 25, 40, self.x, self.y + 15, 50, 80)
            elif self.dir < 0:
                if self.dir < -1:
                    if self.mode == 0:
                        self.image.clip_composite_draw(25 * self.frame, 25, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_composite_draw(25 * self.frame, 35, 25, 25, 0, 'h', self.x + 2, self.y + 2, 50, 50)
                    elif self.mode == 2:
                        self.image3.clip_composite_draw(32 * self.frame, 40, 32, 40, 0, 'h', self.x + 7, self.y + 17, 64, 80)
                    elif self.mode == 3:
                        self.image4.clip_composite_draw(25 * self.frame, 28, 25, 28, 0, 'h', self.x, self.y + 5, 50, 56)
                    elif self.mode == 4:
                        self.image5.clip_composite_draw(40 * self.frame, 40, 40, 32, 0, 'h', self.x, self.y + 5, 80, 64)
                else:
                    if self.mode == 0:
                        self.image.clip_composite_draw(25 * self.frame, 50, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_composite_draw(25 * self.frame, 60, 25, 25, 0, 'h', self.x + 2, self.y + 2, 50, 50)
                    elif self.mode == 2:
                        self.image3.clip_composite_draw(32 * self.frame, 80, 32, 40, 0, 'h', self.x + 7, self.y + 17, 64, 80)
                    elif self.mode == 3:
                        self.image4.clip_composite_draw(25 * self.frame, 56, 25, 28, 0, 'h', self.x, self.y + 5, 50, 56)
                    elif self.mode == 4:
                        self.image5.clip_composite_draw(25 * self.frame, 72, 25, 40, 0, 'h', self.x, self.y + 15, 50, 80)
            else:
                if self.last_dir == 0:
                    if self.mode == 0:
                        self.image.clip_draw(25 * self.frame, 100, 25, 25, self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_draw(25 * self.frame, 110, 25, 25, self.x - 2, self.y + 2, 50, 50)
                    elif self.mode == 2:
                        self.image3.clip_draw(32 * self.frame, 160, 32, 40, self.x - 7, self.y + 17, 64, 80)
                    elif self.mode == 3:
                        self.image4.clip_draw(25 * self.frame, 112, 25, 28, self.x, self.y + 5, 50, 56)
                    elif self.mode == 4:
                        self.image5.clip_draw(25 * self.frame, 152, 25, 40, self.x, self.y + 15, 50, 80)
                elif self.last_dir == 1:
                    if self.mode == 0:
                        self.image.clip_composite_draw(25 * self.frame, 100, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                    elif self.mode == 1:
                        self.image2.clip_composite_draw(25 * self.frame, 110, 25, 25, 0, 'h', self.x + 2, self.y + 2, 50, 50)
                    elif self.mode == 2:
                        self.image3.clip_composite_draw(32 * self.frame, 160, 32, 40, 0, 'h', self.x + 7, self.y + 17, 64, 80)
                    elif self.mode == 3:
                        self.image4.clip_composite_draw(25 * self.frame, 112, 25, 28, 0, 'h', self.x, self.y + 5, 50, 56)
                    elif self.mode == 4:
                        self.image5.clip_composite_draw(25 * self.frame, 152, 25, 40, 0, 'h', self.x, self.y + 15, 50, 80)
        elif self.action == 1:
            if self.last_dir == 0:
                if self.mode == 0:
                    self.image.clip_draw(25 * self.frame, 75, 25, 25, self.x, self.y, 50, 50)
                elif self.mode == 1:
                    self.image2.clip_draw(25 * self.frame, 85, 25, 25, self.x - 2, self.y + 2, 50, 50)
                elif self.mode == 2:
                    self.image3.clip_draw(32 * self.frame, 120, 32, 40, self.x - 7, self.y + 17, 64, 80)
                elif self.mode == 3:
                    self.image4.clip_draw(25 * self.frame, 84, 25, 28, self.x, self.y + 5, 50, 56)
                elif self.mode == 4:
                    self.image5.clip_draw(25 * self.frame, 112, 25, 40, self.x, self.y + 15, 50, 80)
            if self.last_dir == 1:
                if self.mode == 0:
                    self.image.clip_composite_draw(25 * self.frame, 75, 25, 25, 0, 'h', self.x, self.y, 50, 50)
                elif self.mode == 1:
                    self.image2.clip_composite_draw(25 * self.frame, 85, 25, 25, 0, 'h', self.x + 2, self.y + 2, 50, 50)
                elif self.mode == 2:
                    self.image3.clip_composite_draw(32 * self.frame, 120, 32, 40, 0, 'h', self.x + 7, self.y + 17, 64, 80)
                elif self.mode == 3:
                    self.image4.clip_composite_draw(25 * self.frame, 84, 25, 28, 0, 'h', self.x, self.y + 5, 50, 56)
                elif self.mode == 4:
                    self.image5.clip_composite_draw(25 * self.frame, 112, 25, 40, 0, 'h', self.x, self.y + 15, 50, 80)
        elif self.action == 2:
            pass
        elif self.action == 3:
            pass
