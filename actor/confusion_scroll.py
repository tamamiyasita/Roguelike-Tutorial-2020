
import arcade
from actor.ai import ConfusedMonster
from data import *
from constants import *
from actor.item import Item
from actor.actor import Actor
from util import get_blocking_entity, grid_to_pixel, pixel_to_grid


class ConfusionEfc(Actor):
    def __init__(self, x, y, sprite):
        super().__init__(x=x, y=y, texture=effect1[140])

        self.sprite = sprite
        self.com_ai = self.sprite.ai
        self.count = self.sprite.ai.number_of_turns
        self.time_num = 1

        EFFECT_LIST.append(self)

    def update(self, delta_time=1/60):
        super().update(delta_time)
        self.center_x, self.center_y = self.sprite.center_x, self.sprite.center_y
        self.time_num -= delta_time
        if self.time_num < 0:
            self.angle += 90
            self.time_num = 1

        if self.sprite.ai.number_of_turns == 0 or not self.sprite in ACTOR_LIST:
            EFFECT_LIST.remove(self)


class ConfusionScroll(Actor):
    def __init__(self, x: int, y: int):
        super().__init__(x=x, y=y, texture=scroll[15], name="Confuse Scroll", color=COLORS["transparent"],
                         visible_color=arcade.color.WHITE,
                         not_visible_color=COLORS.get("dark_ground"), item=Item())
        self.alpha = 0
        ITEM_LIST.append(self)

    def use(self, game_engine: "GameEngine"):
        print("use")
        self.game_engine = game_engine
        game_engine.game_state = GAME_STATE.SELECT_LOCATION
        game_engine.grid_select_handlers.append(self.click)
        return None

    def confused(self, grid_x, grid_y, results):
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        sprites = arcade.get_sprites_at_point((pixel_x, pixel_y), ACTOR_LIST)
        for sprite in sprites:
            if sprite.fighter and not sprite.is_dead:
                self.sprite = sprite
                confused_ai = ConfusedMonster(sprite.ai, 3001)
                confused_ai.owner = sprite
                sprite.ai = confused_ai

                results.extend(
                    [{"message": f"The eyes of the {sprite.name} look vacant, as he starts to stumble around! "}])

                break
        else:
            results.append(
                {"message": "There is no targetable enemy at that location."})

    def click(self, x, y):
        results = []
        self.confused(x, y, results)
        ConfusionEfc(x, y, self.sprite)
        self.game_engine.player.inventory.remove_item(self)

        return results
