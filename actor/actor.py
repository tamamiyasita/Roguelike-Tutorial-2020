import arcade
import math
from constants import *
from data import *
from util import pixel_to_grid, grid_to_pixel, get_blocking_entity


class Actor(arcade.Sprite):
    def __init__(self, image=None, name=None, x=0, y=0, blocks=False,
                 scale=SPRITE_SCALE, color=arcade.color.WHITE, fighter=None, ai=None,
                 inventory=None, item=None,
                 visible_color=arcade.color.WHITE, not_visible_color=arcade.color.WHITE,
                 state=state.TURN_END, map_tile=None, sub_img=None):
        super().__init__(image, scale)
        if isinstance(image, arcade.texture.Texture):
            self.texture_ = image
        self.name = name
        self.dx, self.dy = 0, 0
        self.center_x, self.center_y = grid_to_pixel(x, y)
        self.x, self.y = pixel_to_grid(self.center_x, self.center_y)
        self.blocks = blocks
        self.color = color
        self.visible_color = visible_color
        self.not_visible_color = not_visible_color
        self.is_visible = False
        self.is_dead = False
        self.inventory = inventory
        self.item = item

        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self
        self.state = state

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.game_map = map_tile
        # self.stop_move = True
        self.sub_img = sub_img
        if sub_img:
            self.left_face = False
            if type(sub_img) != bool:
                self.left_image(image, sub_img)

            if type(sub_img) == bool:
                self.left_image(image)

        ENTITY_LIST.append(self)

    def get_dict(self):
        result = {}
        result["image"] = self

    def t_move(self, dxy):
        try:
            self.dx, self.dy = dxy
            if self.dx == -1:
                self.left_face = True
            if self.dx == 1:
                self.left_face = False

            if not get_blocking_entity(self.x + self.dx, self.y + self.dy, ENTITY_LIST):
                self.x += self.dx
                self.y += self.dy
                self.center_x, self.center_y = grid_to_pixel(self.x, self.y)
                self.state = state.TURN_END
        except:
            pass

    def move(self, dxy, target=None):
        try:
            self.dx, self.dy = dxy
            if self.dx == -1:
                self.left_face = True
            if self.dx == 1:
                self.left_face = False

            self.target_x = self.center_x
            self.target_y = self.center_y

            # 行先を変数dst_tileに入れる
            self.dst_tile = self.game_map.tiles[self.x +
                                                self.dx][self.y+self.dy]

            blocking_actor = get_blocking_entity(
                self.x+self.dx, self.y+self.dy, ACTOR_LIST)
            if blocking_actor and not target:
                target = blocking_actor[0]
                if not target.is_dead:
                    attack_results = self.fighter.attack(target)
                    if attack_results:
                        self.state = state.ATTACK
                        self.change_y = self.dy * MOVE_SPEED
                        self.change_x = self.dx * MOVE_SPEED

                    return attack_results

            elif target and self.distance_to(target) <= 1.46:
                attack_results = self.fighter.attack(target)
                if attack_results:
                    self.state = state.ATTACK
                    self.change_y = self.dy * MOVE_SPEED
                    self.change_x = self.dx * MOVE_SPEED

                return attack_results

            elif not get_blocking_entity(self.x + self.dx, self.y + self.dy, ACTOR_LIST) and\
                    self.dst_tile.blocked == False:
                    # self.game_map.tiles[self.x+self.dx][self.y+self.dy].blocked == False:

                self.dst_tile.blocked = True
                self.state = state.ON_MOVE
                self.change_y = self.dy * MOVE_SPEED
                self.change_x = self.dx * MOVE_SPEED

        except:
            pass

    def update(self):
        super().update()
        grid = SPRITE_SCALE * SPRITE_SIZE
        step = SPRITE_SCALE * SPRITE_SIZE // 2
        if self.state == state.ON_MOVE:
            if abs(self.target_x - self.center_x) >= grid and self.dx:
                self.change_x = 0
                if self.dx == 1:
                    self.center_x = self.target_x + grid
                    self.x += self.dx
                    self.dst_tile.blocked = False
                    self.state = state.TURN_END
                if self.dx == -1:
                    self.center_x = self.target_x - grid
                    self.x += self.dx
                    self.dst_tile.blocked = False
                    self.state = state.TURN_END

            if abs(self.target_y - self.center_y) >= grid and self.dy:
                self.change_y = 0
                if self.dy == 1:
                    self.center_y = self.target_y + grid
                    self.y += self.dy
                    self.dst_tile.blocked = False
                    self.state = state.TURN_END
                if self.dy == -1:
                    self.center_y = self.target_y - grid
                    self.y += self.dy
                    self.dst_tile.blocked = False
                    self.state = state.TURN_END

        if self.state == state.ATTACK:
            if abs(self.target_x - self.center_x) >= step and self.dx:
                self.change_x = 0
                self.center_x = self.target_x
                self.state = state.TURN_END
            if abs(self.target_y - self.center_y) >= step and self.dy:
                self.change_y = 0
                self.center_y = self.target_y
                self.state = state.TURN_END

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def update_animation(self, delta_time=1 / 60):
        if type(self.sub_img) != bool and self.state:
            if self.state == state.ON_MOVE and not self.left_face:
                self.texture = self.textures.get("move_left")
            if self.state == state.ON_MOVE and self.left_face:
                self.texture = self.textures.get("move_right")
            if self.state == state.ATTACK and not self.left_face:
                self.texture = pc_attack[0]
                # self.texture = self.textures.get("move_left")
            if self.state == state.ATTACK and self.left_face:
                self.texture = pc_attack[1]
                # self.texture = self.textures.get("move_right")
            if self.state == state.READY and not self.left_face:
                self.texture = self.textures.get("left")
            if self.state == state.READY and self.left_face:
                self.texture = self.textures.get("right")
        elif self.sub_img:
            if self.state == state.ON_MOVE and self.dx == 1:
                self.texture = self.textures.get("left")
            if self.state == state.ON_MOVE and self.dx == -1:
                self.texture = self.textures.get("right")

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

    @property
    def texture_(self):
        return self._texture_

    @texture_.setter
    def texture_(self, value):
        self._texture_ = value
        self.texture = self._texture_
