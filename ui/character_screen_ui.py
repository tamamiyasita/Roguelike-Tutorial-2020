import arcade
from constants import *
from data import *



def draw_character_screen(engine, viewport):#player, viewport_x, viewport_y):
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
        color=COLORS["status_panel_background"]
    )

    """タイトル"""
    spacing = 1.8
    text_position_y = panel_height + viewport_bottom
    text_position_x = 10 + viewport_left
    text_size = 24
    screen_title = "Character Screen"
    title_color = arcade.color.AFRICAN_VIOLET
    text_color = arcade.color.AIR_FORCE_BLUE
    
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
    states_text = f"H P: {player.fighter.hp} / {player.fighter.max_hp}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    text_position_y -= text_size * spacing
    states_text = f"STR: {player.fighter.base_strength} + {player.equipment.states_bonus['STR']}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    text_position_y -= text_size * spacing  # TODO ゼロならボーナス非表示にしよう
    states_text = f"DEX: {player.fighter.base_dexterity} + {player.equipment.states_bonus['DEX']}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    text_position_y -= text_size * spacing
    states_text = f"INT: {player.fighter.base_intelligence} + {player.equipment.states_bonus['INT']}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size,
        font_name=font_name
    )

    left_position = viewport_left + GRID_SIZE*3
    top_position = panel_height + viewport_bottom - 50
    y = 0
    item_font_size = 15
    skill_list = list(player.fighter.skill_list)
    skill_list = sorted(skill_list, key=lambda x: x.level, reverse=True)
    for skill in skill_list:
        item_text = f"{skill.name}".replace("_", " ").title()

 
        arcade.draw_text(
            text=item_text,
            start_x=left_position,
            start_y=top_position + y,
            color=arcade.color.BANGLADESH_GREEN,
            font_size=item_font_size-4,
            # font_name="consola.ttf"
        )

        arcade.draw_texture_rectangle(
            center_x=left_position+17,
            center_y=top_position + y-18,
            width=32,
            height=32,
            texture=skill.icon
        )
            
        arcade.draw_text(
            text=f"level {skill.level}",
            start_x=left_position +35,
            start_y=top_position + y,
            color=arcade.color.BISTRE_BROWN,
            font_size=item_font_size-4,
            # font_name="consola.ttf",
            anchor_y="top"
        )
        arcade.draw_text(
            text=f"{skill.explanatory_text}",
            start_x=left_position +35,
            start_y=top_position + y-15,
            color=arcade.color.WHITE,
            font_size=item_font_size-5,
            # font_name="consola.ttf",
            anchor_y="top"
        )


        y -= 74        
