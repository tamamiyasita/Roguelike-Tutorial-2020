
import arcade
from constants import COLORS

class MinimapPoints:

    def __init__(self, engine):
        self.engine = engine
        self.map_sprites = engine.cur_level.map_sprites
        self.item_sprites = engine.cur_level.item_sprites

        self.map_point_list = arcade.SpriteList(spatial_hash_cell_size=32, use_spatial_hash=True)
        self.item_point_list = arcade.SpriteList(spatial_hash_cell_size=32, use_spatial_hash=True)

        for map_sprite in self.map_sprites:
            if "floor" in map_sprite.name:
                self.map_point = arcade.SpriteSolidColor(width=32, height=32, color=arcade.color.YELLOW_ORANGE)
                self.map_point.center_x = map_sprite.center_x
                self.map_point.center_y = map_sprite.center_y
                self.map_point_list.append(self.map_point)

        for item_sprite in self.item_sprites:
            self.item_point = arcade.SpriteSolidColor(width=32, height=32, color=arcade.color.GREEN)
            self.item_point.center_x = item_sprite.center_x
            self.item_point.center_y = item_sprite.center_y
            self.item_point_list.append(self.item_point)

    def update(self):
        pass
        # TODO is_visible





    def draw(self):
        arcade.draw_rectangle_filled(center_x=self.engine.player.center_x, center_y=self.engine.player.center_y, width=32, height=32, color=arcade.color.WHITE)
        for i in self.map_sprites:
            if i.color == i.visible_color:
                arcade.draw_rectangle_filled(center_x=i.center_x, center_y=i.center_y, width=32, height=32, color=arcade.color.ORANGE_RED)
        # self.map_point_list.draw()
        # self.item_point_list.draw()



