from pico2d import *
import game_framework

# 전역 변수
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

    font = load_font()

    highlighted = 1
    selected_character = None

def finish():
    pass

def update():
    pass

def draw():
    clear_canvas()

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

