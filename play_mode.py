from pico2d import *
import game_framework
import game_world
import character_select as character_select_mode
from ui import UI
from background import Background
from character1 import Character1
from character2 import Character2
from character3 import Character3

characters = []
game_over = False
game_over_time = 0
winner = None
# 5판 3선승제 변수
round_over = False
round_over_time = 0
round_winner = None
player1_wins = 0
player2_wins = 0
current_round = 1
match_over = False

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            for char in characters:
                char.handle_event(event)

def reset_round():
    global characters, round_over, round_over_time, round_winner, current_round, game_over, game_over_time

    round_over = False
    round_over_time = 0
    round_winner = None
    game_over = False
    game_over_time = 0
    current_round += 1

    # 캐릭터 위치 및 HP 초기화
    if len(characters) >= 2:
        # Player 1 초기화
        characters[0].x = 200
        characters[0].y = 100
        characters[0].hp = 200
        characters[0].is_dead = False
        characters[0].is_jumping = False
        characters[0].jump_velocity = 0
        characters[0].state = characters[0].STATE_IDLE
        characters[0].frame = 0.0
        characters[0].is_attacking = False
        characters[0].attack_time = 0
        characters[0].is_hit = False
        characters[0].hit_cooldown = 0
        characters[0].hit_time = 0
        characters[0].death_time = 0
        characters[0].dir = 0
        characters[0].is_guarding = False
        characters[0].image = characters[0].idle_image  # 이미지를 idle로 초기화
        # 키 입력 상태 초기화
        for key in characters[0].keys:
            characters[0].keys[key] = False
        characters[0].attack_key_pressed = False
        characters[0].attack2_key_pressed = False
        if hasattr(characters[0], 'attack3_key_pressed'):
            characters[0].attack3_key_pressed = False
        # 대쉬 횟수 초기화
        characters[0].dash_count = 1

        # Player 2 초기화
        characters[1].x = 600
        characters[1].y = 100
        characters[1].hp = 200
        characters[1].is_dead = False
        characters[1].is_jumping = False
        characters[1].jump_velocity = 0
        characters[1].state = characters[1].STATE_IDLE
        characters[1].frame = 0.0
        characters[1].is_attacking = False
        characters[1].attack_time = 0
        characters[1].is_hit = False
        characters[1].hit_cooldown = 0
        characters[1].hit_time = 0
        characters[1].death_time = 0
        characters[1].dir = 0
        characters[1].is_guarding = False
        characters[1].image = characters[1].idle_image  # 이미지를 idle로 초기화
        # 키 입력 상태 초기화
        for key in characters[1].keys:
            characters[1].keys[key] = False
        characters[1].attack_key_pressed = False
        characters[1].attack2_key_pressed = False
        # Character3는 attack3_key_pressed도 있을 수 있음
        if hasattr(characters[1], 'attack3_key_pressed'):
            characters[1].attack3_key_pressed = False
        # 대쉬 횟수 초기화
        characters[1].dash_count = 1

    # UI 초기화
    ui1.update(200)
    ui2.update(200)
    ui1.reset_timer()

def init():
    global characters, ui1, ui2, round_over, round_over_time, round_winner
    global player1_wins, player2_wins, current_round, match_over, game_over, game_over_time

    # 라운드 변수 초기화
    round_over = False
    round_over_time = 0
    round_winner = None
    game_over = False
    game_over_time = 0
    match_over = False

    game_world.world = [[], []]

    background = Background()
    game_world.add_object(background, 0)

    characters = []

    if character_select_mode.selected_character == 1:
        character1 = Character1()
        character1.x = 200
    elif character_select_mode.selected_character == 2:
        character1 = Character2()
        character1.x = 200
    else:
        character1 = Character3()
        character1.x = 200

    character1.player_id = 1
    game_world.add_object(character1, 1)
    characters.append(character1)

    if character_select_mode.selected_character2 == 1:
        character2 = Character1()
        character2.x = 600
    elif character_select_mode.selected_character2 == 2:
        character2 = Character2()
        character2.x = 600
    elif character_select_mode.selected_character2 == 3:
        character2 = Character3()
        character2.x = 600
    else:
        character2 = Character1()
        character2.x = 600

    character2.player_id = 2
    game_world.add_object(character2, 1)
    characters.append(character2)

    ui1 = UI(max_hp = 200)
    ui2 = UI(max_hp = 200)
    ui2.x = 450


