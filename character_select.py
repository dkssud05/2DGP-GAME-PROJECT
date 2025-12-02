from pico2d import *
import game_framework

selected_character = None
selected_character2 = None
highlighted = 1
selection_step = 1
char1_image = None
char2_image = None
char3_image = None

def init():
    global char1_image, char2_image, char3_image, highlighted, selected_character, selected_character2, selection_step

    char1_image = load_image('character1.motion/char1_Idle.png')
    char2_image = load_image('character2.motion/char2_Idle.png')
    char3_image = load_image('character3.motion/char3_Idle.png')

    highlighted = 1
    selected_character = None
    selected_character2 = None
    selection_step = 1

def finish():
    global char1_image, char2_image, char3_image
    del char1_image
    del char2_image
    del char3_image

def update():
    pass

def draw():
    clear_canvas()

    if selected_character == 1:
        draw_rectangle(200 - 90, 300 - 90, 200 + 90, 300 + 90)
        draw_rectangle(200 - 85, 300 - 85, 200 + 85, 300 + 85)
        draw_rectangle(200 - 80, 300 - 80, 200 + 80, 300 + 80)
        char1_image.clip_draw(0, 0, 200, 200, 200, 300, 160, 160)
    elif selected_character2 == 1:
        draw_rectangle(200 - 85, 300 - 85, 200 + 85, 300 + 85)
        draw_rectangle(200 - 80, 300 - 80, 200 + 80, 300 + 80)
        char1_image.clip_draw(0, 0, 200, 200, 200, 300, 155, 155)
    elif highlighted == 1:
        draw_rectangle(200 - 80, 300 - 80, 200 + 80, 300 + 80)
        char1_image.clip_draw(0, 0, 200, 200, 200, 300, 150, 150)
    else:
        draw_rectangle(200 - 70, 300 - 70, 200 + 70, 300 + 70)
        char1_image.clip_draw(0, 0, 200, 200, 200, 300, 130, 130)

    if selected_character == 2:
        draw_rectangle(400 - 90, 300 - 90, 400 + 90, 300 + 90)
        draw_rectangle(400 - 85, 300 - 85, 400 + 85, 300 + 85)
        draw_rectangle(400 - 80, 300 - 80, 400 + 80, 300 + 80)
        char2_image.clip_draw(0, 0, 200, 200, 400, 300, 160, 160)
    elif selected_character2 == 2:
        draw_rectangle(400 - 85, 300 - 85, 400 + 85, 300 + 85)
        draw_rectangle(400 - 80, 300 - 80, 400 + 80, 300 + 80)
        char2_image.clip_draw(0, 0, 200, 200, 400, 300, 155, 155)
    elif highlighted == 2:
        draw_rectangle(400 - 80, 300 - 80, 400 + 80, 300 + 80)
        char2_image.clip_draw(0, 0, 200, 200, 400, 300, 150, 150)
    else:
        draw_rectangle(400 - 70, 300 - 70, 400 + 70, 300 + 70)
        char2_image.clip_draw(0, 0, 200, 200, 400, 300, 130, 130)

    if selected_character == 3:
        draw_rectangle(600 - 90, 300 - 90, 600 + 90, 300 + 90)
        draw_rectangle(600 - 85, 300 - 85, 600 + 85, 300 + 85)
        draw_rectangle(600 - 80, 300 - 80, 600 + 80, 300 + 80)
        char3_image.clip_draw(0, 0, 126, 126, 600, 300, 160, 160)
    elif selected_character2 == 3:
        draw_rectangle(600 - 85, 300 - 85, 600 + 85, 300 + 85)
        draw_rectangle(600 - 80, 300 - 80, 600 + 80, 300 + 80)
        char3_image.clip_draw(0, 0, 126, 126, 600, 300, 155, 155)
    elif highlighted == 3:
        draw_rectangle(600 - 80, 300 - 80, 600 + 80, 300 + 80)
        char3_image.clip_draw(0, 0, 126, 126, 600, 300, 150, 150)
    else:
        draw_rectangle(600 - 70, 300 - 70, 600 + 70, 300 + 70)
        char3_image.clip_draw(0, 0, 126, 126, 600, 300, 130, 130)


    update_canvas()

def handle_events():
    global highlighted, selected_character, selected_character2, selection_step
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                import select_mode
                game_framework.change_mode(select_mode)
            elif event.key == SDLK_LEFT:
                highlighted = max(1, highlighted - 1)
            elif event.key == SDLK_RIGHT:
                highlighted = min(3, highlighted + 1)
            elif event.key == SDLK_RETURN:
                if selection_step == 1:
                    selected_character = highlighted
                    selection_step = 2
                    highlighted = highlighted % 3 + 1
                elif selection_step == 2:
                    if highlighted != selected_character:
                        selected_character2 = highlighted
                        import play_mode
                        game_framework.change_mode(play_mode)

def pause():
    pass

def resume():
    pass

