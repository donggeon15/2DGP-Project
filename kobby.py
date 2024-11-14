from pico2d import load_image
from pico2d import *

import game_framework
import game_world
from air_shoot import Air_shoot
from state_machine import *

#kobby pixel
PIXEL_PER_METER = (25.0 / 0.2) # 25pixel = 20cm
#kobby walk speed
WALK_SPEED_KMPH = 5.0 # km/h
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)
#kobby run speed
RUN_SPEED_KMPH = 9.0 # km/h
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
#kobby gravity
GRAVITY_SPEED_KMPH = 9.8
GRAVITY_SPEED_MPM = (GRAVITY_SPEED_KMPH * 1000.0 / 60.0)
GRAVITY_SPEED_MPS = (GRAVITY_SPEED_MPM / 60.0)
GRAVITY_SPEED_PPS = (GRAVITY_SPEED_MPS * PIXEL_PER_METER)
#kobby jump
JUMP_SPEED_KMPH = 20.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)
#kobby balloon up down speed
BALLOON_SPEED_KMPH = 6.0
BALLOON_SPEED_MPM = (BALLOON_SPEED_KMPH * 1000.0 / 60.0)
BALLOON_SPEED_MPS = (BALLOON_SPEED_MPM / 60.0)
BALLOON_SPEED_PPS = (BALLOON_SPEED_MPS * PIXEL_PER_METER)

#kobby action speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION #시간당 2번 액션

TIME_PER_FAIL = 2.0
FAIL_PER_TIME = 1.0 / TIME_PER_FAIL

