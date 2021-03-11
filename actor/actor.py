from os import stat
from random import random, randint, uniform
from arcade import particle
from arcade.key import F
from arcade.text import draw_text
from actor.ai import Basicmonster, ConfusedMonster,RandomMove,Wait
import arcade
import math

from constants import *
from data import *
from util import pixel_to_grid, grid_to_pixel, get_blocking_entity,  stop_watch
# from particle import AttackParticle, PARTICLE_COUNT
from attack_effect import AttackEffect


from functools import lru_cache


class Actor(arcade.Sprite):
    """ 全てのオブジェクトを作成する基礎となるクラス
    """

    def __init__(self, texture_number=0, name=None, x=0, y=0,
                 blocks=False, block_sight=False,
                 scale=SPRITE_SCALE, color=COLORS["black"],
                #  fighter=None,
                  ai=None, speed=DEFAULT_SPEED,
                 inventory=None, equipment=None,
                 visible_color=COLORS["white"], not_visible_color=COLORS["black"],
                 states=None, npc_state=None, left_face=False,
                 power=None,
            
                 ):
        super().__init__(scale=scale)
        if name:
            self.name = name
            self.texture_number = texture_number
            self.texture_ = self.name
        self.dx, self.dy = 0, 0
        # self.center_x, self.center_y = grid_to_pixel(x, y)
        self._x, self._y = 0, 0
        self.x, self.y = x, y
        self.scale = scale
        self.blocks = blocks
        self.block_sight = block_sight
        self.color = color
        self.visible_color = visible_color
        self.not_visible_color = not_visible_color
        self.is_visible = False
        self.state = states
        self.npc_state = npc_state
        self.left_face = left_face
        self._master = None # 自身がitemだった場合その所持者を表す、主に装備時Spriteの表示位置に使用する
        self.d_time = 170 # 待機モーション時のdelay時間
        self.is_dead = False
        self.count_time = None
        self.from_x, self.from_y = 0,0
        self.dx, self.dy = 0,0

        self.tag = {}


        self.step = GRID_SIZE // 4

        self.inventory = inventory
        if self.inventory:
            self.inventory.owner = self


        self.speed = speed
        self.wait = speed//2

        self.ai = ai
        if self.ai:
            self.ai.owner = self
            self.state = state.TURN_END

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

        # self.fighter = fighter
        # if self.fighter:
        #     self.fighter.owner = self
        #     self.is_dead = False

    def get_dict(self):

        result = {}
        result["texture_number"] = self.texture_number
        result["name"] = self.name
        result["texture"] = self.name
        result["x"] = self.x
        result["y"] = self.y
        result["center_x"] = self.center_x
        result["center_y"] = self.center_y
        result["scale"] = self.scale
        result["visible_color"] = self.visible_color
        result["not_visible_color"] = self.not_visible_color
        result["alpha"] = self.alpha
        result["color"] = self.color
        result["blocks"] = self.blocks
        result["block_sight"] = self.block_sight
        result["is_visible"] = self.is_visible
        result["is_dead"] = self.is_dead
        result["left_face"] = self.left_face

        result["count_time"] = self.count_time

        if self.state:
            result["state"] = self.state.name
        if self.npc_state:
            result["npc_state"] = self.npc_state.name

        if self.ai.__class__.__name__ == "ConfusedMonster":
            result["confused_ai"] = self.ai.get_dict()
        elif self.ai:
            result["ai"] = self.ai.__class__.__name__

        # if self.fighter:
        #     result["fighter"] = self.fighter.get_dict()

        if self.inventory:
            result["inventory"] = self.inventory.get_dict()

        if self.equipment:
            result["equipment"] = self.equipment.get_dict()

        return result

    def restore_from_dict(self, result):
        from actor.fighter import Fighter
        from actor.ai import Basicmonster
        from actor.inventory import Inventory
        from constants import state
        from actor.equipment import Equipment

        self.x = result["x"]
        self.y = result["y"]
        self.center_x = result["center_x"]
        self.center_y = result["center_y"]
        self.scale = result["scale"]
        self.texture_number = result["texture_number"]
        self.name = result["name"]
        self.texture_ = result["name"]
        self.visible_color = result["visible_color"]
        self.not_visible_color = result["not_visible_color"]
        self.alpha = result["alpha"]
        self.color = result["color"]
        self.blocks = result["blocks"]
        self.block_sight = result["block_sight"]
        self.is_visible = result["is_visible"]
        self.is_dead = result["is_dead"]
        self.left_face = result["left_face"]
        self.count_time = result["count_time"]

        if "state" in result:
            self.state = state[result["state"]]
        if "npc_state" in result:
            self.npc_state = NPC_state[result["npc_state"]]

        if "ai" in result:
            self.ai = eval(result["ai"])()
            self.ai.owner = self
        if "confused_ai" in result:
            self.ai = ConfusedMonster()
            self.ai.owner = self
            self.ai.restore_from_dict(result["confused_ai"])

        self.inventory = None
        if "inventory" in result:
            self.inventory = Inventory()
            self.inventory.owner = self
            self.inventory.restore_from_dict(result["inventory"])

        if "equipment" in result:
            self.equipment = Equipment()
            self.equipment.owner = self
            self.equipment.restore_from_dict(result["equipment"])

        # if "fighter" in result:
        #     self.fighter = Fighter()
        #     self.fighter.owner = self
        #     self.fighter.restore_from_dict(result["fighter"])

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.center_x, self.center_y = grid_to_pixel(self._x, self._y)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.center_x, self.center_y = grid_to_pixel(self._x, self._y)


    @property
    def texture_(self):
        return self.textures

    @texture_.setter
    def texture_(self, value):
        self.textures = []
        img = IMAGE_ID.get(value)
        if isinstance(img, list):
            self.textures.extend(img)
        else:
            self.textures.append(img)


        self.texture = self.textures[self.texture_number]

    def update_animation(self, delta_time=1 / 60):
        super().update_animation()

        if self.state == state.ATTACK:
            self.combat_effect.attack()













        if len(self.textures) >= 2:
            if self.left_face:
                self.texture = self.textures[1]
            else:
                self.texture = self.textures[0]
        # NPC待機モーション
        if len(self.textures) >= 4 and self.ai:
            self.d_time -= 1
            if 100 > self.d_time and self.left_face:
                self.texture = self.textures[1]
            if 100 < self.d_time and self.left_face:
                self.texture = self.textures[3]
            if 100 > self.d_time and not self.left_face:
                self.texture = self.textures[0]
            if 100 < self.d_time and not self.left_face:
                self.texture = self.textures[2]
            if self.d_time < 0:
                self.d_time = 170



    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, owner):
        self.center_x = owner.center_x
        self.center_y = owner.center_y
        self._master = owner
        self.owner = owner
        self.color = COLORS["white"]

    @master.deleter
    def master(self):
        self.owner = None
        self._master = None

