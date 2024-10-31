from pico2d import load_image


class Ground:
    def __init__(self):
        self.image=load_image('ground1.png')
        self.x,self.y = 750,150
        self.frame = 0

    def update(self):
        #self.frame = (self.frame + 1) % 4
        pass

    def draw(self):
        self.image.clip_draw(0, self.frame * 205, 1585, 205, self.x,self.y,3000,400)
