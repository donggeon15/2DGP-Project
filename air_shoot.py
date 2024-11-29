from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import server

PIXEL_PER_METER = (25.0 / 0.2) # 25pixel = 20cm
AIRSHOOT_SPEED_KMPH = 9.0 # km/h
AIRSHOOT_SPEED_MPM = (AIRSHOOT_SPEED_KMPH * 1000.0 / 60.0)
AIRSHOOT_SPEED_MPS = (AIRSHOOT_SPEED_MPM / 60.0)
AIRSHOOT_SPEED_PPS = (AIRSHOOT_SPEED_MPS * PIXEL_PER_METER)


class Air_shoot:
    image = None
    image2 = None
    image3 = None

    def __init__(self, x=400, y=300, velocity = 1, air = 0):
        if Air_shoot.image == None:
            Air_shoot.image = load_image('air_shoot.png')
        if Air_shoot.image2 == None:
            Air_shoot.image2 = load_image('sword_shoot.png')
        if Air_shoot.image3 == None:
            Air_shoot.image3 = load_image('fire_shoot.png')
        self.x, self.y, self.velocity, self.air = x, y, velocity, air
        self.sx = self.x - server.ground1.window_left
        self.sy = self.y - server.ground1.window_bottom
        self.frame = 0
        self.frame2 = 0

    def draw(self):
        draw_rectangle(*self.get_bb())
        if self.air == 0:
            if self.velocity > 0:
                self.image.clip_draw(20 * int(self.frame), 0, 20, 20, self.sx, self.sy, 50, 50)
            else:
                self.image.clip_composite_draw(20 * int(self.frame), 0, 20, 20, 0, 'h', self.sx, self.sy, 50, 50)
        elif self.air == 1:
            if self.velocity > 0:
                self.image2.clip_draw(35 * int(self.frame), 0, 35, 30, self.sx, self.sy, 70, 60)
            else:
                self.image2.clip_composite_draw(35 * int(self.frame), 0, 35, 30, 0, 'h', self.sx, self.sy, 70, 60)
        elif self.air == 2:
            if self.velocity > 0:
                self.image3.clip_draw(20 * int(self.frame), 0, 20, 20, self.sx, self.sy, 40, 40)
            else:
                self.image3.clip_composite_draw(20 * int(self.frame), 0, 20, 20, 0, 'h', self.sx, self.sy, 40, 40)

    def update(self):
        self.x += self.velocity * AIRSHOOT_SPEED_PPS * game_framework.frame_time

        if server.kobby.stage == 4:
            self.sx = self.x
            self.sy = self.y
        else:
            self.sx = self.x - server.ground1.window_left
            self.sy = self.y - server.ground1.window_bottom

        if self.air == 0:
            self.frame = (self.frame + 4 * (1.0 / 0.5) * game_framework.frame_time)
            if self.frame >= 5:
                game_world.remove_object(self)
        if self.air == 1:
            self.frame = (self.frame + 4 * (1.0 / 2.0) * game_framework.frame_time)
            if self.frame >= 2:
                game_world.remove_object(self)
        if self.air == 2:
            self.frame = (self.frame + 4 * (1.0 / 1.0) * game_framework.frame_time)
            if self.frame >= 3:
                game_world.remove_object(self)

    def get_bb(self):
        if self.air == 0 or self.air == 1:
            return self.sx - 20, self.sy - 20, self.sx + 20, self.sy + 20
        if self.air == 2:
            return self.sx - 10, self.sy - 10, self.sx + 10, self.sy + 10

    def handle_collision(self, group, other):
        if group == 'air:monster' or group == 'kobby:air':
            if self in game_world.objects[1]:
                game_world.remove_object(self)
