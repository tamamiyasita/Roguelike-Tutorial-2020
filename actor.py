import arcade
import math
from constants import *
from data import *
from util import map_position, pixel_position, get_blocking_entity
# from tick_sys import Ticker


class Actor(arcade.Sprite):
    def __init__(self, image=None, name=None, x=None, y=None, blocks=False,
                 scale=SPRITE_SCALE, color=arcade.color.WHITE, fighter=None, ai=None,
                 visible_color=arcade.color.WHITE, not_visible_color=arcade.color.WHITE,
                 speed=None, ticker=None, my_state=None, map_tile=None, sub_img=None):
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

        self.speed = speed
        self.ticker = ticker
        if ticker:
            self.ticker.schedule_turn(self.speed, self)

        self.my_state = my_state
        
        self.state = State.TICK

        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self
            if not self.my_state:
                self.my_state = State.NPC

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

        ENTITY_LIST.append(self)

    def move(self, dxy):
        self.dx, self.dy = dxy
        if self.dx == -1:
            self.left_face = True
        if self.dx == 1:
            self.left_face = False

        if not get_blocking_entity(self.x+self.dx, self.y+self.dy, ENTITY_LIST):
            if self.stop_move == True:

                self.stop_move = False
                self.target_x = self.center_x
                self.target_y = self.center_y
                self.change_y = self.dy * MOVE_SPEED
                self.change_x = self.dx * MOVE_SPEED

    def do_turn(self):
        print("do_turn ", self.name)
        self.state = self.my_state
        self.ticker.schedule_turn(self.speed, self)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

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
            if self.stop_move:
                self.state = State.TICK

    def left_image(self, image, m_anime=None):
        left, right = arcade.load_texture_pair(image)
        self.textures = {"right": right, "left": left}
        if m_anime:
            move_left, move_right = arcade.load_texture_pair(
                m_anime)
            self.textures = {"right": right, "left": left,
                             "move_right": move_right, "move_left": move_left}
        return self.textures

    def move_towards(self, target_x, target_y, sprite_list):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not get_blocking_entity(self.x + dx, self.y + dy, ENTITY_LIST):
            self.move((dx, dy))
