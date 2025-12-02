from pico2d import *
import game_framework
import character_select

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
    background = load_image('title.png')
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
        (MENU_VS_MODE, '1 vs 1 Mode', 250),
        (MENU_AI_MODE, 'AI Mode', 200),
        (MENU_HELP, 'Help', 150),
        (MENU_EXIT, 'Exit', 100)
    ]

    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                game_framework.change_mode(character_select)

def pause():
    pass

def resume():
    pass
