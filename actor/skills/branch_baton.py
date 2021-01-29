import arcade
from actor.actor import Actor
from constants import *
from data import *
from actor.skills.leaf_blade import LeafBlade

class BranchBaton(LeafBlade):
    def __init__(self, x=0, y=0, name="branch_baton"):
        super().__init__(
            name=name,
            x=x,
            y=y,
        )

        self.damage = 7
        self.hit_rate = 92
        self.speed = 6

        self.level = 1


        self.icon = IMAGE_ID["branch_baton_icon"]

        self.item_margin_x = 6 * SPRITE_SCALE
        self.item_margin_y = 4 * SPRITE_SCALE

