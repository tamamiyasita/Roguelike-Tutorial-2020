import arcade
import random
import pyglet.gl as gl
import tcod
from collections import deque

from constants import *
from data import *
from util import map_position, pixel_position
from actor import Actor
from dungeon_select import dungeon_select
from map_sprite_set import MapSpriteSet
from fov_functions import initialize_fov, recompute_fov, fov_get
from viewport import viewport
from status_bar import draw_status_bar
from fighter import Fighter
from ai import Basicmonster

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
        self.action_queue = []
        self.messages = deque(maxlen=3)
        self.mouse_over_text = None
        self.mouse_position = None

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.actor_list = ACTOR_LIST
        self.map_list = MAP_LIST
        self.game_map = BasicDungeon(MAP_WIDTH, MAP_HEIGHT)

        self.fov_recompute = True
        fighter_component = Fighter(hp=30, defense=2, power=5)
        fighter_component2 = Fighter(hp=3, defense=2, power=5)
        ai_component = Basicmonster()
        self.player = Actor(image["player"], "player", self.game_map.player_pos[0], self.game_map.player_pos[1],
                            blocks=False,
                            fighter=fighter_component,
                            sub_img=image.get("player_move"), map_tile=self.game_map)
        self.player.state = state.READY

        self.crab = Actor(image["crab"], "crab", self.player.x+2, self.player.y,
                          blocks=True, fighter=fighter_component2, ai=ai_component,
                          scale=SPRITE_SCALE*0.5, sub_img=True, map_tile=self.game_map)

        self.actor_list.append(self.player)
        self.actor_list.append(self.crab)

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
        viewport(self.player)

        """fov"""
        if self.player.stop_move and self.fov_recompute:
            recompute_fov(self.fov_map, self.player.x, self.player.y,
                          FOV_RADIUS, FOV_LIGHT_WALL, FOV_ALGO)
            fov_get(self.game_map, self.fov_map)
            self.fov_recompute = False
        ##########
        if self.player.state == state.MOVE_END:
            self.player.state = state.DELAY
            print("enemy_turn")
            self.move_enemies()

        new_action_queue = []
        for action in self.action_queue:
            if "player_turn" in action:
                print("player_turn")

            if "message" in action:
                print("Message")
                self.messages.append(action["message"])

            if "dead" in action:
                print("Death")
                target = action["dead"]
                target.color = arcade.color.GRAY_BLUE
                target.is_dead = True
                if target is self.player:
                    new_action_queue.extend([{"message": "player has died!"}])
                else:
                    new_action_queue.extend(
                        [{"message": f"{target.name} has been killed!"}])
                    new_action_queue.extend(
                        [{"delay": {"time": DEATH_DELAY, "action": {"remove": target}}}])
            if "remove" in action:
                target = action["remove"]
                target.remove_from_sprite_lists()

            if "delay" in action:
                target = action["delay"]
                target["time"] -= delta_time
                if target["time"] > 0:
                    new_action_queue.extend([{"delay": target}])
                else:
                    new_action_queue.extend([target["action"]])

        self.action_queue = new_action_queue

        if self.player.is_dead:
            return
        if self.player.state == state.READY and self.dist:
            attack = self.player.move(self.dist)
            if attack:
                self.action_queue.extend(attack)

            self.fov_recompute = True
            self.action_queue.append({"player_turn": True})

    def on_draw(self):
        arcade.start_render()

        self.map_list.draw(filter=gl.GL_NEAREST)
        self.actor_list.draw(filter=gl.GL_NEAREST)

        size = 65
        margin = 10
        gx = arcade.get_viewport()[0]
        gy = arcade.get_viewport()[2]

        arcade.draw_xywh_rectangle_filled(
            gx, gy, SCREEN_WIDTH, STATES_PANEL_HEIGHT, COLORS["status_panel_background"])

        text = f"HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}"
        arcade.draw_text(
            text, margin+gx, STATES_PANEL_HEIGHT-30+gy, color=COLORS["status_panel_text"], font_size=14)
        draw_status_bar(size / 2 + margin+gx, STATES_PANEL_HEIGHT-8+gy, size, 10,
                        self.player.fighter.hp, self.player.fighter.max_hp)

        y = STATES_PANEL_HEIGHT-14
        for message in self.messages:
            arcade.draw_text(
                message, 200+gx, y+gy, color=COLORS["status_panel_text"])
            y -= 20

        if self.mouse_over_text:
            x, y = self.mouse_position
            arcade.draw_xywh_rectangle_filled(
                x, y, 100, 16, arcade.color.BLACK)
            arcade.draw_text(self.mouse_over_text, x, y, arcade.color.WHITE)

    def move_enemies(self):
        for actor in ACTOR_LIST:
            if actor.ai:
                results = actor.ai.take_turn(
                    target=self.player, game_map=self.game_map, sprite_lists=[MAP_LIST])
        self.action_queue.extend(results)
        self.player.state = state.READY

    def on_key_press(self, key, modifiers):
        print(arcade.get_viewport())
        if key == arcade.key.ESCAPE:
            arcade.close_window()

        elif self.player.state == state.MOVE_END:
            self.dist = self.dist

        elif self.player.state == state.READY:
            if key in KEYMAP_UP:
                dist = (0, 1)
            elif key in KEYMAP_DOWN:
                dist = (0, -1)
            elif key in KEYMAP_LEFT:
                dist = (-1, 0)
            elif key in KEYMAP_RIGHT:
                dist = (1, 0)
            elif key in KEYMAP_UP_LEFT:
                dist = (-1, 1)
            elif key in KEYMAP_DOWN_LEFT:
                dist = (-1, -1)
            elif key in KEYMAP_UP_RIGHT:
                dist = (1, 1)
            elif key in KEYMAP_DOWN_RIGHT:
                dist = (1, -1)

            if self.player.stop_move:
                self.dist = dist

    def on_key_release(self, key, modifiers):
        self.dist = None

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_position = x, y
        actor_list = arcade.get_sprites_at_point((x, y), self.actor_list)
        self.mouse_over_text = None
        for actor in actor_list:
            if actor.fighter and actor.is_visible:
                self.mouse_over_text = f"{actor.name} {actor.fighter.hp}/{actor.fighter.max_hp}"


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    # window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
