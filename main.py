from pico2d import *

open_canvas(800, 600)

# Idle 애니메이션용 이미지 로드
character1 = load_image('character1.motion/char1_Idle.png')

char1_x = 400
char1_y = 300
frame = 0
dir_x = 0

# 점프 관련 변수
is_jumping = False
jump_time = 0

running = True
while running:

    clear_canvas()

    character1.clip_draw(frame * 200, 0, 200, 200, char1_x, char1_y, 200, 200)

    frame = (frame + 1) % 8

    # 좌우 이동
    char1_x += dir_x * 5

    # 점프 처리 (간단한 위아래 이동)
    if is_jumping:
        if jump_time < 10:
            char1_y += 5  # 위로 올라가기
        elif jump_time < 20:
            char1_y -= 5  # 아래로 내려가기
        else:
            is_jumping = False
            jump_time = 0
        jump_time += 1

    update_canvas()

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                dir_x = -1
            elif event.key == SDLK_RIGHT:
                dir_x = 1
            elif event.key == SDLK_UP:
                if not is_jumping:
                    is_jumping = True
                    jump_time = 0
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT or event.key == SDLK_RIGHT:
                dir_x = 0

    delay(0.05)

close_canvas()
