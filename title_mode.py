from pico2d import *
import game_framework

image = None
running = True
start_time = 0

def init():
    global image
    image = load_image('title.png')
    start_time = get_time()

def finish():
    global image
    del image

def update():
    global running
    if get_time() - start_time > 3.0:
        import character_select_mode
        game_framework.change_mode(character_select_mode)

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def pause():
    pass

def resume():
    pass