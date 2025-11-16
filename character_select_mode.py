from pico2d import *
import game_framework

selected_character = None  # 선택된 캐릭터 번호 (1, 2, 3)
highlighted = 1  # 현재 하이라이트된 캐릭터
char1_image = None
char2_image = None
char3_image = None
font = None

def init():
    global char1_image, char2_image, char3_image, font, highlighted, selected_character

    char1_image = load_image('character1.motion/char1_Idle.png')
    char2_image = load_image('character2.motion/char2_Idle.png')
    char3_image = load_image('character3.motion/char3_Idle.png')

    font = load_font(None, 32)

    highlighted = 1
    selected_character = None

def finish():
    global char1_image, char2_image, char3_image, font
    del char1_image
    del char2_image
    del char3_image
    del font

def update():
    pass

def draw():
    clear_canvas()

    # 타이틀 그리기
    font.draw(250, 500, 'SELECT CHARACTER', (255, 255, 255))

    # 캐릭터 1 그리기 (왼쪽)
    char1_image.clip_draw(0, 0, 200, 200, 200, 300, 150, 150)
    font.draw(130, 200, 'Character 1', (200, 200, 200))

    # 캐릭터 2 그리기 (중앙)
    char2_image.clip_draw(0, 0, 200, 200, 400, 300, 150, 150)
    font.draw(330, 200, 'Character 2', (200, 200, 200))

    # 캐릭터 3 그리기 (오른쪽)
    char3_image.clip_draw(0, 0, 200, 200, 600, 300, 150, 150)
    font.draw(530, 200, 'Character 3', (200, 200, 200))

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

