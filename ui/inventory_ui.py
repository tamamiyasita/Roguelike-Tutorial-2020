import arcade
from constants import *
from data import *
from util import grid_to_pixel


def draw_inventory(player, engine, viewport_x, viewport_y, grid_select):
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
        color=[123,123,123,123],

    )

    """インベントリの表示"""

    y = 40
    item_row = back_panel_y + panel_height - 120
    item_font_size = 22
    outline_size = 2
    capacity = player.inventory.capacity
    font_color = arcade.color.RED_DEVIL
    equip_this = ""
    selected_item = engine  # ボタン押下で選択したアイテムオブジェクト


    # キャパシティ数をループし、インベントリのアイテム名とアウトラインを描画する
    # TODO 複数行にする処理を考える（５回ループしたら縦と横の変数に増減するなど）
    slot_item = [i.name for i in player.equipment.item_slot.values() if hasattr(i, "name")]
    print(slot_item)
    for item in range(capacity):
        if player.inventory.item_bag[item]:
            cur_item  = player.inventory.item_bag[item]
            item_name = cur_item.name
            item_tag = cur_item.tag
            if item_name in slot_item:
                equip_this = "[E]"
                font_color = arcade.color.ORANGE_PEEL
            else:
                equip_this = ""
                font_color = arcade.color.BLIZZARD_BLUE

        else:
            item_name = ""
            equip_this = ""
            font_color = arcade.color.YALE_BLUE
            cur_item = None


        if item == selected_item:
            arcade.draw_lrtb_rectangle_outline(
                left=back_panel_x+18,
                right=back_panel_x +430,
                top=item_row + y +33,
                bottom=item_row + y -3,
                color=arcade.color.HOT_PINK,
                border_width=outline_size
            )
            if item_name and Tag.equip in item_tag:
                arcade.draw_text(
                    text="(equip key: E)",
                    start_x=back_panel_x +450,
                    start_y=item_row + y,
                    color=font_color,
                    font_size=item_font_size-3,
                    font_name="consola.ttf",
                    anchor_y="bottom"
                )
            elif item_name and Tag.used in item_tag:
                arcade.draw_text(
                    text="(use key: U)",
                    start_x=back_panel_x +450,
                    start_y=item_row + y,
                    color=font_color,
                    font_size=item_font_size-3,
                    font_name="consola.ttf",
                    anchor_y="bottom"
                )
            if cur_item:
                arcade.draw_scaled_texture_rectangle(back_panel_x +400, back_panel_y + panel_height - 105 + y, cur_item.texture, scale=3)
            
            if hasattr(cur_item, "explanatory_text"):
                arcade.draw_text(
                    text=f"<explanatory note>\n{cur_item.explanatory_text}",
                    start_x=back_panel_x +10,
                    start_y=back_panel_y + panel_height-600,
                    color=font_color,
                    font_size=item_font_size-3,
                    font_name="consola.ttf",
                    anchor_y="top"
                )
            
            # for i, item in enumerate(player.equipment.equip_slot.items()):
            #     items_position = i * field_width + item_left_position  # パネル左からの所持アイテムの表示位置

            #     if item[1]:

            #         item_text = f"{item[0]}: {item[1].name}"
            #     else:
            #         item_text = f"{item[0]}: {item[1]}"

            #     arcade.draw_text(
            #         text=item_text,
            #         start_x=items_position,
            #         start_y=item_top_position,
            #         color=COLORS["status_panel_text"],
            #         font_size=item_font_size
            #     )




        item_text = f"{item+1: >2}: {item_name} {equip_this}"
        
        arcade.draw_text(
            text=item_text,
            start_x=back_panel_x +20,
            start_y=back_panel_y + panel_height - 120 + y,
            color=font_color,
            font_size=item_font_size,
            font_name="consola.ttf",
            anchor_y="bottom"
        )
        y -= 40
