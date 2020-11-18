from constants import UI_FONT
import arcade
from actor.actor import Actor


# def damage_pop(x, y, damage, delta_time):
#     return arcade.draw_text(
#         str(damage), x, y, color=arcade.color.AMARANTH_PURPLE)
# update(txt, delta_time)


# def update(txt, delta_time):
#     txt.start_x += delta_time

class Damagepop(Actor):
    def __init__(self, engine, text, color, target, size=16):
        super().__init__(
            # color=arcade.color.WHITE
        )
        self.engine = engine
        self.target = target
        self.center_x = target.center_x
        self.center_y = target.center_y
        self.tmp_center_y = target.center_y + 60
        self.color = color
        self.text = arcade.draw_text(
            str(text), self.center_x, self.center_y, color, font_size=size, font_name=UI_FONT)
        self.effect_sprites = engine.cur_level.effect_sprites
        self.d_time = 60

        self.alpha = 30
        self.change_y = 4.5

        self.texture = self.text.texture
        self.effect_sprites.append(self)
        self.engine.damage_pop.append(self)

    def start(self):
        if self in self.engine.cur_level.effect_sprites:   
            self.d_time -= 1
            if self.d_time < 25 and 20 < self.alpha:
                self.alpha -= 20
            if 255 > self.alpha:
                self.alpha += 7
            if self.d_time < 0:
                self.engine.cur_level.effect_sprites.remove(self)
                self.engine.damage_pop.remove(self)
            if self.center_y > self.tmp_center_y and self.change_y:
                self.alpha = 255
                self.change_y = 0

