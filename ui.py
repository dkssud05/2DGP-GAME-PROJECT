from pico2d import *

class UI:
    def __init__(self, max_hp = 200):
        self.max_hp = max_hp
        self.current_hp = max_hp

        self.x = 50
        self.y = 550
        self.width = 300
        self.height = 20

    def update(self, hp):
        self.current_hp = max(0, min(hp, self.max_hp))

    def draw(self):
        draw_rectangle(self.x-1, self.y-1, self.x + self.width+1, self.y + self.height+1, 0, 0, 0, filled=False)

        hp_ratio = self.current_hp / self.max_hp
        hp_width = self.width * hp_ratio

        if hp_width > 0:
            draw_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, 255, 0, 0, filled=True)