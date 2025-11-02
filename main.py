from pico2d import *
from character1 import Character1

open_canvas(800, 600)

boy = Boy()

running = True
while running:
    clear_canvas()

    boy.update()
    boy.draw()

    update_canvas()

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)

    delay(0.05)

close_canvas()
