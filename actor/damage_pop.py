import arcade
from actor.actor import Actor


# def damage_pop(x, y, damage, delta_time):
#     return arcade.draw_text(
#         str(damage), x, y, color=arcade.color.AMARANTH_PURPLE)
# update(txt, delta_time)


# def update(txt, delta_time):
#     txt.start_x += delta_time

class Damagepop(Actor):
    def __init__(self, engine, target):
        super().__init__(
            color=arcade.color.WHITE
            # x=target.center_x,
            # y=target.center_y,
        )
        self.engine = engine
        self.target = target
        # self.damage = str(damage)
        self.center_x = target.center_x
        self.center_y = target.center_y
        self.color = arcade.color.YELLOW_ORANGE
        self.effect_sprites = engine.cur_level.effect_sprites
        # self.font_size = 30
        self.d_time = 30

        # self.text = arcade.draw_text(
        #     self.damage, self.x, self.y, self.font_color, self.font_size, anchor_x="center")
        self.alpha = 0
        self.change_y = 2.5

    def set(self, t):
        self.texture = t
        self.effect_sprites.append(self)

    def start(self):
        self.d_time -= 1
        if self.d_time < -5:
            self.engine.cur_level.effect_sprites.remove(self)
            self.engine.damage_pop.remove(self)
        elif self.alpha < 240:
            self.alpha += 20
        elif self.alpha >= 250:
            self.alpha = 255
        elif self.d_time <= 8:
            self.change_y = 0
