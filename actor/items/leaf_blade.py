import arcade
from actor.actor import Actor
from constants import *
from data import *


class LeafBlade(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            name="leaf_blade",
            x=x,
            y=y,
            color=COLORS["white"]
        )

        self.damage = 5
        self.hit_rate = 95
        self.speed = 6

        self.level = 0

        self.tag = [Tag.item, Tag.equip, Tag.skill, Tag.passive]

        self.explanatory_text = f"with excellent attack speed"
        self.icon = IMAGE_ID["leaf_blade_icon"]

        self.item_margin_x = 6 * SPRITE_SCALE
        self.item_margin_y = 3 * SPRITE_SCALE

    def activate(self, owner):
        self.master = owner
        if self.master and self.master.fighter.weapon is None:
            self.master.fighter.weapon = self

    def deactivate(self):
        if self.master and self.master.fighter.weapon is not None:
            self.master.fighter.weapon = None
            del self.master


    # @property
    # def attack_damage(self):
    #     if self.master:
    #         self._attack_damage[0] = 1 + self.level // 2

    #     return self._attack_damage
