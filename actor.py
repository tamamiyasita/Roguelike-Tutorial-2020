import arcade
from constants import *
from data import *
from util import map_position, pixel_position


class Actor(arcade.Sprite):
    def __init__(self, image=None, name=None, x=None, y=None, blocks=False,
                 scale=SPRITE_SCALE, color=arcade.color.WHITE, fighter=None, ai=None,
                 visible_color=arcade.color.WHITE, not_visible_color=arcade.color.WHITE, map_tile=None, sub_img=None):
        super().__init__(image, scale)
        if isinstance(image, arcade.texture.Texture):
            self.texture = image

        self.name = name
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0
        self.center_x, self.center_y = pixel_position(self.x, self.y)
        self.blocks = blocks
        self.color = color
        self.visible_color = visible_color
        self.not_visible_color = not_visible_color
        self.is_visible = False
        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self
        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.game_map = map_tile
        self.stop_move = True
        self.sub_img = sub_img
        if sub_img:
            self.left_face = False
            if type(sub_img) != bool:
                self.left_image(image, sub_img)

            if type(sub_img) == bool:
                self.left_image(image)

    def move(self, dxy):
        self.dx, self.dy = dxy
        if self.dx == -1:
            self.left_face = True
        if self.dx == 1:
            self.left_face = False

        if not self.game_map.is_blocked(self.dx + self.x, self.dy + self.y):
            if self.stop_move == True:

                self.stop_move = False
                self.target_x = self.center_x
                self.target_y = self.center_y
                self.change_y = self.dy * MOVE_SPEED
                self.change_x = self.dx * MOVE_SPEED

    def update_animation(self, delta_time=1 / 60):
        if type(self.sub_img) != bool:
            if not self.stop_move and not self.left_face:
                self.texture = self.textures.get("move_left")
            if not self.stop_move and self.left_face:
                self.texture = self.textures.get("move_right")
            if self.stop_move and not self.left_face:
                self.texture = self.textures.get("left")
            if self.stop_move and self.left_face:
                self.texture = self.textures.get("right")
        if self.sub_img:
            if self.stop_move and self.dx == 1:
                self.texture = self.textures.get("left")
            if self.stop_move and self.dx == -1:
                self.texture = self.textures.get("right")

    def update(self):
        super().update()
        grid = SPRITE_SCALE * SPRITE_SIZE
        if not self.stop_move:
            if abs(self.target_x - self.center_x) >= grid and self.dx:
                self.change_x = 0
                if self.dx == 1:
                    self.center_x = self.target_x + grid
                    self.x += self.dx
                if self.dx == -1:
                    self.center_x = self.target_x - grid
                    self.x += self.dx
                self.stop_move = True

            if abs(self.target_y - self.center_y) >= grid and self.dy:
                self.change_y = 0
                if self.dy == 1:
                    self.center_y = self.target_y + grid
                    self.y += self.dy
                if self.dy == -1:
                    self.center_y = self.target_y - grid
                    self.y += self.dy
                self.stop_move = True

    def left_image(self, image, m_anime=None):
        left, right = arcade.load_texture_pair(image)
        self.textures = {"right": right, "left": left}
        if m_anime:
            move_left, move_right = arcade.load_texture_pair(
                m_anime)
            self.textures = {"right": right, "left": left,
                             "move_right": move_right, "move_left": move_left}
        return self.textures
