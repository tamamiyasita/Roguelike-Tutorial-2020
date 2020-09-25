from constants import *
from data import *
from actor.actor import Actor
from util import grid_to_pixel


class FireballEffect(Actor):
    def __init__(self, x=0, y=0, effect_sprites=None):
        super().__init__(
            x=x,
            y=y,
            name="fireball_effect",
            color=COLORS["white"]
        )
        self.effect_sprites = effect_sprites
        self.alpha = 155
        self.effect_sprites.append(self)
        self.scale = 0.1

    def update(self):
        self.alpha -= 1
        if self.alpha > 100:
            self.scale += 0.3*SPRITE_SCALE
            self.angle += 14
        if self.alpha < 120:
            self.effect_sprites.remove(self)


class FireballScroll(Actor):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(
            x=x,
            y=y,
            name="fireball_scroll",
            not_visible_color=COLORS["black"],

        )
        self.tag = {Tag.item, Tag.used}

        self.level = 2

    def use(self, game_engine):
        print("use")
        self.game_engine = game_engine
        game_engine.game_state = GAME_STATE.SELECT_LOCATION
        game_engine.grid_select_handlers.append(self.click)
        # TODO ターンエンドさせたい
        return None

    def apply_damage(self, grid_x, grid_y, amount, results):
        pixel_x, pixel_y = grid_to_pixel(grid_x, grid_y)
        print(f"{pixel_x}{pixel_y} apply pixel_x_y")
        sprites = arcade.get_sprites_at_point(
            (pixel_x, pixel_y), self.game_engine.cur_level.actor_sprites)
        pc_check = arcade.get_sprites_at_point(
            (pixel_x, pixel_y), self.game_engine.cur_level.chara_sprites)
        sprites.extend(pc_check)
        for sprite in sprites:
            if sprite.fighter and not sprite.is_dead:
                results.extend(
                    [{"message": f"{sprite.name} was struck by a fireball for {amount} points."}])
                result = sprite.fighter.take_damage(amount)
                if result:
                    results.extend(result)

    def click(self, x, y):
        print("Click!", x, y)
        results = []
        FireballEffect(x, y, self.game_engine.cur_level.effect_sprites)
        self.apply_damage(x, y, 10, results)

        self.apply_damage(x-1, y-1, 8, results)
        self.apply_damage(x, y-1, 8, results)
        self.apply_damage(x+1, y-1, 8, results)

        self.apply_damage(x-1, y, 8, results)
        self.apply_damage(x+1, y, 8, results)

        self.apply_damage(x-1, y+1, 8, results)
        self.apply_damage(x, y+1, 8, results)
        self.apply_damage(x + 1, y + 1, 8, results)

        self.game_engine.player.inventory.remove_item(self)

        print(results, "results")
        return results
