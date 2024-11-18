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

    def __init__(self, d = 0):
        self.x = 1200
        self.y = 90
        self.screen_x = 0
        self.number = d #1 기본 몬스터 / 2.기본 몬스터2 / 3. 법사 몬스터 / 4. 검사 몬스터
        # 5. 얼음몬스터1 / 6. 얼음몬스터2 / 7. 불꽃 몬스터1 / 8. 불꽃 몬스터2
        if Monster.images is None:
            self.nomal_monster_image = load_image('nomal_monster.png')
            self.nomal_monster_image2 = load_image('nomal_monster_2.png')
            self.magic_monster_image = load_image('magic_monster.png')
            self.sword_monster_image = load_image('sword_monster.png')
            self.ice_monster_image = load_image('ice_monster_1.png')
            self.ice_monster_image2 = load_image('ice_monster_2.png')
            self.fire_monster_image = load_image('fire_monster_1.png')
            self.fire_monster_image2 = load_image('fire_monster_2.png')
        self.size = 200
        self.action = 0 # 0: 걷기 1: 죽음 2: 공격
        self.collision_size_x = 20
        self.collision_size_y = 20
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])


    def update(self):
        if self.action == 0: # 기본 돌아다니는
            if self.number == 0 or self.number == 1 or self.number == 3:
                self.frame = (self.frame + 5 * ACTION_PER_TIME * game_framework.frame_time) % 5
            if self.number == 2 or self.number == 4 or self.number == 6:
                self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
            if self.number == 5:
                self.frame = (self.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 3
            if self.number == 7:
                self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
        if self.action == 1: # 죽을떄
            self.frame = (self.frame + 2 * ACTION_DEAD_PER_TIME * game_framework.frame_time)
            if self.frame > 2:
                game_world.remove_object(self)
        if self.action == 2: # 공격할때
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
            if self.action == 0:  # 기본
                if self.number == 0:
                    self.nomal_monster_image.clip_composite_draw(37 * int(self.frame), 105, 37, 35, 0, 'h', self.screen_x, self.y, 74, 70)
                if self.number == 1:
                    self.nomal_monster_image2.clip_composite_draw(35 * int(self.frame), 66, 35, 40, 0, 'h', self.screen_x, self.y, 70, 80)
                if self.number == 2:
                    self.magic_monster_image.clip_composite_draw(30 * int(self.frame), 75, 30, 30, 0, 'h', self.screen_x, self.y, 60, 60)
                if self.number == 3:
                    self.sword_monster_image.clip_composite_draw(30 * int(self.frame), 64, 30, 30, 0, 'h', self.screen_x, self.y, 60, 60)
                if self.number == 4:
                    self.ice_monster_image.clip_draw(32 * int(self.frame), 62, 32, 30, self.screen_x, self.y, 64, 60)
                if self.number == 5:
                    self.ice_monster_image2.clip_composite_draw(32 * int(self.frame), 34, 32, 34, 0, 'h', self.screen_x, self.y, 64, 68)
                if self.number == 6:
                    self.fire_monster_image.clip_composite_draw(28 * int(self.frame), 52, 28, 26, 0, 'h', self.screen_x, self.y, 56, 52)
                if self.number == 7:
                    self.fire_monster_image2.clip_draw(28 * int(self.frame), 56, 28, 28, self.screen_x, self.y, 56, 56)
            if self.action == 1:  # 죽을때
                self.nomal_monster_image.clip_composite_draw(37 * int(self.frame), 70, 37, 35, 0, 'h', self.screen_x, self.y, 50, 45)
            if self.action == 2:  # 공격
                pass
        else:
            if self.action == 0:
                if self.number == 0:
                    self.nomal_monster_image.clip_draw(37 * int(self.frame), 105, 37, 35, self.screen_x, self.y, 74, 70)
                if self.number == 1:
                    self.nomal_monster_image2.clip_draw(35 * int(self.frame), 66, 35, 40, self.screen_x, self.y, 70, 80)
                if self.number == 2:
                    self.magic_monster_image.clip_draw(30 * int(self.frame), 75, 30, 30, self.screen_x, self.y, 60, 60)
                if self.number == 3:
                    self.sword_monster_image.clip_draw(30 * int(self.frame), 64, 30, 30, self.screen_x, self.y, 60, 60)
                if self.number == 4:
                    self.ice_monster_image.clip_composite_draw(32 * int(self.frame), 62, 32, 30, 0, 'h',self.screen_x, self.y, 64, 60)
                if self.number == 5:
                    self.ice_monster_image2.clip_draw(32 * int(self.frame), 34, 32, 34, self.screen_x, self.y, 64, 68)
                if self.number == 6:
                    self.fire_monster_image.clip_draw(28 * int(self.frame), 52, 28, 26, self.screen_x, self.y, 56, 52)
                if self.number == 7:
                    self.fire_monster_image2.clip_composite_draw(28 * int(self.frame), 56, 28, 28, 0, 'h', self.screen_x, self.y, 56, 56)
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