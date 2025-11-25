from pico2d import *
import time

class UI:
    def __init__(self, max_hp = 200):
        self.max_hp = max_hp
        self.current_hp = max_hp

        self.x = 50
        self.y = 550
        self.width = 300
        self.height = 20

        self.start_time = time.time()
        self.max_time = 60 # seconds
        self.elapsed_time = 0
        self.font = load_font('C:/Windows/Fonts/arial.ttf', 30)

    def update(self, hp):
        self.current_hp = max(0, min(hp, self.max_hp))
        self.elapsed_time = time.time() - self.start_time

    def is_time_over(self):
        return self.elapsed_time >= self.max_time

    def draw(self):
        draw_rectangle(self.x-1, self.y-1, self.x + self.width+1, self.y + self.height+1, 0, 0, 0, filled=False)

        hp_ratio = self.current_hp / self.max_hp
        hp_width = self.width * hp_ratio

        if hp_width > 0:
            draw_rectangle(self.x, self.y, self.x + hp_width, self.y + self.height, 255, 0, 0, filled=True)

        remaining_time = max(0, self.max_time - self.elapsed_time)
        seconds = int(remaining_time)
        timer_x = self.x + self.width + 35
        self.font.draw(timer_x, self.y + 10, f'{seconds}', (255, 255, 255))