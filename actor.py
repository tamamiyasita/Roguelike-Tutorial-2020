import arcade
from constants import *
from util import map_position, pixel_position
SPEED = 8


class Actor(arcade.Sprite):
    def __init__(self, image, x, y, scale=SPRITE_SCALE, map_tile=None, left_img=None):
        super().__init__(image, scale)
        self.x, self.y = x, y
        self.center_x, self.center_y = pixel_position(x, y)
        self.map_tile = map_tile
        self.stop_move = True
        if left_img:
            self.left_image(image)

    def move(self, dxy):
        if self.stop_move == True:
            self.dx, self.dy = dxy

            self.stop_move = False
            self.target_x = self.center_x + \
                (self.dx * SPRITE_SIZE)*SPRITE_SCALE
            self.target_y = self.center_y + \
                (self.dy * SPRITE_SIZE)*SPRITE_SCALE
            self.change_y = self.dy * SPEED
            self.change_x = self.dx * SPEED
        if self.dx == 1:
            self.texture = self.textures.get("left")
        if self.dx == -1:
            self.texture = self.textures.get("right")
        print(self.dx)

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

    def left_image(self, image):
        right = arcade.load_texture(
            image, mirrored=True)
        left = arcade.load_texture(image)
        self.textures = {"right": right, "left": left}
        print(self.textures)
        return self.textures
