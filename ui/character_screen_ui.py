import arcade
from constants import *
from data import *



def draw_character_screen(self, viewport_x, viewport_y):
    self.viewport_left = viewport_x
    self.viewport_bottom = viewport_y

    """背景"""
    arcade.draw_xywh_rectangle_filled(
        bottom_left_x=0+self.viewport_left,
        bottom_left_y=0+self.viewport_bottom,
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        color=COLORS["status_panel_background"]
    )

    """タイトル"""
    spacing = 1.8
    text_position_y = SCREEN_HEIGHT - 50 + self.viewport_bottom
    text_position_x = 10 + self.viewport_left
    text_size = 24
    screen_title = "Character Screen"
    text_color = arcade.color.AFRICAN_VIOLET
    arcade.draw_text(
        text=screen_title,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )

    """ステータス表示"""
    text_position_y -= text_size * spacing
    text_size = 20
    states_text = f"STR: {self.player.fighter.base_strength} + {self.player.equipment.states_bonus['STR']}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )

    text_position_y -= text_size * spacing  # TODO ゼロならボーナス非表示にしよう
    states_text = f"DEX: {self.player.fighter.base_dexterity} + {self.player.equipment.states_bonus['DEX']}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )

    text_position_y -= text_size * spacing
    states_text = f"INT: {self.player.fighter.base_intelligence} + {self.player.equipment.states_bonus['INT']}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )

    text_position_y -= text_size * spacing
    states_text = f"HP: {self.player.fighter.hp} / {self.player.fighter.max_hp}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )

    text_position_y -= text_size * spacing
    states_text = f"Level: {self.player.fighter.level}"
    arcade.draw_text(
        text=states_text,
        start_x=text_position_x,
        start_y=text_position_y,
        color=text_color,
        font_size=text_size
    )
