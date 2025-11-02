from pico2d import *

class Boy:
    STATE_IDLE, STATE_JUMP = 0, 1

    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.dir = 0
        self.state = self.STATE_IDLE
        self.idle_image = load_image('character1.motion/char1_Idle.png')
        self.jump_image = load_image('character1.motion/char1_Jump.png')
        self.image = self.idle_image
        self.is_jumping = False
        self.jump_time = 0
        self.keys = {SDLK_LEFT: False, SDLK_RIGHT: False}

    def update(self):
        # Update frame
        if self.state == self.STATE_IDLE:
            self.frame = (self.frame + 1) % 8
        elif self.state == self.STATE_JUMP:
            self.frame = (self.frame + 1) % 2

        self.x += self.dir * 5

        if self.is_jumping:
            if self.jump_time < 20:
                # Simple jump physics
                self.y += (10 - self.jump_time) * 2
                self.jump_time += 1
            else:
                self.is_jumping = False
                self.jump_time = 0
                self.state = self.STATE_IDLE
                self.image = self.idle_image
        else:
            # Update direction based on keys
            if self.keys[SDLK_LEFT] and not self.keys[SDLK_RIGHT]:
                self.dir = -1
            elif self.keys[SDLK_RIGHT] and not self.keys[SDLK_LEFT]:
                self.dir = 1
            else:
                self.dir = 0

    def draw(self):
        self.image.clip_draw(self.frame * 200, 0, 200, 200, self.x, self.y, 200, 200)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key in self.keys:
                self.keys[event.key] = True
            elif event.key == SDLK_UP:
                if not self.is_jumping:
                    self.is_jumping = True
                    self.jump_time = 0
                    self.frame = 0
                    self.state = self.STATE_JUMP
                    self.image = self.jump_image
        elif event.type == SDL_KEYUP:
            if event.key in self.keys:
                self.keys[event.key] = False
