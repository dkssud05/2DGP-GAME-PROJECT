from pico2d import *

class Boy:
    STATE_IDLE, STATE_JUMP, STATE_FALL = 0, 1, 2

    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.dir = 0
        self.state = self.STATE_IDLE
        self.idle_image = load_image('character1.motion/char1_Idle.png')
        self.jump_image = load_image('character1.motion/char1_Jump.png')
        self.fall_image = load_image('character1.motion/char1_Fall.png')
        self.image = self.idle_image
        self.is_jumping = False
        self.jump_time = 0
        self.ground_y = 300  # Store ground position
        self.keys = {SDLK_LEFT: False, SDLK_RIGHT: False}

    def update(self):
        # Update frame
        if self.state == self.STATE_IDLE:
            self.frame = (self.frame + 1) % 8
        elif self.state == self.STATE_JUMP:
            self.frame = (self.frame + 1) % 2
        elif self.state == self.STATE_FALL:
            self.frame = (self.frame + 1) % 2

        self.x += self.dir * 5

        if self.is_jumping:
            # Change to FALL state at the peak of the jump
            if self.state == self.STATE_JUMP and (10 - self.jump_time) < 0:
                self.state = self.STATE_FALL
                self.image = self.fall_image
                self.frame = 0

            if self.jump_time < 20:
                # Simple jump physics
                self.y += (10 - self.jump_time) * 2
                self.jump_time += 1
            else:
                self.is_jumping = False
                self.jump_time = 0
                self.y = self.ground_y  # Reset to exact ground position
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
                    self.ground_y = self.y  # Save current ground position
                    self.is_jumping = True
                    self.jump_time = 0
                    self.frame = 0
                    self.state = self.STATE_JUMP
                    self.image = self.jump_image
                    self.dir = 0  # Stop horizontal movement on jump
        elif event.type == SDL_KEYUP:
            if event.key in self.keys:
                self.keys[event.key] = False
