import arcade
import pyglet.gl as gl

from game_engine import GameEngine
from constants import *
from status_bar import draw_status_bar
from util import grid_to_pixel, pixel_to_grid


class MG(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, antialiasing=False)

        self.game_engine = GameEngine()
        self.dist = None
        self.mouse_over_text = None
        self.mouse_position = None

    def setup(self):
        self.game_engine.setup()
        self.game_engine.fov()

    def on_update(self, delta_time):
        self.game_engine.actor_list.update_animation()
        self.game_engine.actor_list.update()

        self.game_engine.process_action_queue(delta_time)
        self.game_engine.turn_change()
        self.game_engine.view()
        EFFECT_LIST.update()

    def on_draw(self):
        try:
            arcade.start_render()

            self.game_engine.map_list.draw(filter=gl.GL_NEAREST)
            ITEM_LIST.draw(filter=gl.GL_NEAREST)
            self.game_engine.actor_list.draw(filter=gl.GL_NEAREST)
            EFFECT_LIST.draw()

            size = 72
            margin = 15
            self.vx = arcade.get_viewport()[0]
            self.vy = arcade.get_viewport()[2]

            # ステータスパネルサイズ
            arcade.draw_xywh_rectangle_filled(
                self.vx, self.vy, SCREEN_WIDTH, STATES_PANEL_HEIGHT, COLORS["status_panel_background"])

            if self.game_engine.game_state == GAME_STATE.NORMAL:

                # HP表示
                text = f"HP: {self.game_engine.player.fighter.hp}/{self.game_engine.player.fighter.max_hp}"
                arcade.draw_text(
                    text, margin + self.vx, STATES_PANEL_HEIGHT - 30 + self.vy, color=COLORS["status_panel_text"], font_size=14)

                # HPバー
                draw_status_bar(size / 2 + margin+self.vx, STATES_PANEL_HEIGHT-8+self.vy, size, 10,
                                self.game_engine.player.fighter.hp, self.game_engine.player.fighter.max_hp)

                # 所持アイテム表示
                capacity = self.game_engine.player.inventory.capacity
                selected_item = self.game_engine.selected_item
                field_width = SCREEN_WIDTH / (capacity + 1) / 1.5
                for i in range(capacity):
                    y = 38
                    x = i * field_width + 400
                    if i == selected_item:
                        arcade.draw_lrtb_rectangle_outline(
                            x+self.vx - 3, x+self.vx + field_width - 5, y+self.vy + 18, y+self.vy - 4, arcade.color.BLACK, 2)
                    if self.game_engine.player.inventory.items[i]:
                        item_name = self.game_engine.player.inventory.items[i].name
                    else:
                        item_name = ""
                    text = f"{i+1}: {item_name}"
                    arcade.draw_text(text, x+self.vx, y+self.vy,
                                     color=COLORS["status_panel_text"])

                # メッセージ表示
                y = STATES_PANEL_HEIGHT-14
                for message in self.game_engine.messages:
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

            elif self.game_engine.game_state == GAME_STATE.SELECT_LOCATION:
                mouse_x, mouse_y = self.mouse_position
                grid_x, grid_y = pixel_to_grid(mouse_x, mouse_y)
                center_x, center_y = grid_to_pixel(grid_x, grid_y)
                print(mouse_x, mouse_y, "MOUSE")
                print(grid_x, grid_y, "GRID")
                print(center_x, center_y, "RECT")
                arcade.draw_rectangle_outline(
                    center_x, center_y, SPRITE_SIZE*SPRITE_SCALE, SPRITE_SIZE*SPRITE_SCALE, arcade.color.LIGHT_BLUE, 2)

        except Exception as e:
            print(e)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            arcade.close_window()

        elif self.game_engine.player.state == state.READY:
            dist = None
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
            elif key in KEYMAP_REST:
                self.game_engine.player.state = state.TURN_END

            elif key in KEYMAP_PICKUP:
                self.game_engine.action_queue.extend([{"pickup": True}])
            elif key in KEYMAP_SELECT_ITEM_1:
                self.game_engine.action_queue.extend([{"select_item": 1}])
            elif key in KEYMAP_SELECT_ITEM_2:
                self.game_engine.action_queue.extend([{"select_item": 2}])
            elif key in KEYMAP_SELECT_ITEM_3:
                self.game_engine.action_queue.extend([{"select_item": 3}])
            elif key in KEYMAP_SELECT_ITEM_4:
                self.game_engine.action_queue.extend([{"select_item": 4}])
            elif key in KEYMAP_SELECT_ITEM_5:
                self.game_engine.action_queue.extend([{"select_item": 5}])
            elif key in KEYMAP_SELECT_ITEM_6:
                self.game_engine.action_queue.extend([{"select_item": 6}])
            elif key in KEYMAP_SELECT_ITEM_7:
                self.game_engine.action_queue.extend([{"select_item": 7}])
            elif key in KEYMAP_SELECT_ITEM_8:
                self.game_engine.action_queue.extend([{"select_item": 8}])
            elif key in KEYMAP_SELECT_ITEM_9:
                self.game_engine.action_queue.extend([{"select_item": 9}])
            elif key in KEYMAP_SELECT_ITEM_0:
                self.game_engine.action_queue.extend([{"select_item": 0}])
            elif key in KEYMAP_USE_ITEM:
                self.game_engine.action_queue.extend([{"use_item": True}])
            elif key in KEYMAP_DROP_ITEM:
                self.game_engine.action_queue.extend([{"drop_item": True}])

            elif key == arcade.key.SPACE:
                self.game_engine.game_state = GAME_STATE.SELECT_LOCATION
            elif key == arcade.key.ESCAPE:
                self.game_engine.game_state = GAME_STATE.NORMAL

            self.dist = dist
            if self.game_engine.player.state == state.READY and self.dist:
                attack = self.game_engine.player.move(self.dist)
                if attack:
                    self.game_engine.action_queue.extend(attack)

                # self.game_engine.action_queue.append({"player_turn": True})

    def on_key_release(self, key, modifiers):
        self.dist = None

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_position = x + self.vx, y + self.vy
        print(self.mouse_position, "POS")
        print(pixel_to_grid(self.mouse_position[0], self.mouse_position[1]))
        # 忘れずにビューポートの座標を足す
        actor_list = arcade.get_sprites_at_point(
            self.mouse_position, ENTITY_LIST)
        self.mouse_over_text = None
        for actor in actor_list:
            if actor.fighter or actor.item and actor.is_visible:
                self.mouse_over_text = f"{actor.name} {actor.fighter.hp}/{actor.fighter.max_hp}"
                print(actor.name)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_engine.game_state == GAME_STATE.SELECT_LOCATION:
            grid_x, grid_y = pixel_to_grid(x + self.vx, y + self.vy)
            print(grid_x, grid_y, "mouse_press")
            self.game_engine.grid_click(grid_x, grid_y)
        self.game_engine.game_state = GAME_STATE.NORMAL


def main():
    window = MG(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.setup()
    # window.set_location(20, 200)

    arcade.run()


if __name__ == "__main__":
    main()
