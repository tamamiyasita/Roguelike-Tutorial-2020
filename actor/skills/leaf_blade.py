from actor.actor import Actor
from constants import *
from data import *
from random import randint






class LeafBlade(Actor):
    def __init__(self, x=0, y=0, name="leaf_blade"):
        super().__init__(
            name=name,
            x=x,
            y=y,
            data={"switch":False}
        )
        self.color=COLORS["white"]

        #attackに渡される属性
        self.damage = 5
        self.hit_rate = 95
        self.speed = 6
        self.attr = "physical"
        self.effect = None

        self.level = 1

        self.tag = [Tag.item, Tag.equip, Tag.weapon, Tag.skill, Tag.passive]

        self.icon = IMAGE_ID["leaf_blade_icon"]

        self.item_weight = 1.1

        self.item_margin_x = 9
        self.item_margin_y = 2

        self.item_position_x = 9
        self.item_position_y = 2

        self.explanatory_text = f"damage: {self.level}D{self.damage}\nhit rate: {self.hit_rate}"

    # @property
    # def explanatory_text(self):
    #     # 説明文を返す
    #     return f"damage: {self.level}D{self.damage}\nhit rate: {self.hit_rate}"

    def activate(self, owner):        
        owner.fighter.data["weapon"] = self
        self.data["switch"] = True
        self.master = owner

    def deactivate(self, owner):        
        owner.fighter.data["weapon"] = None
        self.data["switch"] = False
        del self.master
        self.remove_from_sprite_lists()

    def update(self):
        super().update()
        try:
            if self.master.state == state.ON_MOVE:
                self.item_margin_x = self.item_position_x * SPRITE_SCALE
                self.item_margin_y = (self.item_position_y - 1) * SPRITE_SCALE
            elif self.master.state == state.DELAY:
                self.item_margin_x = self.item_position_x * SPRITE_SCALE
                self.item_margin_y = self.item_position_y * SPRITE_SCALE

            if self.master.state == state.ATTACK and Tag.weapon in self.tag:
                self.item_margin_x = (self.item_position_x + 3) * SPRITE_SCALE
                self.angle += 60
            else:
                self.angle = 0
        except:
            pass




