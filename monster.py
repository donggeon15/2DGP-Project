import random
import math
import game_framework
import game_world

from pico2d import *

import play_mode
import server
from air_shoot import Air_shoot
from behavior_tree import *
from kobby import Ability
from state_machine import StateMachine, time_out, attack

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

GRAVITY_SPEED_KMPH = 2
GRAVITY_SPEED_MPM = (GRAVITY_SPEED_KMPH * 1000.0 / 60.0)
GRAVITY_SPEED_MPS = (GRAVITY_SPEED_MPM / 60.0)
GRAVITY_SPEED_PPS = (GRAVITY_SPEED_MPS * PIXEL_PER_METER)


class Walk:
    @staticmethod
    def enter(kobby, e):
        pass

    @staticmethod
    def exit(kobby, e):
        pass

    @staticmethod
    def do(kobby):
        pass

    @staticmethod
    def draw(kobby):
        pass


# 공격 범위
class Attack:
    sx = 0
    sy = 0
    number = 0
    dir = 0
    @staticmethod
    def enter(monster, e):
        Attack.number = monster.number
        if server.ground1.stage == 4:
            Attack.sx = monster.x
            Attack.sy = monster.y
        else:
            Attack.sx = monster.x - server.ground1.window_left
            Attack.sy = monster.y - server.ground1.window_bottom

        game_world.add_collision_pair('kobby:air', Attack, None)
        if monster.number == 0 or monster.number == 1 or monster.number == 3:
            server.kobby.damage_type = 0
        elif monster.number == 2:
            server.kobby.damage_type = 2
        elif monster.number == 4 or monster.number == 5:
            server.kobby.damage_type = 3
        elif monster.number == 6 or monster.number == 7:
            server.kobby.damage_type = 1

    @staticmethod
    def exit(monster, e):
        game_world.remove_collisions_object(Attack)
        pass

    @staticmethod
    def do(monster):
        Attack.dir = monster.dir
        if server.ground1.stage == 4:
            Attack.sx = monster.x
            Attack.sy = monster.y
        else:
            Attack.sx = monster.x - server.ground1.window_left
            Attack.sy = monster.y - server.ground1.window_bottom

    @staticmethod
    def draw(monster):
        #draw_rectangle(*Attack.get_bb())
        pass

    @staticmethod
    def get_bb():
        if Attack.number == 1:
            if Attack.dir > 0:
                return Attack.sx + 30, Attack.sy - 20, Attack.sx + 110, Attack.sy + 10
            else:
                return Attack.sx - 110, Attack.sy - 20, Attack.sx - 30, Attack.sy + 10
        if Attack.number == 2:
            if Attack.dir > 0:
                return Attack.sx + 40, Attack.sy - 30, Attack.sx + 90, Attack.sy + 30
            else:
                return Attack.sx - 90, Attack.sy - 30, Attack.sx - 40, Attack.sy + 30
        if Attack.number == 3:
            if Attack.dir > 0:
                return Attack.sx + 30, Attack.sy - 25, Attack.sx + 75, Attack.sy + 25
            else:
                return Attack.sx - 75, Attack.sy - 25, Attack.sx - 30, Attack.sy + 25
        if Attack.number == 4:
            if Attack.dir > 0:
                return Attack.sx + 30, Attack.sy - 35, Attack.sx + 90, Attack.sy + 35
            else:
                return Attack.sx - 90, Attack.sy - 35, Attack.sx - 30, Attack.sy + 35

    @staticmethod
    def handle_collision(monster, group):
        pass

