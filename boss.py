import random
import math

import game_clear
import game_framework
import game_world

from pico2d import *

import play_mode
import server
from air_shoot import Air_shoot
from behavior_tree import *
from kobby import Ability
from state_machine import StateMachine, time_out, attack

# boss Run Speed
PIXEL_PER_METER = (25.0 / 0.2)  # 25 pixel 20 cm
RUN_SPEED_KMPH = 5.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# boss Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

# boss Action Dead
TIME_PER_ACTION_DEAD = 10.0
ACTION_DEAD_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_DEAD = 12.0

GRAVITY_SPEED_KMPH = 4
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
    dir = 0
    num = 0
    @staticmethod
    def enter(monster, e):
        Attack.number = monster.action
        if monster.action == 2:
            game_world.add_collision_pair('kobby:boss', None, Attack)
        else:
            game_world.add_collision_pair('kobby:boss_damage', None, Attack)
        pass

    @staticmethod
    def exit(monster, e):
        game_world.remove_collisions_object(Attack)
        pass

    @staticmethod
    def do(monster):
        Attack.dir = monster.dir
        Attack.sx = monster.x
        Attack.sy = monster.y
        Attack.num = monster.action


    @staticmethod
    def draw(monster):
        #draw_rectangle(*Attack.get_bb())
        pass

    @staticmethod
    def get_bb():
        if Attack.num == 0 or Attack.num == 1:
            return 0, 0, 0, 0
        elif Attack.num == 2:
            if Attack.dir > 0:
                return Attack.sx + 50, Attack.sy - 50, Attack.sx + 650, Attack.sy + 50
            else:
                return Attack.sx - 650, Attack.sy - 50, Attack.sx - 50, Attack.sy + 50
        else:
            if Attack.dir > 0:
                return Attack.sx - 50, Attack.sy - 50, Attack.sx + 90, Attack.sy + 90
            else:
                return Attack.sx - 90, Attack.sy - 50, Attack.sx + 50, Attack.sy + 90


    @staticmethod
    def handle_collision(monster, group):
        pass