class Idle:
    @staticmethod
    def enter(kobby, e):
        if right_down(e) or start_event(e):
            kobby.face_dir = 1
        elif left_down(e):
            kobby.face_dir = -1
        kobby.frame = 0
        kobby.action = 0
        kobby.time = get_time()

    @staticmethod
    def exit(kobby, e):
        pass

    @staticmethod
    def do(kobby):
        if kobby.mode == 0 or kobby.mode == 1 or kobby.mode == 2 or kobby.mode == 3:
            if kobby.frame == 0:
                if get_time() - kobby.time > 3:
                    kobby.frame = 1
                    kobby.time2 = get_time()
            elif kobby.frame == 1:
                if get_time() - kobby.time2 > 0.5:
                    kobby.time = get_time()
                    kobby.frame = 0
        elif kobby.mode == 4:
            if kobby.frame < 4:
                kobby.frame = (kobby.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                if get_time() - kobby.time > 3:
                    kobby.frame += 4
                    kobby.time2 = get_time()
            elif kobby.frame >= 4:
                kobby.frame = (kobby.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4 + 4
                if get_time() - kobby.time2 > 0.5:
                    kobby.time = get_time()
                    kobby.frame -= 4

    @staticmethod
    def draw(kobby):
        if kobby.face_dir == 1:
            if kobby.mode == 0:
                kobby.image.clip_draw(25 * int(kobby.frame), 100, 25, 25, kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_draw(25 * int(kobby.frame), 110, 25, 25, kobby.screen_x - 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_draw(32 * int(kobby.frame), 160, 32, 40, kobby.screen_x - 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_draw(25 * int(kobby.frame), 112, 25, 28, kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(25 * int(kobby.frame), 152, 25, 40, kobby.screen_x, kobby.y + 15, 50, 80)
        elif kobby.face_dir == -1:
            if kobby.mode == 0:
                kobby.image.clip_composite_draw(25 * int(kobby.frame), 100, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_composite_draw(25 * int(kobby.frame), 110, 25, 25, 0, 'h', kobby.screen_x + 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_composite_draw(32 * int(kobby.frame), 160, 32, 40, 0, 'h', kobby.screen_x + 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_composite_draw(25 * int(kobby.frame), 112, 25, 28, 0, 'h', kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(25 * int(kobby.frame), 152, 25, 40, 0, 'h', kobby.screen_x, kobby.y + 15, 50, 80)

class Walk:
    @staticmethod
    def enter(kobby, e):
        if right_down(e):
            kobby.face_dir = 1
        elif left_down(e):
            kobby.face_dir = -1
        kobby.frame = 0
        kobby.action = 2
        pass

    @staticmethod
    def exit(kobby, e):
        pass

    @staticmethod
    def do(kobby):
        if kobby.dir == 0:
            kobby.state_machine.add_event(('TIME_OUT', 0))

        if kobby.dir == 1:
            kobby.face_dir = 1
        if kobby.dir == -1:
            kobby.face_dir = -1

        if kobby.mode == 0:
            kobby.frame = (kobby.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 10
        elif kobby.mode == 1:
            kobby.frame = (kobby.frame + 12 * ACTION_PER_TIME * game_framework.frame_time) % 12
        elif kobby.mode == 2:
            kobby.frame = (kobby.frame + 11 * ACTION_PER_TIME * game_framework.frame_time) % 11
        elif kobby.mode == 3:
            kobby.frame = (kobby.frame + 10 * ACTION_PER_TIME * game_framework.frame_time) % 10
        elif kobby.mode == 4:
            kobby.frame = (kobby.frame + 20 * ACTION_PER_TIME * game_framework.frame_time) % 20

        kobby.past_x = kobby.x
        kobby.x += kobby.dir * WALK_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(kobby):
        if kobby.face_dir == 1:
            if kobby.mode == 0:
                kobby.image.clip_draw(25 * int(kobby.frame), 50, 25, 25, kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_draw(25 * int(kobby.frame), 60, 25, 25, kobby.screen_x - 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_draw(32 * int(kobby.frame), 80, 32, 40, kobby.screen_x - 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_draw(25 * int(kobby.frame), 56, 25, 28, kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(25 * int(kobby.frame), 72, 25, 40, kobby.screen_x, kobby.y + 15, 50, 80)
        elif kobby.face_dir == -1:
            if kobby.mode == 0:
                kobby.image.clip_composite_draw(25 * int(kobby.frame), 50, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_composite_draw(25 * int(kobby.frame), 60, 25, 25, 0, 'h', kobby.screen_x + 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_composite_draw(32 * int(kobby.frame), 80, 32, 40, 0, 'h', kobby.screen_x + 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_composite_draw(25 * int(kobby.frame), 56, 25, 28, 0, 'h', kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(25 * int(kobby.frame), 72, 25, 40, 0, 'h', kobby.screen_x, kobby.y + 15, 50, 80)

class Run:
    @staticmethod
    def enter(kobby, e):
        if double_right(e):
            kobby.face_dir = 1
        elif double_left(e):
            kobby.face_dir = -1
        kobby.frame = 0
        kobby.action = 3

    @staticmethod
    def exit(kobby, e):
        pass

    @staticmethod
    def do(kobby):
        if kobby.dir == 0:
            kobby.state_machine.add_event(('TIME_OUT', 0))

        if kobby.dir == 1:
            kobby.face_dir = 1
        if kobby.dir == -1:
            kobby.face_dir = -1

        kobby.frame = (kobby.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 8
        kobby.past_x = kobby.x
        kobby.x += kobby.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(kobby):
        if kobby.face_dir == 1:
            if kobby.mode == 0:
                kobby.image.clip_draw(25 * int(kobby.frame), 25, 25, 25, kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_draw(25 * int(kobby.frame), 35, 25, 25, kobby.screen_x - 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_draw(32 * int(kobby.frame), 40, 32, 40, kobby.screen_x - 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_draw(25 * int(kobby.frame), 28, 25, 28, kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(40 * int(kobby.frame), 40, 40, 32, kobby.screen_x, kobby.y + 5, 80, 64)
        elif kobby.face_dir == -1:
            if kobby.mode == 0:
                kobby.image.clip_composite_draw(25 * int(kobby.frame), 25, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_composite_draw(25 * int(kobby.frame), 35, 25, 25, 0, 'h', kobby.screen_x + 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_composite_draw(32 * int(kobby.frame), 40, 32, 40, 0, 'h', kobby.screen_x + 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_composite_draw(25 * int(kobby.frame), 28, 25, 28, 0, 'h', kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(40 * int(kobby.frame), 40, 40, 32, 0, 'h', kobby.screen_x, kobby.y + 5, 80, 64)

class Squashed:
    @staticmethod
    def enter(kobby, e):
        if right_down(e) or right_up(e) or kobby.face_dir == 1:
            kobby.face_dir = 1
        if left_down(e) or left_up(e) or kobby.face_dir == -1:
            kobby.face_dir = -1
        kobby.frame = 0
        kobby.action = 1
        kobby.time = get_time()

    @staticmethod
    def exit(kobby, e):
        if left_up(e) or right_up(e):
            down_up(e)
        pass

    @staticmethod
    def do(kobby):
        if kobby.mode == 0 or kobby.mode == 1 or kobby.mode == 2 or kobby.mode == 3:
            if kobby.frame == 0:
                if get_time() - kobby.time > 3:
                    kobby.frame = 1
                    kobby.time2 = get_time()
            elif kobby.frame == 1:
                if get_time() - kobby.time2 > 0.5:
                    kobby.time = get_time()
                    kobby.frame = 0
        elif kobby.mode == 4:
            if kobby.frame < 4:
                kobby.frame = (kobby.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
                if get_time() - kobby.time > 3:
                    kobby.frame += 4
                    kobby.time2 = get_time()
            elif kobby.frame >= 4:
                kobby.frame = (kobby.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4 + 4
                if get_time() - kobby.time2 > 0.5:
                    kobby.time = get_time()
                    kobby.frame -= 4

    @staticmethod
    def draw(kobby):
        if kobby.face_dir == 1:
            if kobby.mode == 0:
                kobby.image.clip_draw(25 * kobby.frame, 75, 25, 25, kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_draw(25 * kobby.frame, 85, 25, 25, kobby.screen_x - 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_draw(32 * kobby.frame, 120, 32, 40, kobby.screen_x - 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_draw(25 * kobby.frame, 84, 25, 28, kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(25 * int(kobby.frame), 112, 25, 40, kobby.screen_x, kobby.y + 15, 50, 80)
        elif kobby.face_dir == -1:
            if kobby.mode == 0:
                kobby.image.clip_composite_draw(25 * kobby.frame, 75, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_composite_draw(25 * kobby.frame, 85, 25, 25, 0, 'h', kobby.screen_x + 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_composite_draw(32 * kobby.frame, 120, 32, 40, 0, 'h', kobby.screen_x + 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_composite_draw(25 * kobby.frame, 84, 25, 28, 0, 'h', kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(25 * int(kobby.frame), 112, 25, 40, 0, 'h', kobby.screen_x, kobby.y + 15, 50, 80)
        pass

class Jump:
    @staticmethod
    def enter(kobby, e):
        kobby.jump_frame = 0
        kobby.now_state = e
        if down_k(e):
            kobby.frame = 0
            kobby.y += 1
        if right_down(e):
            kobby.face_dir = 1
        if left_down(e):
            kobby.face_dir = -1
        kobby.time = get_time()
        pass

    @staticmethod
    def exit(kobby, e):
        pass

    @staticmethod
    def do(kobby):
        if JUMP_SPEED_PPS <= kobby.gravity:
            if get_time() - kobby.time > 0.025:
                kobby.frame = (kobby.frame + 8 * FAIL_PER_TIME * game_framework.frame_time) % 8 + 1
                kobby.time = get_time()

        kobby.past_x = kobby.x
        if kobby.action == 3:
            kobby.x += kobby.dir * RUN_SPEED_PPS * game_framework.frame_time
        else:
            kobby.x += kobby.dir * WALK_SPEED_PPS * game_framework.frame_time

        if kobby.ground == False:
            kobby.y += (1 * JUMP_SPEED_PPS * game_framework.frame_time)
        else:
            if kobby.dir == 0:
                kobby.state_machine.add_event(('TIME_OUT', 0))
            else:
                if kobby.action == 3:
                    kobby.state_machine.add_event(('JUMP2', 0))
                else:
                    kobby.state_machine.add_event(('JUMP1', 0))



    @staticmethod
    def draw(kobby):
        if kobby.face_dir == 1:
            if kobby.mode == 0:
                kobby.image.clip_draw(25 * int(kobby.frame), 0, 25, 25, kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_draw(25 * int(kobby.frame), 0, 25, 35, kobby.screen_x - 2, kobby.y + 2, 50, 70)
            elif kobby.mode == 2:
                kobby.image3.clip_draw(32 * int(kobby.frame), 0, 32, 40, kobby.screen_x - 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_draw(25 * int(kobby.frame), 0, 25, 28, kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(25 * int(kobby.frame), 0, 25, 40, kobby.screen_x, kobby.y + 15, 50, 80)
        elif kobby.face_dir == -1:
            if kobby.mode == 0:
                kobby.image.clip_composite_draw(25 * int(kobby.frame), 0, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_composite_draw(25 * int(kobby.frame), 0, 25, 35, 0, 'h', kobby.screen_x + 2, kobby.y + 2, 50, 70)
            elif kobby.mode == 2:
                kobby.image3.clip_composite_draw(32 * int(kobby.frame), 0, 32, 40, 0, 'h', kobby.screen_x + 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_composite_draw(25 * int(kobby.frame), 0, 25, 28, 0, 'h', kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(25 * int(kobby.frame), 0, 25, 40, 0, 'h', kobby.screen_x, kobby.y + 15, 50, 80)

class Balloon:
    @staticmethod
    def enter(kobby, e):
        if double_up(e):
            kobby.temp = 1
        if kobby.action == 4:
            if up_down(e):
                kobby.y_dir = 1
            if down_down(e):
                kobby.y_dir = -1
            if up_up(e) or down_up(e):
                kobby.y_dir = 0
            if down_j(e):
                kobby.temp = 0
                kobby.frame = 0

    @staticmethod
    def exit(kobby, e):
        pass


    @staticmethod
    def do(kobby):
        if kobby.dir == 1:
            kobby.face_dir = 1
        if kobby.dir == -1:
            kobby.face_dir = -1

        if kobby.temp == 0:
            kobby.frame = (kobby.frame + 5 * ACTION_PER_TIME * game_framework.frame_time)
            if kobby.frame > 4:
                kobby.air_shoot()
                kobby.state_machine.add_event(('TIME_OUT', 0))
        else:
            kobby.past_x = kobby.x
            kobby.x += kobby.dir * WALK_SPEED_PPS * game_framework.frame_time
            #위아래 속도
            kobby.y += kobby.y_dir * BALLOON_SPEED_PPS * game_framework.frame_time

            if kobby.action == 4:
                kobby.frame = (kobby.frame + 8 * ACTION_PER_TIME * game_framework.frame_time) % 5 + 5
            else:
                kobby.y += JUMP_SPEED_PPS * game_framework.frame_time
                kobby.frame = (kobby.frame + 5 * ACTION_PER_TIME * game_framework.frame_time)
                if kobby.frame > 4:
                    kobby.action = 4

    @staticmethod
    def draw(kobby):
        if kobby.face_dir == 1:
            if kobby.mode == 0:
                kobby.image1_1.clip_draw(25 * int(kobby.frame), 25 * kobby.temp, 25, 25, kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2_1.clip_draw(26 * int(kobby.frame), 32 * kobby.temp, 26, 32, kobby.screen_x - 2, kobby.y + 2, 52, 64)
            elif kobby.mode == 2:
                if kobby.frame >= 0 and kobby.frame <= 4:
                    kobby.image3_1.clip_draw(32 * int(kobby.frame), 50 * kobby.temp, 32, 50, kobby.screen_x - 7, kobby.y + 17, 64, 100)
                else:
                    kobby.image3_1.clip_draw(32 * int(kobby.frame), 50 * kobby.temp, 32, 50, kobby.screen_x - 3, kobby.y + 17, 64, 100)
            elif kobby.mode == 3:
                kobby.image4_1.clip_draw(28 * int(kobby.frame), 32 * kobby.temp, 28, 32, kobby.screen_x, kobby.y + 5, 56, 64)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(25 * int(kobby.frame), 112, 25, 40, kobby.screen_x, kobby.y + 15, 50, 80)
        elif kobby.face_dir == -1:
            if kobby.mode == 0:
                kobby.image1_1.clip_composite_draw(25 * int(kobby.frame), 25 * kobby.temp, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2_1.clip_composite_draw(26 * int(kobby.frame), 32 * kobby.temp, 26, 32, 0, 'h', kobby.screen_x + 2, kobby.y + 2, 52, 64)
            elif kobby.mode == 2:
                if kobby.frame >= 0 and kobby.frame <= 4:
                    kobby.image3_1.clip_composite_draw(32 * int(kobby.frame), 50 * kobby.temp, 32, 50, 0, 'h', kobby.screen_x + 7, kobby.y + 17, 64, 100)
                else:
                    kobby.image3_1.clip_composite_draw(32 * int(kobby.frame), 50 * kobby.temp, 32, 50, 0, 'h', kobby.screen_x + 3, kobby.y + 17, 64, 100)
            elif kobby.mode == 3:
                kobby.image4_1.clip_composite_draw(28 * int(kobby.frame), 32 * kobby.temp, 28, 32, 0, 'h', kobby.screen_x, kobby.y + 5, 56, 64)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(25 * int(kobby.frame), 112, 25, 40, 0, 'h', kobby.screen_x, kobby.y + 15, 50, 80)

class Ability:
    @staticmethod
    def enter(kobby, e):
        kobby.overtime = 0
        if kobby.mode == 0:
            kobby.frame = 0
            kobby.time = get_time()
            if up_j(e):
                kobby.state_machine.add_event(('TIME_OUT', 0))
        elif kobby.mode == 1:
            kobby.temp = 3
            kobby.frame = 2
        elif kobby.mode == 2:
            kobby.temp = 3
            kobby.frame = 0

    @staticmethod
    def exit(kobby, e):
        pass

    @staticmethod
    def do(kobby):
        if kobby.mode == 0:
            if get_time() - kobby.time <= 3:
                if kobby.frame < 7:
                    kobby.frame = (kobby.frame + 5 *  ACTION_PER_TIME * game_framework.frame_time)
                if kobby.frame >= 6:
                    kobby.frame = (kobby.frame + 3 * ACTION_PER_TIME * game_framework.frame_time) % 2 + 6
            elif get_time() - kobby.time > 3:
                if kobby.overtime == 0:
                    kobby.overtime = 1
                    kobby.frame = 0
                else:
                    kobby.frame = (kobby.frame + 5 * ACTION_PER_TIME * game_framework.frame_time)
                    if kobby.frame >= 5:
                        kobby.state_machine.add_event(('TIME_OUT', 0))
            if kobby.food == True: # 커비가 몬스터 or 별 먹을 경우 바로 time out
                kobby.state_machine.add_event(('TIME_OUT', 0))
        if kobby.mode == 1: # 마법사 모드
            kobby.frame = (kobby.frame + 16 * ACTION_PER_TIME * game_framework.frame_time)
            if kobby.frame > 9:
                kobby.temp -= 1
                kobby.frame = 0
            if kobby.frame > 4 and kobby.temp == 0:
                kobby.state_machine.add_event(('TIME_OUT', 0))
        if kobby.mode == 2: # 검사 모드
            kobby.frame = (kobby.frame + 16 * ACTION_PER_TIME * game_framework.frame_time)
            if kobby.frame > 9:
                kobby.temp -= 1
                kobby.frame = 0
            if kobby.frame > 7 and kobby.temp == 0:
                kobby.x += kobby.face_dir * 40
                kobby.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(kobby):
        if kobby.face_dir == 1:
            if kobby.mode == 0:
                if kobby.overtime == 0:
                    kobby.image1_1.clip_draw(25 * int(kobby.frame), 50, 25, 25, kobby.screen_x, kobby.y, 50, 50)
                else:
                    kobby.image1_1.clip_draw(50 * int(kobby.frame), 75, 50, 40, kobby.screen_x + 25, kobby.y + 15, 100, 80)
            elif kobby.mode == 1:
                kobby.image2_1.clip_draw(80 * int(kobby.frame), 64 + (kobby.temp * 100), 80, 100, kobby.screen_x + 50, kobby.y + 2, 160, 200)
            elif kobby.mode == 2:
                kobby.image3_1.clip_draw(85 * int(kobby.frame), 100 + (kobby.temp * 50), 85, 50, kobby.screen_x + 25, kobby.y + 2, 170, 100)
            elif kobby.mode == 3:
                kobby.image4.clip_draw(25 * int(kobby.frame), 84, 25, 28, kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(25 * int(kobby.frame), 112, 25, 40, kobby.screen_x, kobby.y + 15, 50, 80)
        elif kobby.face_dir == -1:
            if kobby.mode == 0:
                if kobby.overtime == 0:
                    kobby.image1_1.clip_composite_draw(25 * int(kobby.frame), 50, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
                else:
                    kobby.image1_1.clip_composite_draw(50 * int(kobby.frame), 75, 50, 40, 0, 'h', kobby.screen_x - 25, kobby.y + 15, 100, 80)
            elif kobby.mode == 1:
                kobby.image2_1.clip_composite_draw(80 * int(kobby.frame), 64 + (kobby.temp * 100), 80, 100, 0, 'h', kobby.screen_x - 50, kobby.y + 2, 160, 200)
            elif kobby.mode == 2:
                kobby.image3_1.clip_composite_draw(85 * int(kobby.frame), 100 + (kobby.temp * 50), 85, 50, 0, 'h', kobby.screen_x - 25, kobby.y + 2, 170, 100)
            elif kobby.mode == 3:
                kobby.image4.clip_composite_draw(25 * int(kobby.frame), 84, 25, 28, 0, 'h', kobby.screen_x, kobby.y + 5, 50,56)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(25 * int(kobby.frame), 112, 25, 40, 0, 'h', kobby.screen_x, kobby.y + 15,50, 80)

class Kobby:
    first = None
    def __init__(self):
        self.x,self.y = 0, 500
        self.past_x = 0
        self.screen_x = 0
        self.gravity = 1
        self.food = False
        self.frame = 0
        self.dir = 0
        self.frame2 = 0
        self.y_dir = 0
        self.face_dir = 0
        self.d_time = 0
        self.w_time = 0
        self.a_time = 0
        self.temp = 0
        self.action = 0 # 0: 기본 상태 1: 찌그러진 2: 걷기 3: 뛰기 4: 풍선
        self.ground = False
        self.mode = 0 #mode 0: 기본 1: 마법사 2: 검사 3: 얼음 4: 불꽃
        if Kobby.first == None:
            self.image=load_image('nomal_kobby_sheet.png')
            self.image1_1=load_image('nomal_kobby_sheet2.png')
            self.image2=load_image('magic_kobby_sheet.png')
            self.image2_1 = load_image('magic_kobby_sheet2.png')
            self.image3=load_image('sword_kobby_sheet.png')
            self.image3_1 = load_image('sword_kobby_sheet2.png')
            self.image4=load_image('ice_kobby_sheet.png')
            self.image4_1 = load_image('ice_kobby_sheet2.png')
            self.image5=load_image('fire_kobby_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {left_down: Walk, left_up: Walk, right_down: Walk, right_up: Walk, down_down: Squashed, down_up: Idle, double_right: Run, double_left: Run, down_k: Jump, double_up: Balloon, down_j: Ability},
                Squashed: {down_up: Idle, left_down: Squashed, right_down: Squashed, left_up: Squashed, right_up: Squashed},
                Walk: {time_out: Idle, right_down: Walk, right_up: Walk, left_down: Walk, left_up: Walk, down_down: Squashed, down_up: Idle, down_k: Jump, down_j: Ability},
                Run: {time_out: Idle, right_down: Run, left_down: Run, right_up: Idle, left_up: Idle, down_k: Jump, down_j: Ability, down_down: Squashed},
                Jump: {time_out: Idle, jump_end_walk: Walk, jump_end_run: Run, left_down: Jump, right_down: Jump, left_up: Jump, right_up: Jump, down_j: Ability, down_down: Squashed},
                Balloon: {left_down: Balloon, right_down: Balloon, left_up: Balloon, right_up: Balloon, down_down: Balloon, up_down: Balloon, up_up: Balloon, down_up: Balloon, down_j: Balloon, time_out: Idle},
                Ability: {time_out: Idle, up_j: Ability}
            }
        )

    def update(self):
        self.state_machine.update()
        #중력
        if self.ground == False:
            if self.action == 4:
                self.gravity = 98
            else:
                self.gravity += (1 * GRAVITY_SPEED_PPS * 7 * game_framework.frame_time)
        else:
            self.gravity = 1

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_d:
            self.dir += 1
        if event.type == SDL_KEYUP and event.key == SDLK_d:
            self.dir -= 1
            self.d_time = get_time()
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            self.dir -= 1
        if event.type == SDL_KEYUP and event.key == SDLK_a:
            self.dir += 1
            self.a_time = get_time()
        if event.type == SDL_KEYUP and event.key == SDLK_w:
            self.w_time = get_time()

        if event.type == SDL_KEYDOWN and event.key == SDLK_1: # 임시로 변신 키
            self.mode = (self.mode + 1) % 5
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d:
            if get_time() - self.d_time > 0.075:
                self.state_machine.add_event(
                    ('INPUT', event)
                )
            else:
                self.state_machine.add_event(
                    ('DOUBLE_INPUT', event)
                )

        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            if get_time() - self.a_time > 0.075:
                self.state_machine.add_event(
                    ('INPUT', event)
                )
            else:
                self.state_machine.add_event(
                    ('DOUBLE_INPUT', event)
                )
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            if get_time() - self.w_time > 0.075:
                self.state_machine.add_event(
                    ('INPUT', event)
                )
            else:
                self.state_machine.add_event(
                    ('DOUBLE_INPUT', event)
                )
        else:
            self.state_machine.add_event(
                ('INPUT', event)
            )


    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def air_shoot(self):
        if self.face_dir == 1:
            air = Air_shoot(self.screen_x, self.y, self.face_dir)
            game_world.add_object(air,1)
        elif self.face_dir == -1:
            air = Air_shoot(self.screen_x, self.y, self.face_dir)
            game_world.add_object(air, 1)

    def get_bb(self):
        return self.screen_x - 25, self.y - 20, self.screen_x + 25, self.y + 20

    def handle_collision(self, group, other):
        pass