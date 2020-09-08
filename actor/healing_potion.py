from actor.actor import Actor
from constants import *
from data import *


class HealingPotion(Actor):
    def __init__(self, x=0, y=0):
        super().__init__(
            x=x,
            y=y,
            name="healing_potion",
            not_visible_color=COLORS["black"],

        )
        self.category = {ItemType.used}

        self.level = 1

    def use(self, game_engine):
        game_engine.player.fighter.hp += 5
        if game_engine.player.fighter.hp > game_engine.player.fighter.max_hp:
            game_engine.player.fighter.hp = game_engine.player.fighter.max_hp
        game_engine.player.inventory.remove_item(self)

        return [{"message": f"You used the {self.name}"}]
