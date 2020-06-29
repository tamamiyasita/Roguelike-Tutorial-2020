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
from fov_functions import initialize_fov, recompute_fov
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
        self.game_state = self.player.state

        if QUEUE:
            print(QUEUE, "QQQ")
        if self.game_state == State.TICK:
            self.ticker.ticks += 1
            self.ticker.next_turn()

            for actor in self.actor_list:
                if actor.state == State.PLAYER:
                    self.game_state = State.PLAYER
                if actor.state == State.NPC:
                    self.game_state = State.NPC

        self.queue_process()

        if self.game_state == State.PLAYER and not self.player.stop_move:
            viewport(self.player)

        if self.player.stop_move and self.fov_recompute:
            recompute_fov(self.fov_map, self.player.x, self.player.y,
                          FOV_RADIUS, FOV_LIGHT_WALL, FOV_ALGO)

            for y in range(self.game_map.height):
                for x in range(self.game_map.width):
                    visible = tcod.map_is_in_fov(self.fov_map, x, y)
                    if not visible:
                        point = pixel_position(x, y)
                        sprite_point = arcade.get_sprites_at_exact_point(
                            point, self.map_list)
                        for sprite in sprite_point:
                            sprite.is_visible = False

                    elif visible:
                        point = pixel_position(x, y)
                        sprite_point = arcade.get_sprites_at_exact_point(
                            point, self.map_list)
                        for sprite in sprite_point:
                            sprite.is_visible = True
                            sprite.alpha = 255
                    for sprite in self.actor_list:
                        if not tcod.map_is_in_fov(self.fov_map, sprite.x, sprite.y):
                            sprite.alpha = 0
                        else:
                            sprite.alpha = 255

            for sprite in chain(self.map_list, self.actor_list):
                if sprite.is_visible:
                    sprite.color = sprite.visible_color

                else:
                    sprite.color = sprite.not_visible_color

            self.fov_recompute = False
        if self.game_state == State.NPC:
            results = [{"NPC_turn": True}]
            QUEUE.extend(results)
        if self.game_state == State.PLAYER and self.dist:
            results = [{"player_go": self.player}]
            QUEUE.extend(results)
            self.fov_recompute = True

    def on_draw(self):
        arcade.start_render()

        self.map_list.draw(filter=gl.GL_NEAREST)
        self.actor_list.draw(filter=gl.GL_NEAREST)

    def queue_process(self):
        global QUEUE
        new_queue = []
        for action in QUEUE:
            print(action, " Action")
            if "NPC_turn" in action:
                self.move_enemies()
            if "player_go" in action:
                action.get("player_go").move(self.dist)

        QUEUE = new_queue

    def move_enemies(self):
        for actor in ACTOR_LIST:
            if actor.ai:
                actor.ai.take_turn(
                    target=self.player, game_map=self.game_map, sprite_lists=ENTITY_LIST)

    def on_key_press(self, key, modifiers):
        # if self.game_state == State.PLAYER:
        if key == arcade.key.ESCAPE:
            arcade.close_window()

        # if self.player.stop_move:

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
            # if self.dist:
            #     results = [{"player_go": self.player}]
            #     QUEUE.extend(results)
            #     self.fov_recompute = True
            # self.player.move(self.dist)
            # if self.game_state == PLAYER_TURN:
            #     self.game_state = ENEMY_TURN
            # if self.game_state == ENEMY_TURN:
            #     self.move_enemies()
            #     self.game_state = PLAYER_TURN
            # if self.state == State.NPC:
            #     results = [{"NPC_turn": True}]
            #     QUEUE.extend(results)

    def on_key_release(self, key, modifiers):
        self.dist = None


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
