import arcade
from constants import *
from util import map_position, pixel_position
SPEED = 4


class Actor(arcade.Sprite):
    def __init__(self, image, x, y, scale=SPRITE_SCALE, map_tile=None):
        super().__init__(image, scale)
        self.x, self.y = x, y
        self.center_x, self.center_y = pixel_position(x, y)
        self.map_tile = map_tile
        self.stop_move = True

    def move(self, dxy):
        if self.stop_move == True:
            self.stop_move = False
            self.dx, self.dy = dxy
            self.target_x = self.center_x + (self.dx * SPRITE_SIZE)
            self.target_y = self.center_y + (self.dy * SPRITE_SIZE)
            self.change_y = self.dy * SPEED
            self.change_x = self.dx * SPEED

    def update(self):
        super().update()
        if not self.stop_move:
            if abs(self.target_x - self.center_x) <= 1 and self.dx:
                print(self.x)
                self.change_x = 0
                self.center_x = self.target_x
                self.x += self.dx
                print(self.x)
                self.stop_move = True

            if abs(self.target_y - self.center_y) <= 1 and self.dy:
                self.change_y = 0
                self.center_y = self.target_y
                self.y += self.dy
                self.stop_move = True
