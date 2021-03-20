from constants import *
from data import *
from random import randint
from actor.skills.base_skill import BaseSkill
from util import dice




class GrassCutter(BaseSkill):
    def __init__(self, x=0, y=0, name="grass_cutter"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )
        # self.color=COLORS["white"]

        #attackに渡される属性
        self._damage = 5
        self.hit_rate = 95
        self.speed = 6
        self.attr = "physical"
        self.effect = None

        self.owner = None

        self._level = 1

        self.tag = [Tag.item, Tag.equip, Tag.weapon, Tag.skill, Tag.passive]


        self.item_weight = 1.1

        self.explanatory_text = f"damage: {self.level}D{self.damage}\nhit rate: {self.hit_rate}"

        self.icon = IMAGE_ID["grass_cutter_icon"]

    @property
    def damage(self):
        if self.owner:
            attr = self.owner.fighter.description
            return dice((self.level / 3 + 1), ((self.owner.fighter.STR + attr["supple"]))/2, attr["sharp"])

    def update_animation(self, delta_time):
        super().update_animation(delta_time)
        try:

            if self.master.state == state.ATTACK and Tag.weapon in self.tag:
                self.item_margin_x = (self.item_position_x + 5) * SPRITE_SCALE
                self.angle += 90
            else:
                self.angle = 0
        except:
            pass




