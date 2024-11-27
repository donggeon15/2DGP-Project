from pico2d import *

import server


class Background:
    def __init__(self, stage = 1):
        self.image = load_image('background1.png')
        self.image2 = load_image('background2.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.stage = stage

    def update(self):
        self.window_left = clamp(0,int(server.kobby.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.kobby.y) - self.ch // 2, self.h - self.ch - 1)

    def draw(self):
        if self.stage == 1:
            self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
        if self.stage == 2:
            self.image2.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)