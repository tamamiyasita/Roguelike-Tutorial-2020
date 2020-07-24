import arcade
import math

from constants import *
from data import *
from util import pixel_to_grid, grid_to_pixel, get_blocking_entity


class Actor(arcade.Sprite):
    """ 全てのオブジェクトを作成する基礎となるクラス
    """

    def __init__(self, texture_number=0, name=None, x=0, y=0, blocks=False, block_sight=False,
                 scale=SPRITE_SCALE, color=arcade.color.BLACK, fighter=None, ai=None,
                 inventory=None, item=None,
                 visible_color=arcade.color.WHITE, not_visible_color=arcade.color.BLACK,
                 state=state.TURN_END):
        super().__init__(scale=scale)
        self.name = name
        self.texture_number = texture_number
        self.texture_ = self.name
        self.dx, self.dy = 0, 0
        self.center_x, self.center_y = grid_to_pixel(x, y)
        self.x, self.y = pixel_to_grid(self.center_x, self.center_y)
        self.blocks = blocks
        self.block_sight = block_sight
        self.color = color
        self.visible_color = visible_color
        self.not_visible_color = not_visible_color
        self.is_visible = False
        self.is_dead = False
        self.inventory = inventory
        self.item = item

        self.state = None

        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self
            self.state = state

        self.ai = ai
        if self.ai:
            self.ai.owner = self

    def get_dict(self):
        result = {}
        result["texture_number"] = self.texture_number
        result["name"] = self.name
        result["texture"] = self.name
        result["x"] = self.x
        result["y"] = self.y
        result["center_x"] = self.center_x
        result["center_y"] = self.center_y
        result["visible_color"] = self.visible_color
        result["not_visible_color"] = self.not_visible_color
        result["alpha"] = self.alpha
        result["color"] = self.color
        result["blocks"] = self.blocks
        result["block_sight"] = self.block_sight
        result["is_visible"] = self.is_visible
        result["is_dead"] = self.is_dead
        if self.state:
            result["state"] = True
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
        from constants import state

        self.x = result["x"]
        self.y = result["y"]
        self.center_x = result["center_x"]
        self.center_y = result["center_y"]
        self.texture_number = result["texture_number"]
        self.name = result["name"]
        self.texture_ = self.name
        self.visible_color = result["visible_color"]
        self.not_visible_color = result["not_visible_color"]
        self.alpha = result["alpha"]
        self.color = result["color"]
        self.blocks = result["blocks"]
        self.block_sight = result["block_sight"]
        self.is_visible = result["is_visible"]
        self.is_dead = result["is_dead"]
        if "state" in result:
            self.state = state.TURN_END
        if "ai" in result:
            self.ai = Basicmonster()
            self.ai.owner = self
        if "item" in result:
            self.item = Item()
            print(f"Restore item {self.name}")
        self.inventory = None
        if "fighter" in result:
            self.fighter = Fighter()
            self.fighter.owner = self
            self.fighter.restore_from_dict(result["fighter"])
        if "inventory" in result:
            self.inventory = Inventory()
            self.inventory.restore_from_dict(result["inventory"])

    def move(self, dxy, target=None, actor_sprites=None, map_sprites=None):
        try:
            ai_move_speed = 0
            if self.ai:
                ai_move_speed = MOVE_SPEED*3
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
                self.booking_tile.alpha = 10
                self.state = state.ON_MOVE
                self.change_y = self.dy * (MOVE_SPEED+ai_move_speed)
                self.change_x = self.dx * (MOVE_SPEED+ai_move_speed)

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
                    self.booking_tile.blocks = False
                    self.state = state.TURN_END
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
                    self.state = state.TURN_END
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
            self.move((dx, dy), target, actor_sprites, map_sprites)

    @property
    def texture_(self):
        return self.textures

    @texture_.setter
    def texture_(self, value):
        self.textures = []
        self.textures.extend(IMAGE_ID.get(value))
        self.texture = self.textures[self.texture_number]
