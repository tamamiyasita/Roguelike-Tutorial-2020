from os import write
import arcade
import json
import pyglet.gl as gl

from game_engine import GameEngine
from constants import *
from status_bar import draw_status_bar
from util import grid_to_pixel, pixel_to_grid


class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, antialiasing=False)

        self.engine = GameEngine()
        self.dist = None
        self.mouse_over_text = None
        self.mouse_position = None

    def setup(self):
        self.engine.setup()
        self.engine.fov()

    def on_update(self, delta_time):
        self.engine.chara_sprites.update_animation()
        self.engine.chara_sprites.update()
        self.engine.actor_sprites.update_animation()
        self.engine.actor_sprites.update()
        self.engine.item_sprites.update()

        self.engine.process_action_queue(delta_time)
        self.engine.turn_change(delta_time)
        self.engine.view()

        if self.engine.player.state == state.READY and self.dist:
            attack = self.engine.player.move(
                self.dist, None, self.engine.actor_sprites, self.engine.game_map)
            if attack:
                self.engine.action_queue.extend(attack)

    def on_draw(self):
        try:
            arcade.start_render()

            self.engine.map_sprites.draw(filter=gl.GL_NEAREST)
            self.engine.actor_sprites.draw(filter=gl.GL_NEAREST)
            self.engine.item_sprites.draw(filter=gl.GL_NEAREST)
            self.engine.chara_sprites.draw(filter=gl.GL_NEAREST)

            size = 72
            margin = 15
            self.vx = arcade.get_viewport()[0]
            self.vy = arcade.get_viewport()[2]

            # ステータスパネルサイズ
            arcade.draw_xywh_rectangle_filled(
                self.vx, self.vy, SCREEN_WIDTH, STATES_PANEL_HEIGHT, COLORS["status_panel_background"])

            if self.engine.game_state == GAME_STATE.NORMAL:

                # HP表示
                text = f"HP: {self.engine.player.fighter.hp}/{self.engine.player.fighter.max_hp}"
                arcade.draw_text(
                    text, margin + self.vx, STATES_PANEL_HEIGHT - 30 + self.vy, color=COLORS["status_panel_text"], font_size=14)

                # HPバー
                draw_status_bar(size / 2 + margin+self.vx, STATES_PANEL_HEIGHT-8+self.vy, size, 10,
                                self.engine.player.fighter.hp, self.engine.player.fighter.max_hp)

                # 所持アイテム表示
                capacity = self.engine.player.inventory.capacity
                selected_item = self.engine.selected_item
                field_width = SCREEN_WIDTH / (capacity + 1) / 1.5
                for i in range(capacity):
                    y = 38
                    x = i * field_width + 400
                    if i == selected_item:
                        arcade.draw_lrtb_rectangle_outline(
                            x+self.vx - 3, x+self.vx + field_width - 5, y+self.vy + 18, y+self.vy - 4, arcade.color.BLACK, 2)
                    if self.engine.player.inventory.bag[i]:
                        item_name = self.engine.player.inventory.bag[i].name
                    else:
                        item_name = ""
                    text = f"{i+1}: {item_name}"
                    arcade.draw_text(text, x+self.vx, y+self.vy,
                                     color=COLORS["status_panel_text"])

                # メッセージ表示
                y = STATES_PANEL_HEIGHT-14
                for message in self.engine.messages:
                    arcade.draw_text(
                        message, 130+self.vx, y+self.vy, color=COLORS["status_panel_text"])
                    y -= 20

                # マウスオーバーテキスト
                if self.mouse_over_text:
                    x, y = self.mouse_position
                    arcade.draw_xywh_rectangle_filled(
                        x, y, 100, 16, arcade.color.BLACK)
                    arcade.draw_text(self.mouse_over_text, x,
                                     y, arcade.color.WHITE)

            elif self.engine.game_state == GAME_STATE.SELECT_LOCATION:
                mouse_x, mouse_y = self.mouse_position
                grid_x, grid_y = pixel_to_grid(mouse_x, mouse_y)
                center_x, center_y = grid_to_pixel(grid_x, grid_y)
                # print(mouse_x, mouse_y, "MOUSE")
                # print(grid_x, grid_y, "GRID")
                # print(center_x, center_y, "RECT")
                arcade.draw_rectangle_outline(
                    center_x, center_y, SPRITE_SIZE*SPRITE_SCALE, SPRITE_SIZE*SPRITE_SCALE, arcade.color.LIGHT_BLUE, 2)

        except Exception as e:
            print(e)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            arcade.close_window()
        elif key == arcade.key.ESCAPE:
            self.engine.game_state = GAME_STATE.NORMAL

        elif self.engine.player.state == state.READY and self.engine.game_state == GAME_STATE.NORMAL:
            dist = None
            if key in KEYMAP_UP:
                print(self.engine.player.name, "PLAYER")
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
            elif key in KEYMAP_REST:
                self.engine.player.state = state.TURN_END

            elif key in KEYMAP_PICKUP:
                self.engine.action_queue.extend([{"pickup": True}])
            elif key in KEYMAP_SELECT_ITEM_1:
                self.engine.action_queue.extend([{"select_item": 1}])
            elif key in KEYMAP_SELECT_ITEM_2:
                self.engine.action_queue.extend([{"select_item": 2}])
            elif key in KEYMAP_SELECT_ITEM_3:
                self.engine.action_queue.extend([{"select_item": 3}])
            elif key in KEYMAP_SELECT_ITEM_4:
                self.engine.action_queue.extend([{"select_item": 4}])
            elif key in KEYMAP_SELECT_ITEM_5:
                self.engine.action_queue.extend([{"select_item": 5}])
            elif key in KEYMAP_SELECT_ITEM_6:
                self.engine.action_queue.extend([{"select_item": 6}])
            elif key in KEYMAP_SELECT_ITEM_7:
                self.engine.action_queue.extend([{"select_item": 7}])
            elif key in KEYMAP_SELECT_ITEM_8:
                self.engine.action_queue.extend([{"select_item": 8}])
            elif key in KEYMAP_SELECT_ITEM_9:
                self.engine.action_queue.extend([{"select_item": 9}])
            elif key in KEYMAP_SELECT_ITEM_0:
                self.engine.action_queue.extend([{"select_item": 0}])
            elif key in KEYMAP_USE_ITEM:
                self.engine.action_queue.extend([{"use_item": True}])
            elif key in KEYMAP_DROP_ITEM:
                self.engine.action_queue.extend([{"drop_item": True}])

            elif key == arcade.key.P:
                self.save()
            elif key == arcade.key.L:
                self.load()

            elif key == arcade.key.SPACE:
                self.engine.game_state = GAME_STATE.SELECT_LOCATION

            self.dist = dist
            self.engine.fov_recompute = True

            # self.engine.action_queue.append({"player_turn": True})

    def on_key_release(self, key, modifiers):
        self.dist = None

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_position = x + self.vx, y + self.vy
        print(self.mouse_position, "POS")
        print(pixel_to_grid(self.mouse_position[0], self.mouse_position[1]))
        # 忘れずにビューポートの座標を足す
        actor_list = arcade.get_sprites_at_point(
            self.mouse_position, self.engine.actor_sprites)
        self.mouse_over_text = None
        for actor in actor_list:
            if actor.fighter or actor.item and actor.is_visible:
                self.mouse_over_text = f"{actor.name} {actor.fighter.hp}/{actor.fighter.max_hp}"
                print(actor.name)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.engine.game_state == GAME_STATE.SELECT_LOCATION:
            grid_x, grid_y = pixel_to_grid(x + self.vx, y + self.vy)
            print(grid_x, grid_y, "mouse_press")
            self.engine.grid_click(grid_x, grid_y)
        self.engine.game_state = GAME_STATE.NORMAL

    def save(self):
        print("save")
        game_dict = self.engine.get_dict()
        # print(game_dict)

        with open("game_same3.json", "w") as write_file:
            json.dump(game_dict, write_file)
        print("**save**")

    def load(self):
        print("load")
        with open("game_same3.json", "r") as read_file:
            data = json.load(read_file)

        print(data)
        print("**load**")
        self.engine.restore_from_dict(data)
        self.engine.player.state = state.READY


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    # window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
