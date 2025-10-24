from pico2d import *

open_canvas(800, 600)

running = True
while running:

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

    delay(0.01)

close_canvas()
