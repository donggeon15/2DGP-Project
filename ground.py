from pico2d import load_image


class Ground:
    def __init__(self, object):
        self.image1 = load_image('ground1.png')
        self.image2 = load_image('ground1_grass.png')
        self.x,self.y = 750,150
        self.object = object
        self.frame = 0

    def update(self):
        #self.frame = (self.frame + 1) % 4
        pass

    def draw(self):
        if self.object == 0:
            self.image1.clip_draw(0, self.frame * 205, 1585, 205, self.x,self.y,3000,400)
        elif self.object == 1:
            self.image2.clip_draw(0, self.frame * 205, 1585, 205, self.x,self.y,3000,400)