import arcade
import math

from arcade import texture
from constants import *
from data import *
from util import pixel_to_grid, grid_to_pixel, get_blocking_entity


class Actor(arcade.Sprite):
    def __init__(self, texture_number=0, texture=None, name=None, x=0, y=0, blocks=False,
                 scale=SPRITE_SCALE, color=arcade.color.WHITE, fighter=None, ai=None,
                 inventory=None, item=None,
                 visible_color=arcade.color.WHITE, not_visible_color=arcade.color.WHITE,
                 state=state.TURN_END, game_engine=None):
        super().__init__(scale=scale)
        self.texture_number = texture_number
        self.textureID = texture
        self.texture_ = self.textureID
        self.name = name
        self.dx, self.dy = 0, 0
        self.center_x, self.center_y = grid_to_pixel(x, y)
        self.x, self.y = pixel_to_grid(self.center_x, self.center_y)
        self.blocks = blocks
        self.block_sight = False
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

        self.game_engine = game_engine


    def get_dict(self):
        result = {}
        result["texture_number"] = self.texture_number
        result["texture"] = self.textureID
        result["x"] = self.x
        result["y"] = self.y
        result["center_x"] = self.center_x
        result["center_y"] = self.center_y
        result["visible_color"] = self.visible_color
        result["not_visible_color"] = self.not_visible_color
        result["alpha"] = self.alpha
        result["color"] = self.color
        result["name"] = self.name
        result["blocks"] = self.blocks
        result["block_sight"] = self.block_sight
        result["is_visible"] = self.is_visible
        result["is_dead"] = self.is_dead
        if self.ai:
            result["ai"] = True
        if self.fighter:
            result["fighter"] = self.fighter.get_dict()
        if self.item:
            result["item"] = True
        if self.inventory:
            result["inventory"] = self.inventory.get_dict()

        return result

    def restore_from_dict(self, result):
        from actor.fighter import Fighter
        from actor.ai import Basicmonster
        from actor.item import Item
        from actor.inventory import Inventory

        self.x = result["x"]
        self.y = result["y"]
        self.center_x = result["center_x"]
        self.center_y = result["center_y"]
        self.texture_number = result["texture_number"]
        self.textureID = result["texture"]
        self.texture_ = self.textureID
        self.visible_color = result["visible_color"]
        self.not_visible_color = result["not_visible_color"]
        self.alpha = result["alpha"]
        self.color = result["color"]
        self.name = result["name"]
        self.blocks = result["blocks"]
        self.block_sight = result["block_sight"]
        self.is_visible = result["is_visible"]
        self.is_dead = result["is_dead"]
        if "ai" in result:
            self.ai = Basicmonster()
        if "item" in result:
            self.item = Item()
        if "fighter" in result:
            self.fighter = Fighter()
            self.fighter.restore_from_dict(result["fighter"])
        if "inventory" in result:
            self.inventory = Inventory()
            self.inventory.restore_from_dict(result["inventory"])

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
            self.dst_tile = self.game_engine.game_map.tiles[self.x +
                                                self.dx][self.y+self.dy]

            blocking_actor = get_blocking_entity(
                self.x+self.dx, self.y+self.dy, self.game_engine.map_sprits)
            if blocking_actor and not target:
                target = blocking_actor[0]
                if not target.is_dead:
                    attack_results = self.fighter.attack(target)
                    if target == self:
                        self.state = state.TURN_END
                    elif attack_results:
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

            elif not get_blocking_entity(self.x + self.dx, self.y + self.dy, self.game_engine.map_sprits) and\
                    self.dst_tile.blocked == False:

                self.dst_tile.blocked = True
                self.state = state.ON_MOVE
                self.change_y = self.dy * MOVE_SPEED
                self.change_x = self.dx * MOVE_SPEED

        except:
            pass

    def update(self, delta_time=1/60):
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

    # def move_towards(self, target_x, target_y, sprite_list):
    #     dx = target_x - self.x
    #     dy = target_y - self.y
    #     distance = math.sqrt(dx ** 2 + dy ** 2)

    #     dx = int(round(dx / distance))
    #     dy = int(round(dy / distance))

    #     if not get_blocking_entity(self.x + dx, self.y + dy, ENTITY_LIST):
    #         self.move((dx, dy))

    @property
    def texture_(self):
        return self.textures

    @texture_.setter
    def texture_(self, value):
        self.textures = []
        # TODO set
        self.textures.extend(ID.get(value))
        self.texture = self.textures[self.texture_number]
