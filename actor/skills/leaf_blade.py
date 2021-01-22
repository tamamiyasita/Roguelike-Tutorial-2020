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
            actor_data={"switch":True},
            color=COLORS["white"]
        )

        self.damage = 5
        self.hit_rate = 95
        self.speed = 6

        self.level = 1

        self.tag = [Tag.item, Tag.equip, Tag.skill, Tag.passive]

        # self.explanatory_text = f"with excellent attack speed"
        self.icon = IMAGE_ID["leaf_blade_icon"]

        self.item_margin_x = 6 * SPRITE_SCALE
        self.item_margin_y = 3 * SPRITE_SCALE

    @property
    def explanatory_text(self):
        return f"damage: {self.level}D{self.damage}\nhit rate: {self.hit_rate}"

    def activate(self, owner):        
        if not owner.fighter.weapon:
            owner.fighter.weapon = self
            self.master = owner

    def deactivate(self, owner):        
        owner.fighter.weapon = None
        if self.master:
            del self.master


