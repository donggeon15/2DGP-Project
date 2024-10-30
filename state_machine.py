from pico2d import *

def start_event(e):
    return e[0] == 'START'

def time_out(e):
    return e[0] == 'TIME_OUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def double_right(e):
    return e[0] == 'DOUBLE_INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def double_left(e):
    return e[0] == 'DOUBLE_INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

class StateMachine:
    def __init__(self, o):
        self.o = o
        self.event_que = []

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            e = self.event_que.pop(0)
            for event_check, next_state in self.transitions[self.cur_state].items():
                if event_check(e):
                    self.cur_state.exit(self.o, e)
                    print(f'EXIT from {self.cur_state}')
                    self.cur_state = next_state
                    self.cur_state.enter(self.o, e)
                    print(f'ENTER into {self.cur_state}')
                    return

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.o, ('START', 0))
        print(f'ENTER into {self.cur_state}')

    def draw(self):
        self.cur_state.draw(self.o)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def add_event(self, e):
        self.event_que.append(e)
        print(f'   DEBUG: new event {e} is added to event Que')