from pico2d import *
import game_framework

class Character1:
    STATE_IDLE, STATE_RUN, STATE_JUMP, STATE_FALL, STATE_ATTACK, STATE_DEATH, STATE_HIT, STATE_GUARD, STATE_DASH= 0, 1, 2, 3, 4, 5, 6, 7, 8

    PIXEL_PER_METER = (10.0 / 0.3)
    RUN_SPEED_KMPH = 15.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_IDLE = 8
    FRAMES_PER_RUN = 8
    FRAMES_PER_JUMP = 2
    FRAMES_PER_ATTACK = 6
    FRAMES_PER_DEATH = 6
    FRAMES_PER_HIT = 4

    def __init__(self):
        self.x, self.y = 400, 100
        self.frame = 0.0
        self.dir = 0
        self.face_dir = 1
        self.state = self.STATE_IDLE
        self.idle_image = load_image('character1.motion/char1_Idle.png')
        self.run_image = load_image('character1.motion/char1_Run.png')
        self.jump_image = load_image('character1.motion/char1_Jump.png')
        self.fall_image = load_image('character1.motion/char1_Fall.png')
        self.attack_image = load_image('character1.motion/char1_Attack1.png')
        self.attack2_image = load_image('character1.motion/char1_Attack2.png')
        self.death_image = load_image('character1.motion/char1_Death.png')
        self.hit_image = load_image('character1.motion/char1_TakeHit.png')
        self.image = self.idle_image
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 800
        self.initial_jump_velocity = 400
        self.ground_y = 300
        self.is_attacking = False
        self.attack_frame_count = 0
        self.attack_time = 0
        self.attack_duration = 0.5
        self.current_attack_type = 1  # 1: Attack1, 2: Attack2
        self.player_id = 1
        self.keys = {SDLK_LEFT: False, SDLK_RIGHT: False, SDLK_a: False, SDLK_d: False}
        self.attack_key_pressed = False
        self.attack2_key_pressed = False
        self.hitbox_width = 80
        self.hitbox_height = 120

        self.max_hp = 200
        self.hp = 200
        self.is_hit = False
        self.hit_cooldown = 0
        self.attack_damage = 16  # 균형형 - 중간 데미지

        self.is_dead = False
        self.death_time = 0
        self.hit_time = 0
        self.hit_duration = 0.5

        self.attack_id = 0
        self.last_hit_by_attack_id = -1

        # 방어 관련
        self.is_guarding = False
        self.guard_damage_reduction = 0.5  # 방어 시 데미지 50% 감소

        # 대쉬 관련
        self.is_dashing = False
        self.dash_time = 0
        self.dash_cooldown_time = 0
        self.dash_dir = 0
        self.dash_key_pressed = False
        self.dash_count = 1  # 라운드당 사용 가능한 대쉬 횟수

    def update(self):
        frame_time = game_framework.frame_time

        # 죽음 상태 처리
        if self.state == self.STATE_DEATH:
            if self.frame < self.FRAMES_PER_DEATH - 1:
                self.frame += self.FRAMES_PER_DEATH * self.ACTION_PER_TIME * frame_time
            else:
                self.frame = self.FRAMES_PER_DEATH - 1  # 마지막 프레임 유지
            self.death_time += frame_time
            return

        if self.state == self.STATE_HIT:
            self.frame = (self.frame + self.FRAMES_PER_HIT * self.ACTION_PER_TIME * frame_time) % self.FRAMES_PER_HIT
            self.hit_time += frame_time
            if self.hit_time >= self.hit_duration:
                self.is_hit = False
                self.hit_time = 0
                self.state = self.STATE_IDLE
                self.image = self.idle_image
                self.frame = 0
            return

        # 대쉬 상태 처리 (순간이동 방식)
        if self.state == self.STATE_DASH:
            # 대쉬 시작 시 즉시 이동 (첫 프레임에만)
            if self.dash_time < frame_time:
                dash_distance = 150  # 순간이동 거리
                self.x += self.dash_dir * dash_distance

                # 화면 경계 체크
                if self.x < 40:
                    self.x = 40
                elif self.x > 760:
                    self.x = 760

            # 대쉬 애니메이션
            self.frame = (self.frame + self.FRAMES_PER_RUN * self.ACTION_PER_TIME * frame_time * 3) % self.FRAMES_PER_RUN
            self.dash_time += frame_time

            # 대쉬 종료
            if self.dash_time >= 0.15:  # 짧은 애니메이션 시간
                self.is_dashing = False
                self.dash_time = 0
                self.dash_cooldown_time = 0.8
                self.state = self.STATE_IDLE
                self.image = self.idle_image
                self.frame = 0
            return

        if self.state == self.STATE_IDLE:
            self.frame = (self.frame + self.FRAMES_PER_IDLE * self.ACTION_PER_TIME * frame_time) % self.FRAMES_PER_IDLE
        elif self.state == self.STATE_RUN:
            self.frame = (self.frame + self.FRAMES_PER_RUN * self.ACTION_PER_TIME * frame_time) % self.FRAMES_PER_RUN
        elif self.state == self.STATE_JUMP:
            self.frame = (self.frame + self.FRAMES_PER_JUMP * self.ACTION_PER_TIME * frame_time) % self.FRAMES_PER_JUMP
        elif self.state == self.STATE_FALL:
            self.frame = (self.frame + self.FRAMES_PER_JUMP * self.ACTION_PER_TIME * frame_time) % self.FRAMES_PER_JUMP
        elif self.state == self.STATE_ATTACK:
            self.frame = (self.frame + self.FRAMES_PER_ATTACK * self.ACTION_PER_TIME * frame_time) % self.FRAMES_PER_ATTACK
            self.attack_time += frame_time
            if self.attack_time >= self.attack_duration:
                self.is_attacking = False
                self.attack_time = 0
                self.attack_key_pressed = False
                self.attack2_key_pressed = False
                if self.dir != 0:
                    self.state = self.STATE_RUN
                    self.image = self.run_image
                else:
                    self.state = self.STATE_IDLE
                    self.image = self.idle_image
                self.frame = 0

        if not self.is_attacking:
            self.x += self.dir * self.RUN_SPEED_PPS * frame_time

            if self.x < 40:
                self.x = 40
            elif self.x > 760:
                self.x = 760

        if self.is_jumping:
            self.jump_velocity -= self.gravity * frame_time
            self.y += self.jump_velocity * frame_time

            if self.jump_velocity < 0 and self.state == self.STATE_JUMP:
                self.state = self.STATE_FALL
                self.image = self.fall_image
                self.frame = 0

            if self.y <= self.ground_y:
                self.is_jumping = False
                self.jump_velocity = 0
                self.y = self.ground_y
                self.state = self.STATE_IDLE
                self.image = self.idle_image
                self.frame = 0
        elif not self.is_attacking:
            if self.player_id == 1:
                left_key, right_key = SDLK_a, SDLK_d
                guard_key = SDLK_s
            else:
                left_key, right_key = SDLK_LEFT, SDLK_RIGHT
                guard_key = SDLK_DOWN

            # 방어 키를 누르고 있으면 방어 상태
            if self.keys.get(guard_key, False):
                self.is_guarding = True
                self.dir = 0  # 방어 중에는 이동 불가
                if self.state != self.STATE_GUARD:
                    self.state = self.STATE_GUARD
                    self.image = self.idle_image
                    self.frame = 0
            elif self.keys[left_key] and not self.keys[right_key]:
                self.is_guarding = False
                self.dir = -1
                self.face_dir = -1
                if self.state != self.STATE_RUN:
                    self.state = self.STATE_RUN
                    self.image = self.run_image
                    self.frame = 0
            elif self.keys[right_key] and not self.keys[left_key]:
                self.is_guarding = False
                self.dir = 1
                self.face_dir = 1
                if self.state != self.STATE_RUN:
                    self.state = self.STATE_RUN
                    self.image = self.run_image
                    self.frame = 0
            else:
                self.is_guarding = False
                self.dir = 0
                if self.state != self.STATE_IDLE:
                    self.state = self.STATE_IDLE
                    self.image = self.idle_image
                    self.frame = 0

    def draw(self):
        if self.face_dir == 1:
            self.image.clip_draw(int(self.frame) * 200, 0, 200, 200, self.x, self.y, 400, 400)
        else:
            self.image.clip_composite_draw(int(self.frame) * 200, 0, 200, 200, 0, 'h', self.x, self.y, 400, 400)

        draw_rectangle(*self.get_bb())

        # 공격 범위 표시
        attack_bb = self.get_attack_bb()
        if attack_bb:
            draw_rectangle(*attack_bb)

    def handle_event(self, event):
        # 죽은 상태에서는 모든 입력 무시
        if self.is_dead:
            return

        if self.player_id == 1:
            left_key, right_key = SDLK_a, SDLK_d
            jump_key = SDLK_w
            attack_key = SDLK_LCTRL
            attack2_key = SDLK_LSHIFT
            guard_key = SDLK_s
            dash_key = SDLK_SPACE
        else:
            left_key, right_key = SDLK_LEFT, SDLK_RIGHT
            jump_key = SDLK_UP
            attack_key = SDLK_RCTRL
            attack2_key = SDLK_RSHIFT
            guard_key = SDLK_DOWN
            dash_key = SDLK_KP_0  # 숫자패드 0

        if event.type == SDL_KEYDOWN:
            if event.key == left_key or event.key == right_key or event.key == guard_key:
                self.keys[event.key] = True
            elif event.key == jump_key:
                if not self.is_jumping and not self.is_attacking:
                    self.ground_y = self.y
                    self.is_jumping = True
                    self.jump_velocity = self.initial_jump_velocity
                    self.frame = 0.0
                    self.state = self.STATE_JUMP
                    self.image = self.jump_image
            elif event.key == attack_key:
                if not self.attack_key_pressed and not self.is_attacking and not self.is_hit:
                    self.is_attacking = True
                    self.attack_time = 0
                    self.frame = 0.0
                    self.state = self.STATE_ATTACK
                    self.current_attack_type = 1
                    self.image = self.attack_image
                    self.attack_key_pressed = True
                    self.attack_id += 1  # 새로운 공격마다 ID 증가
            elif event.key == attack2_key:
                if not self.attack2_key_pressed and not self.is_attacking and not self.is_hit:
                    self.is_attacking = True
                    self.attack_time = 0
                    self.frame = 0.0
                    self.state = self.STATE_ATTACK
                    self.current_attack_type = 2
                    self.image = self.attack2_image
                    self.attack2_key_pressed = True
                    self.attack_id += 1  # 새로운 공격마다 ID 증가
            elif event.key == dash_key:
                if not self.dash_key_pressed and not self.is_dashing and not self.is_attacking and not self.is_hit and self.dash_cooldown_time <= 0 and self.dash_count > 0:
                    # 현재 방향키가 눌려있는 방향으로 대쉬
                    if self.keys.get(left_key, False):
                        self.dash_dir = -1
                        self.face_dir = -1
                    elif self.keys.get(right_key, False):
                        self.dash_dir = 1
                        self.face_dir = 1
                    else:
                        # 방향키가 안 눌려있으면 보고있는 방향으로 대쉬
                        self.dash_dir = self.face_dir

                    self.is_dashing = True
                    self.dash_time = 0
                    self.state = self.STATE_DASH
                    self.image = self.run_image
                    self.frame = 0.0
                    self.dash_key_pressed = True
                    self.dash_count -= 1  # 대쉬 횟수 감소
                    print(f"[Player {self.player_id}] 대쉬 사용! 남은 횟수: {self.dash_count}")
        elif event.type == SDL_KEYUP:
            if event.key == left_key or event.key == right_key or event.key == guard_key:
                self.keys[event.key] = False
            elif event.key == attack_key:
                self.attack_key_pressed = False
            elif event.key == attack2_key:
                self.attack2_key_pressed = False
            elif event.key == dash_key:
                self.dash_key_pressed = False

    def get_bb(self):
        return self.x - self.hitbox_width // 2, self.y - self.hitbox_height // 2, self.x + self.hitbox_width // 2, self.y + self.hitbox_height // 2

    def get_attack_bb(self):
        if not self.is_attacking:
            return None

        current_frame = int(self.frame)
        if current_frame not in [2, 3, 4]:
            return None

        attack_width = 160
        attack_height = 100

        if self.face_dir == 1:  # 오른쪽 공격
            left = self.x + 20
            right = self.x + 20 + attack_width
            bottom = self.y - attack_height // 2
            top = self.y + attack_height // 2
        else:  # 왼쪽 공격
            left = self.x - 20 - attack_width
            right = self.x - 20
            bottom = self.y - attack_height // 2
            top = self.y + attack_height // 2

        return left, bottom, right, top

    def take_damage(self, damage, attack_id):
        # 같은 공격 ID로는 중복 피격 방지
        if attack_id == self.last_hit_by_attack_id:
            return

        # 피격 중이거나 죽은 상태면 데미지를 받지 않음 (피격 애니메이션 중 = 무적)
        if self.is_hit or self.is_dead:
            return

        self.last_hit_by_attack_id = attack_id  # 이 공격 ID 기록

        # 방어 중이면 데미지 감소
        if self.is_guarding:
            damage = int(damage * self.guard_damage_reduction)
            print(f"[Player {self.player_id}] 방어! 데미지 {int(damage / self.guard_damage_reduction)} -> {damage}")

        self.hp -= damage

        # 공격 상태 초기화 (피격당하면 공격 취소)
        self.is_attacking = False
        self.attack_time = 0
        self.attack_key_pressed = False
        self.attack2_key_pressed = False

        if self.hp <= 0:
            self.hp = 0
            self.is_dead = True
            self.state = self.STATE_DEATH
            self.image = self.death_image
            self.frame = 0
            self.death_time = 0
        else:
            # 방어 중이면 피격 애니메이션 없이 방어 유지
            if not self.is_guarding:
                self.is_hit = True
                self.hit_time = 0
                self.state = self.STATE_HIT
                self.image = self.hit_image
                self.frame = 0

        pick_order = "1번째 선택" if self.player_id == 1 else "2번째 선택"
        print(f"[{pick_order}] Character1 HP: {self.hp}/{self.max_hp}")

    def get_attack_damage(self):
        return self.attack_damage

