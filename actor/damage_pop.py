from constants import UI_FONT
import arcade
from actor.actor import Actor
from random import randint


class Damagepop(Actor):
    def __init__(self, engine, text, color, target, y,  size=13):
        super().__init__(
            # color=arcade.color.WHITE
        )
        if isinstance(text, str):
            size = 11
        self.engine = engine
        self.target = target
        self.center_x = target.center_x+randint(-5,5)
        self.center_y = target.center_y
        self.tmp_center_y = target.center_y + y
        self.color = color
        self.text = arcade.draw_text(
            str(text), self.center_x, self.center_y, color, font_size=size+randint(0,1))
        self.effect_sprites = engine.tmp_effect_sprites
        self.d_time = 75

        self.alpha = 20
        self.change_y = 5

        self.texture = self.text.texture
        self.effect_sprites.append(self)
        # self.engine.damage_pop.append(self)

    def update_animation(self, delta_time):
        if self in self.engine.tmp_effect_sprites: 
            self.d_time -= 1
            if self.d_time < 50 and 20 < self.alpha:
                self.alpha -= 20
            if 255 > self.alpha:
                self.alpha += 7
            if self.d_time < 0:
                self.engine.tmp_effect_sprites.remove(self)

            # 規定位置に到達したら動きを止めて255にアルファ値を固定
            if self.center_y > self.tmp_center_y and self.change_y:
                self.alpha = 255
                self.change_y = 0

