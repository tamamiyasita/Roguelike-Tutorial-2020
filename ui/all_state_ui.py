import arcade
from constants import *

def all_state_ui(viewport_x, viewport_y):
    #画面下のパネルをarcadeの四角形を描画する変数で作成
    arcade.draw_xywh_rectangle_filled(
                    bottom_left_x=viewport_x,
                    bottom_left_y=viewport_y,
                    width=SCREEN_WIDTH,
                    height=STATES_PANEL_HEIGHT,
                    color=COLORS["status_panel_background"]
                    )

