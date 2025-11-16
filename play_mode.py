from pico2d import *
import game_framework
import game_world
import character_select_mode
from background import Background
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
        else:
            for char in characters:
                char.handle_event(event)

def init():
    global characters

    game_world.world = [[], []]

    background = Background()
    game_world.add_object(background, 0)

    # 선택된 캐릭터에 따라 생성
    if character_select_mode.selected_character == 1:
        character = Character1()
    elif character_select_mode.selected_character == 2:
        character = Character2()
    else:  # 3 or None (default)
        character = Character3()

    game_world.add_object(character, 1)
    characters = [character]


def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass