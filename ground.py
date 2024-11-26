from pico2d import *

import game_framework
import server

#Grass Action Speed
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Ground:
    def __init__(self, object, stage = 1):
        # 스테이지 1
        self.image1 = load_image('ground1.png')
        self.image2 = load_image('ground1_grass.png')
        self.image3 = load_image('ground_grass2.png')
        self.image4 = load_image('ground_grass3.png')
        self.image5 = load_image('ground_grass4.png')
        # 스테이지 2
        self.image6 = load_image('ground2.png')
        self.image7 = load_image('ground2_1.png')
        self.image8 = load_image('ground2_2.png')
        self.image9 = load_image('ground2_3.png')
        # 스테이즈 3 - 보스 -
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image1.w
        self.h = self.image1.h
        self.object = object
        self.frame = 0
        self.stage = stage

    def update(self):
        # 스테이지1 잔디 좌표
        if self.stage == 1:
            if ((server.kobby.x > 315 and server.kobby.x < 515 and server.kobby.ground == True) or
                    (server.kobby.x > 1550 and server.kobby.x < 1640 and server.kobby.ground == True) or
                    (server.kobby.x > 2425 and server.kobby.x < 2640 and server.kobby.ground == True)):
                self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        elif server.kobby.stage == 2:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        self.window_left = clamp(0, int(server.kobby.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.kobby.y) - self.ch // 2, self.h - self.ch - 1)

    def draw(self):
        if self.stage == 1:
            if self.object == 0:
                self.image1.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
            elif self.object == 1:
                if int(self.frame) == 0:
                    self.image2.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
                elif int(self.frame) == 1:
                    self.image3.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
                elif int(self.frame) == 2:
                    self.image4.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
                else:
                    self.image5.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
        elif self.stage == 2:
            if int(self.frame) == 0:
                self.image6.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
            elif int(self.frame) == 1:
                self.image7.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
            elif int(self.frame) == 2:
                self.image8.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
            else:
                self.image9.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass