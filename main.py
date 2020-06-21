import arcade
import random
import pyglet.gl as gl

from constants import *
from data import *
from util import map_position
from actor import Actor
from dungeon_select import dungeon_select
from map_sprite_set import MapSpriteSet

from basic_dungeon import BasicDungeon


class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, antialiasing=False)
        self.player = None
        self.crab = None
        self.actor_list = None
        self.game_map = None
        self.dist = None

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.actor_list = ACTOR_LIST
        self.map_list = MAP_LIST

        self.game_map = dungeon_select(MAP_WIDTH, MAP_HEIGHT)
        # self.game_map = BasicDungeon(MAP_WIDTH, MAP_HEIGHT)
        MapSpriteSet(MAP_WIDTH, MAP_HEIGHT, self.game_map.tiles)

        self.player = Actor(image["player"], self.game_map.player_pos[0], self.game_map.player_pos[1],
                            left_img=True, map_tile=self.game_map)
        self.crab = Actor(image["crab"], self.player.x+1, self.player.y,
                          scale=0.5, left_img=True, map_tile=self.game_map)

        self.actor_list.append(self.crab)
        self.actor_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.map_list.draw(filter=gl.GL_NEAREST)
        self.actor_list.draw(filter=gl.GL_NEAREST)

    def on_update(self, delta_time):
        self.actor_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

        if self.player.stop_move:

            if key == arcade.key.UP:
                self.dist = (0, 1)
            elif key == arcade.key.DOWN:
                self.dist = (0, -1)
            elif key == arcade.key.LEFT:
                self.dist = (-1, 0)
            elif key == arcade.key.RIGHT:
                self.dist = (1, 0)
            elif key == arcade.key.HOME:
                self.dist = (-1, 1)
            elif key == arcade.key.END:
                self.dist = (-1, -1)
            elif key == arcade.key.PAGEUP:
                self.dist = (1, 1)
            elif key == arcade.key.PAGEDOWN:
                self.dist = (1, -1)
            if self.dist:
                self.player.move(self.dist)
                cdist = (random.choice([1, 0, -1]), random.choice([1, 0, -1]))
                if self.crab.stop_move and cdist[0] or cdist[1]:
                    self.crab.move(cdist)


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
