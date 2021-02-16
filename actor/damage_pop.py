from constants import *
import arcade
from actor.actor import Actor
from random import randint


class Damagepop(Actor):
    def __init__(self, engine, text, color, target, y,  size=13):
        super().__init__(
            # color=arcade.color.WHITE
        )
        self.is_int = True
        if isinstance(text, str):
            size = 11
            self.is_int = False
        self.engine = engine
        self.target = target
        self.center_x = target.center_x+randint(-5,5)
        self.center_y = target.center_y
        self.tmp_center_y = target.center_y + y
        self.color = color
        self.text = arcade.draw_text(
            str(text), self.center_x, self.center_y, color, font_size=size+randint(0,1))
        self.d_time = 75

        self.alpha = 20
        self.change_y = 5

        self.texture = self.text.texture
        TMP_EFFECT_SPRITES.append(self)
        # self.engine.damage_pop.append(self)

    def update_animation(self, delta_time):
        if self in TMP_EFFECT_SPRITES: 
            self.d_time -= 1

            if self.d_time > 66 and self.is_int:
                if self.d_time % 2 == 0:
                    self.target.alpha = 20
                if self.d_time % 2 != 0:
                    self.target.alpha = 150
            else:
                self.target.alpha = 255

            if self.d_time < 50 and 20 < self.alpha:
                self.alpha -= 20
            if 255 > self.alpha:
                self.alpha += 7
            if self.d_time < 0:
                self.remove_from_sprite_lists()

            # 規定位置に到達したら動きを止めて255にアルファ値を固定
            if self.center_y > self.tmp_center_y and self.change_y:
                self.alpha = 255
                self.change_y = 0

