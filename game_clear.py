from pico2d import load_image, get_time, clear_canvas, update_canvas, get_events, load_music
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
import game_framework
import title_mode


def init():
    global image
    global sound
    global game_clear_time

    image = load_image('game_clear.png')
    sound = load_music('game_clear.mp3')
    sound.set_volume(10)
    sound.play()
    game_clear_time = get_time()

def finish():
    global image
    global sound
    del image
    del sound

def update():
    global game_clear_time
    if get_time() - game_clear_time >= 4:
        game_clear_time = get_time()
        game_framework.change_mode(title_mode)


def draw():
    clear_canvas()
    image.draw(400, 300, 800, 600)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def pause():
    pass

def resume():
    pass