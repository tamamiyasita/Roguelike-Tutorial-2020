import arcade
from constants import *
from data import *
from util import grid_to_pixel


def draw_inventory(player, selected_item, viewport_x, viewport_y):
    """インベントリを描画する"""
    viewport_left = viewport_x
    viewport_bottom = viewport_y

    back_panel_x = viewport_left + SCREEN_WIDTH // 4 # 背景パネルの左端
    back_panel_y = viewport_bottom + SCREEN_HEIGHT // 8 # 背景パネルの下端
    panel_width = SCREEN_WIDTH//2.3 # パネルの幅
    panel_height = SCREEN_HEIGHT //1.3 # パネルの高さ

    # 背景パネル
    arcade.draw_xywh_rectangle_filled(
        bottom_left_x=back_panel_x,
        bottom_left_y=back_panel_y,
        width=panel_width,
        height=panel_height,
        color=[123,123,123,123],
        )


    y = 40 # itemtextの改行スペース
    item_row = back_panel_y + panel_height - 120 # 行の最上段
    item_font_size = 22
    capacity = player.inventory.capacity
    font_color = arcade.color.RED_DEVIL
    equip_this = ""


    # キャパシティ数をループし、インベントリのアイテム名とアウトラインを描画する
    slot_item = [i.name for i in player.equipment.item_slot.values() if hasattr(i, "name")]
    for item in range(capacity):
        if player.inventory.item_bag[item]:
            cur_item  = player.inventory.item_bag[item]
            item_name = cur_item.name
            item_tag = cur_item.tag
            if item_name in slot_item:
                equip_this = "[E]" # そのitemが装備中ならEマークを付ける
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
            # アウトラインをitemカーソルとして描画
            arcade.draw_lrtb_rectangle_outline(
                left=back_panel_x+18,
                right=back_panel_x +430,
                top=item_row + y +33,
                bottom=item_row + y -3,
                color=arcade.color.HOT_PINK,
                border_width=3
            )
            # 装備出来るアイテムならitemの左に(equip key: E)と表示
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

            # 使用可能アイテムならitemの左に(use key: U)と表示
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
            # itemのアイコンを描画
            if cur_item:
                arcade.draw_scaled_texture_rectangle(back_panel_x +400, back_panel_y + panel_height - 105 + y, cur_item.texture, scale=3)
            
            # itemの説明文をパネル下部に表示
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

            




        # item名の表示
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


    y = 40
    for slot, equip in player.equipment.equip_slot.items():

        if equip:

            item_text = f"{slot}: {equip.name} (level {equip.level})".replace("_", " ").title()
        else:
            continue

        arcade.draw_text(
            text=item_text,
            start_x=back_panel_x +650,
            start_y=item_row + y,
            color=arcade.color.ARYLIDE_YELLOW,
            font_size=item_font_size-4,
            font_name="consola.ttf"
        )

        arcade.draw_texture_rectangle(
            center_x=back_panel_x +730,
            center_y=item_row + y-25,
            width=40,
            height=40,
            texture=equip.icon
        )
            
        arcade.draw_text(
            text=f"damage: {player.fighter.level//3}D/{equip.attack_damage}",
            start_x=back_panel_x +755,
            start_y=item_row + y-25,
            color=arcade.color.APPLE_GREEN,
            font_size=item_font_size-6,
            font_name="consola.ttf"
        )
        arcade.draw_text(
            text=f"hit rate: {equip.hit_rate}",
            start_x=back_panel_x +755,
            start_y=item_row + y-47,
            color=arcade.color.ORCHID_PINK,
            font_size=item_font_size-6,
            font_name="consola.ttf"
        )
        arcade.draw_text(
            text=f"{equip.explanatory_text}",
            start_x=back_panel_x +717,
            start_y=item_row + y-65,
            color=arcade.color.WHITE,
            font_size=item_font_size-7,
            font_name="consola.ttf"
        )

        y -= 104