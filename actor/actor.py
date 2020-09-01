from arcade import particle
from actor.ai import Basicmonster, ConfusedMonster
import arcade
import math

from constants import *
from data import *
from util import pixel_to_grid, grid_to_pixel, get_blocking_entity, get_door
from actor.item import Item
from particle import AttackParticle, PARTICLE_COUNT


class Actor(arcade.Sprite):
    """ 全てのオブジェクトを作成する基礎となるクラス
    """

    def __init__(self, texture_number=0, name=None, x=0, y=0,
                 blocks=False, block_sight=False,
                 scale=SPRITE_SCALE, color=COLORS["black"],
                 fighter=None, ai=None, speed=DEFAULT_SPEED,
                 inventory=None, item=None, equipment=None, equippable=None,
                 visible_color=COLORS["white"], not_visible_color=COLORS["black"],
                 state=state.TURN_END, left_face=False):
        super().__init__(scale=scale)
        if name:
            self.name = name
            self.texture_number = texture_number
            self.texture_ = self.name
        self.dx, self.dy = 0, 0
        self.center_x, self.center_y = grid_to_pixel(x, y)
        self.x, self.y = pixel_to_grid(self.center_x, self.center_y)
        self.scale = scale
        self.blocks = blocks
        self.block_sight = block_sight
        self.color = color
        self.visible_color = visible_color
        self.not_visible_color = not_visible_color
        self.is_visible = False
        self.is_dead = False
        self.state = state
        self.left_face = left_face
        self._master = None

        self.item = item
        self.inventory = inventory
        if self.inventory:
            self.inventory.owner = self

        self.state = None

        self.speed = speed
        self.wait = speed//2

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
                self.item.owner = self


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

        if self.state:
            result["state"] = True

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
        self.left_face = result["left_face"]

        if "state" in result:
            self.state = state.TURN_END
        if "ai" in result:
            self.ai = Basicmonster()
            self.ai.owner = self
        if "confused_ai" in result:
            self.ai = ConfusedMonster()
            self.ai.owner = self
            self.ai.restore_from_dict(result["confused_ai"])
        if "item" in result:
            self.item = Item()

        self.inventory = None
        if "inventory" in result:
            self.inventory = Inventory()
            self.inventory.owner = self
            self.inventory.restore_from_dict(result["inventory"])

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

        if "fighter" in result:
            self.fighter = Fighter()
            self.fighter.owner = self
            self.fighter.restore_from_dict(result["fighter"])

    def move(self, dxy, target=None, engine=None):
        self.attack_delay = 7
        floor_sprites = engine.cur_level.floor_sprites
        wall_sprites = engine.cur_level.wall_sprites
        map_obj_sprites = engine.cur_level.map_obj_sprites
        actor_sprites = engine.cur_level.actor_sprites
        self.effect_sprites = engine.cur_level.effect_sprites

        ai_move_speed = 5
        if self.ai:
            ai_move_speed = MOVE_SPEED*2
        self.dx, self.dy = dxy

        if self.dx == -1:
            self.left_face = True
        if self.dx == 1:
            self.left_face = False

        destination_x = self.dx + self.x
        destination_y = self.dy + self.y

        self.target_x = self.center_x
        self.target_y = self.center_y


        # ドアのチェック
        door_actor = get_door(destination_x, destination_y, map_obj_sprites)

        if door_actor:
            self.state = state.DOOR
            door_actor = door_actor[0]
            if door_actor.left_face == False:
                # engine.action_queue.extend([{"delay": {"time": 0.2, "action": {"turn_end": self}}}])

                door_actor.left_face = True
                # self.state = state.TURN_END
                print("open door")
                self.state = state.TURN_END
                # engine.action_queue.extend([{"turn_end": self}])
                return [{"delay": {"time": 0.2, "action": "None"}}]

        # 行き先がBlockされてるか調べる
        blocking_actor = get_blocking_entity(
            destination_x, destination_y, {actor_sprites, wall_sprites})

        if blocking_actor and not target:
            # playerの攻撃チェック
            actor = blocking_actor[0]
            if actor in wall_sprites:
                return [{"None": True}]
                
            elif not actor.is_dead:
                attack_results = self.fighter.attack(actor)
                if actor == self:
                    self.state = state.TURN_END
                elif attack_results:
                    self.state = state.ATTACK
                    self.change_y = self.dy * MOVE_SPEED
                    self.change_x = self.dx * MOVE_SPEED
                    engine.action_queue.extend(
                        [{"delay": {"time": 0.2, "action": {"None": self}}}])

                return attack_results

        elif target and self.distance_to(target) <= 1.46:
            # monsterの攻撃チェック
            attack_results = self.fighter.attack(target)
            if attack_results:
                self.state = state.ATTACK
                self.change_y = self.dy * MOVE_SPEED
                self.change_x = self.dx * MOVE_SPEED

            return attack_results

        elif not get_blocking_entity(destination_x, destination_y, {actor_sprites, wall_sprites}):
            # playerとmonsterの移動
            self.state = state.ON_MOVE
            self.change_y = self.dy * (MOVE_SPEED+ai_move_speed)
            self.change_x = self.dx * (MOVE_SPEED+ai_move_speed)

        else:
            # A*パスがBlockされたらturn_endを返す
            print(f"actor {self.name} blocking pass!")
            return [{"turn_end": self}]

    def update(self, delta_time=1/60):
        super().update()
        if self.state == state.ON_MOVE:
            if abs(self.target_x - self.center_x) >= GRID_SIZE and self.dx:
                self.change_x = 0
                if self.dx == 1:
                    self.center_x = self.target_x + GRID_SIZE
                    self.x += self.dx
                    # self.state = state.TURN_END
                if self.dx == -1:
                    self.center_x = self.target_x - GRID_SIZE
                    self.x += self.dx
                self.state = state.TURN_END

            if abs(self.target_y - self.center_y) >= GRID_SIZE and self.dy:
                self.change_y = 0
                if self.dy == 1:
                    self.center_y = self.target_y + GRID_SIZE
                    self.y += self.dy
                    # self.state = state.TURN_END
                if self.dy == -1:
                    self.center_y = self.target_y - GRID_SIZE
                    self.y += self.dy
                self.state = state.TURN_END

            self.wait = self.speed

        if self.state == state.ATTACK:
            self.attack()
            

    def attack(self):
        step = GRID_SIZE // 2.5


        if abs(self.target_x - self.center_x) >= step and self.dx:
            self.change_x = 0
                # self.state = state.TURN_END
        if abs(self.target_y - self.center_y) >= step and self.dy:
            self.change_y = 0
            # self.attack_delay -= 1
            # if 0 > self.attack_delay:
            #     self.state = state.TURN_END
        if self.attack_delay == 6:
            for i in range(PARTICLE_COUNT):
                particle = AttackParticle()
                particle.position = (self.center_x + (self.dx*20), self.center_y + (self.dy*20))
                self.effect_sprites.append(particle)

        if self.change_x == 0 and self.change_y == 0 and self.state != state.TURN_END:
            self.attack_delay -= 1




            if 0 > self.attack_delay:
                self.center_y = self.target_y
                self.center_x = self.target_x
                self.change_x, self.change_y = 0, 0
                self.state = state.TURN_END

        if self.state == state.TURN_END:
            self.wait = self.fighter.attack_speed

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_towards(self, target, engine):

        actor_sprites = engine.cur_level.actor_sprites

        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not get_blocking_entity(self.x + dx, self.y + dy, {actor_sprites}):
            move = self.move((dx, dy), target, engine)
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
