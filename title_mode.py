from pico2d import get_events, clear_canvas, update_canvas, load_image, load_wav, load_music
from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDL_QUIT, SDLK_SPACE

import description_mode
import game_framework


def init():
    global image
    global sound
    image = load_image('./resource/title.png')
    sound = load_music('./resource/Title.mp3')
    sound.set_volume(10)
    sound.repeat_play()

def finish():
    global image
    global sound
    del image
    del sound

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(description_mode)

def draw():
    clear_canvas()
    image.draw(400, 300 ,800, 600)
    update_canvas()

def update():
    pass

def pause():
    pass

def resume():
    pass