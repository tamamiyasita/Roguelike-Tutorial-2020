import arcade
from constants import *
from data import *
from util import grid_to_pixel


def draw_inventory(player, selected_item, viewport_x, viewport_y, grid_select):
    viewport_left = viewport_x
    viewport_bottom = viewport_y
    grid_x, grid_y = grid_to_pixel(grid_select[0],grid_select[1])

    """背景"""

    back_panel_x = viewport_left + SCREEN_WIDTH // 4
    back_panel_y = viewport_bottom + SCREEN_HEIGHT // 8
    panel_width = SCREEN_WIDTH//2.3
    panel_height = SCREEN_HEIGHT //1.3
    arcade.draw_xywh_rectangle_filled(
        bottom_left_x=back_panel_x,
        bottom_left_y=back_panel_y,
        width=panel_width,
        height=panel_height,
        color=COLORS["status_panel_background"]
    )

    """インベントリの表示"""
    item_left_position = back_panel_x#viewport_left + ((SCREEN_WIDTH-STATES_PANEL_WIDTH) / 2.8)   # パネル左からの所持アイテム表示位置の調整に使う変数
    item_top_position = back_panel_y + panel_height - 50#viewport_bottom + STATES_PANEL_HEIGHT - 220  # パネル上端からの所持アイテム表示位置の調整に使う変数
    separate_size = 1.6  # アイテム名の表示間隔の調整に使う変数
    margin = 3  # 選択したアイテムのアウトライン線の位置調整に使う変数
    item_font_size = 22
    outline_size = 2
    capacity = player.inventory.capacity
    selected_item = selected_item  # ボタン押下で選択したアイテムオブジェクト
    field_width = SCREEN_WIDTH / \
        (capacity + 1) / separate_size  # アイテム表示感覚を決める変数

    # キャパシティ数をループし、インベントリのアイテム名とアウトラインを描画する
    # TODO 複数行にする処理を考える（５回ループしたら縦と横の変数に増減するなど）
    y = 40
    for item in range(capacity):
        items_position = item * back_panel_x + grid_x  # パネル左からの所持アイテムの表示位置
        if item == selected_item:
            arcade.draw_lrtb_rectangle_outline(
                left=items_position - margin,
                right=items_position + field_width - margin,
                top=item_top_position + item_font_size + margin*2,
                bottom=item_top_position - margin,
                color=arcade.color.BLACK,
                border_width=outline_size
            )

        if player.inventory.item_bag[item]:
            item_name = player.inventory.item_bag[item].name
        else:
            item_name = ""

        item_text = f"{item+1: >2}: {item_name}"
        
        arcade.draw_text(
            text=item_text,
            start_x=back_panel_x +20,
            start_y=back_panel_y + panel_height - 120 + y,
            color=arcade.color.ORANGE,
            font_size=item_font_size,
            font_name="consola.ttf"
        )
        y -= 40
