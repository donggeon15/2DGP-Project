import random
import math
import game_framework
import game_world

from pico2d import *

# moster Run Speed
PIXEL_PER_METER = (25.0 / 0.2)  # 25 pixel 20 cm
RUN_SPEED_KMPH = 5.0  # Km / Hour
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
        self.x = 1200
        self.y = 90
        self.screen_x = 0
        if Monster.images is None:
            self.nomal_monster_image = load_image('nomal_monster.png')
        self.size = 200
        self.action = 0 # 0: 걷기 1: 죽음 2: 공격
        self.collision_size_x = 20
        self.collision_size_y = 20
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])


    def update(self):
        if self.action == 0:
            self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
        if self.action == 1:
            self.frame = (self.frame + 2 * ACTION_DEAD_PER_TIME * game_framework.frame_time)
            if self.frame > 2:
                game_world.remove_object(self)
        if self.action == 2:
            self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time)
            if self.frame >= 7:
                game_framework.quit()

        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1050:
            self.dir = -1
        elif self.x < 770:
            self.dir = 1
        pass


    def draw(self):
        if self.dir < 0:
            if self.action == 0:
                self.nomal_monster_image.clip_composite_draw(37 * int(self.frame), 105, 37, 35, 0, 'h', self.screen_x, self.y, 50, 45)
            if self.action == 1:
                self.nomal_monster_image.clip_composite_draw(37 * int(self.frame), 70, 37, 35, 0, 'h', self.screen_x, self.y, 50, 45)
            if self.action == 2:
                pass
        else:
            if self.action == 0:
                self.nomal_monster_image.clip_draw(37 * int(self.frame), 105, 37, 35, self.screen_x, self.y, 50, 45)
            if self.action == 1:
                self.nomal_monster_image.clip_draw(37 * int(self.frame), 70, 37, 35, self.screen_x, self.y, 50, 45)
            if self.action == 2:
                pass
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.screen_x - self.collision_size_x, self.y - self.collision_size_y, self.screen_x + self.collision_size_x, self.y + self.collision_size_y

    def handle_collision(self, group, other):
        if group == 'air:monster':
            if self.action == 0:
                self.action = 1
                self.frame = 0