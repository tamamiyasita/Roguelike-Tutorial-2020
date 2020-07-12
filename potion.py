from actor import Actor
from constants import *
from data import *
from item import Item


class Potion(Actor):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, image=potion[0], name="Healing Potion",
                         color=COLORS["transparent"], visible_color=COLORS["light_ground"], not_visible_color=COLORS["dark_ground"],
                         item=Item())
        self.alpha = 0
        ITEM_LIST.append(self)

    def use(self, game_engine):
        game_engine.player.fighter.hp += 5
        if game_engine.player.fighter.hp > game_engine.player.fighter.max_hp:
            game_engine.player.fighter.hp = game_engine.player.fighter.max_hp
        game_engine.player.inventory.remove_item(self)

        return [{"message": f"You used the {self.name}"}]
