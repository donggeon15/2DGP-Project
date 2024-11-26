from pico2d import *

import game_framework
import server

#Grass Action Speed
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Ground:
    def __init__(self, object):
        self.image1 = load_image('ground1.png')
        self.image2 = load_image('ground1_grass.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image1.w
        self.h = self.image1.h
        self.object = object
        self.frame = 0

    def update(self):
        #self.frame = (self.frame + 1) % 4
        # 스테이지1 잔디 좌표
        #if ((server.kobby.x > 315 and server.kobby.x < 515 and server.kobby.ground == True) or
        #        (server.kobby.x > 1550 and server.kobby.x < 1640 and server.kobby.ground == True) or
        #        (server.kobby.x > 2425 and server.kobby.x < 2640 and server.kobby.ground == True)):
        #    server.ground1_grass.frame = (server.ground1_grass.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.window_left = clamp(0, int(server.kobby.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.kobby.y) - self.ch // 2, self.h - self.ch - 1)

    def draw(self):
        if self.object == 0:
            self.image1.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
        elif self.object == 1:
            #self.image2.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
            pass
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        #return self.x - 1500, self.y - 150, self.x - 900, self.y - 55
        pass

    def handle_collision(self, group, other):
        pass