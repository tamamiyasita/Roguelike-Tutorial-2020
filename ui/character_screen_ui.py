import arcade
from constants import *
from data import *



def draw_character_screen(engine, viewport, selected_item):
    engine = engine
    player = engine.player
    viewport_left = viewport[0] + GRID_SIZE*3
    viewport_right = viewport[1]
    viewport_bottom = viewport[2] + GRID_SIZE*3
    viewport_top = viewport[3]
    font_name="consola.ttf"

    # viewport_left = viewport_x+100
    # viewport_bottom = viewport_y+100
    panel_width = SCREEN_WIDTH-GRID_SIZE*6
    panel_height = SCREEN_HEIGHT-GRID_SIZE*6
    """背景"""

    
    arcade.draw_xywh_rectangle_filled(
        bottom_left_x=viewport_left,
        bottom_left_y=viewport_bottom,
        width=panel_width,
        height=panel_height,
        color=(75,75,75,125)
    )

    """タイトル"""
    spacing = 1.8
    text_position_y = panel_height + viewport_bottom
    text_position_x = 10 + viewport_left
    text_size = 24
    screen_title = "Character Screen"
    title_color = (255, 122, 248)
    text_color = (186, 253, 143)
    
    arcade.draw_text(
        text=screen_title,
        start_x=text_position_x,
        start_y=text_position_y,
        color=title_color,
        font_size=text_size
    )

    """ステータス表示"""
    text_position_y -= text_size * spacing
    text_size = 20

    states_text = f"Level: {player.fighter.level}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    text_position_y -= text_size * spacing
    states_text = f"H P: {player.fighter.hp: >2} / {player.fighter.max_hp: >2}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    text_position_y -= text_size * spacing
    states_text = f"STR: {player.fighter.base_strength} + {player.equipment.states_bonus['STR']: >2}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    text_position_y -= text_size * spacing 
    states_text = f"DEX: {player.fighter.base_dexterity} + {player.equipment.states_bonus['DEX']: >2}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    text_position_y -= text_size * spacing
    states_text = f"INT: {player.fighter.base_intelligence} + {player.equipment.states_bonus['INT']: >2}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    """スキルリストの表示"""
    left_position = viewport_left + GRID_SIZE*4
    top_position = panel_height + viewport_bottom - GRID_SIZE*1.5
    y = 0 # セパレート
    item_font_size = 15
    skill_list = list(player.fighter.skill_list)
    skill_list = sorted(skill_list, key=lambda x: x.level, reverse=True)

    arcade.draw_text(
        text="Skill List",
        start_x=left_position,
        start_y=top_position+GRID_SIZE-10 ,
        color=(129, 255, 71),
        font_size=item_font_size+5,
        font_name="consola.ttf"
    )
    arcade.draw_text(
        text="<key Enter> Skill on / off",
        start_x=left_position,
        start_y=top_position+GRID_SIZE-25 ,
        color=(255, 102, 102),
        font_size=item_font_size-3,
    )



    for i, skill in enumerate(skill_list):


        item_text = f"{skill.name}".replace("_", " ").title()
        
           
        # 上下移動出来る選択枠
        if i == selected_item:
            arcade.draw_lrtb_rectangle_outline(
                left=left_position,
                right=left_position + GRID_SIZE*3,
                top=top_position + y,
                bottom=top_position + y - (GRID_SIZE/2) - 9,
                color=[252,250,20,255],
                border_width=1
            )



        # タイトル
        arcade.draw_text(
            text=item_text,
            start_x=left_position,
            start_y=top_position + y,
            color=(129, 255, 81),
            font_size=item_font_size-4,
            # font_name="consola.ttf"
        )

        # スキルのテクスチャ
        arcade.draw_texture_rectangle(
            center_x=left_position + 20,
            center_y=top_position + y-21,
            width=36,
            height=36,
            texture=skill.icon
        )

            
        # スキルレベル
        arcade.draw_text(
            text=f"level {skill.level}",
            start_x=left_position + 43,
            start_y=top_position + y-2,
            color=(234, 255, 96),
            font_size=item_font_size-4,
            # font_name="consola.ttf",
            anchor_y="top"
        )

        # スキルの説明文
        arcade.draw_text(
            text=f"{skill.explanatory_text}",
            start_x=left_position + 43,
            start_y=top_position + y-15,
            color=arcade.color.WHITE,
            font_size=item_font_size-5,
            # font_name="consola.ttf",
            anchor_y="top"
        )


        y -= 74        





