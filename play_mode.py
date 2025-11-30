from pico2d import *
import game_framework
import game_world
import character_select_mode
from ui import UI
from background import Background
from character1 import Character1
from character2 import Character2
from character3 import Character3

characters = []
game_over = False
game_over_time = 0
winner = None

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

def init():
    global characters, ui1, ui2

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
    global game_over, game_over_time, winner

    if len(characters) >= 2:
        char1 = characters[0]
        char2 = characters[1]

        char1_prev_x = char1.x
        char2_prev_x = char2.x

    game_world.update()

    if len(characters) >= 2:
        char1 = characters[0]
        char2 = characters[1]

        char1_bb = char1.get_bb()
        char2_bb = char2.get_bb()
        if collide(char1_bb, char2_bb):
            char1.x = char1_prev_x
            char2.x = char2_prev_x

        if not game_over:
            char1_attack_bb = char1.get_attack_bb()
            if char1_attack_bb:
                char2_bb = char2.get_bb()
                if collide(char1_attack_bb, char2_bb):
                    damage = char1.get_attack_damage()
                    char2.take_damage(damage)

            char2_attack_bb = char2.get_attack_bb()
            if char2_attack_bb:
                char1_bb = char1.get_bb()
                if collide(char2_attack_bb, char1_bb):
                    damage = char2.get_attack_damage()
                    char1.take_damage(damage)

        if char1.is_dead and not game_over:
            game_over = True
            game_over_time = 0
            winner = "2번째 선택 캐릭터"
            print("=" * 50)
            print(f"{winner} 승리!")
            print("3초 후 게임이 종료됩니다...")
            print("=" * 50)
        elif char2.is_dead and not game_over:
            game_over = True
            game_over_time = 0
            winner = "1번째 선택 캐릭터"
            print("=" * 50)
            print(f"{winner} 승리!")
            print("3초 후 게임이 종료됩니다...")
            print("=" * 50)

        if game_over:
            game_over_time += game_framework.frame_time
            if game_over_time >= 3.0:
                print("게임 종료!")
                game_framework.quit()

        if len(characters) == 2:
            ui1.update(characters[0].hp)
            ui2.update(characters[1].hp)

        if ui1.is_time_over() and not game_over:
            game_over = True
            game_over_time = 0
            if char1.hp > char2.hp:
                winner = "1번째 선택 캐릭터"
            elif char2.hp > char1.hp:
                winner = "2번째 선택 캐릭터"
            else:
                winner = "무승부"
            print("=" * 50)
            print("시간 종료!")
            print(f"{winner} 승리!")
            print("3초 후 게임이 종료됩니다...")
            print("=" * 50)

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
    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass