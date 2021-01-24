import arcade
from constants import *
from data import *



def draw_character_screen(player, viewport_x, viewport_y):
    viewport_left = viewport_x+100
    viewport_bottom = viewport_y+100
    panel_width = SCREEN_WIDTH-200
    panel_height = SCREEN_HEIGHT-200

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
    states_text = f"STR: {player.fighter.base_strength} + {player.equipment.states_bonus['STR']}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )

    text_position_y -= text_size * spacing  # TODO ゼロならボーナス非表示にしよう
    states_text = f"DEX: {player.fighter.base_dexterity} + {player.equipment.states_bonus['DEX']}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )

    text_position_y -= text_size * spacing
    states_text = f"INT: {player.fighter.base_intelligence} + {player.equipment.states_bonus['INT']}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )

    text_position_y -= text_size * spacing
    states_text = f"HP: {player.fighter.hp} / {player.fighter.max_hp}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )

    text_position_y -= text_size * spacing
    states_text = f"Level: {player.fighter.level}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )
