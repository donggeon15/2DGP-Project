from pico2d import load_image, draw_rectangle, get_time, load_wav
from pygame.examples.cursors import image

import game_framework
import game_world
import server

PIXEL_PER_METER = (25.0 / 0.2) # 25pixel = 20cm
AIRSHOOT_SPEED_KMPH = 8.5 # km/h
AIRSHOOT_SPEED_MPM = (AIRSHOOT_SPEED_KMPH * 1000.0 / 60.0)
AIRSHOOT_SPEED_MPS = (AIRSHOOT_SPEED_MPM / 60.0)
AIRSHOOT_SPEED_PPS = (AIRSHOOT_SPEED_MPS * PIXEL_PER_METER)


class Air_shoot:
    image = None
    image2 = None
    image3 = None
    image4 = None
    image5 = None
    sound = None

    def __init__(self, x=400, y=300, velocity = 1, air = 0, type = 0):
        if Air_shoot.image == None:
            Air_shoot.image = load_image('./resource/air_shoot.png')
        if Air_shoot.image2 == None:
            Air_shoot.image2 = load_image('./resource/sword_shoot.png')
        if Air_shoot.image3 == None:
            Air_shoot.image3 = load_image('./resource/fire_shoot.png')
        if Air_shoot.image4 == None:
            Air_shoot.image4 = load_image('./resource/ice_shoot.png')
        if Air_shoot.image5 == None:
            Air_shoot.image5 = load_image('./resource/star_shoot.png')
        if Air_shoot.sound == None:
            self.star_sound = load_wav('./resource/movestar.wav')
            self.star_sound.set_volume(30)
            self.fire_sound = load_wav('./resource/fire_shoot.wav')
            self.fire_sound.set_volume(20)
            self.ice_sound = load_wav('./resource/ice_shoot.wav')
            self.ice_sound.set_volume(20)
        self.x, self.y, self.velocity, self.air = x, y, velocity, air
        self.past_x = x
        self.sx = self.x - server.ground1.window_left
        self.sy = self.y - server.ground1.window_bottom
        self.frame = 0
        self.frame2 = 0
        self.type = type
        self.sound_time = get_time()
        self.time = get_time()
        if self.air == 4:
            self.star_sound.play(1)
        if self.air == 3:
            self.ice_sound.play(1)
        if self.air == 2:
            self.fire_sound.play(1)


    def draw(self):
        #draw_rectangle(*self.get_bb())
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
        elif self.air == 3:
            if self.velocity > 0:
                self.image4.clip_draw(24 * int(self.frame), 0, 24, 24, self.sx, self.sy, 48, 48)
            else:
                self.image4.clip_composite_draw(24 * int(self.frame), 0, 24, 24, 0, 'h', self.sx, self.sy, 48, 48)
        elif self.air == 4:
            if self.velocity > 0:
                self.image5.clip_draw(25 * int(self.frame), 0, 25, 25, self.sx, self.sy, 50, 50)
            else:
                self.image5.clip_composite_draw(25 * int(self.frame), 0, 25, 25, 0, 'h', self.sx, self.sy, 50, 50)

    def update(self):
        self.past_x = self.x
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
        if self.air == 3:
            self.frame = (self.frame + 4 * (1.0 / 0.7) * game_framework.frame_time)
            if self.frame >= 6:
                game_world.remove_object(self)
        if self.air == 4:
            if get_time() - self.sound_time > 1:
                self.star_sound.play(1)
                self.sound_time = get_time()
            self.frame = (self.frame + 4 * (1.0 / 0.5) * game_framework.frame_time) % 4
            if get_time() - self.time > 7:
                game_world.remove_object(self)
            if server.kobby.stage == 1:
                if (self.x <= 0):
                    if self.x < self.past_x:
                        self.velocity = -self.velocity
                    else:
                        self.velocity = -self.velocity
                elif ((self.x >= 600 and self.x < 760) or (self.x >= 1070 and self.x < 1140) or
                      (self.x >= 1350 and self.x < 1525) or (self.x > 1820 and self.x < 2280) or
                      (self.x > 2420 and self.x < 3000)):
                    if self.y > 200 - 25:
                        pass
                    elif self.y <= 200 - 25 and self.y > 200 - 35:
                        pass
                    else:
                        if self.x < self.past_x:
                            self.velocity  = -self.velocity
                        else:
                            self.velocity  = -self.velocity
                elif ((self.x >= 1525 and self.x < 1640) or (self.x >= 2370 and self.x < 2420)):
                    if self.y > 200 + 70:
                        pass
                    elif self.y <= 200 + 70 and self.y > 200 + 60:
                        pass
                    else:
                        if self.x < self.past_x:
                            self.velocity  = -self.velocity
                        else:
                            self.velocity  = -self.velocity
                elif ((self.x >= 2280 and self.x < 2370)):
                    if self.y > 200 + 135:
                        pass
                    elif self.y <= 200 + 135 and self.y > 200 + 125:
                        pass
                    else:
                        if self.x < self.past_x:
                            self.velocity = -self.velocity
                        else:
                            self.velocity = -self.velocity
                elif (self.x >= 3000):
                    if self.x < self.past_x:
                        self.velocity = -self.velocity
                    else:
                        self.velocity = -self.velocity
            elif server.kobby.stage == 2:
                if (self.x <= 0):
                    if self.x < self.past_x:
                        self.velocity = -self.velocity
                    else:
                        self.velocity = -self.velocity
                elif ((self.x >= 780 and self.x < 900)):
                    if self.y > 235:
                        pass
                    elif self.y <= 235 and self.y > 230:
                        pass
                    else:
                        if self.x < self.past_x:
                            self.velocity = -self.velocity
                        else:
                            self.velocity = -self.velocity
                elif ((self.x >= 900 and self.x < 1200) or (self.x >= 1740 and self.x < 1850) or (
                        self.x >= 1970 and self.x < 2085)):
                    if self.y > 270:
                        pass
                    elif self.y <= 270 and self.y > 265:
                        pass
                    else:
                        if self.x < self.past_x:
                            self.velocity = -self.velocity
                        else:
                            self.velocity = -self.velocity
                elif ((self.x >= 1850 and self.x < 1880) or (self.x >= 1940 and self.x < 1970)):
                    if self.y > 110:
                        pass
                    elif self.y <= 110 and self.y > 108:
                        pass
                    else:
                        if self.x < self.past_x:
                            self.velocity = -self.velocity
                        else:
                            self.velocity = -self.velocity
                elif (self.x >= 3000):
                    if self.x < self.past_x:
                        self.velocity = -self.velocity
                    else:
                        self.velocity = -self.velocity
            elif server.kobby.stage == 3:
                if (self.x <= 0):
                    if self.x < self.past_x:
                        self.velocity = -self.velocity
                    else:
                        self.velocity = -self.velocity
                elif (self.x >= 3000):
                    if self.x < self.past_x:
                        self.velocity = -self.velocity
                    else:
                        self.velocity = -self.velocity
            elif server.kobby.stage == 4:
                if (self.x <= 0):
                    if self.x < self.past_x:
                        self.velocity = -self.velocity
                    else:
                        self.velocity = -self.velocity
                elif (self.x >= 800):
                    if self.x < self.past_x:
                        self.velocity = -self.velocity
                    else:
                        self.velocity = -self.velocity


    def get_bb(self):
        if self.air == 0 or self.air == 1 or self.air == 4:
            return self.sx - 20, self.sy - 20, self.sx + 20, self.sy + 20
        if self.air == 2 or self.air == 3:
            return self.sx - 10, self.sy - 10, self.sx + 10, self.sy + 10

    def handle_collision(self, group, other):
        if group == 'air:monster' or group == 'kobby:air':
            if self.air == 2: #불꽃
                server.kobby.damage_type = 1
            elif self.air == 3: #얼음
                server.kobby.damage_type = 3
            else:
                server.kobby.damage_type = 0
            if self in game_world.objects[1]:
                game_world.remove_object(self)
        if group == 'kobby:food':
            if server.kobby.x < self.x:
                self.past_x = self.x
                self.x -= AIRSHOOT_SPEED_PPS * 1.4 * game_framework.frame_time
            else:
                self.past_x = self.x
                self.x += AIRSHOOT_SPEED_PPS * 1.4 * game_framework.frame_time
            if server.kobby.y < self.y:
                self.y -= AIRSHOOT_SPEED_PPS * 1.4 * game_framework.frame_time
            else:
                self.y += AIRSHOOT_SPEED_PPS * 1.4 * game_framework.frame_time

            if server.kobby.x <= self.x + 3 and server.kobby.x >= self.x - 3:
                server.kobby.food = True
                if self.type == 0:
                    server.kobby.food_type = 0
                    server.kobby.star_type = 0
                elif self.type == 1:
                    server.kobby.food_type = 1
                    server.kobby.star_type = 1
                elif self.type == 2:
                    server.kobby.food_type = 2
                    server.kobby.star_type = 2
                elif self.type == 3:
                    server.kobby.food_type = 3
                    server.kobby.star_type = 3
                elif self.type == 4:
                    server.kobby.food_type = 4
                    server.kobby.star_type = 4
                game_world.remove_object(self)