from random import random, randint, uniform
from PIL.ImageOps import scale
from arcade import particle
from arcade.text import draw_text
from actor.ai import Basicmonster, ConfusedMonster,RandomMove,Wait
import arcade
import math

from constants import *
from data import *
from util import pixel_to_grid, grid_to_pixel, get_blocking_entity, get_door, stop_watch
from particle import AttackParticle, PARTICLE_COUNT

from functools import lru_cache


class Actor:
    """ 全てのオブジェクトを作成する基礎となるクラス
    """

    def __init__(self,name=None, x=0, y=0,
                 blocks=False, block_sight=False,
                 scale=SPRITE_SCALE, color=COLORS["black"],
                 fighter=None, ai=None, speed=DEFAULT_SPEED,
                 inventory=None, equipment=None,
                 visible_color=COLORS["white"], not_visible_color=COLORS["black"],
                 explanatory_text="", tag={Tag.free},
                 state=state.TURN_END, left_face=False
                 ):
        # super().__init__(scale=scale)
        self.name = name
        self._sprite = None

        self.dx, self.dy = 0, 0
        self._center_x, self._center_y = grid_to_pixel(x, y)
        self._x, self._y = 0, 0
        self.x, self.y = x, y
        self._scale = scale
        self.blocks = blocks
        self.block_sight = block_sight
        self._color = color
        self.visible_color = visible_color
        self.not_visible_color = not_visible_color
        self.is_visible = False
        self.state = state
        self.explanatory_text = explanatory_text # Lコマンド等の説明文に使用する
        self.tag = tag
        self.left_face = left_face
        self._master = None # 自身がitemだった場合その所持者を表す、主に装備時Spriteの表示位置に使用する
        self.d_time = 100 # 待機モーション時のdelay時間
        self.is_dead = None
        self.skill_add = {} # skillLevelの追加に使う

        self.inventory = inventory
        if self.inventory:
            self.inventory.owner = self

        self.state = None

        self.speed = speed
        self.wait = speed//2

        self.ai = ai
        if self.ai:
            self.ai.owner = self
            self.state = state

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self
            self.is_dead = False
        self.sprite_set()


    def join_sprites(self, sprites):
        sprites.append(self.sprite)

    @property
    def center_x(self):
        return self.sprite.center_x
    @property
    def center_y(self):
        return self.sprite.center_y
    @center_x.setter
    def center_x(self, value):
        self._center_x = value
        if self.sprite:
            self.sprite.center_x = self._center_x
    @center_y.setter
    def center_y(self, value):
        self._center_y = value
        if self.sprite:
            self.sprite.center_y = self._center_y

    @property
    def color(self):
        return self.sprite.color
    @color.setter
    def color(self, value):
        self._color = value
        self.sprite.color = value

    @property
    def alpha(self):
        return self.sprite.alpha

    @alpha.setter
    def alpha(self, value):
        self.sprite.alpha = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        

        


    @property
    def sprite(self):
        return self._sprite

    def sprite_set(self):
        sprite = arcade.Sprite()
        self._sprite = sprite
        self.texture=self.name
        sprite.scale = 2


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

        if self.ai.__class__.__name__ == "ConfusedMonster":
            result["confused_ai"] = self.ai.get_dict()
        elif self.ai:
            result["ai"] = self.ai.__class__.__name__

        if self.fighter:
            result["fighter"] = self.fighter.get_dict()

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

        if "state" in result:
            self.state = state.TURN_END
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

        if "fighter" in result:
            self.fighter = Fighter()
            self.fighter.owner = self
            self.fighter.restore_from_dict(result["fighter"])

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
    def texture(self):
        return self._sprite.texture

    @texture.setter
    def texture(self, value):
        self.textures = []
        img = IMAGE_ID.get(value)
        if isinstance(img, list):
            self.textures.extend(img)
        else:
            self.textures.append(img)


        self._sprite.texture = self.textures[0]


    def move(self, dxy, target=None, engine=None):
        self.attack_delay = 7
        wall_sprites = engine.cur_level.wall_sprites
        map_obj_sprites = engine.cur_level.map_obj_sprites
        actor_sprites = engine.cur_level.actor_sprites
        self.effect_sprites = engine.cur_level.effect_sprites

        self.dx, self.dy = dxy

        # 振動ダメージエフェクトに使う変数
        self.other = None
        self.other_x = None

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

                door_actor.left_face = True
                self.state = state.TURN_END
                return [{"delay": {"time": 0.2, "action": "None"}}]

        # 行き先がBlockされてるか調べる
        blocking_actor = get_blocking_entity(
            destination_x, destination_y, [actor_sprites, wall_sprites])

        def player_move():

            if blocking_actor and not target:
                # playerの攻撃チェック
                actor = blocking_actor[0]
                if actor in wall_sprites:
                    return [{"None": True}]

                if Tag.friendly in actor.tag:
                    result = [{"talk": actor}]
                    if Tag.quest in actor.tag:
                        result.extend([{"turn_end": self}])
                    return result

                elif not actor.is_dead:
                    attack_results = self.fighter.attack(actor)

                    self.other = actor
                    self.other_x = actor.center_x
                    if attack_results:
                        self.state = state.ATTACK
                        self.change_y = self.dy * MOVE_SPEED
                        self.change_x = self.dx * MOVE_SPEED
                        engine.action_queue.extend(
                            [{"delay": {"time": 0.2, "action": {"None": self}}}])

                    return attack_results

            else:
                self.state = state.ON_MOVE
                self.change_y = self.dy * (MOVE_SPEED)
                self.change_x = self.dx * (MOVE_SPEED)
        @stop_watch
        def monster_move(target):
            ai_move_speed = MOVE_SPEED*2

            if target and self.distance_to(target) <= 1.46:
                # monsterの攻撃チェック
                attack_results = self.fighter.attack(target)

                self.other = target
                self.other_x = target.center_x
                if attack_results:
                    self.state = state.ATTACK
                    self.change_y = self.dy * MOVE_SPEED
                    self.change_x = self.dx * MOVE_SPEED

                return attack_results

            elif not get_blocking_entity(destination_x, destination_y, [actor_sprites, wall_sprites]):
                # monsterの移動
                self.x = destination_x
                self.y = destination_y
                self.wait = self.speed
                self.state = state.TURN_END

            else:
                # A*パスがBlockされたらturn_endを返す
                print(f"actor {self.name} blocking pass!")
                return [{"turn_end": self}]

        if self.ai:
            return monster_move(target)

        else:
            return player_move()

    def update(self, delta_time=1/60):
        super().update()
        if self.state == state.ON_MOVE:
            if abs(self.target_x - self.center_x) >= GRID_SIZE and self.dx or\
                    abs(self.target_y - self.center_y) >= GRID_SIZE and self.dy:
                self.change_x = 0
                self.change_y = 0
                self.x += self.dx
                self.y += self.dy
                self.wait = self.speed
                self.target_x, self.target_y = self.center_x, self.center_y
                self.state = state.TURN_END

        if self.state == state.ATTACK:
            self.attack()
    @stop_watch
    def attack(self):
        step = GRID_SIZE // 2.5

        if abs(self.target_x - self.center_x) >= step and self.dx or\
                abs(self.target_y - self.center_y) >= step and self.dy:
            self.change_x = 0
            self.change_y = 0

        if self.attack_delay == 6:
            for i in range(PARTICLE_COUNT):
                particle = AttackParticle()
                particle.position = (
                    self.center_x + (self.dx*20), self.center_y + (self.dy*20))
                self.effect_sprites.append(particle)
                self.other.change_x += uniform(-0.7, 0.7)

        if self.attack_delay % 2 == 0:
            self.other.alpha = 10
        else:
            self.other.alpha = 155

        if self.change_x == 0 and self.change_y == 0 and self.state != state.TURN_END:
            self.attack_delay -= 1

            if 0 > self.attack_delay:
                self.center_y = self.target_y
                self.center_x = self.target_x
                self.change_x, self.change_y = 0, 0
                self.other.alpha = 255
                self.other.change_x = 0
                self.other.center_x = self.other_x
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

        if not get_blocking_entity(self.x + dx, self.y + dy, [actor_sprites]):
            move = self.move((dx, dy), target, engine)
            return move


    def update_animation(self, delta_time=1 / 60):
        # 左右を向く
        if len(self.textures) >= 2:
            if self.left_face:
                self.texture = self.textures[1]
            else:
                self.texture = self.textures[0]
        # NPC待機モーション
        if len(self.textures) >= 4 and self.ai:
            self.d_time -= 1
            if 50 > self.d_time and self.left_face:
                self.texture = self.textures[1]
            if 50 < self.d_time and self.left_face:
                self.texture = self.textures[3]
            if 50 > self.d_time and not self.left_face:
                self.texture = self.textures[0]
            if 50 < self.d_time and not self.left_face:
                self.texture = self.textures[2]
            if self.d_time < 0:
                self.d_time = 100

        # itemを装備した時のsprite表示
        if self.master and Tag.flower not in self.tag:
            x = self.master.center_x
            if self.master.left_face:
                self.left_face = True
                self.center_y = self.master.center_y - self.item_margin_y
                self.center_x = x - self.item_margin_x
            if self.master.left_face == False:
                self.left_face = False
                self.center_y = self.master.center_y - self.item_margin_y
                self.center_x = x + self.item_margin_x
        elif self.master and Tag.flower in self.tag:
            self.flower_setup(self.master)

    def flower_setup(self, target):
        if target.left_face:
            item_margin_x = self.item_margin_x
        else:
            item_margin_x = -self.item_margin_x
        self.angle += uniform(0.1, 3)
        x_diff = (target.center_x + item_margin_x + random()) - (self.center_x)
        y_diff = (target.center_y + self.item_margin_y +
                  random()) - (self.center_y)
        angle = math.atan2(y_diff, x_diff)

        if abs(x_diff) > 15 or abs(y_diff) > 15:

            self.change_x = math.cos(
                angle) * (self.my_speed + uniform(0.6, 4.2))
            self.change_y = math.sin(
                angle) * (self.my_speed + uniform(0.6, 4.2))
        else:
            self.change_x = math.cos(angle) * uniform(0.02, 0.3)
            self.change_y = math.sin(angle) * uniform(0.02, 0.3)

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, owner):
        self._master = owner
        self.center_x = owner.center_x
        self.center_y = owner.center_y
        self.color = arcade.color.WHITE

    @master.deleter
    def master(self):
        self._master = None
