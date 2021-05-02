import arcade
from itertools import chain
from constants import *
from data import *


def draw_inventory(engine, selected_item, viewport):
    """インベントリを描画する"""

    player = engine.player

    if selected_item == 99:
        player.equipment.equip_update()
        engine.flower_light()
        engine.game_state = GAME_STATE.NORMAL


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
    # arcade.draw_xywh_rectangle_outline(
    #     bottom_left_x=back_panel_left,
    #     bottom_left_y=back_panel_bottom_left - GRID_SIZE,
    #     width=panel_width,
    #     height=panel_height,
    #     color=[70,221,130,255],
    #     border_width=3
    #     )
    arcade.draw_text(text="Inventory".upper(),
                        start_x=back_panel_left+20,
                        start_y=viewport_top - GRID_SIZE-9,
                        color=arcade.color.DAFFODIL,
                        font_size=20,
                        font_name=UI_FONT2,
                        # anchor_y="
                        )
    ip = arcade.load_texture(r"image\i_p.png")
    arcade.draw_lrwh_rectangle_textured(
        bottom_left_x=back_panel_left,
        bottom_left_y=back_panel_bottom_left - GRID_SIZE,
        width=panel_width,
        height=panel_height,
        texture=ip

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
            # arcade.draw_lrtb_rectangle_filled(
            #     left=back_panel_left + x,
            #     right=back_panel_right + x,
            #     top=back_panel_top_left + y,
            #     bottom=back_panel_top_left + y - GRID_SIZE,
            #     color=[155,255,155,55],
            # )
            # arcade.draw_lrtb_rectangle_outline(
            #     left=back_panel_left + x,
            #     right=back_panel_right + x,
            #     top=back_panel_top_left + y,
            #     bottom=back_panel_top_left + y - GRID_SIZE,
            #     color=[252,250,20,255],
            #     border_width=3
            # )

            # カーソル表示
            cs = arcade.load_texture(r"image\c_s.png")
            arcade.draw_lrwh_rectangle_textured(
                bottom_left_x=back_panel_left + x,
                bottom_left_y=back_panel_top_left-GRID_SIZE + y,
                width=64*7,
                height=64,
                texture=cs
            )
            cy = 13 + item_font_size
            if cur_item:
                font_color2 = arcade.color.PINK_SHERBET
            # itemの説明文をパネル下部に表示

                arcade.draw_lrtb_rectangle_filled(
                    left=back_panel_left,
                    right=back_panel_right+GRID_SIZE*7,
                    top=back_panel_bottom_left-GRID_SIZE-2,
                    bottom=back_panel_bottom_left-(GRID_SIZE*6),
                    color=[100,100,100,250],
                )
                left = back_panel_left + 15
                arcade.draw_text(
                    text=f"LEVEL {cur_item.level}",
                    start_x=left,
                    start_y=back_panel_bottom_left-GRID_SIZE-cy,
                    color=font_color2,
                    font_size=item_font_size,
                    font_name=UI_FONT,
                    anchor_y="top"
                )
                arcade.draw_text(
                    text=f"HP {cur_item.hp}/{cur_item.max_hp}",
                    start_x=left,
                    start_y=back_panel_bottom_left-GRID_SIZE-cy*2,
                    color=font_color2,
                    font_size=item_font_size,
                    font_name=UI_FONT,
                    anchor_y="top"
                )
                arcade.draw_text(
                    text=f"EXP {cur_item.current_xp}",
                    start_x=left,
                    start_y=back_panel_bottom_left-GRID_SIZE-cy*3,
                    color=font_color2,
                    font_size=item_font_size,
                    font_name=UI_FONT,
                    anchor_y="top"
                )
                arcade.draw_texture_rectangle(
                    center_x=left+25,
                    center_y=back_panel_bottom_left-GRID_SIZE-cy*7,
                    width=40,
                    height=40,
                    texture=IMAGE_ID["black_board"]
                )
                arcade.draw_texture_rectangle(
                    center_x=left+25,
                    center_y=back_panel_bottom_left-GRID_SIZE-cy*7,
                    width=40,
                    height=40,
                    texture=cur_item.flower_skill.icon,

                )
                arcade.draw_text(
                    text=f"SKILL",
                    start_x=left,
                    start_y=back_panel_bottom_left-GRID_SIZE-cy*5,
                    color=font_color2,
                    font_size=item_font_size,
                    font_name=UI_FONT,
                    anchor_y="top"
                )
                # arcade.draw_lrwh_rectangle_textured(
                #     bottom_left_x=back_panel_left+15,
                #     bottom_left_y=back_panel_bottom_left-GRID_SIZE-cy*8,
                #     width=40,
                #     height=40,
                #     texture=cur_item.flower_skill.icon

                # )
                arcade.draw_text(
                    text=f"States Bonus",
                    start_x=back_panel_left+GRID_SIZE*3,
                    start_y=back_panel_bottom_left-GRID_SIZE-cy,
                    color=arcade.color.GREEN_YELLOW,
                    font_size=item_font_size,
                    font_name=UI_FONT,
                    anchor_y="top"
                )

                ky = GRID_SIZE+item_font_size
                for key, val in cur_item.states_bonus.items():
                    if val:
                        

                        arcade.draw_text(
                            text=f"{key: <13} + {val}".replace("_", " ").title(),
                            start_x=back_panel_left+GRID_SIZE*3,
                            start_y=back_panel_bottom_left-GRID_SIZE-ky,
                            color=font_color,
                            font_size=item_font_size-2,
                            font_name=UI_FONT,
                            # anchor_y="top"
                        )
                        ky += 10+item_font_size
                arcade.draw_text(
                    text=f"Resist Bonus",
                    start_x=back_panel_left+GRID_SIZE*7,
                    start_y=back_panel_bottom_left-GRID_SIZE-cy,
                    color=arcade.color.ORIOLES_ORANGE,
                    font_size=item_font_size,
                    font_name=UI_FONT,
                    anchor_y="top"
                )
                ky = GRID_SIZE+item_font_size
                for key, val in cur_item.resist_bonus.items():
                    if val:
                        

                        arcade.draw_text(
                            text=f"{key: <13} + {val}".replace("_", " ").title(),
                            start_x=back_panel_left+GRID_SIZE*7,
                            start_y=back_panel_bottom_left-GRID_SIZE-ky,
                            color=font_color,
                            font_size=item_font_size-2,
                            font_name=UI_FONT,
                            # anchor_y="top"
                        )
                        ky += 10+item_font_size

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
            # arcade.draw_lrtb_rectangle_filled(
            #     left=back_panel_left,
            #     right=back_panel_right+GRID_SIZE*7,
            #     top=back_panel_bottom_left-GRID_SIZE-2,
            #     bottom=back_panel_bottom_left-(GRID_SIZE*6),
            #     color=[100,100,200,250],
            # )
            # if item == selected_item:

            #     arcade.draw_text(
            #         text=f"States Bonus",
            #         start_x=back_panel_left+GRID_SIZE*3,
            #         start_y=back_panel_bottom_left-GRID_SIZE-12,
            #         color=font_color,
            #         font_size=item_font_size-5,
            #         font_name=UI_FONT,
            #         anchor_y="top"
            #     )

            #     ky = GRID_SIZE
            #     for key, val in cur_item.states_bonus.items():
            #         if val:
                        

            #             arcade.draw_text(
            #                 text=f"{key} : {val}",
            #                 start_x=back_panel_left+GRID_SIZE*3,
            #                 start_y=back_panel_bottom_left-GRID_SIZE-ky,
            #                 color=font_color,
            #                 font_size=item_font_size-5,
            #                 font_name=UI_FONT,
            #                 # anchor_y="top"
            #             )
            #             ky += 22



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


    # y = 12
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