def update():
    global game_over, game_over_time, winner, round_over, round_over_time, round_winner
    global player1_wins, player2_wins, match_over

    if len(characters) >= 2:
        char1 = characters[0]
        char2 = characters[1]

        char1_prev_x = char1.x
        char2_prev_x = char2.x

    # 매치가 끝나지 않았을 때만 게임 진행
    if not match_over:
        game_world.update()

    if len(characters) >= 2:
        char1 = characters[0]
        char2 = characters[1]

        char1_bb = char1.get_bb()
        char2_bb = char2.get_bb()
        if collide(char1_bb, char2_bb):
            char1.x = char1_prev_x
            char2.x = char2_prev_x

        if not round_over and not match_over:
            char1_attack_bb = char1.get_attack_bb()
            if char1_attack_bb:
                char2_bb = char2.get_bb()
                if collide(char1_attack_bb, char2_bb):
                    damage = char1.get_attack_damage()
                    char2.take_damage(damage, char1.attack_id)

            char2_attack_bb = char2.get_attack_bb()
            if char2_attack_bb:
                char1_bb = char1.get_bb()
                if collide(char2_attack_bb, char1_bb):
                    damage = char2.get_attack_damage()
                    char1.take_damage(damage, char2.attack_id)

        # 라운드 종료 처리
        if char1.is_dead and not round_over and not match_over:
            round_over = True
            round_over_time = 0
            round_winner = 2
            player2_wins += 1
            print("=" * 50)
            print(f"라운드 {current_round} - 2P 승리!")
            print(f"현재 스코어: 1P {player1_wins} vs {player2_wins} 2P")
            print("=" * 50)

            if player2_wins >= 3:
                match_over = True
                winner = "2P"
                print("=" * 50)
                print(f"*** {winner} 최종 승리! ***")
                print("3초 후 게임이 종료됩니다...")
                print("=" * 50)

        elif char2.is_dead and not round_over and not match_over:
            round_over = True
            round_over_time = 0
            round_winner = 1
            player1_wins += 1
            print("=" * 50)
            print(f"라운드 {current_round} - 1P 승리!")
            print(f"현재 스코어: 1P {player1_wins} vs {player2_wins} 2P")
            print("=" * 50)

            if player1_wins >= 3:
                match_over = True
                winner = "1P"
                print("=" * 50)
                print(f"*** {winner} 최종 승리! ***")
                print("3초 후 게임이 종료됩니다...")
                print("=" * 50)

        # 시간 종료 처리
        if ui1.is_time_over() and not round_over and not match_over:
            round_over = True
            round_over_time = 0
            if char1.hp > char2.hp:
                round_winner = 1
                player1_wins += 1
                print("=" * 50)
                print("시간 종료!")
                print(f"라운드 {current_round} - 1P 승리!")
                print(f"현재 스코어: 1P {player1_wins} vs {player2_wins} 2P")
                print("=" * 50)

                if player1_wins >= 3:
                    match_over = True
                    winner = "1P"
                    print("=" * 50)
                    print(f"*** {winner} 최종 승리! ***")
                    print("3초 후 게임이 종료됩니다...")
                    print("=" * 50)

            elif char2.hp > char1.hp:
                round_winner = 2
                player2_wins += 1
                print("=" * 50)
                print("시간 종료!")
                print(f"라운드 {current_round} - 2P 승리!")
                print(f"현재 스코어: 1P {player1_wins} vs {player2_wins} 2P")
                print("=" * 50)

                if player2_wins >= 3:
                    match_over = True
                    winner = "2P"
                    print("=" * 50)
                    print(f"*** {winner} 최종 승리! ***")
                    print("3초 후 게임이 종료됩니다...")
                    print("=" * 50)
            else:
                # 무승부는 라운드를 다시 함
                print("=" * 50)
                print("시간 종료! 무승부!")
                print("라운드를 다시 시작합니다...")
                print("=" * 50)

        # 라운드 대기 시간
        if round_over and not match_over:
            round_over_time += game_framework.frame_time
            if round_over_time >= 2.0:
                reset_round()

        # 매치 종료 대기 시간
        if match_over:
            round_over_time += game_framework.frame_time
            if round_over_time >= 3.0:
                print("게임 종료!")
                game_framework.quit()

        if len(characters) == 2:
            ui1.update(characters[0].hp)
            ui2.update(characters[1].hp)

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a
    left_b, bottom_b, right_b, top_b = b

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def draw():
    clear_canvas()
    game_world.render()
    ui1.draw()
    ui2.draw()

    # 스코어 표시
    score_font = load_font('C:/Windows/Fonts/arial.ttf', 25)
    score_font.draw(150, 520, f'1P: {player1_wins}', (255, 255, 255))
    score_font.draw(550, 520, f'2P: {player2_wins}', (255, 255, 255))

    # 라운드 승자 표시
    if round_over and not match_over:
        result_font = load_font('C:/Windows/Fonts/arial.ttf', 40)
        if round_winner == 1:
            result_font.draw(250, 300, 'Round Win: 1P!', (255, 0, 0))
        elif round_winner == 2:
            result_font.draw(250, 300, 'Round Win: 2P!', (0, 0, 255))

    # 최종 승자 표시
    if match_over:
        final_font = load_font('C:/Windows/Fonts/arial.ttf', 50)
        if winner == "1P":
            final_font.draw(200, 300, 'WINNER: 1P!!!', (255, 0, 0))
        elif winner == "2P":
            final_font.draw(200, 300, 'WINNER: 2P!!!', (0, 0, 255))

    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass