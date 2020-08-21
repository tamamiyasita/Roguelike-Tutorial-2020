from actor.ai import Basicmonster, ConfusedMonster
import arcade
import math
from dataclasses import dataclass

from constants import *
from data import *
from util import pixel_to_grid, grid_to_pixel, get_blocking_entity
from actor.item import Item

@dataclass
class Actor(arcade.Sprite):
    """ 全てのオブジェクトを作成する基礎となるクラス
    """

    # def __init__(self, texture_number=0, name=None, x=0, y=0, blocks=False, block_sight=False,
    #              scale=SPRITE_SCALE, color=arcade.color.BLACK, fighter=None, ai=None,
    #              inventory=None, item=None, equipment=None, equippable=None,
    #              visible_color=COLORS["white"], not_visible_color=arcade.color.BLACK,
    #              state=state.TURN_END):
    # super().__init__(scale=scale)
    scale:float = SPRITE_SCALE
    name:str = None
    texture_number:int = 0
    texture_:str = name
    dx:float = 0
    dy:float = 0
    x:int = 0
    y:int = 0
    blocks:bool = False
    block_sight:bool = False 
    color:str = ""
    visible_color:str = ""
    not_visible_color:str = ""
    is_visible:bool = False
    is_dead:bool = False
    left_face:bool = False
    _master:any = None


    item:any = None
    inventory:any = None

    state = None

    self.fighter = fighter
    if self.fighter:
        self.fighter.owner = self
        self.state = state

    self.ai = ai
    if self.ai:
        self.ai.owner = self

    self.equipment = equipment
    if self.equipment:
        self.equipment.owner = self

    self.equippable = equippable
    if self.equippable:
        self.equippable.owner = self
        if not self.item:
            item = Item()
            self.item = item
            self.item.owner =self

    def __post_init__(self):
        self.center_x, self.center_y = grid_to_pixel(self.x, self.y)
        self.x, self.y = pixel_to_grid(self.center_x, self.center_y)
        if self.inventory:
            self.inventory.owner = self

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

        if self.ai.__class__.__name__ == "Basicmonster":
            result["ai"] = True
        if self.ai.__class__.__name__ == "ConfusedMonster":
            result["confused_ai"] = self.ai.get_dict()
            
        if self.fighter:
            result["fighter"] = self.fighter.get_dict()
        if self.item:
            result["item"] = True
        if self.inventory:
            result["inventory"] = self.inventory.get_dict()
  
        if self.equippable:
            result["equippable"] = self.equippable.get_dict()

        if self.equipment:
            result["equipment"] = self.equipment.get_dict()
        
        return result

    def restore_from_dict(self, result):
        from actor.fighter import Fighter
        from actor.ai import Basicmonster
        from actor.inventory import Inventory
        from constants import state
        from actor.equippable import Equippable
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

        if "ai" in result:
            self.ai = Basicmonster()
            self.ai.owner = self
        if "confused_ai" in result:
            self.ai = ConfusedMonster()
            self.ai.owner = self
            self.ai.restore_from_dict(result["confused_ai"])
        if "item" in result:
            self.item = Item()

        if "equipment" in result:
            self.equipment = Equipment()
            self.equipment.owner = self
            self.equipment.restore_from_dict(result["equipment"])

        if "equippable" in result:
            self.equippable = Equippable()
            self.equippable.owner = self
            self.equippable.restore_from_dict(result["equippable"])
            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

        
        
        self.inventory = None
        if "inventory" in result:
            self.inventory = Inventory()
            self.inventory.owner = self
            self.inventory.restore_from_dict(result["inventory"])

        if "fighter" in result:
            self.fighter = Fighter()
            self.fighter.owner = self
            self.fighter.restore_from_dict(result["fighter"])


    def move(self, dxy, target=None, actor_sprites=None, map_sprites=None):
        ai_move_speed = 0
        if self.ai:
            ai_move_speed = MOVE_SPEED*1.3
        self.dx, self.dy = dxy

        if self.dx == -1:
            self.left_face = True
        if self.dx == 1:
            self.left_face = False
        
        destination_x = self.dx + self.x
        destination_y = self.dy + self.y

        self.target_x = self.center_x
        self.target_y = self.center_y

        # 行先のfloorオブジェクトを変数booking_tileに入れる
        self.booking_tile = arcade.get_sprites_at_exact_point(grid_to_pixel(destination_x, destination_y), map_sprites)[0]

        blocking_actor = get_blocking_entity(destination_x, destination_y, actor_sprites)
        if blocking_actor and not target:
            actor = blocking_actor[0]
            if not actor.is_dead:
                attack_results = self.fighter.attack(actor)
                if actor == self:
                    self.state = state.TURN_END
                elif attack_results:
                    self.state = state.ATTACK
                    self.change_y = self.dy * (MOVE_SPEED+ai_move_speed)
                    self.change_x = self.dx * (MOVE_SPEED+ai_move_speed)

                return attack_results

        elif target and self.distance_to(target) <= 1.46:
            attack_results = self.fighter.attack(target)
            if attack_results:
                self.state = state.ATTACK
                self.change_y = self.dy * MOVE_SPEED
                self.change_x = self.dx * MOVE_SPEED

            return attack_results

        elif not get_blocking_entity(destination_x, destination_y, actor_sprites) and self.booking_tile.blocks == False:
            self.booking_tile.blocks = True
            self.state = state.ON_MOVE
            self.change_y = self.dy * (MOVE_SPEED+ai_move_speed)
            self.change_x = self.dx * (MOVE_SPEED+ai_move_speed)



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
                    self.booking_tile.blocks = False
                    # self.state = state.TURN_END
                if self.dx == -1:
                    self.center_x = self.target_x - grid
                    self.x += self.dx
                    self.booking_tile.blocks = False
                self.state = state.TURN_END

            if abs(self.target_y - self.center_y) >= grid and self.dy:
                self.change_y = 0
                if self.dy == 1:
                    self.center_y = self.target_y + grid
                    self.y += self.dy
                    self.booking_tile.blocks = False
                    # self.state = state.TURN_END
                if self.dy == -1:
                    self.center_y = self.target_y - grid
                    self.y += self.dy
                    self.booking_tile.blocks = False
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

    def move_towards(self, target, actor_sprites, map_sprites):

        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not get_blocking_entity(self.x + dx, self.y + dy, actor_sprites):
            move = self.move((dx, dy), target, actor_sprites, map_sprites)
            return move


    @property
    def texture_(self):
        return self.textures

    @texture_.setter
    def texture_(self, value):
        self.textures = []
        self.textures.extend(IMAGE_ID.get(value))
        self.texture = self.textures[self.texture_number]

    def update_animation(self, delta_time=1 / 60):
        if len(self.textures) >= 2:
            if self.left_face:
                self.texture = self.textures[1]
            else:
                self.texture = self.textures[0]

        # itemを装備した時のsprite表示
        if self.master:
            self.color = COLORS["white"]
            self.alpha = 255
            x = self.master.center_x
            if self.master.left_face:
                self.left_face = True
                self.center_y = self.master.center_y - self.item_margin_y
                self.center_x = x - self.item_margin_x
            if self.master.left_face == False:
                self.left_face = False
                self.center_y = self.master.center_y - self.item_margin_y
                self.center_x = x + self.item_margin_x


    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, owner):
        self._master = owner
    
    @master.deleter
    def master(self):
        self._master = None