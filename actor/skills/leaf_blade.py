from actor.actor import Actor
from constants import *
from data import *







class LeafBlade(Actor):
    def __init__(self, x=0, y=0, name="leaf_blade"):
        super().__init__(
            name=name,
            x=x,
            y=y,
            data={"switch":True}
        )
        self.color=COLORS["white"]


        self.damage = 5
        self.hit_rate = 95
        self.speed = 6

        self.level = 1

        self.tag = [Tag.item, Tag.equip, Tag.weapon, Tag.skill, Tag.passive]

        self.icon = IMAGE_ID["leaf_blade_icon"]

        self.item_margin_x = 6 * SPRITE_SCALE
        self.item_margin_y = 3 * SPRITE_SCALE

    @property
    def explanatory_text(self):
        # 説明文を返す
        return f"damage: {self.level}D{self.damage}\nhit rate: {self.hit_rate}"

    def activate(self, owner):        
        if owner.fighter.weapon is None:
            owner.fighter.weapon = self
            self.master = owner

    def deactivate(self, owner):        
        owner.fighter.weapon = None
        del self.master
        self.remove_from_sprite_lists()


