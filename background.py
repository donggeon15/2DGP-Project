from pico2d import load_image


class Background:
    def __init__(self):
        self.image = load_image('background1.png')
        self.x = 750
    def update(self):
        pass
    def draw(self):
        self.image.draw(self.x,300,3000,800)
