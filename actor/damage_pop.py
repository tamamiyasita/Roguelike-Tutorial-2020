import arcade


# def damage_pop(x, y, damage, delta_time):
#     return arcade.draw_text(
#         str(damage), x, y, color=arcade.color.AMARANTH_PURPLE)
# update(txt, delta_time)


# def update(txt, delta_time):
#     txt.start_x += delta_time

class Damagepop(arcade.Text):
    def __init__(self, target, damage, engine):
        super().__init__(
            # str(damage),
            # target.center_x,
            # target.center_y,
            # arcade.color.YELLOW_ORANGE
        )
        self.damage = str(damage)
        self.target = target
        self.x = target.center_x
        self.y = target.center_y
        arcade.color.YELLOW_ORANGE
        self.effect_sprites = engine.cur_level.effect_sprites

        # self.text = arcade.draw_text(
        #     self.damage, self.x, self.y, color=arcade.color.YELLOW_ORANGE, font_size=30)
        self.effect_sprites.append(self)
        self.t = 5
        self.text.change_y = 1

    def update(self, delta_time):
        super().update()
        self.t -= delta_time
        print(self.t)
        self.text.alpha -= 10
        if self.t < 0:
            self.effect_sprites.remove(self)
