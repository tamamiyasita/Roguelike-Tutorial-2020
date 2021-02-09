from actor.actor import Actor
from constants import *
from data import *
from random import randint
from actor.skills.melee_attack import MeleeAttack





class LeafBlade(MeleeAttack):
    def __init__(self, x=0, y=0, name="leaf_blade", data={"switch":False}):
        super().__init__(
            name=name,
            x=x,
            y=y,
            data=data
        )
        # self.color=COLORS["white"]

        #attackに渡される属性
        self.damage = 5
        self.hit_rate = 95
        self.speed = 6
        self.attr = "physical"
        self.effect = None

        self.level = 1

        self.tag = [Tag.item, Tag.equip, Tag.weapon, Tag.skill, Tag.passive]


        self.item_weight = 1.1

        # self.item_margin_x = 9
        # self.item_margin_y = 2

        # self.item_position_x = 9
        # self.item_position_y = 2
        self.explanatory_text = f"damage: {self.level}D{self.damage}\nhit rate: {self.hit_rate}"

        self.icon = IMAGE_ID["leaf_blade_icon"]

    def update_animation(self, delta_time):
        super().update_animation(delta_time)
        try:

            if self.master.state == state.ATTACK and Tag.weapon in self.tag:
                self.item_margin_x = (self.item_position_x + 5) * SPRITE_SCALE
                self.angle += 60
            else:
                self.angle = 0
        except:
            pass




