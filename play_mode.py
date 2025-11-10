from pico2d import *
import game_framework
import game_world
from character1 import Character1
from character2 import Character2
from character3 import Character3

characters = []

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def init():
    global characters

    character1 = Character1()
    character2 = Character2()
    character3 = Character3()

    game_world.add_object(character1, 1)
    game_world.add_object(character2, 1)

def update():
    pass

def draw():
    global characters

    clear_canvas()

    for char in characters:
        char.draw()

    update_canvas()

def finish():
    pass

def pause():
    pass

def resume():
    pass