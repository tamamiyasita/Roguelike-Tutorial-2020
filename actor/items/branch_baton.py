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
        self.states_bonus = {"STR": 1}
        self.attack_damage = (1, 2, 7)
        self.hit_rate = 92

        self.level = 0

        self.tag = [Tag.item, Tag.equip, Tag.skill]

        self.explanatory_text = f"testtesttest and test"
        self.icon = IMAGE_ID["branch_baton_icon"]

        self.item_margin_x = 6 * SPRITE_SCALE
        self.item_margin_y = 3 * SPRITE_SCALE