class Boss:
    images = None

    def __init__(self, x = 0, y = 90):
        self.x = x
        self.past_x = x
        self.y = y
        self.ground = False
        self.gravity = 1
        self.size = 200
        self.action = 0
        self.collision_size_x = 20
        self.collision_size_y = 20
        self.pattern = 0
        self.frame = 0
        self.time = 0
        self.dir = -1
        self.hp = 30
        self.sound_time = 0
        self.hurt = False
        self.hurt_time = 0
        self.no_damage = False
        self.no_damage_time = 0
        if Boss.images is None:
            self.image = load_image('./resource/boss_sheet.png')
            self.boss_sound1 = load_wav('./resource/boss_sound1.wav')
            self.boss_sound1.set_volume(40)
            self.boss_sound2 = load_wav('./resource/suction2.wav')
            self.boss_sound2.set_volume(5)
            self.hit_sound = load_wav('./resource/boss_hit.wav')
            self.hit_sound.set_volume(30)
            self.image_hp_30 = load_image('./boss hp/boss_hp.png')
            self.image_hp_29 = load_image('./boss hp/boss_hp_29.png')
            self.image_hp_28 = load_image('./boss hp/boss_hp_28.png')
            self.image_hp_27 = load_image('./boss hp/boss_hp_27.png')
            self.image_hp_0 = load_image('./boss hp/boss_hp_0.png')
            self.image_hp_1 = load_image('./boss hp/boss_hp_1.png')
            self.image_hp_2 = load_image('./boss hp/boss_hp_2.png')
            self.image_hp_3 = load_image('./boss hp/boss_hp_3.png')
            self.image_hp_4 = load_image('./boss hp/boss_hp_4.png')
            self.image_hp_5 = load_image('./boss hp/boss_hp_5.png')
            self.image_hp_6 = load_image('./boss hp/boss_hp_6.png')
            self.image_hp_7 = load_image('./boss hp/boss_hp_7.png')
            self.image_hp_8 = load_image('./boss hp/boss_hp_8.png')
            self.image_hp_9 = load_image('./boss hp/boss_hp_9.png')
            self.image_hp_10 = load_image('./boss hp/boss_hp_10.png')
            self.image_hp_11 = load_image('./boss hp/boss_hp_11.png')
            self.image_hp_12 = load_image('./boss hp/boss_hp_12.png')
            self.image_hp_13 = load_image('./boss hp/boss_hp_13.png')
            self.image_hp_14 = load_image('./boss hp/boss_hp_14.png')
            self.image_hp_15 = load_image('./boss hp/boss_hp_15.png')
            self.image_hp_16 = load_image('./boss hp/boss_hp_16.png')
            self.image_hp_17 = load_image('./boss hp/boss_hp_17.png')
            self.image_hp_18 = load_image('./boss hp/boss_hp_18.png')
            self.image_hp_19 = load_image('./boss hp/boss_hp_19.png')
            self.image_hp_20 = load_image('./boss hp/boss_hp_20.png')
            self.image_hp_21 = load_image('./boss hp/boss_hp_21.png')
            self.image_hp_22 = load_image('./boss hp/boss_hp_22.png')
            self.image_hp_23 = load_image('./boss hp/boss_hp_23.png')
            self.image_hp_24 = load_image('./boss hp/boss_hp_24.png')
            self.image_hp_25 = load_image('./boss hp/boss_hp_25.png')
            self.image_hp_26 = load_image('./boss hp/boss_hp_26.png')
            self.image_boss = load_image('./boss hp/boss_icon.png')
        self.build_behavior_tree()
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

        self.x = clamp(50, self.x, 800 - 50)
        self.y = clamp(50, self.y, 600 - 50)

        if self.action == 0:
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        elif self.action == 1:
            self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4

        if self.action == 0:
            if server.kobby.x < self.x:
                self.dir = -1
            else:
                self.dir = 1

        # 중력
        if self.ground == False:
            if self.action == 4:
                self.gravity = 98
            else:
                if self.gravity <= 1200:
                    self.gravity += (1 * GRAVITY_SPEED_PPS * 7 * game_framework.frame_time)
        else:
            self.gravity = 1


        if self.y > 200:
            self.ground = False
            self.y -= self.gravity * game_framework.frame_time
        else:
            self.y = 200
            self.ground = True

        if get_time() - self.hurt_time > 0.2:
            self.hurt = False

        if get_time() - self.no_damage_time > 0.5:
            self.no_damage = False

        if self.hp <= 0:
            self.action = 5

        # ai 작동
        if self.action == 5:
            game_world.remove_collisions_object(Attack)
            game_world.remove_collisions_object(self)
            if self.frame < 3:
                self.frame = (self.frame + 2 * ACTION_PER_TIME * game_framework.frame_time)
            game_world.clear()
            game_framework.change_mode(game_clear)
        else:
            self.bt.run()


    def draw(self):
        self.state_machine.draw()
        if self.hurt == False:
            if self.action == 0:
                if self.dir > 0:
                    self.image.clip_composite_draw(64 * int(self.frame), 396, 64, 64, 0, 'h', self.x, self.y, 128, 128)
                else:
                    self.image.clip_draw(64 * int(self.frame), 396, 64, 64, self.x, self.y, 128, 128)
            elif self.action == 1:
                if self.dir > 0:
                    self.image.clip_composite_draw(64 * int(self.frame), 332, 64, 64, 0, 'h', self.x, self.y, 128, 128)
                else:
                    self.image.clip_draw(64 * int(self.frame), 332, 64, 64, self.x, self.y, 128, 128)
            elif self.action == 2:
                if self.dir > 0:
                    self.image.clip_composite_draw(70 * int(self.frame), 262, 70, 70, 0, 'h', self.x, self.y, 140, 140)
                else:
                    self.image.clip_draw(70 * int(self.frame), 262, 70, 70, self.x, self.y, 140, 140)
            elif self.action == 3:
                if self.dir > 0:
                    self.image.clip_composite_draw(90 * int(self.frame), 166, 90, 96, 0, 'h', self.x, self.y + 30, 180,
                                                   192)
                else:
                    self.image.clip_draw(90 * int(self.frame), 166, 90, 96, self.x, self.y + 30, 180, 192)
            elif self.action == 4:
                if self.dir > 0:
                    self.image.clip_composite_draw(90 * int(self.frame), 70, 90, 96, 0, 'h', self.x, self.y + 30, 180,
                                                   192)
                else:
                    self.image.clip_draw(90 * int(self.frame), 70, 90, 96, self.x, self.y + 30, 180, 192)
            elif self.action == 5:
                if self.dir > 0:
                    self.image.clip_composite_draw(70 * int(self.frame), 0, 70, 70, 0, 'h', self.x, self.y, 140, 140)
                else:
                    self.image.clip_draw(70 * int(self.frame), 0, 70, 70, self.x, self.y, 140, 140)
        else:
            if self.dir > 0:
                self.image.clip_composite_draw(0, 0, 70, 70, 0, 'h', self.x, self.y, 140, 140)
            else:
                self.image.clip_draw(0, 0, 70, 70, self.x, self.y, 140, 140)

        self.image_boss.draw(730, 60, 200, 70)

        if self.hp == 30:
            self.image_hp_30.draw(470, 45, 450, 40)
        elif self.hp == 1:
            self.image_hp_1.draw(500, 45, 450, 40)
        elif self.hp == 2:
            self.image_hp_2.draw(500, 45, 450, 40)
        elif self.hp == 3:
            self.image_hp_3.draw(500, 45, 450, 40)
        elif self.hp == 4:
            self.image_hp_4.draw(500, 45, 450, 40)
        elif self.hp == 5:
            self.image_hp_5.draw(500, 45, 450, 40)
        elif self.hp == 6:
            self.image_hp_6.draw(500, 45, 450, 40)
        elif self.hp == 7:
            self.image_hp_7.draw(500, 45, 450, 40)
        elif self.hp == 8:
            self.image_hp_8.draw(500, 45, 450, 40)
        elif self.hp == 9:
            self.image_hp_9.draw(500, 45, 450, 40)
        elif self.hp == 10:
            self.image_hp_10.draw(500, 45, 450, 40)
        elif self.hp == 11:
            self.image_hp_11.draw(500, 45, 450, 40)
        elif self.hp == 12:
            self.image_hp_12.draw(500, 45, 450, 40)
        elif self.hp == 13:
            self.image_hp_13.draw(500, 45, 450, 40)
        elif self.hp == 14:
            self.image_hp_14.draw(500, 45, 450, 40)
        elif self.hp == 15:
            self.image_hp_15.draw(500, 45, 450, 40)
        elif self.hp == 16:
            self.image_hp_16.draw(500, 45, 450, 40)
        elif self.hp == 17:
            self.image_hp_17.draw(500, 45, 450, 40)
        elif self.hp == 18:
            self.image_hp_18.draw(500, 45, 450, 40)
        elif self.hp == 19:
            self.image_hp_19.draw(500, 45, 450, 40)
        elif self.hp == 20:
            self.image_hp_20.draw(500, 45, 450, 40)
        elif self.hp == 21:
            self.image_hp_21.draw(500, 45, 450, 40)
        elif self.hp == 22:
            self.image_hp_22.draw(500, 45, 450, 40)
        elif self.hp == 23:
            self.image_hp_23.draw(500, 45, 450, 40)
        elif self.hp == 24:
            self.image_hp_24.draw(500, 45, 450, 40)
        elif self.hp == 25:
            self.image_hp_25.draw(500, 45, 450, 40)
        elif self.hp == 26:
            self.image_hp_26.draw(500, 45, 450, 40)
        elif self.hp == 27:
            self.image_hp_27.draw(500, 45, 450, 40)
        elif self.hp == 28:
            self.image_hp_28.draw(500, 45, 450, 40)
        elif self.hp == 29:
            self.image_hp_29.draw(500, 45, 450, 40)
        else:
            self.image_hp_0.draw(500, 45, 450, 40)

        #draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 50, self.y - 60, self.x + 50, self.y + 50


    def handle_collision(self, group, other):
        if group == 'air:monster':
            if self.no_damage == False:
                self.hit_sound.play(1)
                self.hp -= 1
                self.hurt = True
                self.hurt_time = get_time()
                self.no_damage = True
                self.no_damage_time = get_time()

    def wait_time(self):
        self.time = get_time()

        return BehaviorTree.SUCCESS

    def random_pattern(self):
        # 0 : 걷기
        # 1 : 흡입 후 하늘 날고 떨어지기
        # 2 : 점프 망치
        # 3 : 망치 휘두르며 돌진
        self.action = 0
        self.pattern  = random.randint(0, 3)
        if get_time() - self.time > 3:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def check_pattern(self, num):
        if self.pattern == num:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def pattern_1_move(self):
        self.action = 1
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.x > 800 - 50:
            self.dir = -1
        if self.x < 0 + 50:
            self.dir = 1

        if get_time() - self.time > 4:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def pattern_2_move_1(self):
        self.action = 2
        self.frame = 0
        if get_time() - self.time > 2:
            self.state_machine.add_event(('ATTACK', 0))
            self.sound_time = get_time()
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def pattern_2_move_2(self):
        self.frame = ((self.frame - 1) + 4 * ACTION_PER_TIME * game_framework.frame_time) % 2 + 1

        if get_time() - self.sound_time > 0.5:
            self.boss_sound2.play(1)

        if get_time() - self.time > 4:
            self.state_machine.add_event(('TIME_OUT', 0))
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def pattern_2_move_3(self):
        self.frame = 4

        self.y += GRAVITY_SPEED_PPS * 8 * game_framework.frame_time

        self.x += self.dir * RUN_SPEED_PPS * 3 * game_framework.frame_time

        if self.x > 800 - 50:
            self.dir = -1
        if self.x < 0 + 50:
            self.dir = 1

        if get_time() - self.time > 5.5:
            self.frame = 3

        if get_time() - self.time > 6:
            self.boss_sound1.play(1)
            star = Air_shoot(self.x, 250, random.choice([-1,1]), 4, 0)
            game_world.add_object(star, 1)
            game_world.add_collision_pair('kobby:food', None, star)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def pattern_3_move_1(self):
        self.action = 4
        self.frame = 0
        if get_time() - self.time > 2:
            self.state_machine.add_event(('ATTACK', 0))
            self.sound_time = get_time()
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def pattern_3_move_2(self):
        self.frame = ((self.frame - 1) + 7 * ACTION_PER_TIME * game_framework.frame_time) % 7 + 1
        self.x += self.dir * RUN_SPEED_PPS * 4 * game_framework.frame_time
        if get_time() - self.sound_time > 0.5:
            self.boss_sound1.play(1)
            self.sound_time = get_time()
        if self.x > 800 - 50:
            self.dir = -1
        if self.x < 0 + 50:
            self.dir = 1

        if get_time() - self.time > 4:
            self.state_machine.add_event(('TIME_OUT', 0))
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def pattern_4_move_1(self):
        self.action = 3
        self.frame = 0
        if get_time() - self.time > 2:
            self.state_machine.add_event(('ATTACK', 0))
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def pattern_4_move_2(self):
        if self.frame < 5:
            self.frame = ((self.frame - 1) + 2.5 * ACTION_PER_TIME * game_framework.frame_time) + 1

        if self.x < server.kobby.x:
            self.dir = 1
        else:
            self.dir = -1

        self.x += self.dir * RUN_SPEED_PPS * 1.2 * game_framework.frame_time
        self.y += GRAVITY_SPEED_PPS * 5 * game_framework.frame_time



        if get_time() - self.time > 1.5:
            self.boss_sound1.play(1)
            self.state_machine.add_event(('TIME_OUT', 0))
            star = Air_shoot(self.x, self.y - 50, random.choice([-1,1]), 4, 0)
            game_world.add_object(star, 1)
            game_world.add_collision_pair('kobby:food', None, star)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING



    def build_behavior_tree(self):
        # 랜덤 패턴
        a1  = Action('timer', self.wait_time)
        a2  = Action('random pattern', self.random_pattern)
        root = random_pattern = Sequence('random set patten', a1, a2)
        # 패턴 == 0
        c1 = Condition('pattern == 0', self.check_pattern, 0)
        a3 = Action('timer2', self.wait_time)
        a4 = Action('move move', self.pattern_1_move)
        root = pattern_1 = Sequence('move to move', c1, a3, a4)
        # 패턴 == 1
        c2 = Condition('pattern == 1', self.check_pattern, 1)
        a5 = Action('timer3', self.wait_time)
        a6 = Action('ready_pattern 1', self.pattern_2_move_1)
        a7 = Action('timer4', self.wait_time)
        a8 = Action('suction', self.pattern_2_move_2)
        a9 = Action('timer5', self.wait_time)
        a10 = Action('fly', self.pattern_2_move_3)
        root = pattern_2 = Sequence('suction & fly', c2, a5, a6, a7, a8, a9, a10)
        # 패턴 == 2
        c3 = Condition('pattern == 2', self.check_pattern, 2)
        a11 = Action('timer6', self.wait_time)
        a12 = Action('attack move ready', self.pattern_3_move_1)
        a13 = Action('timer7', self.wait_time)
        a14 = Action('attack move', self.pattern_3_move_2)
        root = pattern_3 = Sequence('attack & move', c3, a11, a12, a13, a14, a14)
        # 패턴 == 3
        c4 = Condition('pattern == 3', self.check_pattern, 3)
        a15 = Action('timer8', self.wait_time)
        a16 = Action('jump attack', self.pattern_4_move_1)
        a17 = Action('timer9', self.wait_time)
        a18 = Action('jump attack2', self.pattern_4_move_2)
        root = pattern_4 = Sequence('attack & jump', c4, a15, a16, a17, a18, a18)

        root = pattern_go = Selector('pattern go', pattern_1, pattern_2, pattern_3, pattern_4)

        root = boss_ai = Sequence('boss ai', random_pattern, pattern_go)

        self.bt = BehaviorTree(root)