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

    characters = []

    if character_select_mode.selected_character == 1:
        character1 = Character1()
        character1.x = 200
    elif character_select_mode.selected_character == 2:
        character1 = Character2()
        character1.x = 200
    else:
        character1 = Character3()
        character1.x = 200

    character1.player_id = 2
    game_world.add_object(character1, 1)
    characters.append(character1)

    if character_select_mode.selected_character2 == 1:
        character2 = Character1()
        character2.x = 600
    elif character_select_mode.selected_character2 == 2:
        character2 = Character2()
        character2.x = 600
    elif character_select_mode.selected_character2 == 3:
        character2 = Character3()
        character2.x = 600
    else:
        character2 = Character1()
        character2.x = 600

    character2.player_id = 1
    game_world.add_object(character2, 1)
    characters.append(character2)


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