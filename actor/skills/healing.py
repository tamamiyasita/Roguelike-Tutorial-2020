from actor.actor import Actor
from actor.damage_pop import Damagepop
from constants import *
from data import *
import random
from util import dice, result_add
from actor.skills.base_skill import BaseSkill


class HealingEffect(Actor):
    def __init__(self, owner, engine):
        super().__init__(
            x=owner.x,
            y=owner.y,
            name="healing_potion_effect",
            color=COLORS["white"]
        )
        self.owner = owner
        self.engine = engine
        self.alpha = 150
        self.particle_time = 100
        self.emitter = arcade.Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=arcade.EmitterIntervalWithTime(0.003 * 5, 0.2),
            particle_factory=lambda emitter: arcade.LifetimeParticle(
                filename_or_texture=IMAGE_ID["healing_potion_effect"][0],
                change_xy=arcade.rand_on_circle((0.0, 0.0), 1.2),
                lifetime=0.8,
                scale=random.random()*2,
                alpha=random.randint(25, 115)

            )
        )
        self.alpha = 0
        engine.tmp_effect_sprites.append(self)

    def update(self):
        self.x = self.owner.x
        self.y = self.owner.y
        self.emitter.center_x = self.owner.center_x
        self.emitter.center_y = self.owner.center_y

        self.particle_time -= 1
        self.emitter.update()
        if self.particle_time < 0:
            self.remove_from_sprite_lists()


class Healing(BaseSkill):
    def __init__(self,x=0, y=0, name="healing"):
        super().__init__(
            name=name,
            x=x,
            y=y
        )
        self.data={"switch":False,
                  "count_time":0,
                  "cooldown":False}
        self.owner = None

        self.level = 1

        self.max_cooldown_time = 4

        self.item_weight = 5


        self.tag = [Tag.item, Tag.equip, Tag.used, Tag.active, Tag.skill]

        self.explanatory_text = f"Recover a small\namount of hp"
        self.icon = IMAGE_ID["healing_icon"]

        # self.item_margin_x = 9 * SPRITE_SCALE
        # self.item_margin_y = 3 * SPRITE_SCALE

        # self.item_position_x = 9
        # self.item_position_y = 2

    @property
    def hp_return(self):
        if self.owner:

            max_hp_return = 7 + int(self.owner.fighter.INT/2)

            return self.level, max_hp_return




    def use(self, engine):
        self.engine = engine

        if self.data["count_time"] <= 0:
            self.data["count_time"] = self.max_cooldown_time

            hp_return = dice(*self.hp_return)

            result = self.owner.fighter.change_hp(hp_return)
            Healing = HealingEffect(
                self.owner, self.engine)

            return [{"turn_end":self.owner, "message": f"{self.owner.name} have recovered {hp_return} using {self.name}"}, *result]

    def update_animation(self, delta_time):
        super().update_animation(delta_time)
        pass

    #     if self.master.state == state.HEAL:
    #         self.item_margin_