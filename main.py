from pico2d import *

open_canvas(800, 600)

# Idle 애니메이션용 이미지 로드
character1 = load_image('character1.motion/char1_Idle.png')

char1_x = 400
char1_y = 300
frame = 0  # 애니메이션 프레임

running = True
while running:

    clear_canvas()

    # Idle 애니메이션 (10프레임)
    character1.clip_draw(frame * 200, 0, 200, 200, char1_x, char1_y, 200, 200)

    # 프레임 업데이트
    frame = (frame + 1) % 8

    update_canvas()

    #이벤트 처리
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

    delay(0.05)

close_canvas()
