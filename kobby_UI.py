from pico2d import load_image

class UI:
    def __init__(self, heart = 0, hp = 0):
        self.image1 = load_image('hpUI1.png')
        self.image2 = load_image('hpUI2.png')
        self.image3 = load_image('hpUI3.png')
        self.icon_image = load_image('heart_icon1.png')
        self.icon_image2 = load_image('heart_icon2.png')
        self.icon_image3 = load_image('heart_icon3.png')
        self.heart = heart
        self.hp = hp


    def draw(self):
        self.image1.draw(100, 550, 162, 56)
        self.icon_image3.draw(60, 500, 74, 32)

    def update(self):
        pass