class Monster:
    images = None
    attack_range = None
    sound = None

    def __init__(self, d = 0, x = 0, y = 90, move_time = 2, stage = 1):
        self.x = x
        self.past_x = x
        if Monster.sound is None:
            self.hit_sound = load_wav('./resource/hit.wav')
            self.hit_sound.set_volume(30)
            self.magic_sound = load_wav('./resource/magicmonster.wav')
            self.magic_sound.set_volume(30)
            self.monster_hit = load_wav('./resource/monster_hit.wav')
            self.monster_hit.set_volume(20)
            self.sword = load_wav('./resource/sword.wav')
            self.sword.set_volume(20)
            self.ice = load_wav('./resource/ice.wav')
            self.ice.set_volume(15)
            self.fire = load_wav('./resource/fire.wav')
            self.fire.set_volume(15)
        self.y = y
        self.ground = False
        self.gravity = 1
        self.number = d #1 기본 몬스터 / 2.기본 몬스터2 / 3. 법사 몬스터 / 4. 검사 몬스터
        # 5. 얼음몬스터1 / 6. 얼음몬스터2 / 7. 불꽃 몬스터1 / 8. 불꽃 몬스터2
        if Monster.images is None:
            self.nomal_monster_image = load_image('./resource/nomal_monster.png') # 일반 몬스터
            self.nomal_monster_image2 = load_image('./resource/nomal_monster_2.png')
            self.magic_monster_image = load_image('./resource/magic_monster.png')
            self.sword_monster_image = load_image('./resource/sword_monster.png')
            self.ice_monster_image = load_image('./resource/ice_monster_1.png')
            self.ice_monster_image2 = load_image('./resource/ice_monster_2.png') # 눈사람
            self.fire_monster_image = load_image('./resource/fire_monster_1.png')
            self.fire_monster_image2 = load_image('./resource/fire_monster_2.png') #불꽃 돼지
        self.size = 200
        self.stage = stage
        self.action = 0 # 0: 걷기 1: 죽음 2: 공격
        self.move_time = move_time
        self.collision_size_x = 20
        self.collision_size_y = 20
        self.frame = random.randint(0, 9)
        self.dir = 1
        self.build_behavior_tree()
        self.time = get_time()
        self.attack_time = 0
        self.sound_time = get_time()
        self.state_machine = StateMachine(self)
        self.state_machine.start(Walk)
        self.state_machine.set_transitions(
            {
                Walk: {attack: Attack},
                Attack: {time_out: Walk},
            }
        )


    def update(self):
        self.state_machine.update()

        if (self.stage == 4):
            self.x = clamp(25, self.x, 800 - 25)
        else:
            self.x = clamp(25, self.x, 3000 - 25)

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
            game_world.remove_collisions_object(Attack)
            self.state_machine.add_event(('TIME_OUT', 0))
            self.frame = (self.frame + 2 * ACTION_DEAD_PER_TIME * game_framework.frame_time)
            if self.number == 0 or self.number == 7 or self.number == 5 or self.number == 2 or self.number == 3 or self.number == 4 or self.number == 6:
                if self.frame > 2:
                    game_world.remove_object(self)
                    if self.stage == 3:
                        server.ground1.catch += 1
            if self.number == 1:
                if self.frame > 3:
                    game_world.remove_object(self)
                    if self.stage == 3:
                        server.ground1.catch += 1

        if self.action == 2: # 공격할때
            if self.number == 0:
                self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time)
                if self.frame > 4:
                    self.monster_hit.play(1)
                    self.action = 0
                    self.frame = 0
            if self.number == 1:
                self.state_machine.add_event(('ATTACK', 0))
                self.collision_size_x = 20
                self.frame = (self.frame + 8 * ACTION_PER_TIME * game_framework.frame_time)
                if self.frame > 4:
                    self.monster_hit.play(1)
                    self.action = 0
                    self.frame = 0
                    self.state_machine.add_event(('TIME_OUT', 0))
            if self.number == 2:
                self.state_machine.add_event(('ATTACK', 0))
                self.frame = ((self.frame - 3) + 8 * ACTION_PER_TIME * game_framework.frame_time) % 4 + 3
                if get_time() - self.sound_time > 0.5:
                    self.magic_sound.play(1)
                    self.sound_time = get_time()
                if get_time() - self.attack_time > 2.5:
                    self.action = 0
                    self.frame = 0
                    self.state_machine.add_event(('TIME_OUT', 0))
            if self.number == 3:
                self.state_machine.add_event(('ATTACK', 0))
                self.frame = (self.frame + 8 * ACTION_PER_TIME * 2 * game_framework.frame_time)
                if self.frame > 8:
                    self.sword.play(1)
                    self.action = 0
                    self.frame = 0
                    self.state_machine.add_event(('TIME_OUT', 0))
            if self.number == 4:
                self.state_machine.add_event(('ATTACK', 0))
                self.frame = ((self.frame - 1) + 8 * ACTION_PER_TIME * game_framework.frame_time) % 7 + 1
                if get_time() - self.sound_time > 0.7:
                    self.ice.play(1)
                    self.sound_time= get_time()
                if get_time() - self.attack_time > 0.05:
                    self.action = 0
                    self.frame = 0
                    self.collision_size_x = 20
                    self.collision_size_y = 20
                    self.state_machine.add_event(('TIME_OUT', 0))
            if self.number == 5:
                self.frame = (self.frame + 8 * ACTION_PER_TIME/4 * game_framework.frame_time)
                if self.frame > 3:
                    ice = Air_shoot(self.x, self.y, self.dir, 3)
                    game_world.add_object(ice, 1)
                    game_world.add_collision_pair('kobby:air', ice, None)
                    self.action = 0
                    self.frame = 0
            if self.number == 6:
                self.frame = (self.frame + 8 * ACTION_PER_TIME * 2 * game_framework.frame_time) % 4
                if get_time() - self.attack_time > 0.05:
                    self.fire.play(1)
                    self.action = 0
                    self.frame = 0
            if self.number == 7:
                self.frame = (self.frame + 8 * ACTION_PER_TIME/4 * game_framework.frame_time)
                if self.frame > 3:
                    fire = Air_shoot(self.x, self.y, self.dir, 2)
                    game_world.add_object(fire, 1)
                    game_world.add_collision_pair('kobby:air', fire, None)
                    self.action = 0
                    self.frame = 0

        # 몬스터 낙사
        if self.y < -50:
            game_world.remove_collisions_object(Attack)
            game_world.remove_object(self)


        # 중력
        if self.ground == False:
            if self.action == 4:
                self.gravity = 98
            else:
                if self.gravity <= 1200:
                    self.gravity += (1 * GRAVITY_SPEED_PPS * 7 * game_framework.frame_time)
        else:
            self.gravity = 1

        if self.number == 6:
            self.gravity = 0

        # 스테이지 1 몬스터
        if self.stage == 1:
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
                        self.x = self.past_x + 1
                        self.dir = 1
                    else:
                        self.x = self.past_x - 1
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
                        self.x = self.past_x + 1
                        self.dir = 1
                    else:
                        self.x = self.past_x - 1
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
                        self.x = self.past_x + 1
                        self.dir = 1
                    else:
                        self.x = self.past_x - 1
                        self.dir = -1
                    self.ground = True
                    if ((self.x >= 2281 and self.x < 2369)):
                        self.y = 200 + 135
        elif self.stage == 2:
            if ((self.x >= 0 and self.x < 780) or (self.x >= 2215 and self.x < 2700)):
                if (self.x >= 151 and self.x < 333):
                    if self.y > 300:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    elif self.y <= 300 and self.y > 290:
                        self.ground = True
                        self.y = 300
                    elif self.y <= 297 and self.y > 200 - 55:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    elif self.y <= 200 - 55:
                        self.y = 200 - 55
                        self.ground = True
                elif (self.x >= 333 and self.x < 417):
                    if self.y > 235:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    elif self.y <= 235 and self.y > 225:
                        self.ground = True
                        self.y = 235
                    elif self.y <= 232 and self.y > 200 - 55:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    elif self.y <= 200 - 55:
                        self.y = 200 - 55
                        self.ground = True
                elif (self.x >= 2343 and self.x < 2520):
                    if self.y > 325:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    elif self.y <= 325 and self.y > 315:
                        self.ground = True
                        self.y = 325
                    elif self.y <= 322 and self.y > 200 - 55:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    elif self.y <= 200 - 55:
                        self.y = 200 - 55
                        self.ground = True
                else:
                    if self.y > 200 - 55:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    else:
                        self.y = 200 - 55
                        self.ground = True
            elif ((self.x >= 780 and self.x < 900)):
                if self.y > 235:
                    self.ground = False
                    self.y -= self.gravity * game_framework.frame_time
                elif self.y <= 235 and self.y > 230:
                    self.y = 235
                    self.ground = True
                else:
                    if self.x < self.past_x:
                        self.x = self.past_x + 1
                        self.dir = 1
                    else:
                        self.x = self.past_x - 1
                        self.dir = -1
                    self.ground = True
                    if ((self.x >= 781 and self.x < 899)):
                        self.y = 235
            elif ((self.x >= 900 and self.x < 1200) or (self.x >= 1740 and self.x < 1850) or (self.x >= 1970 and self.x < 2085)):
                if self.y > 270:
                    self.ground = False
                    self.y -= self.gravity * game_framework.frame_time
                elif self.y <= 270 and self.y > 265:
                    self.y = 270
                    self.ground = True
                else:
                    if self.x < self.past_x:
                        self.x = self.past_x + 1
                        self.dir = 1
                    else:
                        self.x = self.past_x - 1
                        self.dir = -1
                    self.ground = True
                    if ((self.x >= 901 and self.x < 1199)):
                        self.y = 270
            elif ((self.x >= 1200 and self.x < 1300)):
                if self.y > 270 - ((self.x - 1200)):
                    self.ground = False
                    self.y -= self.gravity * game_framework.frame_time
                else:
                    self.y = 270 - ((self.x - 1200))
                    self.ground = True
            elif ((self.x >= 1300 and self.x < 1640)):
                if (self.x >= 1355 and self.x < 1586):
                    if self.y > 300:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    elif self.y <= 300 and self.y > 290:
                        self.ground = True
                        self.y = 300
                    elif self.y <= 297 and self.y > 170:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    elif self.y <= 170:
                        self.y = 170
                        self.ground = True
                else:
                    if self.y > 170:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    else:
                        self.y = 170
                        self.ground = True
            elif ((self.x >= 1640 and self.x < 1740)):
                if self.y > 170 + ((self.x - 1640)):
                    self.ground = False
                    self.y -= self.gravity * game_framework.frame_time
                else:
                    self.y = 170 + ((self.x - 1640))
                    self.ground = True
            elif ((self.x >= 1850 and self.x < 1880) or (self.x >= 1940 and self.x < 1970)):
                if self.y > 110:
                    self.ground = False
                    self.y -= self.gravity * game_framework.frame_time
                elif self.y <= 110 and self.y > 100:
                    self.y = 110
                    self.ground = True
                else:
                    if self.x < self.past_x:
                        self.x = self.past_x + 1
                        self.dir = 1
                    else:
                        self.x = self.past_x - 1
                        self.dir = -1
                    self.ground = False
                    self.y -= self.gravity * game_framework.frame_time
            elif ((self.x >= 1880 and self.x < 1940)):
                self.ground = False
                self.y -= self.gravity * game_framework.frame_time
            elif ((self.x >= 2085 and self.x < 2215)):
                if self.y > 270 - ((self.x - 2085)*1.04):
                    self.ground = False
                    self.y -= self.gravity * game_framework.frame_time
                else:
                    self.y = 270 - ((self.x - 2085)*1.04)
                    self.ground = True
            elif ((self.x >= 2700 and self.x < 2770)):
                if self.y > 145 + ((self.x - 2700)):
                    self.ground = False
                    self.y -= self.gravity * game_framework.frame_time
                else:
                    self.y = 145 + ((self.x - 2700))
                    self.ground = True
            elif ((self.x >= 2770 and self.x < 3000)):
                if (self.x >= 2855 and self.x < 3000):
                    if self.y > 295:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    elif self.y <= 295 and self.y > 285:
                        self.ground = True
                        self.y = 295
                    elif self.y <= 292 and self.y > 210:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    elif self.y <= 210:
                        self.y = 210
                        self.ground = True
                else:
                    if self.y > 210:
                        self.ground = False
                        self.y -= self.gravity * game_framework.frame_time
                    else:
                        self.y = 210
                        self.ground = True
        elif self.stage == 3:
            if self.y > 110:
                self.ground = False
                self.y -= self.gravity * game_framework.frame_time
            else:
                self.y = 110
                self.ground = True
        elif self.stage == 4:
            if self.y > 165:
                self.ground = False
                self.y -= self.gravity * game_framework.frame_time
            else:
                self.y = 165
                self.ground = True
        # ai 작동
        self.bt.run()


    def draw(self):
        self.state_machine.draw()

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
                if self.number == 0:
                    self.nomal_monster_image.clip_composite_draw(37 * int(self.frame), 70, 37, 35, 0, 'h', sx, sy, 55, 52)
                if self.number == 1:
                    self.nomal_monster_image2.clip_composite_draw(36 * int(self.frame), 30, 36, 36, 0, 'h', sx, sy + 10, 72, 72)
                if self.number == 2:
                    self.magic_monster_image.clip_composite_draw(0 * int(self.frame), 45, 30, 30, 0, 'h', sx, sy + 3, 60, 60)
                if self.number == 3:
                    self.sword_monster_image.clip_composite_draw(30 * int(self.frame), 34, 30, 30, 0, 'h', sx, sy + 5, 60, 60)
                if self.number == 4:
                    self.ice_monster_image.clip_draw(32 * int(self.frame), 32, 32, 30, sx, sy + 5, 64, 60)
                if self.number == 5:
                    self.ice_monster_image2.clip_composite_draw(0 * int(self.frame), 0, 32, 34, 0, 'h', sx, sy + 10, 64, 68)
                if self.number == 6:
                    self.fire_monster_image.clip_composite_draw(28 * int(self.frame), 26, 28, 26, 0, 'h', sx, sy, 56, 52)
                if self.number == 7:
                    self.fire_monster_image2.clip_draw(28 * int(self.frame), 28, 28, 28, sx, sy + 5, 56, 56)
            if self.action == 2:  # 공격
                if self.number == 0:
                    self.nomal_monster_image.clip_composite_draw(37 * int(self.frame), 0, 37, 70, 0, 'h', sx, sy, 50, 105)
                if self.number == 1:
                    self.nomal_monster_image2.clip_composite_draw(90 * int(self.frame), 0, 90, 30, 0, 'h', sx - 40, sy, 180, 60)
                if self.number == 2:
                    self.magic_monster_image.clip_composite_draw(70 * int(self.frame), 0, 70, 45, 0, 'h', sx - 30, sy + 3, 140, 90)
                if self.number == 3:
                    self.sword_monster_image.clip_composite_draw(65 * int(self.frame), 0, 65, 34, 0, 'h', sx - 20, sy + 5, 130, 68)
                if self.number == 4:
                    self.ice_monster_image.clip_draw(64 * int(self.frame), 0, 64, 32, sx - 30, sy + 5, 128, 64)
                if self.number == 5:
                    self.ice_monster_image2.clip_composite_draw(32 * int(self.frame) + 1, 0, 32, 34, 0, 'h', sx, sy + 10, 64, 68)
                if self.number == 6:
                    self.fire_monster_image.clip_composite_draw(28 * int(self.frame), 0, 28, 26, 0, 'h', sx, sy, 56, 52)
                if self.number == 7:
                    self.fire_monster_image2.clip_draw(28 * int(self.frame), 0, 28, 28, sx, sy + 5, 56, 56)
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
                if self.number == 0:
                    self.nomal_monster_image.clip_draw(37 * int(self.frame), 70, 37, 35, sx, sy, 55, 52)
                if self.number == 1:
                    self.nomal_monster_image2.clip_draw(36 * int(self.frame), 30, 36, 36, sx, sy + 10, 72, 72)
                if self.number == 2:
                    self.magic_monster_image.clip_draw(0 * int(self.frame), 45, 30, 30, sx, sy + 3, 60, 60)
                if self.number == 3:
                    self.sword_monster_image.clip_draw(30 * int(self.frame), 34, 30, 30, sx, sy + 5, 60, 60)
                if self.number == 4:
                    self.ice_monster_image.clip_composite_draw(32 * int(self.frame), 32, 32, 30, 0, 'h', sx, sy + 5, 64, 60)
                if self.number == 5:
                    self.ice_monster_image2.clip_draw(0 * int(self.frame), 0, 32, 34, sx, sy + 10, 64, 68)
                if self.number == 6:
                    self.fire_monster_image.clip_draw(28 * int(self.frame), 26, 28, 26, sx, sy, 56, 52)
                if self.number == 7:
                    self.fire_monster_image2.clip_composite_draw(28 * int(self.frame), 28, 28, 28, 0, 'h', sx, sy + 5, 56, 56)
            if self.action == 2:
                if self.number == 0:
                    self.nomal_monster_image.clip_draw(37 * int(self.frame), 0, 37, 70, sx, sy, 50, 105)
                if self.number == 1:
                    self.nomal_monster_image2.clip_draw(90 * int(self.frame), 0, 90, 30, sx + 40, sy, 180, 60)
                if self.number == 2:
                    self.magic_monster_image.clip_draw(70 * int(self.frame), 0, 70, 45, sx + 30, sy + 3, 140, 90)
                if self.number == 3:
                    self.sword_monster_image.clip_draw(65 * int(self.frame), 0, 65, 34, sx + 20, sy + 5, 130, 68)
                if self.number == 4:
                    self.ice_monster_image.clip_composite_draw(64 * int(self.frame), 0, 64, 32, 0, 'h', sx + 30, sy + 5, 128, 64)
                if self.number == 5:
                    self.ice_monster_image2.clip_draw(32 * int(self.frame) + 1, 0, 32, 34, sx, sy + 10, 64, 68)
                if self.number == 6:
                    self.fire_monster_image.clip_draw(28 * int(self.frame), 0, 28, 26, sx, sy, 56, 52)
                if self.number == 7:
                    self.fire_monster_image2.clip_composite_draw(28 * int(self.frame), 0, 28, 28, 0, 'h', sx, sy + 5, 56, 56)
        #draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx = self.x - server.ground1.window_left
        sy = self.y - server.ground1.window_bottom
        if self.dir < 0:
            return sx - self.collision_size_x, sy - self.collision_size_y, sx + 20, sy + self.collision_size_y
        else:
            return sx - 20, sy - self.collision_size_y, sx + self.collision_size_x, sy + self.collision_size_y


    def handle_collision(self, group, other):
        if group == 'air:monster':
            self.hit_sound.play(1)
            if self.action == 0 or self.action == 2:
                self.action = 1
                self.frame = 0
        if group == 'kobby:monster':
            if self.number == 0: # 일반
                if self.action == 0:
                    self.action = 2
                    self.frame = 0
                server.kobby.damage_type = 0
            elif self.number == 1: # 창
                server.kobby.damage_type = 0
            elif self.number == 2: # 법사
                server.kobby.damage_type = 2
            elif self.number == 3: # 검사
                server.kobby.damage_type = 0
            elif self.number == 4 or self.number == 5:
                server.kobby.damage_type = 3
            elif self.number == 6 or self.number == 7:
                server.kobby.damage_type = 1
        if group == 'kobby:food':
            if server.kobby.x < self.x:
                self.past_x = self.x
                self.x -= RUN_SPEED_PPS * 1.4 * game_framework.frame_time
            else:
                self.past_x = self.x
                self.x += RUN_SPEED_PPS * 1.4 * game_framework.frame_time
            if server.kobby.y < self.y:
                self.y -= RUN_SPEED_PPS * 1.4 * game_framework.frame_time
            else:
                self.y += RUN_SPEED_PPS * 1.4 * game_framework.frame_time
            server.kobby.suction = True
            if server.kobby.x <= self.x + 3 and server.kobby.x >= self.x - 3:
                server.kobby.food = True
                if self.number == 0 or self.number == 1:
                    server.kobby.food_type = 0
                    server.kobby.star_type = 0
                elif self.number == 2:
                    server.kobby.food_type = 1
                    server.kobby.star_type = 1
                elif self.number == 3:
                    server.kobby.food_type = 2
                    server.kobby.star_type = 2
                elif self.number == 4 or self.number == 5:
                    server.kobby.food_type = 3
                    server.kobby.star_type = 3
                elif self.number == 6 or self.number == 7:
                    server.kobby.food_type = 4
                    server.kobby.star_type = 4
                game_world.remove_collisions_object(Attack)
                game_world.remove_object(self)
                if self.stage == 3:
                    server.ground1.catch += 1
                server.kobby.suction = False



    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1- x2) **2 + (y1- y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir2 = math.atan2(ty - self.y, tx - self.x)
        if server.kobby.x < self.x:
            self.dir = -1
        else :
            self.dir = 1
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.past_x = self.x
        self.x += distance * math.cos(self.dir2)/2
        if self.number == 6:
            self.y += distance * math.sin(self.dir2)


    def move_to(self, r=0.5): #r은 범위
        #이동하는데 속도와 시간 필요
        self.action = 0  # 돌아 다니는 상태
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING


    def is_kobby_nearby(self, distance):
        if self.distance_less_than(server.kobby.x, server.kobby.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass


    def move_to_kobby(self, r=0.5):
        #self.action = 0
        if self.number == 6 and self.action == 0:
            self.action = 2
            self.attack_time = get_time()
        self.move_slightly_to(server.kobby.x, server.kobby.y)
        if self.distance_less_than(server.kobby.x, server.kobby.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def move_to_LR(self):
        self.past_x = self.x
        if self.number == 4:
            self.x += self.dir * RUN_SPEED_PPS/2 * 2 * game_framework.frame_time
        else:
            self.x += self.dir * RUN_SPEED_PPS/2 * game_framework.frame_time
        if get_time() - self.time > self.move_time:
            self.dir = -self.dir
            self.time = get_time()
        return BehaviorTree.SUCCESS

    def attack_to_kobby(self):
        if server.kobby.x < self.x:
            self.dir = -1
        else :
            self.dir = 1

        if self.action == 0:
            self.action = 2
        return BehaviorTree.SUCCESS

    def attack_to_move_kobby(self):
        if server.kobby.x < self.x:
            self.dir = -1
        else :
            self.dir = 1

        self.past_x = self.x
        if self.number == 1:
            self.x += self.dir * 0.2 * RUN_SPEED_PPS/6 * 2 * game_framework.frame_time
        if self.number == 3:
            self.x += self.dir * 0.4 * RUN_SPEED_PPS/6 * 2 * game_framework.frame_time

        if self.action == 0:
            self.action = 2

        return BehaviorTree.SUCCESS

    def change_attack_mode(self):
        if self.action == 0:
            self.action = 2
        self.attack_time = get_time()
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # 좌우 왔다 갔다
        a1 = Action('repeat left right', self.move_to_LR)
        c1 = Condition('커비 근처에 있는가?', self.is_kobby_nearby, 0.75)

        # 커비가 근처에 있나
        c2 = Condition('커비 근처에 있는가?', self.is_kobby_nearby, 1)
        a2 = Action('커비한데 접근', self.move_to_kobby)

        # 범위안에 들어오면 공격
        c3 = Condition('커비 근처에 있는가?', self.is_kobby_nearby, 2)
        a3 = Action('커비를 향해 공격', self.attack_to_kobby)

        # 근처 오면 각성
        c4 = Condition('커비 근처에 있는가?', self.is_kobby_nearby, 2.5)
        a4 = Action('각성모드로 변경', self.change_attack_mode)

        c5 = Condition('커비 근처에 있는가?', self.is_kobby_nearby, 1.5)
        a5 = Action('커비 향해 이동 공격', self.attack_to_move_kobby)

        if self.number == 0:
            root = move_repeat = Sequence('move repeat', a1)
            root = chase_kobby = Sequence('커비를 추적', c2, a2)
            root = monster0 = Selector("일반 Ai", chase_kobby, move_repeat)
        if self.number == 1:
            root = move_repeat = Sequence('move repeat', a1)
            root = attack_move_kobby = Sequence('커비를 이동 공격', c3, a5)
            root = monster1 = Selector('창 Ai', attack_move_kobby, move_repeat)
        if self.number == 2:
            root = move_repeat = Sequence('move repeat', a1)
            root = change_attack = Sequence('커비를 공격', c4, a4, a1)
            root = monster2 = Selector('마법사 Ai', change_attack, move_repeat)
        if self.number == 3:
            root = move_repeat = Sequence('move repeat', a1)
            root = attack_move_kobby = Sequence('커비를 이동 공격', c5, a5)
            root = monster1 = Selector('검 Ai', attack_move_kobby, move_repeat)
        if self.number == 4:
            root = move_repeat = Sequence('move repeat', a1)
            root = change_attack = Sequence('커비를 공격', c1, a4)
            root = monster2 = Selector('팽귄 Ai', change_attack, move_repeat)
        if self.number == 5:
            root = move_repeat = Sequence('move repeat', a1)
            root = attack_kobby = Sequence('커비를 공격', c3, a3)
            root = monster5 = Selector('눈사람 Ai', attack_kobby, move_repeat)
        if self.number == 6:
            root = move_repeat = Sequence('move repeat', a1)
            root = chase_kobby = Sequence('커비를 추적', c2, a2)
            root = monster0 = Selector("불꽃 Ai", chase_kobby, move_repeat)
        if self.number == 7:
            root = move_repeat = Sequence('move repeat', a1)
            root = attack_kobby = Sequence('커비를 공격', c3, a3)
            root = monster7 = Selector('불꽃 돼지 Ai', attack_kobby, move_repeat)

        self.bt = BehaviorTree(root)