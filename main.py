import arcade
import random
import pyglet.gl as gl
import tcod
from itertools import chain

from constants import *
from data import *
from util import map_position, pixel_position
from actor import Actor
from dungeon_select import dungeon_select
from map_sprite_set import MapSpriteSet
from fov_functions import initialize_fov, recompute_fov, fov_get
from viewport import viewport
from fighter import Fighter
from ai import Basicmonster
from tick_sys import Ticker

from basic_dungeon import BasicDungeon
from caves_dungeon import CavesDungeon
from dmap_dungeon import DmapDungeon


class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, antialiasing=False)
        self.player = None
        self.crab = None
        self.actor_list = None
        self.game_map = None
        self.dist = None

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.game_state = State.PLAYER
        self.ticker = Ticker()
        self.actor_list = ACTOR_LIST
        self.map_list = MAP_LIST
        self.game_map = BasicDungeon(MAP_WIDTH, MAP_HEIGHT, ticker=self.ticker)

        self.fov_recompute = True
        fighter_component = Fighter(hp=30, defense=2, power=5)
        ai_component = Basicmonster()
        self.player = Actor(image["player"], "player", self.game_map.player_pos[0], self.game_map.player_pos[1],
                            blocks=True, speed=5, ticker=self.ticker, my_state=State.PLAYER,
                            fighter=fighter_component,
                            sub_img=image.get("player_move"), map_tile=self.game_map)

        self.crab = Actor(image["crab"], "crab", self.player.x+2, self.player.y,
                          blocks=True, speed=15, ticker=self.ticker, my_state=State.NPC, fighter=fighter_component, ai=ai_component,
                          scale=0.5, sub_img=True, map_tile=self.game_map)

        self.actor_list.append(self.crab)
        self.actor_list.append(self.player)

        # self.game_map = DmapDungeon(MAP_WIDTH, MAP_HEIGHT)
        # self.game_map = CavesDungeon(MAP_WIDTH, MAP_HEIGHT)
        # self.game_map = dungeon_select(MAP_WIDTH, MAP_HEIGHT)
        self.fov_map = initialize_fov(self.game_map)
        self.mapsprite = MapSpriteSet(
            MAP_WIDTH, MAP_HEIGHT, self.game_map.tiles, floors.get(0), wall_3)
        self.mapsprite.sprite_set()

    def on_update(self, delta_time):
        self.actor_list.update_animation()
        self.actor_list.update()

        """fov"""
        if self.player.stop_move and self.fov_recompute:
            recompute_fov(self.fov_map, self.player.x, self.player.y,
                          FOV_RADIUS, FOV_LIGHT_WALL, FOV_ALGO)
            fov_get(self.game_map, self.fov_map)
            self.fov_recompute = False
        ##########

    def on_draw(self):
        arcade.start_render()

        self.map_list.draw(filter=gl.GL_NEAREST)
        self.actor_list.draw(filter=gl.GL_NEAREST)

    def move_enemies(self):
        for actor in ACTOR_LIST:
            if actor.ai:
                actor.ai.take_turn(
                    target=self.player, game_map=self.game_map, sprite_lists=ENTITY_LIST)
        self.game_state = State.PLAYER

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

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
            self.fov_recompute = True
            self.game_state = State.NPC

        if self.game_state == State.NPC:
            self.move_enemies()

        # if self.game_state == State.PLAYER and self.dist and self.player.stop_move:

    def on_key_release(self, key, modifiers):
        self.dist = None


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    # window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
