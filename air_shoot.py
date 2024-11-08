from pico2d import load_image

import game_world


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
            self.image.clip_draw(20 * self.frame, 0, 20, 20, self.x, self.y, 50, 50)
        else:
            self.image.clip_composite_draw(20 * self.frame, 0, 20, 20, 0, 'h', self.x, self.y, 50, 50)

    def update(self):
        self.x += self.velocity
        self.frame2 += 1
        if self.frame2 >= 3:
            self.frame = (self.frame + 1)
            if self.frame == 6:
                game_world.remove_object(self)

