import arcade
from itertools import chain
from constants import *
from data import *


def draw_inventory(player, selected_item, viewport):
    """インベントリを描画する"""
    viewport_left = viewport[0]
    viewport_right = viewport[1]
    viewport_bottom = viewport[2]
    viewport_top = viewport[3]

    # back_panel_left = viewport_left + SCREEN_WIDTH // 5 # 背景パネルの左端
    back_panel_left = viewport_left + (GRID_SIZE*3) # 背景パネルの左端
    back_panel_right = back_panel_left+GRID_SIZE*7 # 背景パネルの左端
    back_panel_bottom_left = viewport_bottom + (GRID_SIZE*6) # 背景パネルの下端
    back_panel_top_left = viewport_top - (GRID_SIZE*2) # 背景パネルの下端
    panel_width = MAIN_PANEL_X - (GRID_SIZE*5)#SCREEN_WIDTH//2.3 # パネルの幅
    panel_height = MAIN_PANEL_Y - (GRID_SIZE*6) # パネルの高さ

    # 背景パネル
    arcade.draw_xywh_rectangle_filled(
        bottom_left_x=back_panel_left,
        bottom_left_y=back_panel_bottom_left - GRID_SIZE,
        width=panel_width,
        height=panel_height,
        color=[5,5,5,180],
        )
    arcade.draw_xywh_rectangle_outline(
        bottom_left_x=back_panel_left,
        bottom_left_y=back_panel_bottom_left - GRID_SIZE,
        width=panel_width,
        height=panel_height,
        color=[70,221,130,255],
        border_width=3
        )


    y = GRID_SIZE # itemtextの改行スペース
    item_font_size = 17
    capacity = player.inventory.capacity
    font_color = arcade.color.WHITE
    equip_this = ""

    


    # キャパシティ数をループし、インベントリのアイテム名とアウトラインを描画する
    slot_item = [i for i in player.equipment.flower_slot]
    for i, item in enumerate(range(capacity)):
        x = 0
        if i >= 9:
            x = GRID_SIZE*7
        if i == 9:
            y = GRID_SIZE

        if player.inventory.item_bag[item]:
            cur_item  = player.inventory.item_bag[item]
            
            if cur_item in slot_item:
                equip_this = "[E]" # そのitemが装備中ならEマークを付ける
                font_color = arcade.color.YELLOW_ROSE


            else:
                equip_this = ""
                font_color = arcade.color.BLIZZARD_BLUE
        else:
            cur_item = ""
            equip_this = ""
            font_color = arcade.color.YALE_BLUE

        if item == selected_item:
            # アウトラインをitemカーソルとして描画
            arcade.draw_lrtb_rectangle_filled(
                left=back_panel_left + x,
                right=back_panel_right + x,
                top=back_panel_top_left + y,
                bottom=back_panel_top_left + y - GRID_SIZE,
                color=[155,255,155,55],
            )
            arcade.draw_lrtb_rectangle_outline(
                left=back_panel_left + x,
                right=back_panel_right + x,
                top=back_panel_top_left + y,
                bottom=back_panel_top_left + y - GRID_SIZE,
                color=[252,250,20,255],
                border_width=3
            )
        # itemのアイコンを描画
        if cur_item:
            arcade.draw_texture_rectangle(
                center_x=back_panel_left + 60 + x,
                center_y=back_panel_top_left - ((GRID_SIZE/2)) + y,
                width=40,
                height=40,
                texture=IMAGE_ID["black_board"]
            )
            arcade.draw_texture_rectangle(
                center_x=back_panel_left + 60 + x,
                center_y=back_panel_top_left - ((GRID_SIZE/2)) + y,
                width=40,
                height=40,
                texture=cur_item.icon,

            )



            # 装備出来るアイテムならitemの左に(equip key: E)と表示
            if cur_item and Tag.equip in cur_item.tag:
                arcade.draw_text(
                    text="(equip key: E)",
                    start_x=back_panel_right - (GRID_SIZE),
                    start_y=back_panel_top_left -(GRID_SIZE/2) + y,
                    color=font_color,
                    font_size=item_font_size-7,
                    font_name=UI_FONT2,
                    anchor_y="center",
                    anchor_x="center"
                )

            # 使用可能アイテムならitemの左に(use key: U)と表示
            elif cur_item and Tag.used in cur_item.tag:
                arcade.draw_text(
                    text="(use key: U)",
                    start_x=back_panel_right - (GRID_SIZE),
                    start_y=back_panel_top_left -(GRID_SIZE/2) + y,
                    color=font_color,
                    font_size=item_font_size-7,
                    font_name=UI_FONT2,
                    anchor_y="center",
                    anchor_x="center"
                )
            
            # itemの説明文をパネル下部に表示
            # if hasattr(cur_item, "explanatory_text"):
            arcade.draw_lrtb_rectangle_filled(
                left=back_panel_left+GRID_SIZE,
                right=back_panel_right+GRID_SIZE*6,
                top=back_panel_bottom_left-GRID_SIZE-2,
                bottom=back_panel_bottom_left-(GRID_SIZE*3),
                color=[20,20,20,250],
            )

                # arcade.draw_text(
                #     text=f"<explanatory note>\n{cur_item.explanatory_text}",
                #     start_x=back_panel_left +10,
                #     start_y=back_panel_bottom_left - (GRID_SIZE) - 5,
                #     color=font_color,
                #     font_size=item_font_size-7,
                #     font_name=UI_FONT2,
                #     anchor_y="top"
                # )



        # item名の表示
        if cur_item:# インベントリのアイテムNone時にエラー防止措置
            cur_item = cur_item.name
        item_text = f" {cur_item}".replace("_", " ").title()
        arcade.draw_text(
            text=f"{item+1: >2} {equip_this: >52} ",
            start_x=back_panel_left + 10 + x,
            start_y=back_panel_top_left -(GRID_SIZE/2) + y, #bottom_left + panel_height - 120 + y,
            color=font_color,
            font_size=item_font_size-2,
            font_name=UI_FONT2,
            anchor_y="center",
            anchor_x="left"
        )
        arcade.draw_text(
            text=item_text,
            start_x=back_panel_left + GRID_SIZE+25 + x,
            start_y=back_panel_top_left -(GRID_SIZE/2) + y, #bottom_left + panel_height - 120 + y,
            color=font_color,
            font_size=item_font_size-2,
            font_name=UI_FONT2,
            anchor_y="center"
            )





        y -= GRID_SIZE


    # y = GRID_SIZE
    # for item in player.equipment.flower_slot:

    #     if item:

    #         item_text = f"{item.name}".replace("_", " ").title()
    #         scale = 2
    #         if Tag.flower in item.tag:
    #             scale = 4
    #         arcade.draw_scaled_texture_rectangle(
    #             center_x=back_panel_right + GRID_SIZE+(GRID_SIZE/2),
    #             center_y=back_panel_top_left - (GRID_SIZE) + y,
    #             texture=item.texture,
    #             scale=scale
    #             )
                

    #         arcade.draw_text(
    #             text=f"Additional skill levels and status bonuses",
    #             start_x=back_panel_right + (GRID_SIZE * 2),
    #             start_y=back_panel_top_left + y - item_font_size,
    #             color=arcade.color.APPLE_GREEN,
    #             font_size=item_font_size-7,
    #             # font_name=UI_FONT2,
    #             anchor_y="top"
    #         )

    #         ifs = 10
    #         for k, v in item.skill_bonus.items():
    #             arcade.draw_text(
    #                 text=f"{k} level {v}".replace("_", " ").title(),
    #                 start_x=back_panel_right + (GRID_SIZE * 2),
    #                 start_y=back_panel_top_left + y - (item_font_size + 8) - ifs,
    #                 color=arcade.color.CORNSILK,
    #                 font_size=item_font_size-6,
    #                 font_name=UI_FONT2,
    #                 anchor_y="top"
    #             )
    #             ifs += 17
    #         wfs = 3
    #         for k,v in item.states_bonus.items():
    #             arcade.draw_text(
    #                 text=f"{k}:{v}",
    #                 start_x=back_panel_right + (GRID_SIZE * 2) + wfs,
    #                 start_y=back_panel_top_left + y - (item_font_size+10) - ifs,
    #                 color=arcade.color.PALE_LAVENDER,
    #                 font_size=item_font_size-6,
    #                 font_name=UI_FONT2,
    #                 anchor_y="top"
    #             )
    #             wfs += 55


            




    #     else:
    #         # continue
    #         item_text = f" -".replace("_", " ").title()

    #     arcade.draw_text(
    #         text=item_text,
    #         start_x=back_panel_right + GRID_SIZE,
    #         start_y=back_panel_top_left + y,
    #         color=arcade.color.ARYLIDE_YELLOW,
    #         font_size=item_font_size-4,
    #         font_name=UI_FONT2,
    #         anchor_y="top"
    #     )



    #     y -= GRID_SIZE *2