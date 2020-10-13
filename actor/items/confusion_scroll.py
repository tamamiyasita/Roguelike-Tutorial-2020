
import arcade
from actor.ai import ConfusedMonster
from data import *
from constants import *
from actor.actor import Actor
from util import get_blocking_entity, grid_to_pixel, pixel_to_grid


class ConfusionEffect(Actor):
    def __init__(self, x=0, y=0, enemy=None, effect_sprites=None, actor_sprites=None):
        super().__init__(
            x=x,
            y=y,
            color=COLORS["white"],
            not_visible_color=COLORS["black"],
            name="confusion_effect"),

        self.enemy = enemy
        self.effect_sprites = effect_sprites
        self.actor_sprites = actor_sprites

        self.count = self.enemy.ai.confused_turn
        self.time_num = 2

        self.effect_sprites.append(self)

    def update(self, delta_time=1/60):
        super().update(delta_time)
        self.center_x, self.center_y = self.enemy.center_x, self.enemy.center_y
        self.time_num -= 1
        if self.time_num < 0:
            self.angle += 1
            self.time_num = 2

        if self.enemy.ai.confused_turn == 0 or not self.enemy in self.actor_sprites:
            self.effect_sprites.remove(self)


class ConfusionScroll(Actor):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(
            x=x,
            y=y,
            name="confusion_scroll",
            not_visible_color=COLORS["black"],

        )
        self.tag = [Tag.item, Tag.used]

        self.level = 2

    def use(self, game_engine):
        print("use")
        self.game_engine = game_engine
        self.game_engine.game_state = GAME_STATE.SELECT_LOCATION
        self.game_engine.grid_select_handlers.append(self.click)
        return None

    def confused(self, grid_x, grid_y, results):
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        sprites = arcade.get_sprites_at_point(
            (pixel_x, pixel_y), self.game_engine.cur_level.actor_sprites)
        for sprite in sprites:
            if sprite.fighter and not sprite.is_dead:
                self.enemy = sprite
                confused_ai = ConfusedMonster(self.enemy.ai)
                confused_ai.owner = self.enemy
                self.enemy.ai = confused_ai

                results.extend(
                    [{"message": f"The eyes of the {self.enemy.name} look vacant, as he starts to stumble around! "}])

                break
        else:
            results.append(
                {"message": "There is no targetable enemy at that location."})

    def click(self, x, y):
        results = []
        self.confused(x, y, results)
        ConfusionEffect(
            x, y, self.enemy, self.game_engine.cur_level.effect_sprites, self.game_engine.cur_level.actor_sprites)
        self.game_engine.player.inventory.remove_item(self)

        return results
