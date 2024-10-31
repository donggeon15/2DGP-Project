from pico2d import load_image


class Ground:
    def __init__(self):
        self.image=load_image('ground1.png')
        self.x,self.y = 750,100

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x,self.y,1500,200)
