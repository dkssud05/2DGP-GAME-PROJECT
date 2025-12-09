from pico2d import *
import game_framework
import select_mode

help_image = None

def init():
    global help_image
    help_image = load_image('Help.png')

def finish():
    global help_image
    del help_image

def update():
    pass

def draw():
    clear_canvas()

    # Help 이미지를 화면 중앙에 표시
    help_image.draw(400, 300)

    # ESC 안내 문구
    font = load_font('C:/Windows/Fonts/arial.ttf', 20)
    font.draw(250, 30, 'Press ESC to return to menu', (255, 255, 255))

    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                # ESC를 누르면 모드 선택창으로 돌아가기
                game_framework.change_mode(select_mode)

def pause():
    pass

def resume():
    pass

