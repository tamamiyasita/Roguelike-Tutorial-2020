import arcade
from constants import *
from util import map_position, pixel_position


class Actor(arcade.Sprite):
    def __init__(self, image, name=None, x=None, y=None, scale=SPRITE_SCALE, color=arcade.color.WHITE, visible_color=arcade.color.WHITE, not_visible_color=arcade.color.WHITE, map_tile=None, left_img=None):
        super().__init__(image, scale)
        self.name = name
        self.x, self.y = x, y
        self.center_x, self.center_y = pixel_position(self.x, self.y)
        self.game_map = map_tile
        self.color = color
        self.visible_color = visible_color
        self.not_visible_color = not_visible_color
        self.is_visible = False
        self.stop_move = True
        if left_img:
            self.left_image(image)

    def move(self, dxy):
        self.dx, self.dy = dxy
        if self.dx == 1:
            self.texture = self.textures.get("left")
        if self.dx == -1:
            self.texture = self.textures.get("right")

        if not self.game_map.is_blocked(self.dx + self.x, self.dy + self.y):
            if self.stop_move == True:

                self.stop_move = False
                self.target_x = self.center_x
                self.target_y = self.center_y
                self.change_y = self.dy * MOVE_SPEED
                self.change_x = self.dx * MOVE_SPEED

    def update(self):
        super().update()
        if not self.stop_move:
            if abs(self.target_x - self.center_x) >= SPRITE_SIZE and self.dx:
                self.change_x = 0
                if self.dx == 1:
                    self.center_x = self.target_x + SPRITE_SIZE
                    self.x += self.dx
                if self.dx == -1:
                    self.center_x = self.target_x - SPRITE_SIZE
                    self.x += self.dx
                self.stop_move = True

            if abs(self.target_y - self.center_y) >= SPRITE_SIZE and self.dy:
                self.change_y = 0
                if self.dy == 1:
                    self.center_y = self.target_y + SPRITE_SIZE
                    self.y += self.dy
                if self.dy == -1:
                    self.center_y = self.target_y - SPRITE_SIZE
                    self.y += self.dy
                self.stop_move = True

    def left_image(self, image):
        right = arcade.load_texture(
            image, mirrored=True)
        left = arcade.load_texture(image)
        self.textures = {"right": right, "left": left}
        return self.textures
