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

GRAVITY_SPEED_KMPH = 9.8
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
        game_world.add_collision_pair('kobby:air', Attack, None)
        pass

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
        draw_rectangle(*Attack.get_bb())
        pass

    @staticmethod
    def get_bb():
        if Attack.number == 1:
            if Attack.dir > 0:
                return Attack.sx + 30, Attack.sy - 20, Attack.sx + 120, Attack.sy + 10
            else:
                return Attack.sx - 120, Attack.sy - 20, Attack.sx - 30, Attack.sy + 10
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

class Boss:
    images = None
    attack_range = None

    def __init__(self, d = 0, x = 0, y = 90, move_time = 2, stage = 1):
        self.x = x
        self.past_x = x
        self.y = y
        self.ground = False
        self.gravity = 1
        self.size = 200
        self.stage = stage
        self.action = 0 # 0: 걷기 1: 죽음 2: 공격
        self.collision_size_x = 20
        self.collision_size_y = 20
        self.frame = 0
        self.dir = 1
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

        if (self.stage == 4):
            self.x = clamp(25, self.x, 800 - 25)
        else:
            self.x = clamp(25, self.x, 3000 - 25)


        # 중력
        if self.ground == False:
            if self.action == 4:
                self.gravity = 98
            else:
                if self.gravity <= 1200:
                    self.gravity += (1 * GRAVITY_SPEED_PPS * 7 * game_framework.frame_time)
        else:
            self.gravity = 1


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
                    elif self.y <= 300 and self.y > 297:
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
                    elif self.y <= 235 and self.y > 232:
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
                    elif self.y <= 325 and self.y > 322:
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
                    elif self.y <= 300 and self.y > 297:
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
                elif self.y <= 110 and self.y > 108:
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
                    elif self.y <= 295 and self.y > 292:
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

        draw_rectangle(*self.get_bb())

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
        pass




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
        self.x += distance * math.cos(self.dir2)
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
            self.x += self.dir * RUN_SPEED_PPS * 2 * game_framework.frame_time
        else:
            self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
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
            self.x += self.dir * 0.2 * RUN_SPEED_PPS * 2 * game_framework.frame_time
        if self.number == 3:
            self.x += self.dir * 0.4 * RUN_SPEED_PPS * 2 * game_framework.frame_time

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



        #self.bt = BehaviorTree(root)


    #a1 = Action('Set target location', self.set_target_location, 1000, 1000)

    #    a2 = Action('Move to', self.move_to)

    #    root = move_to_target_location = Sequence('Move to target location', a1, a2)

    #    a3 = Action('Set random location', self.set_random_location)
    #    root = wander = Sequence('Wander', a3, a2)

    #    c1 = Condition('좀비 공 >= 소년 공?', self.is_ball_more_boy)
    #    a4 = Action('소년한데 접근', self.move_to_boy)
    #    root = chase_boy = Sequence('소년을 추적', c1, a4)

    #    a5 = Action('소년한데 도망', self.run_to_boy)
    #   root = run_boy = Sequence('소년한데 도망', a5)

    #    root = chase_or_run_boy = Selector('소년을 추적 또는 도망', chase_boy, run_boy)

    #    c2 = Condition('소년이 근처에 있는가?', self.is_boy_nearby, 7)
    #    root = chase_run_boy = Sequence('소년 추적, 도망', c2, chase_or_run_boy)

    #    root = chase_run_or_flee = Selector('추적 또는 배회', chase_run_boy, wander)