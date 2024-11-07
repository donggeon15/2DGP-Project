from pico2d import load_image
from pico2d import *
from state_machine import *

class Idle:
    @staticmethod
    def enter(kobby, e):
        if right_up(e) or right_down(e) or start_event(e):
            kobby.face_dir = 1
        elif left_up(e) or left_down(e):
            kobby.face_dir = -1
        kobby.frame = 0
        kobby.dir = 0
        kobby.time = get_time()

    @staticmethod
    def exit(kobby, e):
        pass

    @staticmethod
    def do(kobby):
        if kobby.mode == 0 or kobby.mode == 1 or kobby.mode == 2 or kobby.mode == 3:
            if kobby.frame == 0:
                if get_time() - kobby.time > 3:
                    kobby.frame = (kobby.frame + 1) % 2
            elif kobby.frame == 1:
                kobby.time = get_time()
                kobby.frame = (kobby.frame + 1) % 2
        elif kobby.mode == 4:
            if kobby.frame < 4:
                kobby.frame = (kobby.frame + 1) % 4
                if get_time() - kobby.time > 3:
                    kobby.frame += 4
            elif kobby.frame >= 4:
                kobby.frame = (kobby.frame + 1) % 4 + 4
                kobby.time = get_time()
                kobby.frame -= 4

    @staticmethod
    def draw(kobby):
        if kobby.face_dir == 1:
            if kobby.mode == 0:
                kobby.image.clip_draw(25 * kobby.frame, 100, 25, 25, kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_draw(25 * kobby.frame, 110, 25, 25, kobby.screen_x - 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_draw(32 * kobby.frame, 160, 32, 40, kobby.screen_x - 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_draw(25 * kobby.frame, 112, 25, 28, kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(25 * kobby.frame, 152, 25, 40, kobby.screen_x, kobby.y + 15, 50, 80)
        elif kobby.face_dir == -1:
            if kobby.mode == 0:
                kobby.image.clip_composite_draw(25 * kobby.frame, 100, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_composite_draw(25 * kobby.frame, 110, 25, 25, 0, 'h', kobby.screen_x + 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_composite_draw(32 * kobby.frame, 160, 32, 40, 0, 'h', kobby.screen_x + 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_composite_draw(25 * kobby.frame, 112, 25, 28, 0, 'h', kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(25 * kobby.frame, 152, 25, 40, 0, 'h', kobby.screen_x, kobby.y + 15, 50, 80)

class Walk:
    @staticmethod
    def enter(kobby, e):
        if right_down(e) or left_up(e):
            kobby.face_dir = 1
            kobby.dir = 1
        elif right_up(e) or left_down(e):
            kobby.face_dir = -1
            kobby.dir = -1
        kobby.frame = 0
        pass

    @staticmethod
    def exit(kobby, e):
        kobby.dir = 0
        pass

    @staticmethod
    def do(kobby):
        if kobby.mode == 0:
            kobby.frame = (kobby.frame + 1) % 10
        elif kobby.mode == 1:
            kobby.frame = (kobby.frame + 1) % 12
        elif kobby.mode == 2:
            kobby.frame = (kobby.frame + 1) % 11
        elif kobby.mode == 3:
            kobby.frame = (kobby.frame + 1) % 10
        elif kobby.mode == 4:
            kobby.frame = (kobby.frame + 1) % 20

        kobby.past_x = kobby.x
        kobby.x += kobby.dir * 5

    @staticmethod
    def draw(kobby):
        if kobby.dir == 1:
            if kobby.mode == 0:
                kobby.image.clip_draw(25 * kobby.frame, 50, 25, 25, kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_draw(25 * kobby.frame, 60, 25, 25, kobby.screen_x - 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_draw(32 * kobby.frame, 80, 32, 40, kobby.screen_x - 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_draw(25 * kobby.frame, 56, 25, 28, kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(25 * kobby.frame, 72, 25, 40, kobby.screen_x, kobby.y + 15, 50, 80)
        elif kobby.dir == -1:
            if kobby.mode == 0:
                kobby.image.clip_composite_draw(25 * kobby.frame, 50, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_composite_draw(25 * kobby.frame, 60, 25, 25, 0, 'h', kobby.screen_x + 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_composite_draw(32 * kobby.frame, 80, 32, 40, 0, 'h', kobby.screen_x + 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_composite_draw(25 * kobby.frame, 56, 25, 28, 0, 'h', kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(25 * kobby.frame, 72, 25, 40, 0, 'h', kobby.screen_x, kobby.y + 15, 50, 80)

class Run:
    @staticmethod
    def enter(kobby, e):
        if double_right(e):
            kobby.dir = 2
            kobby.face_dir = 1
        elif double_left(e):
            kobby.dir = -2
            kobby.face_dir = -1
        kobby.frame = 0

    @staticmethod
    def exit(kobby, e):
        pass

    @staticmethod
    def do(kobby):
        kobby.frame = (kobby.frame + 1) % 8
        kobby.past_x = kobby.x
        kobby.x += kobby.dir * 5

    @staticmethod
    def draw(kobby):
        if kobby.dir == 2:
            if kobby.mode == 0:
                kobby.image.clip_draw(25 * kobby.frame, 25, 25, 25, kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_draw(25 * kobby.frame, 35, 25, 25, kobby.screen_x - 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_draw(32 * kobby.frame, 40, 32, 40, kobby.screen_x - 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_draw(25 * kobby.frame, 28, 25, 28, kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(40 * kobby.frame, 40, 40, 32, kobby.screen_x, kobby.y + 5, 80, 64)
        elif kobby.dir == -2:
            if kobby.mode == 0:
                kobby.image.clip_composite_draw(25 * kobby.frame, 25, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_composite_draw(25 * kobby.frame, 35, 25, 25, 0, 'h', kobby.screen_x + 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_composite_draw(32 * kobby.frame, 40, 32, 40, 0, 'h', kobby.screen_x + 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_composite_draw(25 * kobby.frame, 28, 25, 28, 0, 'h', kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(40 * kobby.frame, 40, 40, 32, 0, 'h', kobby.screen_x, kobby.y + 5, 80, 64)



class Squashed:
    @staticmethod
    def enter(kobby, e):
        if right_down(e) or right_up(e) or kobby.face_dir == 1:
            kobby.face_dir = 1
        if left_down(e) or left_up(e) or kobby.face_dir == -1:
            kobby.face_dir = -1
        kobby.frame = 0
        kobby.dir = 0
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
                    kobby.frame = (kobby.frame + 1) % 2
            elif kobby.frame == 1:
                kobby.time = get_time()
                kobby.frame = (kobby.frame + 1) % 2
        elif kobby.mode == 4:
            if kobby.frame < 4:
                kobby.frame = (kobby.frame + 1) % 4
                if get_time() - kobby.time > 3:
                    kobby.frame += 4
            elif kobby.frame >= 4:
                kobby.frame = (kobby.frame + 1) % 4 + 4
                kobby.time = get_time()
                kobby.frame -= 4
        pass

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
                kobby.image5.clip_draw(25 * kobby.frame, 112, 25, 40, kobby.screen_x, kobby.y + 15, 50, 80)
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
                kobby.image5.clip_composite_draw(25 * kobby.frame, 112, 25, 40, 0, 'h', kobby.screen_x, kobby.y + 15, 50, 80)
        pass



class Jump:
    @staticmethod
    def enter(kobby, e):
        kobby.jump_frame = 0
        if kobby.dir != 0:
            if kobby.dir == 1:
                kobby.dir = 1
            elif kobby.dir == -1:
                kobby.dir = -1

            if left_up(e):
                kobby.dir += 1
            elif right_up(e):
                kobby.dir -= 1
            elif down_k(e):
                kobby.frame = 0
                kobby.y += 1
        else:
            if right_down(e):
                kobby.face_dir = 1
                kobby.dir += 1
            elif left_down(e):
                kobby.face_dir = -1
                kobby.dir -= 1
            elif down_k(e):
                kobby.frame = 0
                kobby.y += 1

        pass

    @staticmethod
    def exit(kobby, e):
        kobby.jump_power = 10
        pass

    @staticmethod
    def do(kobby):
        if kobby.jump_power <= kobby.gravity:
            kobby.jump_frame += 0.45
            if kobby.jump_frame >= 1.0:
                kobby.frame = (kobby.frame + 1) % 8 + 1
                kobby.jump_frame = 0.0
        kobby.past_x = kobby.x
        kobby.x += kobby.dir * 5
        if kobby.ground == False:
            kobby.y += 10
        else:
            kobby.state_machine.add_event(('TIME_OUT', 0))


    @staticmethod
    def draw(kobby):
        if kobby.face_dir == 1:
            if kobby.mode == 0:
                kobby.image.clip_draw(25 * kobby.frame, 0, 25, 25, kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_draw(25 * kobby.frame, 85, 25, 25, kobby.screen_x - 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_draw(32 * kobby.frame, 120, 32, 40, kobby.screen_x - 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_draw(25 * kobby.frame, 84, 25, 28, kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_draw(25 * kobby.frame, 112, 25, 40, kobby.screen_x, kobby.y + 15, 50, 80)
        elif kobby.face_dir == -1:
            if kobby.mode == 0:
                kobby.image.clip_composite_draw(25 * kobby.frame, 0, 25, 25, 0, 'h', kobby.screen_x, kobby.y, 50, 50)
            elif kobby.mode == 1:
                kobby.image2.clip_composite_draw(25 * kobby.frame, 85, 25, 25, 0, 'h', kobby.screen_x + 2, kobby.y + 2, 50, 50)
            elif kobby.mode == 2:
                kobby.image3.clip_composite_draw(32 * kobby.frame, 120, 32, 40, 0, 'h', kobby.screen_x + 7, kobby.y + 17, 64, 80)
            elif kobby.mode == 3:
                kobby.image4.clip_composite_draw(25 * kobby.frame, 84, 25, 28, 0, 'h', kobby.screen_x, kobby.y + 5, 50, 56)
            elif kobby.mode == 4:
                kobby.image5.clip_composite_draw(25 * kobby.frame, 112, 25, 40, 0, 'h', kobby.screen_x, kobby.y + 15, 50, 80)

class Balloon:
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


class Kobby:
    first = None
    def __init__(self):
        self.x,self.y = 0, 500
        self.past_x = 0
        self.screen_x = 0
        self.gravity = 1
        self.jump_power = 10
        self.frame = 0
        self.dir = 0
        self.face_dir = 0
        self.timer = 0
        self.action = 0
        self.ground = False
        self.mode = 0 #mode 0: 기본 1: 마법사 2: 검사 3: 얼음 4: 불꽃
        if Kobby.first == None:
            self.image=load_image('nomal_kobby_sheet.png')
            self.image2=load_image('magic_kobby_sheet.png')
            self.image3=load_image('sword_kobby_sheet.png')
            self.image4=load_image('ice_kobby_sheet.png')
            self.image5=load_image('fire_kobby_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {left_down: Walk, left_up: Idle, right_down: Walk, right_up: Idle, down_down: Squashed, down_up: Idle, double_right: Run, double_left: Run, down_k: Jump},
                Squashed: {down_up: Idle, left_down: Squashed, right_down: Squashed, left_up: Squashed, right_up: Squashed},
                Walk: {right_down: Idle, right_up: Idle, left_down: Idle, left_up: Idle, down_down: Squashed, down_up: Idle, down_k: Jump},
                Run: {right_down: Run, left_down: Run, right_up: Idle, left_up: Idle, down_k: Jump},
                Jump: {time_out: Idle, left_down: Jump, right_down: Jump, left_up: Jump, right_up: Jump},
            }
        )

    def update(self):
        self.state_machine.update()
        if self.timer != 0:
            self.timer += 0.05
            if self.timer >= 0.5:
                self.timer = 0
        #중력
        if self.ground == False:
            self.gravity = (self.gravity + 0.5)
        else:
            self.gravity = 1

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_1: # 임시로 변신 키
            self.mode = (self.mode + 1) % 5
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            if self.timer == 0:
                self.timer = 0.01
                self.state_machine.add_event(
                    ('INPUT', event)
                )
            elif self.timer <= 0.3:
                self.state_machine.add_event(
                    ('DOUBLE_INPUT', event)
                )
            else:
                self.state_machine.add_event(
                    ('INPUT', event)
                )
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            if self.timer == 0:
                self.timer = 0.01
                self.state_machine.add_event(
                    ('INPUT', event)
                )
            elif self.timer <= 0.3:
                self.state_machine.add_event(
                    ('DOUBLE_INPUT', event)
                )
            else:
                self.state_machine.add_event(
                    ('INPUT', event)
                )
        else:
            self.state_machine.add_event(
                ('INPUT', event)
            )

    def draw(self):
        self.state_machine.draw()