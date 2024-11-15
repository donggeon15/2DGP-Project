import random
import math
import game_framework
import game_world

from pico2d import *

# moster Run Speed
PIXEL_PER_METER = (25.0 / 0.2)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# moster Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

# moster Action Dead
TIME_PER_ACTION_DEAD = 10.0
ACTION_DEAD_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_DEAD = 12.0

class Monster:
    images = None

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.nomal_monster_image = load_image('nomal_monster.png')
        self.size = 200
        self.action = 0 # 0: 걷기 1: 죽음 2: 공격
        self.collision_size_x = 20
        self.collision_size_y = 20
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])


    def update(self):
        if self.action == 0:
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.action == 1:
            self.frame = (self.frame + 2 * ACTION_DEAD_PER_TIME * game_framework.frame_time)
            if self.frame > 2:
                game_world.remove_object(self)
        if self.action == 2:
            self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time)
            if self.frame >= 7:
                game_framework.quit()

        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 800:
            self.dir = -1
        elif self.x < 400:
            self.dir = 1
        #self.x = clamp(800, self.x, 1600)
        pass


    def draw(self):
        if self.dir < 0:
            if self.action == 0:
                self.nomal_monster_image.clip_composite_draw(37 * int(self.frame), 35, 37, 35, 0, 'h', self.x, self.y, 74, 70)
            if self.action == 1:
                pass
            if self.action == 2:
                pass
        else:
            if self.action == 0:
                self.nomal_monster_image.clip_draw(37 * int(self.frame), 35, 37, 35, self.x, self.y, 74, 70)
            if self.action == 1:
                pass
            if self.action == 2:
                pass
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - self.collision_size_x, self.y - self.collision_size_y, self.x + self.collision_size_x, self.y + self.collision_size_y

    def handle_collision(self, group, other):
        pass