from pico2d import *
import game_framework

class Character3:
    STATE_IDLE, STATE_RUN, STATE_JUMP, STATE_FALL, STATE_ATTACK = 0, 1, 2, 3, 4

    PIXEL_PER_METER = (10.0 / 0.3)
    RUN_SPEED_KMPH = 21.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_IDLE = 8
    FRAMES_PER_RUN = 8
    FRAMES_PER_JUMP = 2
    FRAMES_PER_ATTACK = 6

    def __init__(self):
        self.x, self.y = 500, 100
        self.frame = 0.0
        self.dir = 0
        self.face_dir = 1
        self.state = self.STATE_IDLE
        # Character3 전용 이미지 (character3.motion 폴더 사용)
        self.idle_image = load_image('character3.motion/char3_Idle.png')
        self.run_image = load_image('character3.motion/char3_Run.png')
        self.jump_image = load_image('character3.motion/char3_Jump.png')
        self.fall_image = load_image('character3.motion/char3_Fall.png')
        self.attack_image = load_image('character3.motion/char3_Attack1.png')
        self.image = self.idle_image
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 800
        self.initial_jump_velocity = 400
        self.ground_y = 300
        self.is_attacking = False
        self.attack_time = 0
        self.attack_duration = 0.5
        # Character3 전용 조작키 (J, L, I, K)
        self.keys = {SDLK_j: False, SDLK_l: False}

        self.max_hp = 200
        self.hp = 200
        self.is_hit = False
        self.hit_cooldown = 0

    def update(self):
        frame_time = game_framework.frame_time

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
            if self.keys[SDLK_j] and not self.keys[SDLK_l]:
                self.dir = -1
                self.face_dir = -1
                if self.state != self.STATE_RUN:
                    self.state = self.STATE_RUN
                    self.image = self.run_image
                    self.frame = 0
            elif self.keys[SDLK_l] and not self.keys[SDLK_j]:
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
            self.image.clip_draw(int(self.frame) * 200, 0, 200, 200, self.x, self.y, 200, 200)
        else:
            self.image.clip_composite_draw(int(self.frame) * 200, 0, 200, 200, 0, 'h', self.x, self.y, 200, 200)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in self.keys:
                self.keys[event.key] = True
            elif event.key == SDLK_i:  # Jump key
                if not self.is_jumping and not self.is_attacking:
                    self.ground_y = self.y
                    self.is_jumping = True
                    self.jump_velocity = self.initial_jump_velocity
                    self.frame = 0.0
                    self.state = self.STATE_JUMP
                    self.image = self.jump_image
            elif event.key == SDLK_k:  # Attack key
                if not self.is_attacking and not self.is_jumping:
                    self.is_attacking = True
                    self.attack_time = 0
                    self.frame = 0.0
                    self.state = self.STATE_ATTACK
                    self.image = self.attack_image
        elif event.type == SDL_KEYUP:
            if event.key in self.keys:
                self.keys[event.key] = False