import arcade
from constants import *
from util import grid_to_pixel
from itertools import chain


class SelectUI:
    def __init__(self, engine, viewport_x, viewport_y, sprite_list, grid_select, grid_press):
        self.engine = engine
        self.viewport_x = viewport_x
        self.viewport_y = viewport_y
        self.sprites = sprite_list
        self.dx, self.dy = engine.player.x, engine.player.y
        self.grid_select = grid_select
        self.grid_press = grid_press
        self.buttom_panel_width = SCREEN_WIDTH-STATES_PANEL_WIDTH
        self.panel_line_width = 4



    def draw_in_select_ui(self):
        self.panel_ui()
        self.grid_cursor()

    def panel_ui(self):
        # 画面下のパネルをarcadeの四角形を描画する変数で作成
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_x,
            bottom_left_y=self.viewport_y,
            width=self.buttom_panel_width,
            height=STATES_PANEL_HEIGHT,
            color=COLORS["status_panel_background"]
        )

        # 下パネルの周りの線
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.viewport_x+self.panel_line_width*0.5,
            bottom_left_y=self.viewport_y+self.panel_line_width*0.5,
            width=self.buttom_panel_width-self.panel_line_width,
            height=STATES_PANEL_HEIGHT,
            color=arcade.color.ORANGE,
            border_width=self.panel_line_width
        )

        # 画面横のパネル
        arcade.draw_xywh_rectangle_filled(
            bottom_left_x=self.viewport_x + SCREEN_WIDTH - STATES_PANEL_WIDTH,
            bottom_left_y=self.viewport_y,
            width=STATES_PANEL_WIDTH,
            height=SCREEN_HEIGHT,
            color=arcade.color.LIBERTY
        )

        # 横パネルの周りの線
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.viewport_x + SCREEN_WIDTH - STATES_PANEL_WIDTH + self.panel_line_width*0.5,
            bottom_left_y=self.viewport_y + self.panel_line_width*0.5,
            width=STATES_PANEL_WIDTH - self.panel_line_width,
            height=SCREEN_HEIGHT - self.panel_line_width-231,
            color=arcade.color.LEMON_CHIFFON,
            border_width=self.panel_line_width
        )

        # ミニマップ囲い線
        arcade.draw_xywh_rectangle_outline(
            bottom_left_x=self.viewport_x + SCREEN_WIDTH - STATES_PANEL_WIDTH + self.panel_line_width*0.5,
            bottom_left_y=self.viewport_y + SCREEN_HEIGHT - 228,
            width=STATES_PANEL_WIDTH - self.panel_line_width,
            height=225,
            color=arcade.color.BABY_BLUE,
            border_width=self.panel_line_width
        )

    def grid_cursor(self):
        self.dx += self.grid_select[0]
        self.dy += self.grid_select[1]

        self.x, self.y = grid_to_pixel(self.dx, self.dy)

        if self.grid_press:
            self.engine.grid_click(self.dx, self.dy)
            self.engine.game_state = GAME_STATE.NORMAL

        # グリッド囲い線の描写
        arcade.draw_rectangle_outline(
            center_x=self.x,
            center_y=self.y,
            width=SPRITE_SIZE*SPRITE_SCALE,
            height=SPRITE_SIZE*SPRITE_SCALE,
            color=arcade.color.LIGHT_BLUE,
            border_width=2
        )
        # グリッド囲い線の中にあるオブジェクトの情報の表示
        actor_at_point = arcade.get_sprites_at_exact_point(
            (self.x, self.y), self.sprites[0])
        item_at_point = arcade.get_sprites_at_exact_point(
            (self.x, self.y), self.sprites[1])
        if actor_at_point or item_at_point:
            y = 20
            for actor in chain(actor_at_point, item_at_point):
                if actor.ai:
                    arcade.draw_text(
                        text=f"{actor.name.capitalize()}\n{actor.fighter.hp}/{actor.fighter.max_hp}",
                        start_x=self.viewport_x + SCREEN_WIDTH - STATES_PANEL_WIDTH + 10,
                        start_y=self.viewport_y + SCREEN_HEIGHT - 400 - y,
                        color=arcade.color.RED_PURPLE,
                        font_size=20,
                    )
                    y += 20
                
                y += 10

                if not actor.ai:
                    arcade.draw_text(
                        text=f"{actor.__class__.__name__}",
                        start_x=self.viewport_x + SCREEN_WIDTH - STATES_PANEL_WIDTH + 10,
                        start_y=self.viewport_y + SCREEN_HEIGHT - 400 - y,
                        color=arcade.color.GREEN_YELLOW,
                        font_size=20,
                    )
                    y += 20

