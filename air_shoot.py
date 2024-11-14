from pico2d import load_image

import game_framework
import game_world

PIXEL_PER_METER = (25.0 / 0.2) # 25pixel = 20cm
AIRSHOOT_SPEED_KMPH = 9.0 # km/h
AIRSHOOT_SPEED_MPM = (AIRSHOOT_SPEED_KMPH * 1000.0 / 60.0)
AIRSHOOT_SPEED_MPS = (AIRSHOOT_SPEED_MPM / 60.0)
AIRSHOOT_SPEED_PPS = (AIRSHOOT_SPEED_MPS * PIXEL_PER_METER)


class Air_shoot:
    image = None

    def __init__(self, x=400, y=300, velocity = 1):
        if Air_shoot.image == None:
            Air_shoot.image = load_image('air_shoot.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.frame2 = 0

    def draw(self):
        if self.velocity > 0:
            self.image.clip_draw(20 * int(self.frame), 0, 20, 20, self.x, self.y, 50, 50)
        else:
            self.image.clip_composite_draw(20 * int(self.frame), 0, 20, 20, 0, 'h', self.x, self.y, 50, 50)

    def update(self):
        self.x += self.velocity * AIRSHOOT_SPEED_PPS * game_framework.frame_time
        self.frame = (self.frame + 4 * (1.0 / 0.5) * game_framework.frame_time)
        if self.frame == 6:
            game_world.remove_object(self)

