from pico2d import *
import game_framework

class Character1:
    STATE_IDLE, STATE_RUN, STATE_JUMP, STATE_FALL, STATE_ATTACK, STATE_DEATH, STATE_HIT = 0, 1, 2, 3, 4, 5, 6

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
        self.player_id = 1
        self.keys = {SDLK_LEFT: False, SDLK_RIGHT: False, SDLK_a: False, SDLK_d: False}
        self.hitbox_width = 80
        self.hitbox_height = 120

        self.max_hp = 200
        self.hp = 200
        self.is_hit = False
        self.hit_cooldown = 0
        self.attack_damage = 15

        self.is_dead = False
        self.death_time = 0
        self.hit_time = 0
        self.hit_duration = 0.3

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

        # hit_cooldown 감소
        if self.hit_cooldown > 0:
            self.hit_cooldown -= frame_time

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
            else:
                left_key, right_key = SDLK_LEFT, SDLK_RIGHT

            if self.keys[left_key] and not self.keys[right_key]:
                self.dir = -1
                self.face_dir = -1
                if self.state != self.STATE_RUN:
                    self.state = self.STATE_RUN
                    self.image = self.run_image
                    self.frame = 0
            elif self.keys[right_key] and not self.keys[left_key]:
                self.dir = 1
                self.face_dir = 1
                if self.state != self.STATE_RUN:
                    self.state = self.STATE_RUN
                    self.image = self.run_image
                    self.frame = 0
            else:
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
        if self.player_id == 1:
            left_key, right_key = SDLK_a, SDLK_d
            jump_key = SDLK_w
            attack_key = SDLK_LCTRL
        else:
            left_key, right_key = SDLK_LEFT, SDLK_RIGHT
            jump_key = SDLK_UP
            attack_key = SDLK_RCTRL

        if event.type == SDL_KEYDOWN:
            if event.key == left_key or event.key == right_key:
                self.keys[event.key] = True
            elif event.key == jump_key:
                if not self.is_jumping and not self.is_attacking and not self.is_hit:
                    self.ground_y = self.y
                    self.is_jumping = True
                    self.jump_velocity = self.initial_jump_velocity
                    self.frame = 0.0
                    self.state = self.STATE_JUMP
                    self.image = self.jump_image
            elif event.key == attack_key:
                if not self.is_attacking and not self.is_jumping:
                    self.is_attacking = True
                    self.attack_time = 0
                    self.frame = 0.0
                    self.state = self.STATE_ATTACK
                    self.image = self.attack_image
        elif event.type == SDL_KEYUP:
            if event.key == left_key or event.key == right_key:
                self.keys[event.key] = False

    def get_bb(self):
        return self.x - self.hitbox_width // 2, self.y - self.hitbox_height // 2, self.x + self.hitbox_width // 2, self.y + self.hitbox_height // 2

    def get_attack_bb(self):
        if not self.is_attacking:
            return None

        current_frame = int(self.frame)
        if current_frame not in [2, 3, 4]:
            return None

        attack_width = 140
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

    def take_damage(self, damage):
        if self.hit_cooldown <= 0 and not self.is_dead:
            self.hp -= damage
            self.hit_cooldown = 0.5  # 0.5초 무적 시간
            if self.hp <= 0:
                self.hp = 0
                self.is_dead = True
                self.state = self.STATE_DEATH
                self.image = self.death_image
                self.frame = 0
                self.death_time = 0
            pick_order = "1번째 선택" if self.player_id == 1 else "2번째 선택"
            print(f"[{pick_order}] Character1 HP: {self.hp}/{self.max_hp}")
        else:
            self.is_hit = True
            self.hit_time = 0
            self.state = self.STATE_HIT
            self.image = self.hit_image
            self.frame = 0

    def get_attack_damage(self):
        return self.attack_damage

