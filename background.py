from pico2d import load_image


class Background:
    def __init__(self):
        self.image = load_image('background1.png')
    def update(self):
        pass
    def draw(self):
        self.image.draw(750,300,1500,600)
