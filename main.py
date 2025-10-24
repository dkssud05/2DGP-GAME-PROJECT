from pico2d import *

open_canvas(800, 600)

character1 = load_image('character1.motion/char1_Attack1.png')

char1_x = 400
char1_y = 300

running = True
while running:

    clear_canvas()

    character1.draw(char1_x, char1_y)

    update_canvas()

    #이벤트 처리
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

    delay(0.01)

close_canvas()
