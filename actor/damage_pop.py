import arcade


# def damage_pop(x, y, damage, delta_time):
#     return arcade.draw_text(
#         str(damage), x, y, color=arcade.color.AMARANTH_PURPLE)
# update(txt, delta_time)


# def update(txt, delta_time):
#     txt.start_x += delta_time

class Damagepop():
    def __init__(self, engine, target, damage):
        # super().__init__(
        #     text=str(damage),
        #     start_x=target.center_x,
        #     start_y=target.center_y,
        # )
        self.engine = engine
        self.damage = str(damage)
        self.x = target.center_x
        self.y = target.center_y
        self.font_color = arcade.color.YELLOW_ORANGE
        # self.effect_sprites = engine.cur_level.effect_sprites
        self.font_size = 30
        self.d_time = 40

        self.text = arcade.draw_text(
            self.damage, self.x, self.y, self.font_color, self.font_size, anchor_x="center")
        self.engine.cur_level.effect_sprites.append(self.text)
        self.text.alpha = 100
        self.text.change_y = 1


    def start(self, delta_time):
        self.text.center_y * delta_time
        self.d_time -= 1
        if self.d_time < 1:
            self.engine.cur_level.effect_sprites.remove(self.text)
            self.engine.damage_pop.remove(self)
            # TODO テクスチャのコピーでいけないか
        elif self.text.alpha < 240:
            self.text.alpha += 5
        elif self.text.alpha >= 250:
            self.text.alpha = 255
        elif self.d_time <= 30:
            self.text.change_y = 0

        
     
