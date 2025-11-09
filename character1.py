from pico2d import *

class Character1:
    STATE_IDLE, STATE_RUN, STATE_JUMP, STATE_FALL, STATE_ATTACK = 0, 1, 2, 3, 4

    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.state = self.STATE_IDLE
        self.idle_image = load_image('character1.motion/char1_Idle.png')
        self.run_image = load_image('character1.motion/char1_Run.png')
        self.jump_image = load_image('character1.motion/char1_Jump.png')
        self.fall_image = load_image('character1.motion/char1_Fall.png')
        self.attack_image = load_image('character1.motion/char1_Attack1.png')
        self.image = self.idle_image
        self.is_jumping = False
        self.jump_time = 0
        self.ground_y = 300
        self.is_attacking = False
        self.attack_frame_count = 0
        self.keys = {SDLK_LEFT: False, SDLK_RIGHT: False}

        self.max_hp = 100
        self.hp = 100
        self.is_hit = False
        self.hit_cooldown = 0

    def update(self):
        if self.state == self.STATE_IDLE:
            self.frame = (self.frame + 1) % 8
        elif self.state == self.STATE_RUN:
            self.frame = (self.frame + 1) % 8
        elif self.state == self.STATE_JUMP:
            self.frame = (self.frame + 1) % 2
        elif self.state == self.STATE_FALL:
            self.frame = (self.frame + 1) % 2
        elif self.state == self.STATE_ATTACK:
            if self.attack_frame_count % 3 == 0:
                self.frame = (self.frame + 1) % 6
            self.attack_frame_count += 1
            if self.attack_frame_count >= 18:
                self.is_attacking = False
                self.attack_frame_count = 0
                if self.dir != 0:
                    self.state = self.STATE_RUN
                    self.image = self.run_image
                else:
                    self.state = self.STATE_IDLE
                    self.image = self.idle_image
                self.frame = 0

        if not self.is_attacking:
            self.x += self.dir * 5

        if self.is_jumping:
            if self.state == self.STATE_JUMP and (10 - self.jump_time) < 0:
                self.state = self.STATE_FALL
                self.image = self.fall_image
                self.frame = 0

            if self.jump_time < 20:
                self.y += (10 - self.jump_time) * 2
                self.jump_time += 1
            else:
                self.is_jumping = False
                self.jump_time = 0
                self.y = self.ground_y
                self.state = self.STATE_IDLE
                self.image = self.idle_image
                self.frame = 0
        elif not self.is_attacking:
            if self.keys[SDLK_LEFT] and not self.keys[SDLK_RIGHT]:
                self.dir = -1
                self.face_dir = -1
                if self.state != self.STATE_RUN:
                    self.state = self.STATE_RUN
                    self.image = self.run_image
                    self.frame = 0
            elif self.keys[SDLK_RIGHT] and not self.keys[SDLK_LEFT]:
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
            self.image.clip_draw(self.frame * 200, 0, 200, 200, self.x, self.y, 200, 200)
        else:
            self.image.clip_composite_draw(self.frame * 200, 0, 200, 200, 0, 'h', self.x, self.y, 200, 200)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in self.keys:
                self.keys[event.key] = True
            elif event.key == SDLK_UP:
                if not self.is_jumping and not self.is_attacking:
                    self.ground_y = self.y
                    self.is_jumping = True
                    self.jump_time = 0
                    self.frame = 0
                    self.state = self.STATE_JUMP
                    self.image = self.jump_image
                    self.dir = 0
            elif event.key == SDLK_z:
                if not self.is_attacking and not self.is_jumping:
                    self.is_attacking = True
                    self.attack_frame_count = 0
                    self.frame = 0
                    self.state = self.STATE_ATTACK
                    self.image = self.attack_image
        elif event.type == SDL_KEYUP:
            if event.key in self.keys:
                self.keys[event.key] = False
