import random
import math
import game_framework
import game_world

from pico2d import *

import server

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

GRAVITY_SPEED_KMPH = 9.8
GRAVITY_SPEED_MPM = (GRAVITY_SPEED_KMPH * 1000.0 / 60.0)
GRAVITY_SPEED_MPS = (GRAVITY_SPEED_MPM / 60.0)
GRAVITY_SPEED_PPS = (GRAVITY_SPEED_MPS * PIXEL_PER_METER)

class Monster:
    images = None

    def __init__(self, d = 0):
        self.x = 1200
        self.past_x = 0
        self.y = 90
        self.ground = False
        self.gravity = 1
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

        self.past_x = self.x
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time


        # 중력
        if self.ground == False:
            if self.action == 4:
                self.gravity = 98
            else:
                if self.gravity <= 1200:
                    self.gravity += (1 * GRAVITY_SPEED_PPS * 7 * game_framework.frame_time)
        else:
            self.gravity = 1


        if ((self.x >= 0 and self.x < 600) or (self.x >= 760 and self.x < 1070) or
                (self.x >= 1140 and self.x < 1350)):
            if self.y > 200 - 55:
                self.ground = False
                self.y -= self.gravity * game_framework.frame_time
            else:
                self.y = 200 - 55
                self.ground = True
        elif ((self.x >= 600 and self.x < 760) or (self.x >= 1070 and self.x < 1140) or
              (self.x >= 1350 and self.x < 1525) or (self.x > 1820 and self.x < 2280) or
              (self.x > 2420 and self.x < 3000)):
            if self.y > 200 - 25:
                self.ground = False
                self.y -= self.gravity * game_framework.frame_time
            elif self.y <= 200 - 25 and self.y > 200 - 35:
                self.y = 200 - 25
                self.ground = True
            else:
                if self.x < self.past_x:
                    self.x = self.past_x + 10
                    self.dir = 1
                else:
                    self.x = self.past_x - 10
                    self.dir = -1
                self.ground = True
                if ((self.x >= 601 and self.x < 759) or (self.x >= 1071 and self.x < 1139) or
                        (self.x >= 1351 and self.x < 1524) or (self.x > 1821 and self.x < 2279) or
                        (self.x > 2421 and self.x < 2999)):
                    self.y = 200 - 25
        elif ((self.x >= 1525 and self.x < 1640) or (self.x >= 2370 and self.x < 2420)):
            if self.y > 200 + 70:
                self.ground = False
                self.y -= self.gravity * game_framework.frame_time
            elif self.y <= 200 + 70 and self.y > 200 + 60:
                self.y = 200 + 70
                self.ground = True
            else:
                if self.x < self.past_x:
                    self.x = self.past_x + 10
                    self.dir = 1
                else:
                    self.x = self.past_x - 10
                    self.dir = -1
                self.ground = True
                if ((self.x >= 1526 and self.x < 1639) or (self.x >= 2371 and self.x < 2419)):
                    self.y = 200 + 70
        elif ((self.x >= 1640 and self.x <= 1820)):
            if self.y > 200 + 70 - ((self.x - 1640) * (1 / 2)):
                self.ground = False
                self.y -= self.gravity * game_framework.frame_time
            else:
                self.y = 200 + 70 - ((self.x - 1640) * (1 / 2))
                self.ground = True
        elif ((self.x >= 2280 and self.x < 2370)):
            if self.y > 200 + 135:
                self.ground = False
                self.y -= self.gravity * game_framework.frame_time
            elif self.y <= 200 + 135 and self.y > 200 + 125:
                self.y = 200 + 135
                self.ground = True
            else:
                if self.x < self.past_x:
                    self.x = self.past_x + 10
                    self.dir = 1
                else:
                    self.x = self.past_x - 10
                    self.dir = -1
                self.ground = True
                if ((self.x >= 2281 and self.x < 2369)):
                    self.y = 200 + 135


    def draw(self):
        if server.ground1.stage == 4:
            sx = self.x
            sy = self.y
        else:
            sx = self.x - server.ground1.window_left
            sy = self.y - server.ground1.window_bottom
        if self.dir < 0:
            if self.action == 0:  # 기본
                if self.number == 0:
                    self.nomal_monster_image.clip_composite_draw(37 * int(self.frame), 105, 37, 35, 0, 'h', sx, sy + 3, 55, 52)
                if self.number == 1:
                    self.nomal_monster_image2.clip_composite_draw(35 * int(self.frame), 66, 35, 40, 0, 'h', sx, sy + 10, 70, 80)
                if self.number == 2:
                    self.magic_monster_image.clip_composite_draw(30 * int(self.frame), 75, 30, 30, 0, 'h', sx, sy + 3, 60, 60)
                if self.number == 3:
                    self.sword_monster_image.clip_composite_draw(30 * int(self.frame), 64, 30, 30, 0, 'h', sx, sy + 5, 60, 60)
                if self.number == 4:
                    self.ice_monster_image.clip_draw(32 * int(self.frame), 62, 32, 30, sx, sy + 5, 64, 60)
                if self.number == 5:
                    self.ice_monster_image2.clip_composite_draw(32 * int(self.frame), 34, 32, 34, 0, 'h', sx, sy + 10, 64, 68)
                if self.number == 6:
                    self.fire_monster_image.clip_composite_draw(28 * int(self.frame), 52, 28, 26, 0, 'h', sx, sy, 56, 52)
                if self.number == 7:
                    self.fire_monster_image2.clip_draw(28 * int(self.frame), 56, 28, 28, sx, sy + 5, 56, 56)
            if self.action == 1:  # 죽을때
                self.nomal_monster_image.clip_composite_draw(37 * int(self.frame), 70, 37, 35, 0, 'h', sx, sy, 50, 45)
            if self.action == 2:  # 공격
                pass
        else:
            if self.action == 0:
                if self.number == 0:
                    self.nomal_monster_image.clip_draw(37 * int(self.frame), 105, 37, 35, sx, sy + 3, 55, 52)
                if self.number == 1:
                    self.nomal_monster_image2.clip_draw(35 * int(self.frame), 66, 35, 40, sx, sy + 10, 70, 80)
                if self.number == 2:
                    self.magic_monster_image.clip_draw(30 * int(self.frame), 75, 30, 30, sx, sy + 3, 60, 60)
                if self.number == 3:
                    self.sword_monster_image.clip_draw(30 * int(self.frame), 64, 30, 30, sx, sy + 5, 60, 60)
                if self.number == 4:
                    self.ice_monster_image.clip_composite_draw(32 * int(self.frame), 62, 32, 30, 0, 'h', sx, sy + 5, 64, 60)
                if self.number == 5:
                    self.ice_monster_image2.clip_draw(32 * int(self.frame), 34, 32, 34, sx, sy + 10, 64, 68)
                if self.number == 6:
                    self.fire_monster_image.clip_draw(28 * int(self.frame), 52, 28, 26, sx, sy, 56, 52)
                if self.number == 7:
                    self.fire_monster_image2.clip_composite_draw(28 * int(self.frame), 56, 28, 28, 0, 'h', sx, sy + 5, 56, 56)
            if self.action == 1:
                self.nomal_monster_image.clip_draw(37 * int(self.frame), 70, 37, 35, sx, sy, 50, 45)
            if self.action == 2:
                pass
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx = self.x - server.ground1.window_left
        sy = self.y - server.ground1.window_bottom
        return sx - self.collision_size_x, sy - self.collision_size_y, sx + self.collision_size_x, sy + self.collision_size_y

    def handle_collision(self, group, other):
        if group == 'air:monster':
            if self.action == 0:
                self.action = 1
                self.frame = 0
