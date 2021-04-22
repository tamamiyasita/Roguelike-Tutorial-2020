import arcade
from constants import *
from data import *
import pyglet.gl as gl



def draw_character_screen(engine, viewport, selected_item):
    engine = engine
    player = engine.player
    viewport_left = viewport[0] + GRID_SIZE*3
    viewport_right = viewport[1]
    viewport_bottom = viewport[2] + GRID_SIZE*3
    viewport_top = viewport[3]
    font_name=UI_FONT

    ui_sprites = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=32)


    # viewport_left = viewport_x+100
    # viewport_bottom = viewport_y+100
    panel_width = SCREEN_WIDTH-GRID_SIZE*6
    panel_height = SCREEN_HEIGHT-GRID_SIZE*6

    panel_top = viewport_bottom + panel_height
    panel_side = viewport_left + 16
    """背景"""
    cs = arcade.load_texture(r"image\chara_screen.png")
    arcade.draw_lrwh_rectangle_textured(
        bottom_left_x=viewport_left,
        bottom_left_y=viewport_bottom,
        width=panel_width,
        height=panel_height,
        texture=cs
    )
    # キャラクターアイコン
    c = arcade.Sprite(filename=r"image\chara_sheet.png", scale=6,
                      center_x=viewport_left + 66,
                      center_y=panel_top - GRID_SIZE - 20)
    ui_sprites.append(c)
    ui_sprites.draw(filter=gl.GL_NEAREST)
    


    """タイトル"""
    spacing = 1.8
    text_position_y = panel_top 
    text_position_x = panel_side+2
    text_size = 24 
    text_color = (186, 253, 143)

    
    arcade.draw_text(
        text="Character Screen",
        start_x=panel_side,
        start_y=panel_top-12,
        color=(255, 122, 248),
        font_size=text_size
    )

    """ステータス表示"""
    text_position_y -= text_size * spacing
    text_size = 15
    m = 3
    u = GRID_SIZE *2

    states_text = f"Race: {player.race}"
    arcade.draw_text(
        text=states_text,
        start_x=panel_side+u,
        start_y=text_position_y+m,
        color=text_color,
        font_size=text_size+m,
        font_name=font_name
    )

    text_position_y -= text_size * spacing
    states_text = f"Name: {player.name}"
    arcade.draw_text(
        text=states_text,
        start_x=panel_side+u,
        start_y=text_position_y+m,
        color=text_color,
        font_size=text_size+m,
        font_name=font_name
    )

    text_position_y -= text_size * spacing
    states_text = f"Lv  : {player.fighter.level}"
    arcade.draw_text(
        text=states_text,
        start_x=panel_side+u,
        start_y=text_position_y+m,
        color=text_color,
        font_size=text_size+m,
        font_name=font_name
    )
    text_position_y -= text_size * spacing
    states_text = f"Next: {player.experience_per_level[player.fighter.level+1]-player.fighter.current_xp}.exp"
    arcade.draw_text(
        text=states_text,
        start_x=panel_side+u,
        start_y=text_position_y+m,
        color=text_color,
        font_size=text_size+m,
        font_name=font_name
    )


    text_position_y -= text_size * spacing 
    states_text = f"[States]"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size-1,
        font_name=font_name
    )
    text_position_y -= text_size * spacing
    states_text = f"MHP: {player.fighter.max_hp: >3}  + {player.equipment.states_bonus['max_hp']: >3}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    text_position_y -= text_size * spacing
    states_text = f"STR: {player.fighter.base_strength: >3}  + {player.equipment.states_bonus['STR']: >3}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    text_position_y -= text_size * spacing 
    states_text = f"DEX: {player.fighter.base_dexterity: >3}  + {player.equipment.states_bonus['DEX']: >3}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    text_position_y -= text_size * spacing
    states_text = f"INT: {player.fighter.base_intelligence: >3}  + {player.equipment.states_bonus['INT']: >3}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )
    text_position_y -= text_size * spacing
    states_text = f"DEF: {player.fighter.defense: >3}  + {player.equipment.states_bonus['defense']: >3}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )
    text_position_y -= text_size * spacing
    states_text = f"EVE: {player.fighter.defense: >3}  + {player.equipment.states_bonus['evasion']: >3}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )
    text_position_y -= text_size * spacing
    states_text = f"SPD: {player.fighter.speed: >3}  + {player.equipment.states_bonus['speed']: >3}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )
    text_position_y -= text_size * spacing +4
    states_text = f"[Resistance]"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )
    text_position_y -= text_size * spacing
    for r_key, r_val in player.fighter.resist.items():
        states_text = f"{r_key[:4]:<4}:  {r_val}  + {player.equipment.resist_bonus[r_key]: >3}"
        arcade.draw_text(
            text=states_text,
            start_x=panel_side,
            start_y=text_position_y,
            color=text_color,
            font_size=15,
            font_name=font_name
            )
        text_position_y -= text_size * spacing


    """スキルリストの表示"""
    left_position = viewport_left + GRID_SIZE*3
    top_position = panel_top-GRID_SIZE*2-20
    y = -24 # セパレート
    item_font_size = 15
    flowers = player.equipment.flower_slot
    skill_list = list(player.fighter.skill_list)
    skill_list = sorted(skill_list, key=lambda x: x.level, reverse=True)

    arcade.draw_text(
        text="Flowers",
        start_x=left_position,
        start_y=top_position,
        color=(129, 255, 71),
        font_size=item_font_size+2,
        font_name=UI_FONT
    )


    for i, flower in enumerate(flowers):


        item_text = f"{flower.name}".replace("_", " ").title()
        
           
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
            # font_name=UI_FONT2
        )

        # スキルのテクスチャ
        arcade.draw_texture_rectangle(
            center_x=left_position + 20,
            center_y=top_position + y-21,
            width=36,
            height=36,
            texture=flower.icon
        )

            
        # スキルレベル
        arcade.draw_text(
            text=f"level {flower.level}",
            start_x=left_position + 43,
            start_y=top_position + y-2,
            color=(234, 255, 96),
            font_size=item_font_size-4,
            # font_name=UI_FONT2,
            anchor_y="top"
        )

        y -= 74        





