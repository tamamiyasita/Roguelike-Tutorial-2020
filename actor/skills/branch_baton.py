
from constants import *
from data import *
from actor.skills.melee_attack import MeleeAttack
from random import randint

class BranchBaton(MeleeAttack):
    def __init__(self, x=0, y=0, name="branch_baton"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )

        self.damage = 7
        self.hit_rate = 92
        self.speed = 6
        self.attr = "physical"
        self.effect = None

        self.tag = [Tag.item, Tag.equip, Tag.weapon, Tag.skill, Tag.passive]

        self.level = 1
        
        self.item_weight = 1


        self.explanatory_text = f"damage: {self.level}D{self.damage}\nhit rate: {self.hit_rate}"

        self.icon = IMAGE_ID["branch_baton_icon"]


    def update_animation(self, delta_time):
        super().update_animation(delta_time)
        try:

            if self.master.state == state.ATTACK and Tag.weapon in self.tag:
                self.item_margin_x = (self.item_position_x + 3) * SPRITE_SCALE
                self.item_margin_y += randint(-8,8)
                self.item_margin_x += randint(-8,8)
            else:
                self.angle = 0
        except:
            pass
