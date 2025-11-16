from pico2d import *
import game_framework

selected_character = None
highlighted = 1
char1_image = None
char2_image = None
char3_image = None

def init():
    global char1_image, char2_image, char3_image, highlighted, selected_character

    char1_image = load_image('character1.motion/char1_Idle.png')
    char2_image = load_image('character2.motion/char2_Idle.png')
    char3_image = load_image('character3.motion/char3_Idle.png')

    highlighted = 1
    selected_character = None

def finish():
    global char1_image, char2_image, char3_image
    del char1_image
    del char2_image
    del char3_image

def update():
    pass

def draw():
    clear_canvas()

    if highlighted == 1:
        char1_image.clip_draw(0, 0, 200, 200, 200, 300, 180, 180)
    else:
        char1_image.clip_draw(0, 0, 200, 200, 200, 300, 150, 150)

    if highlighted == 2:
        char2_image.clip_draw(0, 0, 200, 200, 400, 300, 180, 180)
    else:
        char2_image.clip_draw(0, 0, 200, 200, 400, 300, 150, 150)

    if highlighted == 3:
        char3_image.clip_draw(0, 0, 200, 200, 600, 300, 180, 180)
    else:
        char3_image.clip_draw(0, 0, 200, 200, 600, 300, 150, 150)

    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()

def pause():
    pass

def resume():
    pass

