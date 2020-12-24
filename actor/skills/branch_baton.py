import arcade
from actor.actor import Actor
from constants import *
from data import *


class BranchBaton(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="branch_baton",
            x=x,
            y=y,
            color=arcade.color.WHITE
        )

        self.slot = "main_hand"
        self.attack_damage = 7
        self.hit_rate = 92
        self.speed = 7

        self.level = 0

        self.tag = [Tag.item, Tag.equip, Tag.skill, Tag.passive]

        self.explanatory_text = f"with excellent damage"
        self.icon = IMAGE_ID["branch_baton_icon"]

        self.item_margin_x = 6 * SPRITE_SCALE
        self.item_margin_y = 3 * SPRITE_SCALE
