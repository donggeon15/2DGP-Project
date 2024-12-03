from pico2d import *
import game_framework


import game_world
import server

class Portal:

    def __init__(self, x = 400, y = 300, num = 0):
        self.x, self.y = x, y
        self.num = num

    def draw(self):
        draw_rectangle(*self.get_bb())


    def update(self):
        pass

    def get_bb(self):
        self.sx = self.x - server.ground1.window_left
        self.sy = self.y - server.ground1.window_bottom
        if self.num == 0:
            return self.sx - 25, self.sy - 35, self.sx + 25, self.sy + 30
        else:
            return self.sx - 35, self.sy - 35, self.sx + 35, self.sy + 30

    def handle_collision(self, group, other):
        pass
        if group == 'kobby:portal':
            pass