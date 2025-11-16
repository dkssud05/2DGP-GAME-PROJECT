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

    # 캐릭터 1
    if highlighted == 1:
        draw_rectangle(200 - 80, 300 - 80, 200 + 80, 300 + 80)
        char1_image.clip_draw(0, 0, 200, 200, 200, 300, 150, 150)
    else:
        draw_rectangle(200 - 70, 300 - 70, 200 + 70, 300 + 70)
        char1_image.clip_draw(0, 0, 200, 200, 200, 300, 130, 130)

    # 캐릭터 2
    if highlighted == 2:
        draw_rectangle(400 - 80, 300 - 80, 400 + 80, 300 + 80)
        char2_image.clip_draw(0, 0, 200, 200, 400, 300, 150, 150)
    else:
        draw_rectangle(400 - 70, 300 - 70, 400 + 70, 300 + 70)
        char2_image.clip_draw(0, 0, 200, 200, 400, 300, 130, 130)

    # 캐릭터 3
    if highlighted == 3:
        draw_rectangle(600 - 80, 300 - 80, 600 + 80, 300 + 80)
        char3_image.clip_draw(0, 0, 200, 200, 600, 300, 150, 150)
    else:
        draw_rectangle(600 - 70, 300 - 70, 600 + 70, 300 + 70)
        char3_image.clip_draw(0, 0, 200, 200, 600, 300, 130, 130)


    update_canvas()

def handle_events():
    global highlighted, selected_character
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_LEFT:
                # 왼쪽 방향키: 이전 캐릭터 선택
                highlighted = max(1, highlighted - 1)
            elif event.key == SDLK_RIGHT:
                # 오른쪽 방향키: 다음 캐릭터 선택
                highlighted = min(3, highlighted + 1)
            elif event.key == SDLK_RETURN:
                # 엔터키: 선택 확정 및 게임 시작
                selected_character = highlighted
                import play_mode
                game_framework.change_mode(play_mode)

def pause():
    pass

def resume():
    pass

