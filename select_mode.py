from pico2d import *
import game_framework
import character_select
import help_mode

MENU_VS_MODE = 0
MENU_AI_MODE = 1
MENU_HELP = 2
MENU_EXIT = 3

selected_menu = MENU_VS_MODE
font = None
background = None

def init():
    global font, background, selected_menu
    font = load_font('C:/Windows/Fonts/arial.ttf', 40)
    background = load_image('select_background.png')
    selected_menu = MENU_VS_MODE

def finish():
    global font, background
    del font
    del background

def update():
    pass

def draw():
    clear_canvas()

    background.draw(400, 300)

    font.draw(250, 450, 'FIGHTING GAME', (255, 255, 0))

    menus = [
        (MENU_VS_MODE, '1 vs 1 Mode', 350),
        (MENU_AI_MODE, 'AI Mode', 280),
        (MENU_HELP, 'Help', 210),
        (MENU_EXIT, 'Exit', 140)
    ]

    for menu_id, menu_text, y_pos in menus:
        if menu_id == selected_menu:
            # 선택된 메뉴에만 화살표 표시
            font.draw(220, y_pos, '> ' + menu_text, (255, 255, 255))
        else:
            # 선택되지 않은 메뉴는 화살표 없이 표시
            font.draw(250, y_pos, menu_text, (255, 255, 255))


    update_canvas()

def handle_events():
    global selected_menu
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_UP:
                # 메뉴 위로 이동
                selected_menu = (selected_menu - 1) % 4
            elif event.key == SDLK_DOWN:
                # 메뉴 아래로 이동
                selected_menu = (selected_menu + 1) % 4
            elif event.key == SDLK_RETURN:
                # 선택한 메뉴 실행
                if selected_menu == MENU_VS_MODE:
                    game_framework.change_mode(character_select)
                elif selected_menu == MENU_AI_MODE:
                    # AI 모드는 구현 안됨
                    print("아직 구현 안됐습니다!")
                elif selected_menu == MENU_HELP:
                    # Help 화면으로 이동
                    game_framework.change_mode(help_mode)
                elif selected_menu == MENU_EXIT:
                    game_framework.quit()

def pause():
    pass

def resume():
    pass
